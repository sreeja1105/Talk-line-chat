from tkinter import *
from datetime import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.geometry("600x250")
import sqlite3

mydb = sqlite3.connect('miniproject.db')
c = mydb.cursor()
c.execute(
    "CREATE TABLE IF NOT EXISTS USER(UID INTEGER PRIMARY KEY DEFAULT 1,FNAME VARCHAR(20) NOT NULL,LNAME VARCHAR(20),DOB DATE,GENDER VARCHAR(20) NOT NULL,ADDRESS VARCHAR(20),EMAIL VARCHAR(20) NOT NULL,PASSWORD VARCHAR(20) NOT NULL, PHONE_NO INT,COLLEGE VARCHAR(20))")
c.execute(
    '''CREATE TABLE IF NOT EXISTS GRP(GID INTEGER PRIMARY KEY,GNAME VARCHAR(20),TOT_MEM INT DEFAULT 1,DATE_CREATION DATE,UID INT,CONSTRAINT FK11 FOREIGN KEY(UID) REFERENCES USER(UID))''')
c.execute(
    "CREATE TABLE IF NOT EXISTS EVENT(EID INTEGER PRIMARY KEY,ENAME VARCHAR(20),EDATE DATE,PLACE VARCHAR(30),ETIME TIME,INTERESTED_PPL INT DEFAULT 1,USER_ID INT,CONSTRAINT FK1 FOREIGN KEY(USER_ID) REFERENCES USER(UID))")


c.execute(
    "CREATE TABLE IF NOT EXISTS MESSAGE(MID INTEGER PRIMARY KEY,MSG VARCHAR(100),DATE1 DATE,TIME1 TIME,USER_ID INT,CONSTRAINT FK4 FOREIGN KEY(USER_ID) REFERENCES USER(UID))")
c.execute(
    "CREATE TABLE IF NOT EXISTS JOINS(UID INTEGER,GID INTEGER,PRIMARY KEY(UID,GID),CONSTRAINT FK5 FOREIGN KEY(UID) REFERENCES USER(UID),CONSTRAINT FK6 FOREIGN KEY(GID) REFERENCES GRP(GID))")
c.execute(
    "CREATE TABLE IF NOT EXISTS PARTICIPATE(UID INTEGER,EID INTEGER,CONSTRAINT FK7 FOREIGN KEY(UID) REFERENCES USER(UID),CONSTRAINT FK8 FOREIGN KEY(EID) REFERENCES EVENT(EID))")
c.execute(
    "CREATE TABLE IF NOT EXISTS FRIEND(USERID INTEGER,FRND_ID INTEGER,PRIMARY KEY(USERID,FRND_ID),CONSTRAINT FK9 FOREIGN KEY(USERID) REFERENCES USER(UID),CONSTRAINT FK10 FOREIGN KEY(FRND_ID) REFERENCES USER(UID))")

abc = Frame(root, bg="powder blue", bd=10, width=250, height=100, padx=250, pady=50, relief=RIDGE)
abc.grid(row=2, column=0, columnspan=4)
SEARCH = StringVar()
a = StringVar()


