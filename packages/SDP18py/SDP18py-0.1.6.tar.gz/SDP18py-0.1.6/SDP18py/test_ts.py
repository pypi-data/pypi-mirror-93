import numpy as np
from SDP18py.Generate_initial_solution import initial_solution_random_fit
from SDP18py.MO_fitting_func_calc import MO_calculate
import pareto as pt
from SDP18py import plot_pareto_front as pf, find_legal_neighbors as fd, swapper as sp
import time
import random
from SDP18py.view_timetable1 import show_timetable
from threading import Thread



def run_ts(current_schedule_list, to_schedule_read, mas_read, disc_select):

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
    k = 5  # number of parallel searches
    tabu_tenure = 5
    soln_list = []
    for _ in range(k):
        soln_list.append(
            initial_solution_random_fit(current_schedule, to_schedule, MAS_allowed, day_index, OT_indexes))

    pareto_front = np.array([[9999, 9999, 9999]])
    max_iter = 50
    tabu_list = [[None] for i in range(k)]

    # PARALLEL TABU SEARCH ALGORITHM
    print("TABU SEARCH Algorithm")
    # Trying to esimate pareto front from multiple initial solutions

    for iter in range(max_iter):
        new_search_front_scores = []
        new_search_front = []
        scores_t = np.array([[9999, 9999, 9999]])
        for index, soln in enumerate(soln_list):
            sp.pushback2(soln)
            curr_score = MO_calculate(soln)
            # generate all legal swaps
            legal_swaps = fd.all_legal_swaps_subset(soln, to_schedule, MAS_allowed, day_index,
                                                    OT_indexes)  # use a random subsetted neighbour to make program run faster
            scores = np.array([[9999, 9999, 9999]])
            for swaps in legal_swaps:  # bottleneck
                sc = MO_calculate(sp.swapping(soln, swaps))
                scores = np.vstack((scores, sc))
            scores = np.delete(scores, 0, axis=0)
            scores_t = np.concatenate((scores_t, scores))
            p_front_scores_x = pf.pareto_ranking(
                scores)  # not really pareto front, with some that are not on pareto front, but also quite good
            pareto_front = np.concatenate((pareto_front, p_front_scores_x), axis=0)  # will have to squeeze later

            c = random.choice(p_front_scores_x)
            c_index = np.where((scores == c).all(axis=1))[0][0]
            c_soln = sp.swapping(soln, legal_swaps[c_index])
            while c in tabu_list[index]:
                print('tabu!')
                c = random.choice(p_front_scores_x)
                c_index = np.where((scores == c).all(axis=1))[0][0]
                c_soln = sp.swapping(soln, legal_swaps[c_index])
            new_search_front_scores.append(c)  # the next iteration's soln list
            new_search_front.append(c_soln)
            # update tabu list
            tabu_list[index].pop(0)
            tabu_list[index].extend(c * tabu_tenure)
        scores_t = np.delete(scores_t, 0, axis=0)
        print(new_search_front_scores)
        soln_list = new_search_front

    pareto_front = np.delete(pareto_front, 0, axis=0)
    pareto_front_final = np.array(pt.eps_sort(pareto_front))
    print("Pareto Front Scores:")
    print(pareto_front_final)

    # find minimum overtime score
    min_over_timescore = pareto_front_final[np.argmin(pareto_front_final[:, 0]), :]
    print("Minimum Overtime Score")
    print(min_over_timescore)
    t1 = time.time()
    print("Time Taken for TS: " + str(t1 - t0) + ' seconds')

    # sol_list = [soln, schedule_days]
    # thread1 = Thread(target=show_timetable, args=[sol_list])
    # thread1.start()
    # thread2 = Thread(target=create_table, args=(soln, schedule_date))
    # thread2.start()
    sol_list = [soln, schedule_days, schedule_date]
    thread1 = Thread(target=show_timetable, args=[sol_list])
    thread1.start()

    pf.plot_front(scores, pareto_front_final)