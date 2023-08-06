import numpy as np
from SDP18py import swapper as sp
import copy
from SDP18py.MO_fitting_func_calc import MO_calculate
import random

def all_legal_swaps_subset(solution, to_schedule, MAS_allowed, day_of_week_indexes, OT_indexes):
	legal_swaps = []
	# to find legal swaps between inserted surgeries and empty
	zero_indexes = zero_runs_3d(solution)

	for index, surg in enumerate(to_schedule):

		surg_loc = np.argwhere(solution == surg[0])  # this is where the surgery is slotted

		for empty_slot in zero_indexes:

			days_away_emp = empty_slot[0]
			OT_emp = empty_slot[1]
			start_index_emp = empty_slot[2]
			end_index_emp = empty_slot[3]
			dur_emp = end_index_emp - start_index_emp
			empty_slot_day = day_of_week_indexes[days_away_emp]

			days_away_surg = surg_loc[0, 0]
			OT_surg = surg_loc[0, 1]
			start_index_surg = surg_loc[0, -1]
			end_index_surg = surg_loc[-1, -1]
			if dur_emp >= len(surg) and OT_indexes[OT_emp] in MAS_allowed[empty_slot_day]:  # add MAS constraint later
				legal_swaps.append(((surg[0], days_away_surg, OT_surg, start_index_surg, end_index_surg + 1),
				                    (0, days_away_emp, OT_emp, start_index_emp, end_index_emp + 1)))
	# to find swaps between 2 inserted surgeries
	for i, surg1 in enumerate(to_schedule):
		surg1_loc = np.argwhere(solution == surg1[0])
		days_away1 = surg1_loc[0, 0]
		OT1 = surg1_loc[0, 1]
		start_index1 = surg1_loc[0, -1]
		end_index1 = surg1_loc[-1, -1]
		dur1 = end_index1 - start_index1
		dur1withempty = dur1 + find_empty_ahead(solution, days_away1, OT1, end_index1)
		surg1_slot_day = day_of_week_indexes[days_away1]
		for j, surg2 in enumerate(to_schedule):
			if i < j:
				surg2_loc = np.argwhere(solution == surg2[0])
				days_away2 = surg2_loc[0, 0]
				OT2 = surg2_loc[0, 1]
				start_index2 = surg2_loc[0, -1]
				end_index2 = surg2_loc[-1, -1]
				dur2 = end_index2 - start_index2
				dur2withempty = dur2 + find_empty_ahead(solution, days_away2, OT2, end_index2)
				surg2_slot_day = day_of_week_indexes[days_away2]
				if dur1withempty >= dur2 and dur2withempty >= dur1:  # dont need check MAS because they are both slots with inserted surgeries, which means they must agree to MAS beforehand
					legal_swaps.append(((surg1[0], days_away1, OT1, start_index1, end_index1 + 1),
					                    (surg2[0], days_away2, OT2, start_index2, end_index2 + 1)))

	return random.sample(legal_swaps,50) # will increase speed of the calculation, at the cost of quality of solution


def all_legal_swaps_with_score_calculation(solution, to_schedule, MAS_allowed, day_of_week_indexes, OT_indexes):
	legal_swaps = []
	# to find legal swaps between inserted surgeries and empty
	zero_indexes = zero_runs_3d(solution)
	scores = []

	for index, surg in enumerate(to_schedule):

		surg_loc = np.argwhere(solution == surg[0])  # this is where the surgery is slotted

		for empty_slot in zero_indexes:

			days_away_emp = empty_slot[0]
			OT_emp = empty_slot[1]
			start_index_emp = empty_slot[2]
			end_index_emp = empty_slot[3]
			dur_emp = end_index_emp - start_index_emp
			empty_slot_day = day_of_week_indexes[days_away_emp]

			days_away_surg = surg_loc[0, 0]
			OT_surg = surg_loc[0, 1]
			start_index_surg = surg_loc[0, -1]
			end_index_surg = surg_loc[-1, -1]
			if dur_emp >= len(surg) and OT_indexes[OT_emp] in MAS_allowed[empty_slot_day]:  # add MAS constraint later
				legal_swaps.append(((surg[0], days_away_surg, OT_surg, start_index_surg, end_index_surg + 1),
				                    (0, days_away_emp, OT_emp, start_index_emp, end_index_emp + 1)))
				soln = copy.deepcopy(solution)
				new = sp.swapping(soln, ((surg[0], days_away_surg, OT_surg, start_index_surg, end_index_surg + 1),
				                    (0, days_away_emp, OT_emp, start_index_emp, end_index_emp + 1)))
				scores.append(MO_calculate(new))
	# to find swaps between 2 inserted surgeries
	for i, surg1 in enumerate(to_schedule):
		surg1_loc = np.argwhere(solution == surg1[0])
		days_away1 = surg1_loc[0, 0]
		OT1 = surg1_loc[0, 1]
		start_index1 = surg1_loc[0, -1]
		end_index1 = surg1_loc[-1, -1]
		dur1 = end_index1 - start_index1
		dur1withempty = dur1 + find_empty_ahead(solution, days_away1, OT1, end_index1)
		surg1_slot_day = day_of_week_indexes[days_away1]
		for j, surg2 in enumerate(to_schedule):
			if i < j:
				surg2_loc = np.argwhere(solution == surg2[0])
				days_away2 = surg2_loc[0, 0]
				OT2 = surg2_loc[0, 1]
				start_index2 = surg2_loc[0, -1]
				end_index2 = surg2_loc[-1, -1]
				dur2 = end_index2 - start_index2
				dur2withempty = dur2 + find_empty_ahead(solution, days_away2, OT2, end_index2)
				surg2_slot_day = day_of_week_indexes[days_away2]
				if dur1withempty >= dur2 and dur2withempty >= dur1:  # dont need check MAS because they are both slots with inserted surgeries, which means they must agree to MAS beforehand
					legal_swaps.append(((surg1[0], days_away1, OT1, start_index1, end_index1 + 1),
					                    (surg2[0], days_away2, OT2, start_index2, end_index2 + 1)))
					soln = copy.deepcopy(solution)
					new = sp.swapping(soln, ((surg1[0], days_away1, OT1, start_index1, end_index1 + 1),
					                    (surg2[0], days_away2, OT2, start_index2, end_index2 + 1)))
					scores.append(MO_calculate(new))
	return legal_swaps, np.array(scores)

