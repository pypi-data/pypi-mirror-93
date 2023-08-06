import numpy as np
from SDP18py.Generate_initial_solution import initial_solution_random_fit
from SDP18py.MO_fitting_func_calc import MO_calculate
from SDP18py.MO_fitting_func_calc import calculate_delta_S
from SDP18py import find_legal_neighbors as fd, swapper as sp
import time
import random
from SDP18py.view_timetable1 import show_timetable
from threading import Thread


def run_sa(current_schedule_list, to_schedule_read, mas_read, disc_select):

    random.seed(10)

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

    current_schedule = current_schedule_list
    # add one more schedule_date
    schedule_date = current_schedule[2]
    # code on top ^
    schedule_days = current_schedule[1]
    day_index = current_schedule[3]
    current_schedule = current_schedule[0]
    to_schedule = to_schedule_read
    MAS_full = mas_read
    MAS_allowed = MAS_full[disc_select]

    t0 = time.time()

    # first fit or random fit
    soln = initial_solution_random_fit(current_schedule, to_schedule, MAS_allowed, day_index, OT_indexes)
    # SIMULATED ANNEALING ALGORITHM
    print("SIMULATED ANNEALING Algorithm")
    T = 1000  # higher temperature, higher chance of accepting bad solution (more diversed solution)
    alpha = 0.99  # cooling rate
    termination_number = 30  # how many times of reaching the same fitting value to stop the run?
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
    print("Time Taken for SA: " + str(t1 - t0) + ' seconds')
    # sol_list = [soln, schedule_days]
    # thread1 = Thread(target=show_timetable, args=[sol_list])
    # thread1.start()
    # thread2 = Thread(target=create_table, args=(soln, schedule_date))
    # thread2.start()
    sol_list = [soln, schedule_days, schedule_date]
    thread1 = Thread(target=show_timetable, args=[sol_list])
    thread1.start()
    print(curr_score)