# =================================================================================================================================
def register():
    r1 = Toplevel()
    mydb.commit()

    fname = StringVar()
    lname = StringVar()
    dob = StringVar()
    gender = StringVar()
    add = StringVar()
    email = StringVar()
    passwd = StringVar()
    pno = IntVar()
    college = StringVar()

    l3 = Label(r1, text="FIRST NAME :")
    l3.grid(column=0, row=0)
    t3 = Entry(r1, textvariable=fname)
    t3.grid(column=3, row=0)

    l4 = Label(r1, text="LAST NAME :")
    l4.grid(column=0, row=2)
    t4 = Entry(r1, textvariable=lname)
    t4.grid(column=3, row=2)

    l5 = Label(r1, text="DATE OF BIRTH :")
    l5.grid(column=0, row=4)
    t5 = Entry(r1, textvariable=dob)
    t5.grid(column=3, row=4)
    print(dob)

    l6 = Label(r1, text="GENDER :")
    l6.grid(column=0, row=6)
    t6 = Entry(r1, textvariable=gender)
    t6.grid(column=3, row=6)

    l7 = Label(r1, text="ADDRESS :")
    l7.grid(column=0, row=8)
    t7 = Entry(r1, textvariable=add)
    t7.grid(column=3, row=8)

    l8 = Label(r1, text="EMAIL :")
    l8.grid(column=0, row=10)
    t8 = Entry(r1, textvariable=email)
    t8.grid(column=3, row=10)

    l9 = Label(r1, text="PASSWORD :")
    l9.grid(column=0, row=12)
    t9 = Entry(r1, show='\u25CF', textvariable=passwd)
    t9.grid(column=3, row=12)

    l10 = Label(r1, text="PHONE NO. :")
    l10.grid(column=0, row=14)
    t10 = Entry(r1, textvariable=pno)
    t10.grid(column=3, row=14)

    l11 = Label(r1, text="COLLEGE :")
    l11.grid(column=0, row=16)
    t11 = Entry(r1, textvariable=college)
    t11.grid(column=3, row=16)

    def insert():
        a = fname.get()
        b = lname.get()
        c = dob.get()
        d = gender.get()
        e = add.get()
        f = email.get()
        g = passwd.get()
        h = pno.get()
        i = college.get()
        mydb = sqlite3.connect('miniproject.db')
        c = mydb.cursor()
        c.execute(
            '''INSERT INTO USER(FNAME,LNAME,DOB,GENDER,ADDRESS,EMAIL,PASSWORD,PHONE_NO,COLLEGE) VALUES('%s','%s','%s','%s','%s','%s','%s','%d','%s')''' % (
            a, b, c, d, e, f, g, h, i))
        c.close()
        mydb.commit()
        c.close()
        print("registration successful")
        login()

    b3 = Button(r1, text="REGISTER", command=insert)
    b3.grid(row=20, column=2)


# =================================================================================================================================

def DisplayData():
    mydb = sqlite3.connect('miniproject.db')
    c = mydb.cursor()
    c.execute("SELECT * FROM `USER`")
    fetch = c.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[5], data[4], data[8], data[9]))
    c.close()
    mydb.commit()
    c.close()


def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        mydb = sqlite3.connect('miniproject.db')
        c = mydb.cursor()
        c.execute("SELECT * FROM `USER` WHERE `FNAME` LIKE ?", ('%' + str(SEARCH.get()) + '%',))
        fetch = c.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[5], data[4], data[8], data[9]))
        c.close()
        mydb.commit()
        c.close()


