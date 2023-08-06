import numpy as np
from SDP18py.Generate_initial_solution import initial_solution_first_fit
from SDP18py.MO_fitting_func_calc import MO_calculate
from SDP18py.MO_fitting_func_calc import calc_crowding_distance
from SDP18py import find_legal_neighbors as fd, swapper as sp
import pareto as pt
from SDP18py.plot_pareto_front import plot_front
import time
# from view_timetable1 import show_timetable
from SDP18py.view_timetable1 import show_timetable
from threading import Thread



def run_hco(current_schedule_list, to_schedule_read, mas_read, disc_select):

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
    soln = initial_solution_first_fit(current_schedule, to_schedule, MAS_allowed, day_index, OT_indexes)

    # HILL CLIMBING ALGORITHM
    print("Hill Climbing Algorithm")
    pastsolnscores = np.array([[0, 0, 0]])
    iter = 0
    while True:

        sp.pushback2(soln)
        curr_score = MO_calculate(soln)

        # generate all legal swaps
        legal_swaps = fd.all_legal_swaps(soln, to_schedule, MAS_allowed, day_index, OT_indexes)
        scores = np.array([[9999, 9999, 9999]])

        for swaps in legal_swaps:  # calculate score vector for each swap
            sc = MO_calculate(sp.swapping(soln, swaps))
            scores = np.vstack((scores, sc))

        scores = np.vstack((scores, curr_score))
        scores = np.delete(scores, 0, axis=0)
        p_front_scores = np.array(pt.eps_sort(scores))

        # find the best swap
        if not np.equal(curr_score, p_front_scores).all(
                axis=1).any():  # current solution is not in best possible pareto front
            crowding_dist = calc_crowding_distance(p_front_scores)
            min_crowding_dist_index = np.argmin(crowding_dist)
            find = p_front_scores[min_crowding_dist_index]
            min_index = np.where((scores == find).all(axis=1))[0][0]
            soln = sp.swapping(soln, legal_swaps[min_index])
            best_score = MO_calculate(soln)
        else:
            break  # current solution is already pareto optimal

        # check if the solution is looping
        if len(pastsolnscores) < 3:
            pastsolnscores = np.vstack((pastsolnscores, best_score))
        elif len(pastsolnscores) == 3:
            pastsolnscores = np.delete(pastsolnscores, 0, axis=0)
            pastsolnscores = np.vstack((pastsolnscores, best_score))
            if len(np.unique(pastsolnscores, axis=0)) < 3:
                break
        print("the best score is " + str(best_score))
        iter += 1
    print("Pareto Front Scores:")
    print(p_front_scores)
    t1 = time.time()

    # find minimum overtime score
    min_over_timescore = p_front_scores[np.argmin(p_front_scores[:, 0]), :]
    print("Minimum Overtime Score")
    print(min_over_timescore)
    min_index = np.where((scores == min_over_timescore).all(axis=1))[0][0]
    if min_index != len(scores) - 1:
        soln = sp.swapping(soln, legal_swaps[min_index])
    print("Time Taken for HCO: " + str(t1 - t0) + ' seconds')

    # sol_list = [soln, schedule_days]
    # thread1 = Thread(target=show_timetable, args=[sol_list])
    # thread1.start()
    # thread2 = Thread(target=create_table, args=(soln, schedule_date))
    # thread2.start()
    sol_list = [soln, schedule_days, schedule_date]
    thread1 = Thread(target=show_timetable, args=[sol_list])
    thread1.start()

    plot_front(scores, p_front_scores)