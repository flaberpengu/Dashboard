import tkinter as tk
import time
import processor_info
from PIL import ImageTk,Image
import datetime as dt

root = tk.Tk()
root.geometry('650x1000')
root.title('Dashboard')
root.configure(bg='#bfbfbf')

##Displays top bar with date and time
currentDateTime = dt.datetime.now()
##Gets the string for the current date
if (len(str(currentDateTime.month)) == 1):
    if (len(str(currentDateTime.day)) == 1):
        dateBarString = "%i-0%i-0%i" % (currentDateTime.year, currentDateTime.month, currentDateTime.day)
    else:
        dateBarString = "%i-0%i-%i" % (currentDateTime.year, currentDateTime.month, currentDateTime.day)
else:
    if (len(str(currentDateTime.day)) == 1):
        dateBarString = "%i-%i-0%i" % (currentDateTime.year, currentDateTime.month, currentDateTime.day)
    else:
        dateBarString = "%i-%i-%i" % (currentDateTime.year, currentDateTime.month, currentDateTime.day)
##TODO - Add dynamic time
timeBarString = "%i:%i" % (currentDateTime.hour, currentDateTime.minute)
datetimeBar = tk.Canvas(root, width=650, height=43, bg='#636363', highlightthickness=0).place(x=0, y=0)
lblDate = tk.Label(datetimeBar,
                   text=dateBarString,
                   bg='#636363',
                   fg='#ffffff',
                   font=('Book Antiqua', 20)).place(x=8, y=3)
lblName = tk.Label(datetimeBar,
                   text="Jacob's Dashboard",
                   bg='#636363',
                   fg='#ffffff',
                   font=('Book Antiqua', 20)).place(x=212, y=3)
lblTime = tk.Label(datetimeBar,
                   text=timeBarString,
                   bg='#636363',
                   fg='#ffffff',
                   font=('Book Antiqua', 20)).place(x=582, y=3)

##Gets and displays image of CPU use per core
#processor_info.getCPUInfo()
cpu_info_image = ImageTk.PhotoImage(Image.open('processor_info_percpu_usage.png'))
cpu_info = tk.Canvas(root, width=650, height=300, bg='#636363', highlightthickness=0).place(x=0, y=45)

tk.mainloop()
