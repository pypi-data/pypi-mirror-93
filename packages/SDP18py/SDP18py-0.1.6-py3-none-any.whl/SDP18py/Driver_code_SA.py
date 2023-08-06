import numpy as np
from SDP18py.Generate_initial_solution import initial_solution_random_fit
from SDP18py.MO_fitting_func_calc import MO_calculate
from SDP18py.MO_fitting_func_calc import calculate_delta_S
from SDP18py import find_legal_neighbors as fd, swapper as sp
from SDP18py.read_MAS import read_mas
from SDP18py.read_csv import read_csv
from SDP18py.read_toschedule import read_toschedule
import time
import random
from SDP18py.view_timetable import show_timetable
from threading import Thread


def schedule_SA(ini_temp=1000, cool_rate=0.99, termi_num=30):

	OT_indexes = {0: 'L1',
	              1: 'L2',
	              2: 'L3',
	              3: 'L4',
	              4: 'L5',
	              5: 'L6',
	              6: 'L7',
	              7: 'L8',
	              8: 'M1',
	              9: 'M2',
	              10: 'M3',
	              11: 'M4',
	              12: 'M5',
	              13: 'OT 24',
	              14: 'OT 25',
	              15: 'OT 22',
	              16: 'R1',
	              17: 'R4',
	              18: 'R5',
	              19: 'R6',
	              20: 'R7',
	              21: 'R8',
	              22: 'MRI',
	              }
	current_schedule = read_csv()
	schedule_days = current_schedule[1]
	day_index = current_schedule[3]
	current_schedule = current_schedule[0]
	to_schedule = read_toschedule()
	MAS_full = read_mas()
	MAS_allowed = MAS_full['OTO']

	t0 = time.time()
	# first fit or random fit
	soln = initial_solution_random_fit(current_schedule, to_schedule, MAS_allowed, day_index, OT_indexes)
	# SIMULATED ANNEALING ALGORITHM
	print("SIMULATED ANNEALING Algorithm")
	T = ini_temp  # higher temperature, higher chance of accepting bad solution (more diversed solution)
	alpha = cool_rate  # cooling rate
	termination_number = termi_num  # how many times of reaching the same fitting value to stop the run?
	termination_count = 0

	while termination_count < termination_number:
		sp.pushback2(soln)
		curr_score = MO_calculate(soln)
		legal_swaps = fd.all_legal_swaps(soln, to_schedule, MAS_allowed, day_index, OT_indexes)
		neighbour = random.choice(legal_swaps)
		perturb_soln = sp.swapping(soln, neighbour)
		perturb_score = MO_calculate(perturb_soln)
		before = curr_score
		if np.all(perturb_score <= curr_score):
			soln = perturb_soln
			curr_score = perturb_score
		else:  # if does not dominate, select based on some probability, UMOSA
			p = calculate_delta_S(soln, perturb_soln, T)
			if p > random.uniform(0, 1):
				soln = perturb_soln
				curr_score = perturb_score

		# check improvement for termination
		improvement = before - curr_score
		if np.all(improvement==0):
			termination_count += 1
		else:
			termination_count = 0

		print("The current score is:" + str(curr_score))
		T = T * alpha
	t1 = time.time()
	print("Time Taken for SA: " + str(t1-t0) + ' seconds')

	sol_list = [soln, schedule_days]
	thread = Thread(target=show_timetable, args=[sol_list])
	thread.start()
	print(curr_score)