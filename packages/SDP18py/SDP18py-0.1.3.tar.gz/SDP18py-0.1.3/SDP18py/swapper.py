import numpy as np
import copy
import time

def swapping(soln, swap):

	temp_soln = copy.deepcopy(soln)
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
	if swap1name == 0 or swap2name == 0:

		if swap1name == 0:
			np.put(temp_soln[swap1day][swap1OT], np.arange(start=swap1start, stop=(swap1start+(swap2end-swap2start))), swap2name)
			np.put(temp_soln[swap2day][swap2OT], np.arange(start=swap2start, stop=swap2end), 0)
		elif swap2name == 0:
			np.put(temp_soln[swap2day][swap2OT], np.arange(start=swap2start, stop=(swap2start+(swap1end-swap1start))), swap1name)
			np.put(temp_soln[swap1day][swap1OT], np.arange(start=swap1start, stop=swap1end), 0)
	elif swap1name != 0 and swap2name != 0:

		block1 = copy.deepcopy(temp_soln[swap1day][swap1OT][swap1start:swap1end])
		block2 = copy.deepcopy(temp_soln[swap2day][swap2OT][swap2start:swap2end])
		len1 = len(block1)
		len2 = len(block2)
		len_diff = abs(len1-len2)
		if len1 > len2:
			block2 = np.hstack(block2, [0] * len_diff)
			temp_soln[swap1day][swap1OT][swap1start:swap1end] = block2
			temp_soln[swap2day][swap2OT][swap2start:(swap2end+len_diff)] = block1
		elif len1 < len2:
			block1 = np.hstack(block1, [0] * (len1-len2))
			temp_soln[swap2day][swap2OT][swap2start:swap2end] = block1
			temp_soln[swap1day][swap1OT][swap1start:(swap1end+len_diff)] = block2
		else: #equal length
			temp_soln[swap1day][swap1OT][swap1start:swap1end] = block2
			temp_soln[swap2day][swap2OT][swap2start:swap2end] = block1
	return temp_soln



def pushback2(soln):
	temp_ = copy.deepcopy(soln)
	temp_[temp_ > 2000000] = 9999999
	temp_diff = np.diff(temp_, axis=2)
	indices = (temp_diff > 1100000) & (temp_diff < 1300000)  # find indexes where its empty before a swappable surgery
	match = np.argwhere(indices==True)
	for index_match in match:
		day = index_match[0]
		OT = index_match[1]
		index_of_first_0_end = index_match[2] + 1
		index_of_first_0_start = trailzero(soln[day][OT], index_of_first_0_end - 1)
		index_of_surg_end = trialsurg(soln[day][OT], index_of_first_0_end + 1)
		surg_code = soln[day][OT][index_of_first_0_end + 1]
		trailing0_len = index_of_first_0_end - index_of_first_0_start
		index_of_surg_replace_start = index_of_surg_end - trailing0_len
		np.put(soln[day][OT], np.arange(start=index_of_first_0_start, stop=index_of_first_0_end), [surg_code])
		np.put(soln[day][OT], np.arange(start=index_of_surg_replace_start, stop=index_of_surg_end), [0])
	# check if its done else re do
	temp_ = copy.deepcopy(soln)
	temp_[temp_ > 2000000] = 9999999
	temp_diff = np.diff(temp_, axis=2)
	indices = (temp_diff > 1100000) & (temp_diff < 1300000)  # find indexes where its empty before a swappable surgery
	match = np.argwhere(indices == True)
	if len(match) != 0:
		print("re-pushback")
		pushback2(soln)
	return


def trialsurg(a, b):
	surg_code = a[b]
	while a[b] == surg_code:
		b = b + 1
		if b == 44:
			return b

	return b


def trailzero(a, b):

	while a[b] == 0:
		b = b-1
		if b == 0:
			return b
	return b + 1