def add_frnd(e):
    if not tree.selection():
        print("ERROR")
    else:
        result = tkMessageBox.askquestion('INTERACTIVE MULTIMEDIA', 'Are you sure you want to add him as a friend',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            a = selecteditem[0]
            mydb = sqlite3.connect('miniproject.db')
            c = mydb.cursor()
            c.execute("INSERT INTO `FRIEND` (USERID,FRND_ID) VALUES('%d','%s')" % (e, selecteditem[0]))
            c.close()
            mydb.commit()
            c.close()


def search_frnd(e):
    global tree
    Topr7 = Frame(r7, width=600, bd=1, relief=SOLID)
    Topr7.pack(side=TOP, fill=X)
    Leftr7 = Frame(r7, width=600)
    Leftr7.pack(side=LEFT, fill=Y)
    Midr7 = Frame(r7, width=600)
    Midr7.pack(side=RIGHT)
    lbl_text = Label(Topr7, text="View Friends", font=('arial', 18), width=600).pack(fill=X)
    lbl_txtsearch = Label(Leftr7, text="Search", font=('arial', 15)).pack(side=TOP, anchor=W)
    search = Entry(Leftr7, textvariable=SEARCH, font=('arial', 15), width=10).pack(side=TOP, padx=10, fill=X)
    btn_search = Button(Leftr7, text="Search", command=Search).pack(side=TOP, padx=10, pady=10, fill=X)
    btn_add_frnd = Button(Leftr7, text="ADD FRIEND", command=lambda: add_frnd(e)).pack(side=TOP, padx=10, pady=10,
                                                                                       fill=X)

    scrollbarx = Scrollbar(Midr7, orient=HORIZONTAL)
    scrollbary = Scrollbar(Midr7, orient=VERTICAL)
    tree = ttk.Treeview(Midr7, columns=("USER_ID", "FNAME", "LNAME", "DOB", "ADDRESS", "GENDER", "PHONE_NO", "COLLEGE"),
                        selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('USER_ID', text="UID", anchor=W)
    tree.heading('FNAME', text="FNAME", anchor=W)
    tree.heading('LNAME', text="LNAME", anchor=W)
    tree.heading('DOB', text="DOB", anchor=W)
    tree.heading('ADDRESS', text="ADDRESS", anchor=W)
    tree.heading('GENDER', text="GENDER", anchor=W)
    tree.heading('PHONE_NO', text="PHONE_NO", anchor=W)
    tree.heading('COLLEGE', text="COLLEGE", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=50)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=100)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.column('#5', stretch=NO, minwidth=0, width=200)
    tree.column('#6', stretch=NO, minwidth=0, width=100)
    tree.column('#7', stretch=NO, minwidth=0, width=120)
    tree.column('#8', stretch=NO, minwidth=0, width=200)
    tree.pack()
    DisplayData()


def ShowView(e):
    global r7
    r7 = Toplevel()
    r7.title("INTERACTIVE MULTIMEDIA")
    width = 600
    height = 400
    screen_width = 1366
    screen_height = 768
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    r7.geometry("%dx%d+%d+%d" % (width, height, x, y))
    r7.resizable(0, 0)
    search_frnd(e)


# =================================================================================================================================

def create_group(e):
    r4 = Toplevel()
    gname = StringVar()

    g_l1 = Label(r4, text="Enter group name").grid(column=0, row=0)
    g_t1 = Entry(r4, textvariable=gname).grid(column=3, row=0)

    def insert_group(e):
        a = gname.get()
        date = datetime.now().strftime("%B %d,%Y %I:%M%p")
        mydb = sqlite3.connect('miniproject.db')
        c = mydb.cursor()
        c.execute('''INSERT INTO GRP(GNAME,DATE_CREATION,UID) VALUES('%s','%s','%d')''' % (a, date, e))
        c.close()
        mydb.commit()
        c.close()

    g_b1 = Button(r4, text="CREATE", command=lambda: insert_group(e)).grid(row=6, column=2)


# =================================================================================================================================

def create_event(e):
    r5 = Toplevel()
    ename = StringVar()
    eplace = StringVar()
    edate = StringVar()
    etime = StringVar()

    e_l1 = Label(r5, text="Enter Event name").grid(column=0, row=0)
    e_t1 = Entry(r5, textvariable=ename).grid(column=3, row=0)

    e_l2 = Label(r5, text="Enter Event date").grid(column=0, row=2)
    e_t2 = Entry(r5, textvariable=edate).grid(column=3, row=2)
    print(edate)

    e_l3 = Label(r5, text="Enter Event time").grid(column=0, row=4)
    e_t3 = Entry(r5, textvariable=etime).grid(column=3, row=4)
    print(etime)

    e_l4 = Label(r5, text="Enter Event Place").grid(column=0, row=6)
    e_t4 = Entry(r5, textvariable=eplace).grid(column=3, row=6)

    def insert_event(e):
        a = ename.get()
        b = edate.get()
        c = etime.get()
        d = eplace.get()

        mydb = sqlite3.connect('miniproject.db')
        c = mydb.cursor()
        c.execute(
            '''INSERT INTO EVENT(ENAME,EDATE,ETIME,PLACE,USER_ID) VALUES('%s','%s','%s','%s','%d')''' % (a, b, c, d, e))
        c.close()
        mydb.commit()
        c.close()

    e_b1 = Button(r5, text="CREATE", command=lambda: insert_event(e)).grid(row=8, column=2)


# =================================================================================================================================

def DisplayData5(e):
    mydb = sqlite3.connect('miniproject.db')
    c = mydb.cursor()
    c.execute(
        "SELECT * FROM `USER` WHERE UID IN (SELECT FRND_ID FROM FRIEND,USER WHERE UID=USERID AND USERID IN (%d))" % e)
    fetch = c.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[5], data[4], data[8], data[9]))
    c.close()
    mydb.commit()
    c.close()


def Search1():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        mydb = sqlite3.connect('miniproject.db')
        c = mydb.cursor()
        c.execute("SELECT * FROM `USER` WHERE `FNAME` LIKE ?", ('%' + str(SEARCH.get()) + '%',))
        fetch = c.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[5], data[4], data[8], data[9]))
        c.close()
        mydb.commit()
        c.close()


