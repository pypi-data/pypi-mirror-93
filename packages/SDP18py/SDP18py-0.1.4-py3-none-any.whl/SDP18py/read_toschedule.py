import os
import csv
from tkinter import *
from tkinter import filedialog
from datetime import *

def read_toschedule():

    # this is a window prompt for selecting csv file to be read
    dialog_root = Tk()
    dialog_root.geometry("1200x700+350+150")
    dialog_root.withdraw()

    # this will obtain file path of the selected csv file
    file_path = filedialog.askopenfilename(title='Please select the to be scheduled .csv file')
    file_path = os.path.normpath(file_path)

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

    proc_codes_oto = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    key_list = list(discipline_codes.keys())
    value_list = list(discipline_codes.values())
    proc_key_list = list(proc_codes_oto.keys())
    proc_value_list = list(proc_codes_oto.values())

    procedure_list = []
    to_schedule = []

    # find number of surgeries in the to_schedule csv file
    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        next(mock_csv, None)  # skip header
        for row in mock_csv: # add each array
            duration = int(float(row[1]) / 0.25)
            duplicate_count = procedure_list.count(row[2])
            procedure_list.append(row[2])
            position = value_list.index(row[0])
            proc_position = proc_value_list.index(row[2])
            if int(row[3]) == 1:
                temp_list = [1100000 + (key_list[position])*1000 + (proc_key_list[proc_position])*10 + duplicate_count] * duration
                to_schedule.append(temp_list)
            elif int(row[3]) == 0:
                temp_list = [1200000 + (key_list[position])*1000 + (proc_key_list[proc_position])*10 + duplicate_count] * duration
                to_schedule.append(temp_list)

    return to_schedule


def read_toschedule1(file_path):

    # this is a window prompt for selecting csv file to be read
    dialog_root = Tk()
    dialog_root.geometry("1200x700+350+150")
    dialog_root.withdraw()

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

    proc_codes_oto = {10: 'hip',
                      11: 'tail',
                      12: 'ankle',
                      13: 'knee',
                      14: 'leg',
                      15: 'elbow'
                      }

    key_list = list(discipline_codes.keys())
    value_list = list(discipline_codes.values())
    proc_key_list = list(proc_codes_oto.keys())
    proc_value_list = list(proc_codes_oto.values())

    procedure_list = []
    to_schedule = []

    # find number of surgeries in the to_schedule csv file
    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        next(mock_csv, None)  # skip header
        for row in mock_csv:  # add each array
            duration = int(float(row[1]) / 0.25)
            duplicate_count = procedure_list.count(row[2])
            procedure_list.append(row[2])
            position = value_list.index(row[0])
            proc_position = proc_value_list.index(row[2])
            if int(row[3]) == 1:
                temp_list = [1100000 + (key_list[position]) * 1000 + (
                proc_key_list[proc_position]) * 10 + duplicate_count] * duration
                to_schedule.append(temp_list)
            elif int(row[3]) == 0:
                temp_list = [1200000 + (key_list[position]) * 1000 + (
                proc_key_list[proc_position]) * 10 + duplicate_count] * duration
                to_schedule.append(temp_list)

    return to_schedule