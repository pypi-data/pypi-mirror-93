from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
from SDP18py.test_hco import run_hco
from SDP18py.test_ts import run_ts
from SDP18py.test_sa import run_sa
from SDP18py.test_ga import run_ga
from SDP18py.read_MAS import read_mas1
from SDP18py.read_csv import read_csv1
from SDP18py.read_toschedule import read_toschedule1
import sqlite3
from tkinter.tix import *


def register_page():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title('Register')
    screen1.geometry("400x250+750+350")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(screen1, text='Please enter details below').pack()
    Label(screen1, text='').pack()
    Label(screen1, text='Username *').pack()
    username_entry = Entry(screen1, textvariable=username, justify='center')
    username_entry.pack()
    Label(screen1, text='Password *').pack()
    password_entry = Entry(screen1, textvariable=password, justify='center')
    password_entry.pack()
    msg_label = Label(screen1, text='')
    msg_label.pack()

    def register_user():
        with sqlite3.connect('user_info.db') as db:
            cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user(username TEXT NOT NULL, password TEXT NOT NULL);")
        insert = 'INSERT INTO user(username,password) VALUES(?,?)'
        cursor.execute("SELECT count(*) FROM user")
        table_empty_check = cursor.fetchall()
        if table_empty_check[0][0] == 0: # if table is empty
            if username_entry.get() != "" and password_entry.get() != "" and username_entry.get():
                cursor.execute(insert, [(username_entry.get()), (password_entry.get())])
                db.commit()
                msg_label.config(text='Registration success!', fg='green', font=('calibri', 11))
            elif username_entry.get() != "" and password_entry.get() != "" and username_entry.get():
                msg_label.config(text='Registration unsuccessful, username already exist', fg='red', font=('calibri', 11))
            else:
                msg_label.config(text='Registration unsuccessful', fg='red', font=('calibri', 11))

        elif table_empty_check[0][0] != 0: # if table is not empty
            cursor.execute("""SELECT username FROM user WHERE username=?""", (username_entry.get(),))
            result = cursor.fetchone()
            if username_entry.get() != "" and password_entry.get() != "" and result is None:
                cursor.execute(insert, [(username_entry.get()), (password_entry.get())])
                db.commit()
                msg_label.config(text='Registration success!', fg='green', font=('calibri', 11))
            elif username_entry.get() != "" and password_entry.get() != "" and result:
                msg_label.config(text='Registration unsuccessful, username already exist', fg='red', font=('calibri', 11))
            else:
                msg_label.config(text='Registration unsuccessful', fg='red', font=('calibri', 11))

    Button(screen1, text='Register', width=10, height=2, command=register_user).pack()