def showfrnd(e):
    global tree
    Topr8 = Frame(r8, width=600, bd=1, relief=SOLID)
    Topr8.pack(side=TOP, fill=X)
    Leftr8 = Frame(r8, width=600)
    Leftr8.pack(side=LEFT, fill=Y)
    Midr8 = Frame(r8, width=600)
    Midr8.pack(side=RIGHT)
    lbl_text = Label(Topr8, text="View Friends", font=('arial', 18), width=600).pack(fill=X)
    lbl_txtsearch = Label(Leftr8, text="Search", font=('arial', 15)).pack(side=TOP, anchor=W)
    search = Entry(Leftr8, textvariable=SEARCH, font=('arial', 15), width=10).pack(side=TOP, padx=10, fill=X)
    btn_search = Button(Leftr8, text="SEARCH", command=Search1).pack(side=TOP, padx=10, pady=10, fill=X)
    # btn_msg = Button(Leftr8, text="CHAT", command=chat).pack(side=TOP, padx=10, pady=10, fill=X)

    scrollbarx = Scrollbar(Midr8, orient=HORIZONTAL)
    scrollbary = Scrollbar(Midr8, orient=VERTICAL)
    tree = ttk.Treeview(Midr8, columns=("USER_ID", "FNAME", "LNAME", "DOB", "ADDRESS", "GENDER", "PHONE_NO", "COLLEGE"),
                        selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('USER_ID', text="UID", anchor=W)
    tree.heading('FNAME', text="FNAME", anchor=W)
    tree.heading('LNAME', text="LNAME", anchor=W)
    tree.heading('DOB', text="DOB", anchor=W)
    tree.heading('ADDRESS', text="ADDRESS", anchor=W)
    tree.heading('GENDER', text="GENDER", anchor=W)
    tree.heading('PHONE_NO', text="PHONE_NO", anchor=W)
    tree.heading('COLLEGE', text="COLLEGE", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=50)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=100)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.column('#5', stretch=NO, minwidth=0, width=200)
    tree.column('#6', stretch=NO, minwidth=0, width=100)
    tree.column('#7', stretch=NO, minwidth=0, width=120)
    tree.column('#8', stretch=NO, minwidth=0, width=200)
    tree.pack()
    DisplayData5(e)


def ShowfrndView(e):
    global r8
    r8 = Toplevel()
    r8.title("INTERACTIVE MULTIMEDIA")
    width = 600
    height = 400
    screen_width = 1366
    screen_height = 768
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    r8.geometry("%dx%d+%d+%d" % (width, height, x, y))
    r8.resizable(0, 0)
    showfrnd(e)


# =================================================================================================================================

def DisplayData2():
    mydb = sqlite3.connect('miniproject.db')
    c = mydb.cursor()
    c.execute("SELECT * FROM `GRP`")
    fetch = c.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4]))
    c.close()
    mydb.commit()
    c.close()


