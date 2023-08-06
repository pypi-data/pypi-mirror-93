import numpy as np
import math


def MO_calculate(soln):
	over_time_score = 0
	idle_time_score = 0
	waiting_time_score = 0
	alpha = 2.0  # multiplier for actual surgeries
	beta = 1.0  # multiplier for predicted surgeries

	# overtime
	last2hrs = soln[:, :, -8:]
	overtime_surg = last2hrs[last2hrs != 0]
	overtime_surg_type = [float(str(x)[1:2]) for x in overtime_surg]
	overtime_surg_type = np.array(overtime_surg_type)
	overtime_surg_type[overtime_surg_type == 1] *= alpha
	overtime_surg_type[overtime_surg_type == 2] *= beta
	over_time_score = sum(overtime_surg_type * 15)

	# idletime
	first9hrs = soln[:, :, :-8]
	zero_count = np.count_nonzero(first9hrs == 0, axis=2)
	days_away = np.arange(start=1, stop=len(zero_count) + 1)
	days_away = np.exp(days_away*-0.1)
	zero_count_t = zero_count.transpose()
	res = np.multiply(zero_count_t, days_away)
	res = res.flatten()
	idle_time_score = sum(res)

	# waiting time:
	inserted_surg = np.where((soln//100000>=20), 0, soln)
	inserted_surg = inserted_surg.reshape(len(inserted_surg), -1)
	inserted_surg[:, 1:] *= (np.diff(inserted_surg, axis=1) != 0)
	days_away = np.arange(start=1, stop=len(zero_count) + 1)
	inserted_surg = np.where((inserted_surg//100000==12),beta, inserted_surg)
	inserted_surg = np.where((inserted_surg//100000==11), alpha, inserted_surg)
	inserted_surg_t = inserted_surg.transpose()
	res_w = np.multiply(inserted_surg_t, days_away)
	res_w = res_w.flatten()
	waiting_time_score = sum(res_w)

	return np.array([over_time_score, idle_time_score, waiting_time_score])


def MO_calculate_diff(soln, curr_score, swap):

	alpha = 2.0  # multiplier for actual surgeries
	beta = 1.0  # multiplier for predicted surgeries

	score_vec1 = []
	score_vec2 = []
	swap1name = swap[0][0]
	swap1day = swap[0][1]
	swap1OT = swap[0][2]
	swap1start = swap[0][3]
	swap1end = swap[0][4]
	swap2name = swap[1][0]
	swap2day = swap[1][1]
	swap2OT = swap[1][2]
	swap2start = swap[1][3]
	swap2end = swap[1][4]
	# calculate scores for first slot
	overtime1 = soln[swap1day][swap1OT][swap1start]
	#idletime1 =
	if int(str(swap1name)[:2]) == 11:
		waitingtime1 = swap1day * alpha
	elif int(str(swap1name)[:2]) == 12:
		waitingtime1 = swap1day * beta
	#else:
		print("Warning: not 11 nor 12")
	# calculate scores for secon slot


def calc_crowding_distance(F):
	infinity = 1e+14

	n_points = F.shape[0]
	n_obj = F.shape[1]

	if n_points <= 2:
		return np.full(n_points, infinity)
	else:

		# sort each column and get index
		I = np.argsort(F, axis=0, kind='mergesort')

		# now really sort the whole array
		F = F[I, np.arange(n_obj)]

		# get the distance to the last element in sorted list and replace zeros with actual values
		dist = np.concatenate([F, np.full((1, n_obj), np.inf)]) \
		       - np.concatenate([np.full((1, n_obj), -np.inf), F])

		index_dist_is_zero = np.where(dist == 0)

		dist_to_last = np.copy(dist)
		for i, j in zip(*index_dist_is_zero):
			dist_to_last[i, j] = dist_to_last[i - 1, j]

		dist_to_next = np.copy(dist)
		for i, j in reversed(list(zip(*index_dist_is_zero))):
			dist_to_next[i, j] = dist_to_next[i + 1, j]

		# normalize all the distances
		norm = np.max(F, axis=0) - np.min(F, axis=0)
		norm[norm == 0] = np.nan
		dist_to_last, dist_to_next = dist_to_last[:-1] / norm, dist_to_next[1:] / norm

		# if we divided by zero because all values in one columns are equal replace by none
		dist_to_last[np.isnan(dist_to_last)] = 0.0
		dist_to_next[np.isnan(dist_to_next)] = 0.0

		# sum up the distance to next and last and norm by objectives - also reorder from sorted list
		J = np.argsort(I, axis=0)
		crowding = np.sum(dist_to_last[J, np.arange(n_obj)] + dist_to_next[J, np.arange(n_obj)], axis=1) / n_obj

	# replace infinity with a large number
	crowding[np.isinf(crowding)] = infinity

	return crowding


def calculate_delta_S(curr, neighbor, T): # scalarizing function
	lambda_o = 1
	lambda_i = 5
	lambda_w = 5
	lambda_ = [lambda_o, lambda_i, lambda_w]
	diff_vector = MO_calculate(neighbor) - MO_calculate(curr)
	pi = np.where(diff_vector <= 0, 1, np.exp(-diff_vector/T))
	v = np.power(pi, lambda_)
	return np.prod(v)