def login_page():
    global screen2
    screen2 = Tk()
    screen2.title('Please select optimizer and corresponding csv files')
    screen2.geometry("1200x700+350+150")

    # frame 1 and the widgets
    frame1 = Frame(screen2)
    frame1.place(relx=0, rely=0, relwidth=0.33, relheight=1)

    label1 = Label(frame1, text='Step 1 :')
    label1.place(relx=0, rely=0)
    label1.config(font=('', 20))

    label2 = Label(frame1, text='Select Discipline :')
    label2.place(relx=0.35, rely=0.35)
    label2.config(font=('', 10))

    tooltip1 = Balloon(frame1)
    tooltip1.bind_widget(label2, balloonmsg='Please select the discipline of the surgery procedures to be scheduled')

    disc_list = ['BREAST', 'OTO', 'NES', 'CLR', 'HPB', 'PLS', 'ENT','SUR-ONCO', 'UGI', 'H&N', 'O&G', 'HND', 'OMS', 'VAS', 'CTS', 'URO']

    combobox1 = ttk.Combobox(frame1, values=disc_list, state='readonly')
    combobox1.place(relx=0.35, rely=0.38)

    divider_frame1 = Frame(screen2, bg='grey')
    divider_frame1.place(relx=0.33, rely=0, relwidth=0.005, relheight=1)

    # frame 2 and the widgets
    frame2 = Frame(screen2)
    frame2.place(relx=0.335, rely=0, relwidth=0.33, relheight=1)

    label4 = Label(frame2, text='Step 2 :')
    label4.place(relx=0, rely=0)
    label4.config(font=('', 20))

    label5 = Label(frame2, text='Select the Current Schedule .csv file :')
    label5.place(relx=0.2, rely=0.32)
    label5.config(font=('', 10))

    entry1 = Entry(frame2, width=30)
    entry1.place(relx=0.2, rely=0.35)

    def browsefunc1():
        global file_path_1

        file_name = filedialog.askopenfilename(title='Please select the schedule .csv file')
        file_path_1 = os.path.normpath(file_name)

        head, tail = os.path.split(file_name)
        # file_path = os.path.normpath(file_name)
        entry1.delete(0, 'end')
        entry1.insert(0, tail)  # add this

    b1 = Button(frame2, text="Browse :", command=browsefunc1)
    b1.place(relx=0.75, rely=0.35)

    tooltip = Balloon(frame2)
    tooltip.bind_widget(b1, balloonmsg='Please refer to the documentation for the corresponding csv templates')

    label6 = Label(frame2, text='Select the to be Scheduled .csv file :')
    label6.place(relx=0.2, rely=0.42)
    label6.config(font=('', 10))

    entry2 = Entry(frame2, width=30)
    entry2.place(relx=0.2, rely=0.45)

    def browsefunc2():
        global file_path_2
        file_name = filedialog.askopenfilename(title='Please select the to be scheduled .csv file')
        file_path_2 = os.path.normpath(file_name)

        head, tail = os.path.split(file_name)
        entry2.delete(0, 'end')
        entry2.insert(0, tail)  # add this

    b2 = Button(frame2, text="Browse :", command=browsefunc2)
    b2.place(relx=0.75, rely=0.45)
    tooltip.bind_widget(b2, balloonmsg='Please refer to the documentation for the corresponding csv templates')

    label7 = Label(frame2, text='Select the MAS .csv file :')
    label7.place(relx=0.2, rely=0.52)
    label7.config(font=('', 10))

    entry3 = Entry(frame2 , width=30)
    entry3.place(relx=0.2, rely=0.55)

    def browsefunc3():
        global file_path_3
        file_name = filedialog.askopenfilename(title='Please select the MAS .csv file')
        file_path_3 = os.path.normpath(file_name)

        head, tail = os.path.split(file_name)
        entry3.delete(0, 'end')
        entry3.insert(0, tail)  # add this

    b3 = Button(frame2, text="Browse :", command=browsefunc3)
    b3.place(relx=0.75, rely=0.55)
    tooltip.bind_widget(b3, balloonmsg='Please refer to the documentation for the corresponding csv templates')

    divider_frame2 = Frame(screen2, bg='grey')
    divider_frame2.place(relx=0.665, rely=0, relwidth=0.005, relheight=1)

    # frame 3 and its widgets
    frame3 = Frame(screen2)
    frame3.place(relx=0.67, rely=0, relwidth=0.33, relheight=1)

    label7 = Label(frame3, text='Step 3 :')
    label7.place(relx=0, rely=0)
    label7.config(font=('', 20))

    label8 = Label(frame3, text='Select Optimizer :')
    label8.place(relx=0.35, rely=0.3)
    label8.config(font=('', 10))

    elements = ['Hill Climbing', 'Tabu Search', 'Simulated Annealing', 'Genetic Algorithm']

    list_box = Listbox(frame3, selectmode=SINGLE)
    list_box.insert(END, *elements)
    list_box.place(relx=0.35, rely=0.33)

    def generate_schedule():

        current_schedule = read_csv1(file_path_1)
        to_schedule = read_toschedule1(file_path_2)
        mas_full = read_mas1(file_path_3)
        disc_selected = combobox1.get()

        optimizer_selected = list_box.get(list_box.curselection())

        optimizer_dict = {'Hill Climbing': 1, 'Tabu Search': 2, 'Simulated Annealing': 3,
                          'Genetic Algorithm': 4}

        if optimizer_dict[optimizer_selected] == 1:
            run_hco(current_schedule, to_schedule, mas_full, disc_selected)
        if optimizer_dict[optimizer_selected] == 2:
            run_ts(current_schedule, to_schedule, mas_full, disc_selected)
        if optimizer_dict[optimizer_selected] == 3:
            run_sa(current_schedule, to_schedule, mas_full, disc_selected)
        if optimizer_dict[optimizer_selected] == 4:
            run_ga(current_schedule, to_schedule, mas_full, disc_selected)

    b4 = Button(frame3, text='Generate Schedule', command=generate_schedule)
    b4.place(relx=0.37, rely=0.65)


def main_screen():
    global screen
    screen = Tk()
    screen.geometry("1200x700+350+150")
    screen.title("Scheduling Application")
    Label(text='Singhealth Meta-heuristics Operating Theatre Scheduling Optimization', bg='#D35400', width='1200', height='2').pack()

    username_verify = StringVar()
    password_verify = StringVar()

    # username heading and entry
    u_label = Label(screen, text='Username :')
    u_label.place(relx=.5, rely=.32, anchor="center")
    username_entry_main = Entry(screen, textvariable=username_verify, width=30, justify='center')
    username_entry_main.place(relx=.5, rely=.35, anchor="center")

    # password heading and entry
    p_label = Label(screen, text='Password :')
    p_label.place(relx=.5, rely=.42, anchor="center")
    password_entry_main = Entry(screen, textvariable=password_verify, width=30, justify='center', show='*')
    password_entry_main.place(relx=.5, rely=.45, anchor="center")

    def login_button():
        # create a database or connect to one
        with sqlite3.connect('user_info.db') as db:
            cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user(username TEXT NOT NULL, password TEXT NOT NULL);")
        cursor.execute("SELECT * FROM user")
        db.commit()
        db.close()

        with sqlite3.connect('user_info.db') as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM user WHERE username = ? AND password = ?")
        cursor.execute(find_user, [(username_entry_main.get()), password_entry_main.get()])
        results = cursor.fetchall()
        if results:
            screen.destroy()
            login_page()
        else:
            Label(screen, text='Username or password not found \n Please register an account.', fg='red', font=('calibri', 11)).place(relx=0.5, rely=0.6, anchor='center')

    # login and register buttons
    Button(text='Login', height='1', width='10', command=login_button).place(relx=.5, rely=.5, anchor="center")
    Button(text='Register', height='1' ,width='10', command=register_page).place(relx=.5, rely=.55, anchor="center")

    screen.mainloop()