def join_grp1(e):
    if not tree.selection():
        print("ERROR")
    else:
        result = tkMessageBox.askquestion('INTERACTIVE MULTIMEDIA', 'Are you sure you want to join this group',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            a = selecteditem[0]
            mydb = sqlite3.connect('miniproject.db')
            c = mydb.cursor()
            c.execute("UPDATE GRP SET TOT_MEM=TOT_MEM +:margin WHERE GID = :margin1", {"margin": 1, "margin1": 2})
            c.execute("INSERT INTO `JOINS` (UID,GID) VALUES('%d','%d')" % (e, selecteditem[0]))
            c.close()
            mydb.commit()
            c.close()


def join_grp(e):
    global tree
    Topr9 = Frame(r9, width=600, bd=1, relief=SOLID)
    Topr9.pack(side=TOP, fill=X)
    Leftr9 = Frame(r9, width=600)
    Leftr9.pack(side=LEFT, fill=Y)
    Midr9 = Frame(r9, width=600)
    Midr9.pack(side=RIGHT)
    lbl_text = Label(Topr9, text="Join group", font=('arial', 18), width=600).pack(fill=X)
    lbl_txtsearch = Label(Leftr9, text="Search", font=('arial', 15)).pack(side=TOP, anchor=W)
    search = Entry(Leftr9, textvariable=SEARCH, font=('arial', 15), width=10).pack(side=TOP, padx=10, fill=X)
    btn_search = Button(Leftr9, text="SEARCH", command=Search).pack(side=TOP, padx=10, pady=10, fill=X)
    btn_join_grp = Button(Leftr9, text="JOIN GROUP", command=lambda: join_grp1(e)).pack(side=TOP, padx=10, pady=10,
                                                                                        fill=X)

    scrollbarx = Scrollbar(Midr9, orient=HORIZONTAL)
    scrollbary = Scrollbar(Midr9, orient=VERTICAL)
    tree = ttk.Treeview(Midr9, columns=("GID", "GNAME", "TOT_MEM", "DATE_CREATION", "UID"), selectmode="extended",
                        height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('GID', text="GID", anchor=W)
    tree.heading('GNAME', text="GNAME", anchor=W)
    tree.heading('TOT_MEM', text="TOT_MEM", anchor=W)
    tree.heading('DATE_CREATION', text="DATE_CREATION", anchor=W)
    tree.heading("UID", text="UID", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=50)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=100)
    tree.column('#4', stretch=NO, minwidth=0, width=150)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData2()


def show_grp(e):
    global r9
    r9 = Toplevel()
    r9.title("INTERACTIVE MULTIMEDIA")
    width = 600
    height = 400
    screen_width = 1366
    screen_height = 768
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    r9.geometry("%dx%d+%d+%d" % (width, height, x, y))
    r9.resizable(0, 0)
    join_grp(e)


# ================================================================================================================================

def DisplayData4():
    mydb = sqlite3.connect('miniproject.db')
    c = mydb.cursor()
    c.execute("SELECT * FROM `EVENT`")
    fetch = c.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[4], data[3], data[5], data[6]))
    c.close()
    mydb.commit()
    c.close()


def Search2():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        mydb = sqlite3.connect('miniproject.db')
        c = mydb.cursor()
        c.execute("SELECT * FROM `EVENT` WHERE `ENAME` LIKE ? OR PLACE LIKE ?", ('%' + str(SEARCH.get()) + '%',))
        fetch = c.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[4], data[3], data[5], data[6]))
        c.close()
        mydb.commit()
        c.close()


