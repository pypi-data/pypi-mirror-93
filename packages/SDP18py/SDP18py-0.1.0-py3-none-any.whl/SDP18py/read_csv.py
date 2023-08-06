import numpy as np
import os
import csv
from tkinter import *
from tkinter import filedialog
from datetime import *


# current schedule should have 23 OTs and 44 Rows(to represent 44-15min timeslots)
# current_schedule = np.zeros((5,23,44))

# possible ways to read the data
# find number of unique dates in the csv file
# create numpy array with (23,44,n) where n corresponds to number of unique days in current schedule


def read_csv():

    # this is a window prompt for selecting csv file to be read
    dialog_root = Tk()
    dialog_root.geometry("1200x700+350+150")
    dialog_root.withdraw()

    # this will obtain file path of the selected csv file
    file_path = filedialog.askopenfilename(title='Please select the schedule .csv file')
    file_path = os.path.normpath(file_path)

    current_dates = [] # store the list of unique dates in the csv file
    temp_days = []  # this temp list will number of days from now for each unique date, 3, 4 ...
    key_list = []

    # this will find number of unique dates in the current schedule
    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        next(mock_csv, None)  # skip header
        for row in mock_csv:  # get unique dates in the csv file
            items = row[1].split(' ')
            if items[0] not in current_dates:
                current_dates.append(items[0])

    # for each day in current_dates, create a dictionary i.e day4 = {}
    for i in current_dates:
        selected_date = datetime.strptime(i, '%d/%m/%Y').date()
        days_from_now = (selected_date - date.today()).days
        temp_days.append(days_from_now)  # the days from today for each day_dictionary is stored in temp_days

    for i in range(len(temp_days)):
        key_list.append(i)

    d1 = '2020-11-30'
    d1 = datetime.strptime(d1, '%Y-%m-%d').date()
    d2 = '2020-12-01'
    d2 = datetime.strptime(d2, '%Y-%m-%d').date()
    d3 = '2020-12-02'
    d3 = datetime.strptime(d3, '%Y-%m-%d').date()
    d4 = '2020-12-03'
    d4 = datetime.strptime(d4, '%Y-%m-%d').date()
    d5 = '2020-12-04'
    d5 = datetime.strptime(d5, '%Y-%m-%d').date()

    week_dict = {0: 1, 7: 2, 14: 3, 21: 4, 28: 5}

    value_list = []

    for i in temp_days:  # this will load all the necessary days into the current_schedule dictionary
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Monday':
            temp_date = (((date.today() + timedelta(days=i))-d1).days)%35
            value_list.append((date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Tuesday':
            temp_date = (((date.today() + timedelta(days=i))-d2).days)%35
            value_list.append((date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Wednesday':
            temp_date = (((date.today() + timedelta(days=i))-d3).days)%35
            value_list.append((date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Thursday':
            temp_date = (((date.today() + timedelta(days=i))-d4).days)%35
            value_list.append((date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Friday':
            temp_date = (((date.today() + timedelta(days=i))-d5).days)%35
            value_list.append((date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))

    day_of_week_index = {key_list[i]: value_list[i] for i in range(len(key_list))}

    # create current schedule numpy array filled with zeros
    current_schedule = np.zeros((len(current_dates), 23, 44), dtype=np.int32)

    # (days, OT, time)
    # 20121300 = [2] unswappable, [0] currentsurgery, [12] Discipline type 12, [13] Procedure 13, [0] = not important for unswappable surgeries
    # Everytime its on the array, means the 15 min slot is taken up
    # everything on the initial current scehdule will start with 20
    # All inserted surgeries will begin with 1 (swappable),
    # Second digit of inserted surgeries will be 1 (actual) or 2(predicted)
    # axis = 2 will always be of length 44

    # discipline dictionary to identify code
    discipline_codes = {10: 'BREAST',
                        11: 'OTO',
                        12: 'NES',
                        13: 'CLR',
                        14: 'HPB',
                        15: 'PLS',
                        16: 'ENT',
                        17: 'SUR-ONCO',
                        18: 'UGI',
                        19: 'H&N',
                        20: 'O&G',
                        21: 'HND',
                        22: 'OMS',
                        23: 'VAS',
                        24: 'CTS',
                        25: 'URO'
                        }

    key_list = list(discipline_codes.keys())
    value_list = list(discipline_codes.values())

    # ot_list in order
    ot_list = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'M1', 'M2', 'M3', 'M4', 'M5', 'OT 24',
               'OT 25', 'OT 22', 'R1', 'R4', 'R5', 'R6', 'R7', 'R8', 'MRI']

    current_schedule_list = []

    # read each line in csv and append details to the respective 'OT' dictionaries
    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        # skip header
        next(mock_csv, None)
        for row in mock_csv:
            start_date = row[1].split(' ')
            end_date = row[2].split(' ')
            start_time = start_date[1]  # start time
            end_time = end_date[1]  # end time
            # codes to convert time into appropriate format 08:15 = 8.25, 10:45 = 10.75
            start_time_new = datetime.strptime(start_time, '%H:%M').time()
            end_time_new = datetime.strptime(end_time, '%H:%M').time()
            start_time_deci = (start_time_new.hour + start_time_new.minute / 60.0)
            start_index = int((start_time_deci - 8)/0.25)
            end_time_deci = (end_time_new.hour + end_time_new.minute / 60.0)
            end_index = int((end_time_deci - 8)/0.25)
            duration = int((end_time_deci - start_time_deci)/0.25)  # calculate duration in 15min blocks
            date_index = current_dates.index(start_date[0])  # gets index of the current date
            # this will append the necessary codes into each OT array
            position = value_list.index(row[4])
            current_schedule[date_index, ot_list.index(row[5]), start_index:end_index] = 2000000 + (key_list[position])*1000

    # check current_dates and add 'temp_days' and 'current_dates'
    if (datetime.strptime(current_dates[-1], '%d/%m/%Y').date()).strftime('%A') == 'Friday':
        x1 = (datetime.strptime(current_dates[-1], '%d/%m/%Y').date())
        x2 = temp_days[-1]
        temp_array = np.zeros([1, 23, 44], dtype=np.int32)
        dict_elem_count = len(current_dates)
        mas_week_count = int(day_of_week_index[dict_elem_count - 1].split('y')[1])
        if mas_week_count != 5:
            mas_week_count = mas_week_count + 1
        else:
            mas_week_count = 1
        for i in range(3, 8):
            new_date = x1 + timedelta(days=i)
            new_datez = new_date.strftime("%d/%m/%Y")
            new_day = new_date.strftime('%A')
            current_dates.append(new_datez)
            new_dayfromnow = x2 + i
            temp_days.append(new_dayfromnow)
            current_schedule = np.concatenate([current_schedule, temp_array], axis=0)
            day_of_week_index[dict_elem_count] = str(new_day) + str(mas_week_count)
            dict_elem_count = dict_elem_count + 1

    current_schedule_list.append(current_schedule)
    current_schedule_list.append(temp_days)
    current_schedule_list.append(current_dates)
    current_schedule_list.append(day_of_week_index)

    return current_schedule_list


def read_csv1(file_path):
    # this is a window prompt for selecting csv file to be read
    dialog_root = Tk()
    dialog_root.geometry("1200x700+350+150")
    dialog_root.withdraw()

    current_dates = []  # store the list of unique dates in the csv file
    temp_days = []  # this temp list will number of days from now for each unique date, 3, 4 ...
    key_list = []

    # this will find number of unique dates in the current schedule
    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        next(mock_csv, None)  # skip header
        for row in mock_csv:  # get unique dates in the csv file
            items = row[1].split(' ')
            if items[0] not in current_dates:
                current_dates.append(items[0])

    # for each day in current_dates, create a dictionary i.e day4 = {}
    for i in current_dates:
        selected_date = datetime.strptime(i, '%d/%m/%Y').date()
        days_from_now = (selected_date - date.today()).days
        temp_days.append(days_from_now)  # the days from today for each day_dictionary is stored in temp_days

    for i in range(len(temp_days)):
        key_list.append(i)

    d1 = '2020-11-30'
    d1 = datetime.strptime(d1, '%Y-%m-%d').date()
    d2 = '2020-12-01'
    d2 = datetime.strptime(d2, '%Y-%m-%d').date()
    d3 = '2020-12-02'
    d3 = datetime.strptime(d3, '%Y-%m-%d').date()
    d4 = '2020-12-03'
    d4 = datetime.strptime(d4, '%Y-%m-%d').date()
    d5 = '2020-12-04'
    d5 = datetime.strptime(d5, '%Y-%m-%d').date()

    week_dict = {0: 1, 7: 2, 14: 3, 21: 4, 28: 5}

    value_list = []

    for i in temp_days:  # this will load all the necessary days into the current_schedule dictionary
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Monday':
            temp_date = (((date.today() + timedelta(days=i)) - d1).days) % 35
            value_list.append((date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Tuesday':
            temp_date = (((date.today() + timedelta(days=i)) - d2).days) % 35
            value_list.append((date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Wednesday':
            temp_date = (((date.today() + timedelta(days=i)) - d3).days) % 35
            value_list.append((date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Thursday':
            temp_date = (((date.today() + timedelta(days=i)) - d4).days) % 35
            value_list.append((date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Friday':
            temp_date = (((date.today() + timedelta(days=i)) - d5).days) % 35
            value_list.append((date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))

    day_of_week_index = {key_list[i]: value_list[i] for i in range(len(key_list))}

    # create current schedule numpy array filled with zeros
    current_schedule = np.zeros((len(current_dates), 23, 44), dtype=np.int32)

    # (days, OT, time)
    # 20121300 = [2] unswappable, [0] currentsurgery, [12] Discipline type 12, [13] Procedure 13, [0] = not important for unswappable surgeries
    # Everytime its on the array, means the 15 min slot is taken up
    # everything on the initial current scehdule will start with 20
    # All inserted surgeries will begin with 1 (swappable),
    # Second digit of inserted surgeries will be 1 (actual) or 2(predicted)
    # axis = 2 will always be of length 44

    # discipline dictionary to identify code
    discipline_codes = {10: 'BREAST',
                        11: 'OTO',
                        12: 'NES',
                        13: 'CLR',
                        14: 'HPB',
                        15: 'PLS',
                        16: 'ENT',
                        17: 'SUR-ONCO',
                        18: 'UGI',
                        19: 'H&N',
                        20: 'O&G',
                        21: 'HND',
                        22: 'OMS',
                        23: 'VAS',
                        24: 'CTS',
                        25: 'URO'
                        }

    key_list = list(discipline_codes.keys())
    value_list = list(discipline_codes.values())

    # ot_list in order
    ot_list = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'M1', 'M2', 'M3', 'M4', 'M5', 'OT 24',
               'OT 25', 'OT 22', 'R1', 'R4', 'R5', 'R6', 'R7', 'R8', 'MRI']

    current_schedule_list = []

    # read each line in csv and append details to the respective 'OT' dictionaries
    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        # skip header
        next(mock_csv, None)
        for row in mock_csv:
            start_date = row[1].split(' ')
            end_date = row[2].split(' ')
            start_time = start_date[1]  # start time
            end_time = end_date[1]  # end time
            # codes to convert time into appropriate format 08:15 = 8.25, 10:45 = 10.75
            start_time_new = datetime.strptime(start_time, '%H:%M').time()
            end_time_new = datetime.strptime(end_time, '%H:%M').time()
            start_time_deci = (start_time_new.hour + start_time_new.minute / 60.0)
            start_index = int((start_time_deci - 8) / 0.25)
            end_time_deci = (end_time_new.hour + end_time_new.minute / 60.0)
            end_index = int((end_time_deci - 8) / 0.25)
            duration = int((end_time_deci - start_time_deci) / 0.25)  # calculate duration in 15min blocks
            date_index = current_dates.index(start_date[0])  # gets index of the current date
            # this will append the necessary codes into each OT array
            position = value_list.index(row[4])
            current_schedule[date_index, ot_list.index(row[5]), start_index:end_index] = 2000000 + (
            key_list[position]) * 1000

    # check current_dates and add 'temp_days' and 'current_dates'
    if (datetime.strptime(current_dates[-1], '%d/%m/%Y').date()).strftime('%A') == 'Friday':
        x1 = (datetime.strptime(current_dates[-1], '%d/%m/%Y').date())
        x2 = temp_days[-1]
        temp_array = np.zeros([1, 23, 44], dtype=np.int32)
        dict_elem_count = len(current_dates)
        mas_week_count = int(day_of_week_index[dict_elem_count - 1].split('y')[1])
        if mas_week_count != 5:
            mas_week_count = mas_week_count + 1
        else:
            mas_week_count = 1
        for i in range(3, 8):
            new_date = x1 + timedelta(days=i)
            new_datez = new_date.strftime("%d/%m/%Y")
            new_day = new_date.strftime('%A')
            current_dates.append(new_datez)
            new_dayfromnow = x2 + i
            temp_days.append(new_dayfromnow)
            current_schedule = np.concatenate([current_schedule, temp_array], axis=0)
            day_of_week_index[dict_elem_count] = str(new_day) + str(mas_week_count)
            dict_elem_count = dict_elem_count + 1

    current_schedule_list.append(current_schedule)
    current_schedule_list.append(temp_days)
    current_schedule_list.append(current_dates)
    current_schedule_list.append(day_of_week_index)

    return current_schedule_list