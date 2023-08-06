import numpy as np
import random
import copy
import pareto as pt
from SDP18py.Generate_initial_solution import initial_solution_random_fit


def pareto_ranking(scores1, solns, n):
	scores = copy.deepcopy(scores1)
	pareto_rankings = {}
	pareto_sorted_scores = []
	pareto_sorted_soln = []
	rank = 0
	n_pop = 0
	while len(scores) != 0:
		pareto_efficient_pts = pt.eps_sort(scores)
		l = len(pareto_efficient_pts)
		n_pop += l
		if n_pop >= n:
			overshot = n_pop-n
			pareto_efficient_pts = pareto_efficient_pts[0:(l-overshot)]
			pareto_rankings[rank] = pareto_efficient_pts
			pareto_sorted_scores = pareto_sorted_scores + pareto_efficient_pts
			scores = [x for x in scores if x not in pareto_efficient_pts]
			rank += 1
			for i in pareto_efficient_pts:
				loc = np.where((scores1 == np.array(i)).all(axis=1))[0][0]
				pareto_sorted_soln.append(solns[loc])
			return pareto_rankings, pareto_sorted_scores, pareto_sorted_soln
		pareto_rankings[rank] = pareto_efficient_pts
		pareto_sorted_scores = pareto_sorted_scores + pareto_efficient_pts
		scores = [x for x in scores if x not in pareto_efficient_pts]
		rank += 1
		for i in pareto_efficient_pts:
			loc = np.where((scores1 == np.array(i)).all(axis=1))[0][0]
			pareto_sorted_soln.append(solns[loc])
	return pareto_rankings, pareto_sorted_scores, pareto_sorted_soln


def pareto_score_soln_sore(scores1, soln):
	scores = copy.deepcopy(scores1)
	pareto_sorted_scores = []
	pareto_sorted_soln = []


def select_two_parent(ranks, list_scores, list_soln):
	# roulette wheel to select parent
	dict_len = len(ranks)
	frac = np.flip(np.arange(start=1, stop=dict_len+1))
	space = np.sum(frac)
	frac = frac/space
	cum_frac = np.cumsum(frac)
	r1 = random.uniform(0, 1)
	r2 = random.uniform(0, 1)
	rank_chosen1 = np.argwhere(cum_frac>r1)[0][0]
	rank_chosen2 = np.argwhere(cum_frac>r2)[0][0]
	p1_score = random.choice(ranks[rank_chosen1])
	p2_score = random.choice(ranks[rank_chosen2])
	p1_score_loc = np.where((list_scores==np.array(p1_score)).all(axis=1))[0][0]
	p2_score_loc = np.where((list_scores==np.array(p2_score)).all(axis=1))[0][0]
	return list_soln[p1_score_loc], list_soln[p2_score_loc]


def GA_crossover(p1, p2, sch_list, empty_schedule):
	child = copy.deepcopy(empty_schedule)
	clashes = []
	for to_sch in sch_list:
		r = random.randint(1, 2)
		surg = to_sch[0]
		if r == 1:
			p1_surg_loc = np.argwhere(p1==surg)
			if check_if_zero(child,p1_surg_loc):
				#put it in
				day = p1_surg_loc[0][0]
				OT = p1_surg_loc[0][1]
				start_ts = p1_surg_loc[0][2]
				end_ts = p1_surg_loc[-1][2] + 1
				np.put(child[day][OT], np.arange(start=start_ts, stop=end_ts), [surg])
			else:
				clashes.append(to_sch)
		elif r == 2:
			p2_surg_loc = np.argwhere(p2==surg)
			if check_if_zero(child,p2_surg_loc):
				#put it in
				day = p2_surg_loc[0][0]
				OT = p2_surg_loc[0][1]
				start_ts = p2_surg_loc[0][2]
				end_ts = p2_surg_loc[-1][2] + 1
				np.put(child[day][OT], np.arange(start=start_ts, stop=end_ts), [surg])
			else:
				clashes.append(to_sch)
	#print(clashes)
	return child, clashes


def GA_mutate(child, clashes, MAS_allowed, OT_indexes, day_of_week_indexes):
	if len(clashes)==0:
		return child
	else:
		child = initial_solution_random_fit(child, clashes, MAS_allowed, day_of_week_indexes, OT_indexes)
		return child


def check_if_zero(empty_schedule, locs):
	len_zero = len(locs)
	day = locs[0][0]
	OT = locs[0][1]
	start_ts = locs[0][2]
	end_ts = locs[-1][2] + 1
	partition = empty_schedule[day][OT][start_ts:end_ts]
	if np.all(partition == np.zeros(len_zero)):
		return True
	else:
		return False