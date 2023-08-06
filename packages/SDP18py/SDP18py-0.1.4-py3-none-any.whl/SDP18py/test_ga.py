import numpy as np
from SDP18py.Generate_initial_solution import initial_solution_random_fit
from SDP18py.MO_fitting_func_calc import MO_calculate
import pareto as pt
from SDP18py import genetic_algo_functions as ga
from SDP18py.plot_pareto_front import plot_front
import time
import copy
from SDP18py.view_timetable1 import show_timetable
from threading import Thread


def run_ga(current_schedule_list, to_schedule_read, mas_read, disc_select):

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
    # current_schedule = read_csv()
    # current_schedule = current_schedule[0]
    empty_schedule = copy.deepcopy(current_schedule)
    # to_schedule = read_toschedule()
    MAS_full = mas_read
    # MAS_full = read_mas()

    # MAS_allowed = MAS_full['OTO']
    MAS_allowed = MAS_full[disc_select]

    # first fit or random fit
    print("GENETIC ALGORITHM")
    n_pop = 30
    list_soln = []
    list_scores = []
    soln_list = []
    iter_ = 50
    t0 = time.time()
    # Generate population of solutions first
    for i in range(n_pop):
        current_schedule_temp = copy.deepcopy(current_schedule)
        soln = initial_solution_random_fit(current_schedule_temp, to_schedule, MAS_allowed, day_index, OT_indexes)
        score = MO_calculate(soln).tolist()
        list_soln.append(soln)
        list_scores.append(score)

    old_pop = list_soln
    # do non domintated sort
    pareto_ranks, pareto_sorted_scores, pareto_sorted_solns = ga.pareto_ranking(list_scores, old_pop, n_pop)
    for i in range(iter_):
        child_pop = []
        for _ in range(n_pop):
            # parent selection
            p1, p2 = ga.select_two_parent(pareto_ranks, list_scores, old_pop)
            # crossover + mutation
            child, clashes = ga.GA_crossover(p1, p2, to_schedule, empty_schedule)
            child = ga.GA_mutate(child, clashes, MAS_allowed, OT_indexes, day_index)
            child_pop.append(child)
        total_pop = old_pop + child_pop
        # calculate the new population scores, which consists of all new and old populations
        list_scores = []
        for soln in total_pop:
            list_scores.append(MO_calculate(soln).tolist())

        pareto_ranks, pareto_sorted_scores, pareto_sorted_solns = ga.pareto_ranking(list_scores, total_pop, n_pop)
        # take top n_pop solutions
        old_pop = pareto_sorted_solns[0:n_pop]
        list_scores = pareto_sorted_scores[0:n_pop]
        print(pareto_sorted_scores[0:n_pop])

    a = copy.deepcopy(list_scores)
    non_dom_scores = np.array(pt.eps_sort(list_scores))
    print("Pareto Front Scores:")
    print(non_dom_scores)

    # find minimum overtime score
    min_over_timescore = non_dom_scores[np.argmin(non_dom_scores[:, 0]), :]
    print("Minimum Overtime Score")
    print(min_over_timescore)
    min_index = np.where((pareto_sorted_scores == min_over_timescore).all(axis=1))[0][0]
    soln = pareto_sorted_solns[min_index]
    t1 = time.time()
    print("Time Taken for GA: " + str(t1 - t0) + ' seconds')

    # sol_list = [soln, schedule_days]
    sol_list = [soln, schedule_days, schedule_date]
    thread1 = Thread(target=show_timetable, args=[sol_list])
    thread1.start()
    # thread2 = Thread(target=create_table, args=(soln, schedule_date))
    # thread2.start()

    plot_front(np.array(a), non_dom_scores)