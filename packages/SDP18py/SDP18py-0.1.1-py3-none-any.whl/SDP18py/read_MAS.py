import os
from tkinter import *
from tkinter import filedialog
import csv
from datetime import *


def read_mas():

    mas_allowed = {'BREAST': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                              'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                              'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                              'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                              'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'HND': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'SUR-ONCO': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                                'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                                'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                                'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                                'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'HPB': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'OTO': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'H&N': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'CLR': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'ENT': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'NES': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'VAS': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'O&G': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'UGI': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'PLS': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'CTS': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'URO': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'OMS': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []}}

    # this is a window prompt for selecting csv file to be read
    dialog_root = Tk()
    dialog_root.geometry("1200x700+350+150")
    dialog_root.withdraw()

    # this will obtain file path of the selected csv file
    file_path = filedialog.askopenfilename(title='Please select the MAS schedule .csv file')
    file_path = os.path.normpath(file_path)

    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        next(mock_csv, None)  # skip header
        for row in mock_csv:  # get unique dates in the csv file
            if '/' not in row[4]:  # if discipline column does not contain '/'
                if row[4] in mas_allowed and row[1] == str(0):
                    mas_allowed[row[4]]['Monday'+str(row[3])].append(row[0])
                if row[4] in mas_allowed and row[1] == str(1):
                    mas_allowed[row[4]]['Tuesday'+str(row[3])].append(row[0])
                if row[4] in mas_allowed and row[1] == str(2):
                    mas_allowed[row[4]]['Wednesday'+str(row[3])].append(row[0])
                if row[4] in mas_allowed and row[1] == str(3):
                    mas_allowed[row[4]]['Thursday'+str(row[3])].append(row[0])
                if row[4] in mas_allowed and row[1] == str(4):
                    mas_allowed[row[4]]['Friday'+str(row[3])].append(row[0])
            if '/' in row[4]:  # if discipline column contains '/'
                disciplines_names = row[4].split('/')
                for discs in disciplines_names:
                    if discs in mas_allowed and row[1] == str(0):
                        mas_allowed[discs]['Monday' + str(row[3])].append(row[0])
                    if discs in mas_allowed and row[1] == str(1):
                        mas_allowed[discs]['Tuesday' + str(row[3])].append(row[0])
                    if discs in mas_allowed and row[1] == str(2):
                        mas_allowed[discs]['Wednesday' + str(row[3])].append(row[0])
                    if discs in mas_allowed and row[1] == str(3):
                        mas_allowed[discs]['Thursday' + str(row[3])].append(row[0])
                    if discs in mas_allowed and row[1] == str(4):
                        mas_allowed[discs]['Friday' + str(row[3])].append(row[0])

    return mas_allowed


def read_mas1(file_path):
    mas_allowed = {'BREAST': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                              'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                              'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                              'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                              'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'HND': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'SUR-ONCO': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                                'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                                'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                                'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                                'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'HPB': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'OTO': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'H&N': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'CLR': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'ENT': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'NES': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'VAS': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'O&G': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'UGI': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'PLS': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'CTS': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'URO': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []},
                   'OMS': {'Monday1': [], 'Tuesday1': [], 'Wednesday1': [], 'Thursday1': [], 'Friday1': [],
                           'Monday2': [], 'Tuesday2': [], 'Wednesday2': [], 'Thursday2': [], 'Friday2': [],
                           'Monday3': [], 'Tuesday3': [], 'Wednesday3': [], 'Thursday3': [], 'Friday3': [],
                           'Monday4': [], 'Tuesday4': [], 'Wednesday4': [], 'Thursday4': [], 'Friday4': [],
                           'Monday5': [], 'Tuesday5': [], 'Wednesday5': [], 'Thursday5': [], 'Friday5': []}}

    # this is a window prompt for selecting csv file to be read
    dialog_root = Tk()
    dialog_root.geometry("1200x700+350+150")
    dialog_root.withdraw()

    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        next(mock_csv, None)  # skip header
        for row in mock_csv:  # get unique dates in the csv file
            if '/' not in row[4]:  # if discipline column does not contain '/'
                if row[4] in mas_allowed and row[1] == str(0):
                    mas_allowed[row[4]]['Monday' + str(row[3])].append(row[0])
                if row[4] in mas_allowed and row[1] == str(1):
                    mas_allowed[row[4]]['Tuesday' + str(row[3])].append(row[0])
                if row[4] in mas_allowed and row[1] == str(2):
                    mas_allowed[row[4]]['Wednesday' + str(row[3])].append(row[0])
                if row[4] in mas_allowed and row[1] == str(3):
                    mas_allowed[row[4]]['Thursday' + str(row[3])].append(row[0])
                if row[4] in mas_allowed and row[1] == str(4):
                    mas_allowed[row[4]]['Friday' + str(row[3])].append(row[0])
            if '/' in row[4]:  # if discipline column contains '/'
                disciplines_names = row[4].split('/')
                for discs in disciplines_names:
                    if discs in mas_allowed and row[1] == str(0):
                        mas_allowed[discs]['Monday' + str(row[3])].append(row[0])
                    if discs in mas_allowed and row[1] == str(1):
                        mas_allowed[discs]['Tuesday' + str(row[3])].append(row[0])
                    if discs in mas_allowed and row[1] == str(2):
                        mas_allowed[discs]['Wednesday' + str(row[3])].append(row[0])
                    if discs in mas_allowed and row[1] == str(3):
                        mas_allowed[discs]['Thursday' + str(row[3])].append(row[0])
                    if discs in mas_allowed and row[1] == str(4):
                        mas_allowed[discs]['Friday' + str(row[3])].append(row[0])

    return mas_allowed