def all_legal_swaps(solution, to_schedule, MAS_allowed, day_of_week_indexes, OT_indexes):
	legal_swaps = []
	# to find legal swaps between inserted surgeries and empty
	zero_indexes = zero_runs_3d(solution)

	for index, surg in enumerate(to_schedule):

		surg_loc = np.argwhere(solution == surg[0])  # this is where the surgery is slotted

		for empty_slot in zero_indexes:

			days_away_emp = empty_slot[0]
			OT_emp = empty_slot[1]
			start_index_emp = empty_slot[2]
			end_index_emp = empty_slot[3]
			dur_emp = end_index_emp - start_index_emp
			empty_slot_day = day_of_week_indexes[days_away_emp]

			days_away_surg = surg_loc[0, 0]
			OT_surg = surg_loc[0, 1]
			start_index_surg = surg_loc[0, -1]
			end_index_surg = surg_loc[-1, -1]
			if dur_emp >= len(surg) and OT_indexes[OT_emp] in MAS_allowed[empty_slot_day]:  # add MAS constraint later
				legal_swaps.append(((surg[0], days_away_surg, OT_surg, start_index_surg, end_index_surg + 1), (0, days_away_emp, OT_emp, start_index_emp, end_index_emp + 1)))
	# to find swaps between 2 inserted surgeries
	for i, surg1 in enumerate(to_schedule):
		surg1_loc = np.argwhere(solution == surg1[0])
		days_away1 = surg1_loc[0,0]
		OT1 = surg1_loc[0, 1]
		start_index1 = surg1_loc[0, -1]
		end_index1 = surg1_loc[-1, -1]
		dur1 = end_index1 - start_index1
		dur1withempty = dur1 + find_empty_ahead(solution, days_away1, OT1, end_index1)
		surg1_slot_day = day_of_week_indexes[days_away1]
		for j, surg2 in enumerate(to_schedule):
			if i < j:
				surg2_loc = np.argwhere(solution == surg2[0])
				days_away2 = surg2_loc[0, 0]
				OT2 = surg2_loc[0, 1]
				start_index2 = surg2_loc[0, -1]
				end_index2 = surg2_loc[-1, -1]
				dur2 = end_index2 - start_index2
				dur2withempty = dur2 + find_empty_ahead(solution, days_away2, OT2, end_index2)
				surg2_slot_day = day_of_week_indexes[days_away2]
				if dur1withempty >= dur2 and dur2withempty >= dur1: # dont need check MAS because they are both slots with inserted surgeries, which means they must agree to MAS beforehand
					legal_swaps.append(((surg1[0], days_away1, OT1, start_index1, end_index1 + 1),(surg2[0],days_away2, OT2, start_index2, end_index2 + 1)))

	return legal_swaps


def zero_runs_3d(a):
	iszero = np.equal(a, 0)
	npad = ((0, 0), (0, 0), (1, 1))
	iszero = np.pad(iszero, pad_width=npad, mode='constant', constant_values=0).view(np.int8)
	absdiff = np.abs(np.diff(iszero, axis=2))
	ranges = np.argwhere(absdiff == 1)
	even = ranges[::2]
	odd_c = ranges[1::2][:, 2:]
	return np.hstack((even, odd_c))



def find_empty_ahead(soln, days_away, OT, end):
	block = soln[days_away][OT]
	i = end
	extrazero = 0
	while block[i] == 0:
		extrazero += 1
		i += 1
	return extrazero


def zero_runs(a):
	# Create an array that is 1 where a is 0, and pad each end with an extra 0.
	iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
	absdiff = np.abs(np.diff(iszero))
	# Runs start and end where absdiff is 1.
	r = np.where(absdiff==1)[0]
	ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
	lendiff = np.diff(ranges, axis=1)
	return ranges.tolist(), lendiff.tolist()