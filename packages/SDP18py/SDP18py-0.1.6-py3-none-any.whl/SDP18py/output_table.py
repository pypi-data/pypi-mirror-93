import datetime
from tkinter import *


def create_table(soln_list, sched_dates):

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

    proced_name_dict = { 10: proc_codes_breast,
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
                            25: proc_codes_uro }

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

    # sieve through each time slot in the solution list and find all actual surgeries and their allocated timeslots
    for day in range(len(soln_list)):
        for ot in range(len(soln_list[day])):
            dur_count = 0
            for time_slot in range(len(soln_list[day][ot])):
                if soln_list[day][ot][time_slot] != 0 and str(soln_list[day][ot][time_slot])[4:6] != '00' and str(soln_list[day][ot][time_slot])[1] == '1':
                    dur_count = dur_count + 1
                    # this if statement decides when to end time_slot counts (2 different criterias)
                    if (time_slot == 43 and dur_count != 0) or (str(soln_list[day][ot][time_slot]) != str(soln_list[day][ot][time_slot+1]) and dur_count != 0):
                        disc_num = int(str(soln_list[day][ot][time_slot])[2:4])
                        proced_num = int(str(soln_list[day][ot][time_slot])[4:6])
                        duplicate_num = int(str(soln_list[day][ot][time_slot])[-1])
                        duration_num = dur_count/4.0
                        time_end_deci = 8 + (time_slot+1)/4
                        time_start_deci = time_end_deci - duration_num
                        time_end = str(datetime.timedelta(hours=time_end_deci)).rsplit(':', 1)[0]
                        time_start = str(datetime.timedelta(hours=time_start_deci)).rsplit(':', 1)[0]
                        actual_surgery_ot.append(ot_list[ot])
                        actual_surgery_dates.append(sched_dates[day])
                        actual_surgery_time.append(str(time_start) + ' - ' + str(time_end))
                        actual_surgery_durations.append(str(duration_num)+' hrs')
                        actual_surgery_proced.append(proced_name_dict[disc_num][proced_num] + '_' + str(duplicate_num))
                        dur_count = 0
                else:
                    # if next timeslot is = 0, signify end of actual surgery at previous slot
                    if dur_count != 0:
                        disc_num = int(str(soln_list[day][ot][time_slot-1])[2:4])
                        proced_num = int(str(soln_list[day][ot][time_slot-1])[4:6])
                        duplicate_num = int(str(soln_list[day][ot][time_slot-1])[-1])
                        duration_num = dur_count / 4.0
                        time_end_deci = 8 + (time_slot)/4
                        time_start_deci = time_end_deci - duration_num
                        time_end = str(datetime.timedelta(hours=time_end_deci)).rsplit(':', 1)[0]
                        time_start = str(datetime.timedelta(hours=time_start_deci)).rsplit(':', 1)[0]
                        actual_surgery_ot.append(ot_list[ot])
                        actual_surgery_dates.append(sched_dates[day])
                        actual_surgery_time.append(str(time_start) + ' - ' + str(time_end))
                        actual_surgery_durations.append(str(duration_num)+' hrs')
                        actual_surgery_proced.append(proced_name_dict[disc_num][proced_num] + '_' + str(duplicate_num))
                        dur_count = 0

    actual_surgery_proced = ['Procedures :'] + actual_surgery_proced
    actual_surgery_dates = ['Dates :'] + actual_surgery_dates
    actual_surgery_ot = ['OT :'] + actual_surgery_ot
    actual_surgery_time = ['Time :'] + actual_surgery_time
    actual_surgery_durations = ['Duration :'] + actual_surgery_durations

    final_list.append(actual_surgery_proced)
    final_list.append(actual_surgery_dates)
    final_list.append(actual_surgery_ot)
    final_list.append(actual_surgery_time)
    final_list.append(actual_surgery_durations)

    rows = []
    table_screen = Tk()
    table_screen.title('List of surgery and allocated slots')
    table_screen.geometry("+750+350")

    for i in range(len(actual_surgery_time)):
        cols = []
        for j in range(5):
            e = Label(table_screen, relief=GROOVE, width=20)
            e.grid(row=i, column=j, sticky=NSEW)
            e.config(text='%s' % final_list[j][i])
            cols.append(e)
        rows.append(cols)

    table_screen.mainloop()







