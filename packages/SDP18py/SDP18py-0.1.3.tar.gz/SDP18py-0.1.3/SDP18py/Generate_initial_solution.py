import random
import numpy as np
import copy


def zero_runs(a):
	# Create an array that is 1 where a is 0, and pad each end with an extra 0.
	iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
	absdiff = np.abs(np.diff(iszero))
	# Runs start and end where absdiff is 1.
	r = np.where(absdiff==1)[0]
	ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
	return ranges


def zero_runs_3d(a):
	iszero = np.equal(a, 0)
	npad = ((0, 0), (0, 0), (1, 1))
	iszero = np.pad(iszero, pad_width=npad, mode='constant', constant_values=0).view(np.int8)
	absdiff = np.abs(np.diff(iszero, axis=2))
	ranges = np.argwhere(absdiff == 1)
	even = ranges[::2]
	odd_c = ranges[1::2][:, 2:]
	return np.hstack((even, odd_c))


def initial_solution_first_fit(current_schedule, to_schedule, MAS_allowed, day_of_week_indexes, OT_indexes):
	for slot in to_schedule:
		flag = False
		for index_days, days in enumerate(current_schedule):
			current_day = day_of_week_indexes[index_days]
			for index_OT, OT in enumerate(days):
				if not OT_indexes[index_OT] in MAS_allowed[current_day]:
					continue
				zero_index = zero_runs(OT)
				zero_index_diff = np.diff(zero_index, axis=1) # length of 0 slots
				bool_vec = len(slot) <= zero_index_diff
				if np.any(bool_vec):
					legal_slot_index = np.argmax(bool_vec, axis=0)
					l = zero_index[legal_slot_index][0, 0]
					r = l + len(slot)
					OT[l:r] = slot
					flag = True
					break
			if flag:
				break
		if not flag:
			slot_dur = len(slot) * 15
			print(str(slot[0]) + " of " + str(
				slot_dur) + " mins has no possible arrangements, extend horizon or reduce number of cases to schedule")
	return current_schedule


def initial_solution_random_fit(current_schedule, ts, MAS_allowed, day_of_week_indexes, OT_indexes):
	to_schedule = copy.deepcopy(ts)
	curr_sche = copy.deepcopy(current_schedule)
	while len(to_schedule) != 0:
		zero_index = zero_runs_3d(curr_sche)
		z = np.hstack((zero_index[:, :2], np.diff(zero_index[:, 2:], axis=1)))
		slot_index = random.choice(range(len(to_schedule)))
		slot = to_schedule[slot_index]
		slot_len = len(slot)
		r = [1 if (OT_indexes[i[1]] in MAS_allowed[day_of_week_indexes[i[0]]] and i[2] > slot_len) else 0 for i in z]
		idx_nonzero = np.nonzero(r)
		#print(len(idx_nonzero[0]))
		if len(idx_nonzero[0]) == 0:
			print("no slot for surgery " + str(slot[0]) + ", try extending horizon or changing to use first fit")
			to_schedule.pop(slot_index)
			continue
		random_pick_legal_slot = np.random.choice(idx_nonzero[0])  # random choice of a slot that is legal
		day_chosen = zero_index[random_pick_legal_slot][0]
		OT_chosen = zero_index[random_pick_legal_slot][1]
		chosen_start = zero_index[random_pick_legal_slot][2]
		chosen_end = zero_index[random_pick_legal_slot][3]
		np.put(curr_sche[day_chosen][OT_chosen], np.arange(start=chosen_start, stop=chosen_start + slot_len),
		       slot[0])
		to_schedule.pop(slot_index)
	return curr_sche