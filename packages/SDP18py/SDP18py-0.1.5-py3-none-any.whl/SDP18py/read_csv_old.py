import os
import csv
from tkinter import *
from tkinter import filedialog
from datetime import *
from SDP18py.view_timetable_old import show_timetable


def read_csv():

    # this is a window prompt for selecting csv file to be read
    dialog_root = Tk()
    dialog_root.geometry("1200x700+350+150")
    dialog_root.withdraw()

    # this will obtain file path of the selected csv file
    file_path = filedialog.askopenfilename(title='Please select the schedule .csv file')
    file_path = os.path.normpath(file_path)

    current_schedules = {}  # this will be the final output consisting of all the required information
    current_dates = []  # this will store the unique dates in the csv i.e 17/11/2020, 18/11/2020
    temp_dict = {}  # this temp dictionary will store the dictionaries, day1={}, day2={} ...
    temp_days = []  # this temp list will number of days from now for each unique date, 3, 4 ...

    # this is to find out the number of unique days in the csv, and create a tuple for each unique day
    # with open (r'C:\Users\User\Desktop\mockData.csv', newline='') as csv_file:
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
        temp_dict['day%s' % days_from_now] = {}  # the day_dictionaries are stored in temp_dict

    # create a key for each operating theatre, in each day_dictionary
    for i in range(len(current_dates)):
        (temp_dict['day' + str(temp_days[i])])['L1'] = []
        (temp_dict['day' + str(temp_days[i])])['L2'] = []
        (temp_dict['day' + str(temp_days[i])])['L3'] = []
        (temp_dict['day' + str(temp_days[i])])['L4'] = []
        (temp_dict['day' + str(temp_days[i])])['L5'] = []
        (temp_dict['day' + str(temp_days[i])])['L6'] = []
        (temp_dict['day' + str(temp_days[i])])['L7'] = []
        (temp_dict['day' + str(temp_days[i])])['L8'] = []
        (temp_dict['day' + str(temp_days[i])])['M1'] = []
        (temp_dict['day' + str(temp_days[i])])['M2'] = []
        (temp_dict['day' + str(temp_days[i])])['M3'] = []
        (temp_dict['day' + str(temp_days[i])])['M4'] = []
        (temp_dict['day' + str(temp_days[i])])['M5'] = []
        (temp_dict['day' + str(temp_days[i])])['OT 24'] = []
        (temp_dict['day' + str(temp_days[i])])['OT 25'] = []
        (temp_dict['day' + str(temp_days[i])])['OT 22'] = []
        (temp_dict['day' + str(temp_days[i])])['R1'] = []
        (temp_dict['day' + str(temp_days[i])])['R4'] = []
        (temp_dict['day' + str(temp_days[i])])['R5'] = []
        (temp_dict['day' + str(temp_days[i])])['R6'] = []
        (temp_dict['day' + str(temp_days[i])])['R7'] = []
        (temp_dict['day' + str(temp_days[i])])['R8'] = []
        (temp_dict['day' + str(temp_days[i])])['MRI'] = []

    # read each line in csv and append details to the respective 'OT' dictionaries
    with open (file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        # skip header
        next(mock_csv, None)
        for row in mock_csv:
            start_date = row[1].split(' ')
            end_date = row[2].split(' ')
            start_time = start_date[1]
            end_time = end_date[1]
            # codes to convert time into appropriate format 08:15 = 8.25, 10:45 = 10.75
            start_time_new = datetime.strptime(start_time, '%H:%M').time()
            end_time_new = datetime.strptime(end_time, '%H:%M').time()
            start_time_deci = (start_time_new.hour+start_time_new.minute/60.0)
            end_time_deci = (end_time_new.hour + end_time_new.minute / 60.0)
            duration = end_time_deci - start_time_deci  # calculate duration of surgery procedure
            date_index = current_dates.index(start_date[0])
            # print(temp_dict['day'+str(temp_days[date_index])]) # this will call the respective day_dictionary
            # this is to append list into the OT dictionaries
            (temp_dict['day' + str(temp_days[date_index])])[row[5]].append([start_time_deci, end_time_deci, duration, row[4], False, False])

    d1 = '2020-11-23'
    d1 = datetime.strptime(d1, '%Y-%m-%d').date()
    d2 = '2020-11-24'
    d2 = datetime.strptime(d2, '%Y-%m-%d').date()
    d3 = '2020-11-25'
    d3 = datetime.strptime(d3, '%Y-%m-%d').date()
    d4 = '2020-11-26'
    d4 = datetime.strptime(d4, '%Y-%m-%d').date()
    d5 = '2020-11-27'
    d5 = datetime.strptime(d5, '%Y-%m-%d').date()

    week_dict = {0:1, 7:2, 14:3, 21:4, 28:5}

    for i in temp_days:  # this will load all the necessary days into the current_schedule dictionary
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Monday':
            temp_date = (((date.today() + timedelta(days=i))-d1).days)%35
            current_schedules[i] = (temp_dict['day' + str(i)], (date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Tuesday':
            temp_date = (((date.today() + timedelta(days=i))-d2).days)%35
            current_schedules[i] = (temp_dict['day' + str(i)], (date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Wednesday':
            temp_date = (((date.today() + timedelta(days=i))-d3).days)%35
            current_schedules[i] = (temp_dict['day' + str(i)], (date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Thursday':
            temp_date = (((date.today() + timedelta(days=i))-d4).days)%35
            current_schedules[i] = (temp_dict['day' + str(i)], (date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))
        if (datetime.today() + timedelta(days=i)).strftime('%A') == 'Friday':
            temp_date = (((date.today() + timedelta(days=i))-d5).days)%35
            current_schedules[i] = (temp_dict['day' + str(i)], (date.today() + timedelta(days=i)).strftime('%A') + str(week_dict[temp_date]))

    ot_list = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'M1', 'M2', 'M3', 'M4', 'M5', 'OT 24',
               'OT 25', 'OT 22', 'R1', 'R4', 'R5', 'R6', 'R7', 'R8', 'MRI']

    # access all OT for each day
    for i in current_schedules:
        for j in ot_list:
            if len(current_schedules[i][0][j]) == 0:  # check if each OT_dictionary is empty
                current_schedules[i][0][j].append([8.0, 19.0, 11.0, 'empty', False, False])
            if len(current_schedules[i][0][j]) != 0 and current_schedules[i][0][j][0][
                0] != 8.0:  # add 'empty' from 8am to start of first procedure
                current_schedules[i][0][j].insert(0, [8.0, current_schedules[i][0][j][0][0], current_schedules[i][0][j][0][0] - 8.0, 'empty', False, False])
            if len(current_schedules[i][0][j]) != 0 and current_schedules[i][0][j][-1][
                1] != 19.0:  # add 'empty' from end of last procedure to 7pm
                current_schedules[i][0][j].append(
                    [current_schedules[i][0][j][-1][1], 19.0, 19.0 - current_schedules[i][0][j][-1][1], 'empty', False, False])

    # add 'empty' for empty timeslots in between each procedure allocated
    for i in current_schedules:
        for j in ot_list:
            if current_schedules[i][0][j] != 1:
                for k in range(len(current_schedules[i][0][j])):
                    # this will check if the end time of the preceding procedure = start time of next procedure
                    # this will also make sure that it is not the last item in the list
                    if current_schedules[i][0][j][k] != current_schedules[i][0][j][-1] and current_schedules[i][0][j][k][1] != current_schedules[i][0][j][k + 1][0]:
                        current_schedules[i][0][j].insert(k + 1, [current_schedules[i][0][j][k][1], current_schedules[i][0][j][k + 1][0],
                                                           current_schedules[i][0][j][k + 1][0] - current_schedules[i][0][j][k][1],
                                                           'empty', False, False])

    return current_schedules


output = read_csv()
show_timetable(output)