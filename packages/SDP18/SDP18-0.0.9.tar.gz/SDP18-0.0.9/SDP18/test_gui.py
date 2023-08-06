from tkinter import *
from datetime import *

root = Tk()

# set title and size of the GUI window
root.title('Timetable')
root.geometry("1200x700+350+150")

# set secondary frame position and size (center right)
frame = Frame(root, bg='blue')
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
canvas = Canvas(root, bg='red')
canvas.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

# create and set vertical scrollbar
vbar = Scrollbar(frame)
vbar.config(command=canvas.yview)
canvas.config(yscrollcommand=vbar.set)
vbar.pack(side="right", fill=Y)

# create a frame inside the canvas
# configure size of frame
canvas_frame = Frame(canvas, width=955, height=900, bg='green')
canvas_frame.pack(expand=True, fill=BOTH)

canvas_id = canvas.create_window(0, 0, window=canvas_frame, anchor="nw")

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

# create time-table using labels (44rows*23columns)
rows = 44
cols = 24
blk = [[0 for i in range(cols)] for j in range(rows)]
for i in range(rows):  # Rows
    for j in range(cols):  # Columns
        blk[i][j] = Label(canvas_frame, text="", bg='#FDFEFE', relief=RIDGE)
        blk[i][j].place(relwidth=0.04, relx=0.08 + j * 0.04, y=20 + i * 20)


canvas.configure(scrollregion = canvas.bbox("all"))

root.mainloop()