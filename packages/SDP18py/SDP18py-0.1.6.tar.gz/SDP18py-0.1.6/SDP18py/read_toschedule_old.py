import os
from tkinter import *
from tkinter import filedialog
import csv


def read_toschedule():

    to_schedules = []
    actual_request_dict = { 0: False, 1: True}

    # this is a window prompt for selecting csv file to be read
    dialog_root = Tk()
    dialog_root.geometry("1200x700+350+150")
    dialog_root.withdraw()

    # this will obtain file path of the selected csv file
    file_path = filedialog.askopenfilename(title='Please select the to be scheduled .csv file')
    file_path = os.path.normpath(file_path)

    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        next(mock_csv, None)  # skip header
        for row in mock_csv: # add each tuple into the list
            to_schedules.append((float(row[1]), row[2], actual_request_dict[int(row[3])]))

    return to_schedules