def join_event2(e):
    if not tree.selection():
        print("ERROR")
    else:
        result = tkMessageBox.askquestion('INTERACTIVE MULTIMEDIA', 'Are you sure you want to attend this event',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            a = selecteditem[0]
            mydb = sqlite3.connect('miniproject.db')
            c = mydb.cursor()
            c.execute("UPDATE EVENT SET INTERESTED_PPL=INTERESTED_PPL +:margin WHERE EID = :margin1",
                      {"margin": 1, "margin1": a})
            c.execute("INSERT INTO `PARTICIPATE` (UID,EID) VALUES('%d','%d')" % (e, selecteditem[0]))
            c.close()
            mydb.commit()
            c.close()


def join_event1(e):
    global tree
    Topr10 = Frame(r10, width=600, bd=1, relief=SOLID)
    Topr10.pack(side=TOP, fill=X)
    Leftr10 = Frame(r10, width=600)
    Leftr10.pack(side=LEFT, fill=Y)
    Midr10 = Frame(r10, width=600)
    Midr10.pack(side=RIGHT)
    lbl_text = Label(Topr10, text="View EVENTS", font=('arial', 18), width=600).pack(fill=X)
    lbl_txtsearch = Label(Leftr10, text="Search", font=('arial', 15)).pack(side=TOP, anchor=W)
    search = Entry(Leftr10, textvariable=SEARCH, font=('arial', 15), width=10).pack(side=TOP, padx=10, fill=X)
    btn_search = Button(Leftr10, text="SEARCH", command=Search2).pack(side=TOP, padx=10, pady=10, fill=X)
    btn_join_grp = Button(Leftr10, text="JOIN EVENT", command=lambda: join_event2(e)).pack(side=TOP, padx=10, pady=10,
                                                                                           fill=X)

    scrollbarx = Scrollbar(Midr10, orient=HORIZONTAL)
    scrollbary = Scrollbar(Midr10, orient=VERTICAL)
    tree = ttk.Treeview(Midr10, columns=("EID", "ENAME", "EDATE", "ETIME", "PLACE", "INTERESTED_PPL", "USER_ID"),
                        selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('EID', text="EID", anchor=W)
    tree.heading('ENAME', text="EVENT NAME", anchor=W)
    tree.heading('EDATE', text="EVENT DATE", anchor=W)
    tree.heading('ETIME', text="EVENT TIME", anchor=W)
    tree.heading("PLACE", text="EVENT PLACE", anchor=W)
    tree.heading('INTERESTED_PPL', text="INTERESTED PPL", anchor=W)
    tree.heading("USER_ID", text="EVENT CORDINATOR", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=50)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=100)
    tree.column('#4', stretch=NO, minwidth=0, width=150)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=150)
    tree.column('#7', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData4()


def join_event(e):
    global r10
    r10 = Toplevel()
    r10.title("INTERACTIVE MULTIMEDIA")
    width = 600
    height = 400
    screen_width = 1366
    screen_height = 768
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    r10.geometry("%dx%d+%d+%d" % (width, height, x, y))
    r10.resizable(0, 0)
    join_event1(e)


# =================================================================================================================================







# =============================================================================================================================

def newPage(e):
    r3 = Toplevel()
    r3.title("INTERACTIVE MULTIMEDIA")
    Topr3 = Frame(r3, width=600, bd=1, relief=SOLID)
    Topr3.pack(side=TOP, fill=X)
    Leftr3 = Frame(r3, width=600)
    Leftr3.pack(side=LEFT, fill=Y)
    Midr3 = Frame(r3, width=600)
    Midr3.pack(side=RIGHT)
    width = 600
    height = 400
    screen_width = 1366
    screen_height = 768
    x = (screen_width) - 1000
    y = (screen_height) - 650
    r3.geometry("%dx%d+%d+%d" % (width, height, x, y))
    r3.resizable(0, 0)

    menubar = Menu(r3)
    menubar.add_cascade(label="HOME")
    menubar.add_cascade(label="EVENT")
    menubar.add_cascade(label="FRIENDS LIST")
    menubar.add_cascade(label="GROUP LIST")
    r3.config(menu=menubar)

    new_b1 = Button(Leftr3, text="Search for friends", command=lambda: ShowView(e)).grid(row=0, column=2, padx=10,
                                                                                         pady=10)
    new_b2 = Button(Leftr3, text="Create a Group", command=lambda: create_group(e)).grid(row=2, column=2, padx=10,
                                                                                         pady=10)
    new_b3 = Button(Leftr3, text="Organise an Event", command=lambda: create_event(e)).grid(row=4, column=2, padx=10,
                                                                                            pady=10)

    new_b5 = Button(Leftr3, text="FRIENDS LIST", command=lambda: ShowfrndView(e)).grid(row=8, column=2, padx=10,
                                                                                       pady=10)
    new_b6 = Button(Leftr3, text="Join group", command=lambda: show_grp(e)).grid(row=10, column=2, padx=10, pady=10)
    new_b6 = Button(Leftr3, text="PARTICIPATE IN EVENT", command=lambda: join_event(e)).grid(row=12, column=2, padx=10,
                                                                                             pady=10)


# =================================================================================================================================

def login():
    r2 = Toplevel()
    email_login = StringVar()
    passwd_login = StringVar()

    login_l1 = Label(r2, text="EMAIL :")
    login_l1.grid(column=0, row=2)
    login_t1 = Entry(r2, textvariable=email_login)
    login_t1.grid(column=3, row=2)

    login_l2 = Label(r2, text="PASSWORD :")
    login_l2.grid(column=0, row=4)
    login_t2 = Entry(r2, show='\u25CF', textvariable=passwd_login)
    login_t2.grid(column=3, row=4)

    def login_insert():
        a = email_login.get()
        b = passwd_login.get()
        c.execute("SELECT * FROM USER")
        e = c.fetchall()
        for i in range(0, len(e)):
            if (a == e[i][6] and b == e[i][7]):  # can only be done for first entry
                print("DONE")
                newPage(e[i][0])
            else:
                print("ERROR!")

    b3 = Button(r2, text="LOGIN", command=login_insert)
    b3.grid(row=6, column=2)


b1 = Button(abc, text="LOGIN", command=login)
b1.grid(row=0, column=2)

b2 = Button(abc, text="REGISTER", command=register)
b2.grid(row=2, column=2)
today = date.today()
print("Today's date:", today)

root.mainloop()
