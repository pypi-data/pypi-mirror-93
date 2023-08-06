from tkinter.tix import *
from datetime import *
import numpy as np


def show_timetable(current_schedule):

    root = Tk()

    # set title and size of the GUI window
    root.title('Timetable')
    root.geometry("1200x700+350+150")

    # set secondary frame position and size (center right)
    frame = Frame(root)
    frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    # get today's date and set as heading
    today = date.today()
    if today.weekday() == 5:
        today = date.today() - timedelta(days=1)
    if today.weekday() == 6:
        today = date.today() - timedelta(days=2)
    week_day = today.strftime("%A")

    # place main date label
    heading = Label(frame, text= week_day + " , " + str(today), bg='#E5E7E9', relief=RIDGE)
    heading.place(relx=0.38, relwidth=0.25, y=0)

    # set secondary frame position and size
    canvas = Canvas(root)
    canvas.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    # create a frame inside the canvas
    canvas_frame = Frame(canvas, width=955, height=1500)
    canvas_frame.pack(expand=True, fill=BOTH)

    global tip
    tip = Balloon(canvas_frame)

    canvas_window = canvas.create_window(0, 0, window=canvas_frame, anchor="nw")

    # create and set vertical scrollbar
    vbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    vbar.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=vbar.set)

    # time-table headings
    label1 = Label(canvas_frame, text='Time:', bg='#D0ECE7', relief=RIDGE)
    label2 = Label(canvas_frame, text='L1', bg='#D0ECE7', relief=RIDGE)
    label3 = Label(canvas_frame, text='L2', bg='#D0ECE7', relief=RIDGE)
    label4 = Label(canvas_frame, text='L3', bg='#D0ECE7', relief=RIDGE)
    label5 = Label(canvas_frame, text='L4', bg='#D0ECE7', relief=RIDGE)
    label6 = Label(canvas_frame, text='L5', bg='#D0ECE7', relief=RIDGE)
    label7 = Label(canvas_frame, text='L6', bg='#D0ECE7', relief=RIDGE)
    label8 = Label(canvas_frame, text='L7', bg='#D0ECE7', relief=RIDGE)
    label9 = Label(canvas_frame, text='L8', bg='#D0ECE7', relief=RIDGE)
    label10 = Label(canvas_frame, text='M1', bg='#D0ECE7', relief=RIDGE)
    label11 = Label(canvas_frame, text='M2', bg='#D0ECE7', relief=RIDGE)
    label12 = Label(canvas_frame, text='M3', bg='#D0ECE7', relief=RIDGE)
    label13 = Label(canvas_frame, text='M4', bg='#D0ECE7', relief=RIDGE)
    label14 = Label(canvas_frame, text='M5', bg='#D0ECE7', relief=RIDGE)
    label15 = Label(canvas_frame, text='OT 24', bg='#D0ECE7', relief=RIDGE)
    label16 = Label(canvas_frame, text='OT 25', bg='#D0ECE7', relief=RIDGE)
    label17 = Label(canvas_frame, text='OT 22', bg='#D0ECE7', relief=RIDGE)
    label18 = Label(canvas_frame, text='R1', bg='#D0ECE7', relief=RIDGE)
    label19 = Label(canvas_frame, text='R4', bg='#D0ECE7', relief=RIDGE)
    label20 = Label(canvas_frame, text='R5', bg='#D0ECE7', relief=RIDGE)
    label21 = Label(canvas_frame, text='R6', bg='#D0ECE7', relief=RIDGE)
    label22 = Label(canvas_frame, text='R7', bg='#D0ECE7', relief=RIDGE)
    label23 = Label(canvas_frame, text='R8', bg='#D0ECE7', relief=RIDGE)
    label24 = Label(canvas_frame, text='MRI', bg='#D0ECE7', relief=RIDGE)
    label1.place(relwidth=0.08)
    label2.place(relwidth=0.04, relx=0.08)
    label3.place(relwidth=0.04, relx=0.12)
    label4.place(relwidth=0.04, relx=0.16)
    label5.place(relwidth=0.04, relx=0.20)
    label6.place(relwidth=0.04, relx=0.24)
    label7.place(relwidth=0.04, relx=0.28)
    label8.place(relwidth=0.04, relx=0.32)
    label9.place(relwidth=0.04, relx=0.36)
    label10.place(relwidth=0.04, relx=0.40)
    label11.place(relwidth=0.04, relx=0.44)
    label12.place(relwidth=0.04, relx=0.48)
    label13.place(relwidth=0.04, relx=0.52)
    label14.place(relwidth=0.04, relx=0.56)
    label15.place(relwidth=0.04, relx=0.60)
    label16.place(relwidth=0.04, relx=0.64)
    label17.place(relwidth=0.04, relx=0.68)
    label18.place(relwidth=0.04, relx=0.72)
    label19.place(relwidth=0.04, relx=0.76)
    label20.place(relwidth=0.04, relx=0.80)
    label21.place(relwidth=0.04, relx=0.84)
    label22.place(relwidth=0.04, relx=0.88)
    label23.place(relwidth=0.04, relx=0.92)
    label24.place(relwidth=0.04, relx=0.96)

    # time column labels
    time1 = Label(canvas_frame, text='0800:0815', bg='#FDFEFE', relief=RIDGE)
    time2 = Label(canvas_frame, text='0815:0830', bg='#FDFEFE', relief=RIDGE)
    time3 = Label(canvas_frame, text='0830:0845', bg='#FDFEFE', relief=RIDGE)
    time4 = Label(canvas_frame, text='0845:0900', bg='#FDFEFE', relief=RIDGE)
    time5 = Label(canvas_frame, text='0900:0915', bg='#FDFEFE', relief=RIDGE)
    time6 = Label(canvas_frame, text='0915:0930', bg='#FDFEFE', relief=RIDGE)
    time7 = Label(canvas_frame, text='0930:0945', bg='#FDFEFE', relief=RIDGE)
    time8 = Label(canvas_frame, text='0945:1000', bg='#FDFEFE', relief=RIDGE)
    time9 = Label(canvas_frame, text='1000:1015', bg='#FDFEFE', relief=RIDGE)
    time10 = Label(canvas_frame, text='1015:1030', bg='#FDFEFE', relief=RIDGE)
    time11 = Label(canvas_frame, text='1030:1045', bg='#FDFEFE', relief=RIDGE)
    time12 = Label(canvas_frame, text='1045:1100', bg='#FDFEFE', relief=RIDGE)
    time13 = Label(canvas_frame, text='1100:1115', bg='#FDFEFE', relief=RIDGE)
    time14 = Label(canvas_frame, text='1115:1130', bg='#FDFEFE', relief=RIDGE)
    time15 = Label(canvas_frame, text='1130:1145', bg='#FDFEFE', relief=RIDGE)
    time16 = Label(canvas_frame, text='1145:1200', bg='#FDFEFE', relief=RIDGE)
    time17 = Label(canvas_frame, text='1200:1215', bg='#FDFEFE', relief=RIDGE)
    time18 = Label(canvas_frame, text='1215:1230', bg='#FDFEFE', relief=RIDGE)
    time19 = Label(canvas_frame, text='1230:1245', bg='#FDFEFE', relief=RIDGE)
    time20 = Label(canvas_frame, text='1245:1300', bg='#FDFEFE', relief=RIDGE)
    time21 = Label(canvas_frame, text='1300:1315', bg='#FDFEFE', relief=RIDGE)
    time22 = Label(canvas_frame, text='1315:1330', bg='#FDFEFE', relief=RIDGE)
    time23 = Label(canvas_frame, text='1330:1345', bg='#FDFEFE', relief=RIDGE)
    time24 = Label(canvas_frame, text='1345:1400', bg='#FDFEFE', relief=RIDGE)
    time25 = Label(canvas_frame, text='1400:1415', bg='#FDFEFE', relief=RIDGE)
    time26 = Label(canvas_frame, text='1415:1430', bg='#FDFEFE', relief=RIDGE)
    time27 = Label(canvas_frame, text='1430:1445', bg='#FDFEFE', relief=RIDGE)
    time28 = Label(canvas_frame, text='1445:1500', bg='#FDFEFE', relief=RIDGE)
    time29 = Label(canvas_frame, text='1500:1515', bg='#FDFEFE', relief=RIDGE)
    time30 = Label(canvas_frame, text='1515:1530', bg='#FDFEFE', relief=RIDGE)
    time31 = Label(canvas_frame, text='1530:1545', bg='#FDFEFE', relief=RIDGE)
    time32 = Label(canvas_frame, text='1545:1600', bg='#FDFEFE', relief=RIDGE)
    time33 = Label(canvas_frame, text='1600:1615', bg='#FDFEFE', relief=RIDGE)
    time34 = Label(canvas_frame, text='1615:1630', bg='#FDFEFE', relief=RIDGE)
    time35 = Label(canvas_frame, text='1630:1645', bg='#FDFEFE', relief=RIDGE)
    time36 = Label(canvas_frame, text='1645:1700', bg='#FDFEFE', relief=RIDGE)
    time37 = Label(canvas_frame, text='1700:1715', bg='#FDFEFE', relief=RIDGE)
    time38 = Label(canvas_frame, text='1715:1730', bg='#FDFEFE', relief=RIDGE)
    time39 = Label(canvas_frame, text='1730:1745', bg='#FDFEFE', relief=RIDGE)
    time40 = Label(canvas_frame, text='1745:1800', bg='#FDFEFE', relief=RIDGE)
    time41 = Label(canvas_frame, text='1800:1815', bg='#FDFEFE', relief=RIDGE)
    time42 = Label(canvas_frame, text='1815:1830', bg='#FDFEFE', relief=RIDGE)
    time43 = Label(canvas_frame, text='1830:1845', bg='#FDFEFE', relief=RIDGE)
    time44 = Label(canvas_frame, text='1845:1900', bg='#FDFEFE', relief=RIDGE)

    # placing all title for the time column
    for i in range(1, 45):
        vars()['time' + str(i)].place(relwidth=0.08, y=20 + (i - 1) * 20, )
        i = i + 1

    # create time-table using labels (44rows*23columns)
    rows = 44
    cols = 24
    blk = [[0 for i in range(cols)] for j in range(rows)]
    for i in range(rows):  # Rows
        for j in range(cols):  # Columns
            blk[i][j] = Label(canvas_frame, text="", bg='#FDFEFE', relief=RIDGE)
            blk[i][j].place(relwidth=0.04, relx=0.08 + j * 0.04, y=20 + i * 20)

    color_code = {'OTO':'#D35400', 'H&N':'#D7BDE2', 'CLR':'#27AE60', 'HPB':'#F4ECF7', 'SUR-ONCO':'#E91E63',
                  'BREAST':'#00FF33', 'ENT':'#FFF59D', 'NES':'#FFF59D', 'VAS':'#E0F7FA', 'O&G':'#757575',
                  'HND':'#E0E0E0', 'UGI':'#006600', 'PLS':'#F5F5F5', 'CTS':'#A569BD', 'URO':'#5DADE2',
                  'OMS':'#A9CCE3', 'Actual':'#3F51B5', 'Predicted':'#34495E'}

    ot_dict = {'L1': 0, 'L2': 1, 'L3': 2, 'L4': 3, 'L5': 4, 'L6': 5, 'L7': 6, 'L8': 7, 'M1': 8, 'M2':9, 'M3': 10, 'M4': 11, 'M5': 12, 'OT 24': 13,
               'OT 25': 14, 'OT 22': 15, 'R1': 16, 'R4': 17, 'R5': 18, 'R6': 19, 'R7': 20, 'R8': 21, 'MRI': 22}

    # this section is for the creation of the scheduled surgery table
    ot_list = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'M1', 'M2', 'M3', 'M4', 'M5', 'OT 24',
               'OT 25', 'OT 22', 'R1', 'R4', 'R5', 'R6', 'R7', 'R8', 'MRI']

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

    proc_codes_breast = {10: 'mastectomy',
                         11: 'lumpectomy',
                         12: 'mastopexy',
                         13: 'biopsy',
                         14: 'mammoplasty',
                         15: 'abscess'
                         }

    proc_codes_nes = {10: 'Circumcision',
                      11: 'Pyeloplasty',
                      12: 'Nephrectomy',
                      13: 'Cystoscopy',
                      14: 'Meatoplasty',
                      15: 'Scrotoplasty'
                      }

    proc_codes_oto = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proc_codes_clr = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proc_codes_hpb = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proc_codes_pls = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proc_codes_ent = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proc_codes_suronco = {10: 'hip',
                          11: 'tail',
                          12: 'ankle',
                          13: 'knee',
                          14: 'leg',
                          15: 'elbow'
                          }

    proc_codes_ugi = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proc_codes_hnn = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proc_codes_og = {10: 'hip',
                     11: 'tail',
                     12: 'ankle',
                     13: 'knee',
                     14: 'leg',
                     15: 'elbow'
                     }

    proc_codes_hnd = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proc_codes_oms = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proc_codes_vas = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proc_codes_cts = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proc_codes_uro = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    proced_name_dict = {10: proc_codes_breast,
                        11: proc_codes_oto,
                        12: proc_codes_nes,
                        13: proc_codes_clr,
                        14: proc_codes_hpb,
                        15: proc_codes_pls,
                        16: proc_codes_ent,
                        17: proc_codes_suronco,
                        18: proc_codes_ugi,
                        19: proc_codes_hnn,
                        20: proc_codes_og,
                        21: proc_codes_hnd,
                        22: proc_codes_oms,
                        23: proc_codes_vas,
                        24: proc_codes_cts,
                        25: proc_codes_uro}

    # list to collect data of actual surgeries in the 'soln' array
    # data to retrieve from array : discipline(3-4 digits) (done), procedure(5-6 digits) (done),
    # data to retrieve from array: duplicate no.(7th or last dig) (done),
    # data to retrieve from array : dates, time start and end (done), duration (done)
    actual_surgery_proced = []
    actual_surgery_durations = []
    actual_surgery_time = []
    actual_surgery_dates = []
    actual_surgery_ot = []
    final_list = []

    soln_list = current_schedule[0]
    sched_dates = current_schedule[2]
    # sieve through each time slot in the solution list and find all actual surgeries and their allocated timeslots
    for day in range(len(soln_list)):
        for ot in range(len(soln_list[day])):
            dur_count = 0
            for time_slot in range(len(soln_list[day][ot])):
                if soln_list[day][ot][time_slot] != 0 and str(soln_list[day][ot][time_slot])[4:6] != '00' and \
                        str(soln_list[day][ot][time_slot])[1] == '1':
                    dur_count = dur_count + 1
                    # this if statement decides when to end time_slot counts (2 different criterias)
                    if (time_slot == 43 and dur_count != 0) or (str(soln_list[day][ot][time_slot]) != str(
                            soln_list[day][ot][time_slot + 1]) and dur_count != 0):
                        disc_num = int(str(soln_list[day][ot][time_slot])[2:4])
                        proced_num = int(str(soln_list[day][ot][time_slot])[4:6])
                        duplicate_num = int(str(soln_list[day][ot][time_slot])[-1])
                        duration_num = dur_count / 4.0
                        time_end_deci = 8 + (time_slot + 1) / 4
                        time_start_deci = time_end_deci - duration_num
                        time_end = str(timedelta(hours=time_end_deci)).rsplit(':', 1)[0]
                        time_start = str(timedelta(hours=time_start_deci)).rsplit(':', 1)[0]
                        actual_surgery_ot.append(ot_list[ot])
                        actual_surgery_dates.append(sched_dates[day])
                        actual_surgery_time.append(str(time_start) + ' - ' + str(time_end))
                        actual_surgery_durations.append(str(duration_num) + ' hrs')
                        actual_surgery_proced.append(proced_name_dict[disc_num][proced_num] + '_' + str(duplicate_num))
                        dur_count = 0
                else:
                    # if next timeslot is = 0, signify end of actual surgery at previous slot
                    if dur_count != 0:
                        disc_num = int(str(soln_list[day][ot][time_slot - 1])[2:4])
                        proced_num = int(str(soln_list[day][ot][time_slot - 1])[4:6])
                        duplicate_num = int(str(soln_list[day][ot][time_slot - 1])[-1])
                        duration_num = dur_count / 4.0
                        time_end_deci = 8 + (time_slot) / 4
                        time_start_deci = time_end_deci - duration_num
                        time_end = str(timedelta(hours=time_end_deci)).rsplit(':', 1)[0]
                        time_start = str(timedelta(hours=time_start_deci)).rsplit(':', 1)[0]
                        actual_surgery_ot.append(ot_list[ot])
                        actual_surgery_dates.append(sched_dates[day])
                        actual_surgery_time.append(str(time_start) + ' - ' + str(time_end))
                        actual_surgery_durations.append(str(duration_num) + ' hrs')
                        actual_surgery_proced.append(proced_name_dict[disc_num][proced_num] + '_' + str(duplicate_num))
                        dur_count = 0

    actual_surgery_proced = ['Procedure :'] + actual_surgery_proced
    actual_surgery_dates = ['Date :'] + actual_surgery_dates
    actual_surgery_ot = ['Operating Theatre :'] + actual_surgery_ot
    actual_surgery_time = ['Time :'] + actual_surgery_time
    actual_surgery_durations = ['Duration :'] + actual_surgery_durations

    final_list.append(actual_surgery_proced)
    final_list.append(actual_surgery_dates)
    final_list.append(actual_surgery_ot)
    final_list.append(actual_surgery_time)
    final_list.append(actual_surgery_durations)

    rows_list = []

    # row position starts at 900
    for i in range(len(actual_surgery_time)):
        cols_list = []
        for j in range(5):
            # e = Label(canvas_frame, relief=GROOVE, width=20)
            # e.grid(row=i, column=j, sticky=NSEW)
            e = Label(canvas_frame, relief=GROOVE, bg='white')
            e.place(relwidth=0.2, relx=j * 0.2, y=900 + i * 20)
            e.config(text='%s' % final_list[j][i])
            cols_list.append(e)
        rows_list.append(cols)

    # find first date found in current schedule and set it as date appearing in timetable
    first_day_from_now = current_schedule[1][0]
    today = date.today()
    first_day = (today + timedelta(days=first_day_from_now)).strftime("%A")
    first_date = (today + timedelta(days=first_day_from_now))
    heading.config(text=first_day + " , " + str(first_date))

    # show timetable for first date in schedule
    col_index = 0
    for slots in current_schedule[0][0]:  # this each OT array for the first date
        nonzero_item_index = np.where(slots != 0)  # find indexes in each OT array where element is non-zero
        for j in range(len(nonzero_item_index[0])):  # access each individual index that is non-zero
            discipline_digit = int(str(slots[nonzero_item_index[0][j]])[2:4])
            procedure_digit = int(str(slots[nonzero_item_index[0][j]])[4:6])
            last_digit = int(str(slots[nonzero_item_index[0][j]])[-1])
            if str(slots[nonzero_item_index[0][j]])[4:6] == '00':
                blk[nonzero_item_index[0][j]][col_index].config(bg=color_code[discipline_codes[discipline_digit]], text=discipline_codes[discipline_digit])  # 1st index=row, 2nd index=col
            if str(slots[nonzero_item_index[0][j]])[4:6] != '00' and str(slots[nonzero_item_index[0][j]])[1] == '1':
                blk[nonzero_item_index[0][j]][col_index].config(bg=color_code['Actual'], text=proc_codes_oto[procedure_digit]+str(last_digit))
            if str(slots[nonzero_item_index[0][j]])[4:6] != '00' and str(slots[nonzero_item_index[0][j]])[1] == '2':
                blk[nonzero_item_index[0][j]][col_index].config(bg=color_code['Predicted'], text=proc_codes_oto[procedure_digit]+str(last_digit))
        col_index = col_index+1

    # this section of code is for tool-tipping the scheduled procedures
    # if date correspond to date of scheduled surgery, make tool-tip appear
    for i in range(1, len(final_list[1])):
        heading_text = heading.cget('text')
        heading_parts = heading_text.split(' , ')
        heading_date = str(datetime.strptime(heading_parts[1], '%Y-%m-%d').date())
        list_date = str(datetime.strptime(final_list[1][i], '%d/%m/%Y').date())
        if list_date == heading_date:
            starting_time = final_list[3][i].split(' - ')[0]
            start_hour, start_min = starting_time.split(':')
            starting_slot = int((int(start_hour) + int(start_min) / 60) / 0.25 - 32)
            slot_numbers = int(float(final_list[4][i].split(' ')[0]) / 0.25)
            ot_index = ot_list.index(final_list[2][i])
            for j in range(slot_numbers):
                text = final_list[0][0] + ' ' + final_list[0][i] + '\n' + \
                       final_list[1][0] + ' ' + final_list[1][i] + '\n' + \
                       final_list[2][0] + ' ' + final_list[2][i] + '\n' + \
                       final_list[3][0] + ' ' + final_list[3][i]
                tip.bind_widget(blk[starting_slot + j][ot_index], balloonmsg=text)

    # defining the prev and next function
    def prev_date():
        global tip
        for i in range(rows):  # Rows
            for j in range(cols):  # Columns
                blk[i][j].config(bg='white', text='')
                tip.unbind_widget(blk[i][j])
        str_date = heading.cget('text')
        parts = str_date.split(' , ')
        date_now = datetime.strptime(parts[1], '%Y-%m-%d').date()
        date_prev = date_now - timedelta(days=1)
        if date_prev.weekday() == 6:
            date_prev = date_prev - timedelta(days=2)
        else:
            pass
        day_prev = date_prev.strftime("%A")
        heading.config(text=str(day_prev) + " , " + str(date_prev))

        days_xx = (date_prev - date.today()).days
        # grey out current scheduled appointments
        if days_xx in current_schedule[1]:
            day_index = current_schedule[1].index(days_xx)
            col_index = 0
            for slots in current_schedule[0][day_index]:  # this each OT array for the first date
                nonzero_item_index = np.where(slots != 0)  # find indexes in each OT array where element is non-zero
                for j in range(len(nonzero_item_index[0])):  # access each individual index that is non-zero
                    discipline_digit = int(str(slots[nonzero_item_index[0][j]])[2:4])
                    procedure_digit = int(str(slots[nonzero_item_index[0][j]])[4:6])
                    last_digit = int(str(slots[nonzero_item_index[0][j]])[-1])
                    if str(slots[nonzero_item_index[0][j]])[4:6] == '00':
                        blk[nonzero_item_index[0][j]][col_index].config(bg=color_code[discipline_codes[discipline_digit]], text=discipline_codes[discipline_digit])  # 1st index=row, 2nd index=col
                    if str(slots[nonzero_item_index[0][j]])[4:6] != '00' and str(slots[nonzero_item_index[0][j]])[1] == '1':
                        blk[nonzero_item_index[0][j]][col_index].config(bg=color_code['Actual'], text=proc_codes_oto[procedure_digit] + str(last_digit))
                    if str(slots[nonzero_item_index[0][j]])[4:6] != '00' and str(slots[nonzero_item_index[0][j]])[1] == '2':
                        blk[nonzero_item_index[0][j]][col_index].config(bg=color_code['Predicted'], text=proc_codes_oto[procedure_digit] + str(last_digit))
                col_index = col_index + 1
            # if date correspond to date of scheduled surgery, make tool-tip appear
            for i in range(1, len(final_list[1])):
                heading_text = heading.cget('text')
                heading_parts = heading_text.split(' , ')
                heading_date = str(datetime.strptime(heading_parts[1], '%Y-%m-%d').date())
                list_date = str(datetime.strptime(final_list[1][i], '%d/%m/%Y').date())
                if list_date == heading_date:
                    starting_time = final_list[3][i].split(' - ')[0]
                    start_hour, start_min = starting_time.split(':')
                    starting_slot = int((int(start_hour) + int(start_min) / 60) / 0.25 - 32)
                    slot_numbers = int(float(final_list[4][i].split(' ')[0]) / 0.25)
                    ot_index = ot_list.index(final_list[2][i])
                    for j in range(slot_numbers):
                        text = final_list[0][0] + ' ' + final_list[0][i] + '\n' + \
                               final_list[1][0] + ' ' + final_list[1][i] + '\n' + \
                               final_list[2][0] + ' ' + final_list[2][i] + '\n' + \
                               final_list[3][0] + ' ' + final_list[3][i]
                        # tip = Balloon(canvas_frame)
                        tip.bind_widget(blk[starting_slot + j][ot_index], balloonmsg=text)
        else:
            for i in range(rows):  # Rows
                for j in range(cols):  # Columns
                    blk[i][j].config(bg='white', text='')

    def next_date():
        global tip
        for i in range(rows):  # Rows
            for j in range(cols):  # Columns
                blk[i][j].config(bg='white', text='')
                tip.unbind_widget(blk[i][j])
        str_date = heading.cget('text')
        parts = str_date.split(' , ')
        date_now = datetime.strptime(parts[1], '%Y-%m-%d').date()
        date_next = date_now + timedelta(days=1)
        if date_next.weekday() == 5:
            date_next = date_next + timedelta(days=2)
        else:
            pass
        day_next = date_next.strftime("%A")
        heading.config(text=str(day_next) + " , " + str(date_next))
        # x = label indicated at top of GUI
        days_xx = (date_next - date.today()).days
        # grey out current scheduled appointments
        if days_xx in current_schedule[1]:
            day_index = current_schedule[1].index(days_xx)
            col_index = 0
            for slots in current_schedule[0][day_index]:  # this each OT array for the first date
                nonzero_item_index = np.where(slots != 0)  # find indexes in each OT array where element is non-zero
                for j in range(len(nonzero_item_index[0])):  # access each individual index that is non-zero
                    discipline_digit = int(str(slots[nonzero_item_index[0][j]])[2:4])
                    procedure_digit = int(str(slots[nonzero_item_index[0][j]])[4:6])
                    last_digit = int(str(slots[nonzero_item_index[0][j]])[-1])
                    if str(slots[nonzero_item_index[0][j]])[4:6] == '00':
                        blk[nonzero_item_index[0][j]][col_index].config(bg=color_code[discipline_codes[discipline_digit]], text=discipline_codes[discipline_digit])  # 1st index=row, 2nd index=col
                    if str(slots[nonzero_item_index[0][j]])[4:6] != '00' and str(slots[nonzero_item_index[0][j]])[1] == '1':
                        blk[nonzero_item_index[0][j]][col_index].config(bg=color_code['Actual'], text=proc_codes_oto[procedure_digit] + str(last_digit))
                    if str(slots[nonzero_item_index[0][j]])[4:6] != '00' and str(slots[nonzero_item_index[0][j]])[1] == '2':
                        blk[nonzero_item_index[0][j]][col_index].config(bg=color_code['Predicted'], text=proc_codes_oto[procedure_digit] + str(last_digit))
                col_index = col_index + 1
                # if date correspond to date of scheduled surgery, make tool-tip appear
            for i in range(1, len(final_list[1])):
                heading_text = heading.cget('text')
                heading_parts = heading_text.split(' , ')
                heading_date = str(datetime.strptime(heading_parts[1], '%Y-%m-%d').date())
                list_date = str(datetime.strptime(final_list[1][i], '%d/%m/%Y').date())
                if list_date == heading_date:
                    starting_time = final_list[3][i].split(' - ')[0]
                    start_hour, start_min = starting_time.split(':')
                    starting_slot = int((int(start_hour) + int(start_min) / 60) / 0.25 - 32)
                    slot_numbers = int(float(final_list[4][i].split(' ')[0]) / 0.25)
                    ot_index = ot_list.index(final_list[2][i])
                    for j in range(slot_numbers):
                        text = final_list[0][0] + ' ' + final_list[0][i] + '\n' + \
                               final_list[1][0] + ' ' + final_list[1][i] + '\n' + \
                               final_list[2][0] + ' ' + final_list[2][i] + '\n' + \
                               final_list[3][0] + ' ' + final_list[3][i]
                        # tip = Balloon(canvas_frame)
                        tip.bind_widget(blk[starting_slot + j][ot_index], balloonmsg=text)
        else:
            for i in range(rows):  # Rows
                for j in range(cols):  # Columns
                    blk[i][j].config(bg='white', text='')

    prev_button = Button(frame, text='prev', width=10, bg='#E5E7E9',command=prev_date)
    next_button = Button(frame, text='next', width=10, bg='#E5E7E9',command=next_date)
    prev_button.place(relx=0.40, rely=0.95)
    next_button.place(relx=0.58, rely=0.95)

    def FrameWidth(event):
        canvas_width = event.width
        canvas.itemconfig(canvas_window, width=canvas_width)

    def OnFrameConfigure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas_frame.bind("<Configure>", OnFrameConfigure)
    canvas.bind('<Configure>', FrameWidth)

    root.mainloop()


# current_schedules = read_csv()
# show_timetable(current_schedules)