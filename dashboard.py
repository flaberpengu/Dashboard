import tkinter as tk
import time
import processor_info
from PIL import ImageTk,Image
import datetime as dt
import threading
import queue

root = tk.Tk()
root.geometry('650x1000')
root.title('Dashboard')
root.configure(bg='#bfbfbf')

##Section of code that makes top bar with dynamic time
#Create GUI elements
datetimeBar = tk.Canvas(root, width=650, height=43, bg='#636363', highlightthickness=0).place(x=0, y=0)
lblDate = tk.Label(datetimeBar,
                   text="f",
                   bg='#636363',
                   fg='#ffffff',
                   font=('Book Antiqua', 20))
lblDate.place(x=8, y=3)
lblName = tk.Label(datetimeBar,
                   text="Jacob's Dashboard",
                   bg='#636363',
                   fg='#ffffff',
                   font=('Book Antiqua', 20))
lblName.place(x=212, y=3)
lblTime = tk.Label(datetimeBar,
                   text="f",
                   bg='#636363',
                   fg='#ffffff',
                   font=('Book Antiqua', 20))
lblTime.place(x=545, y=3)
#Method to get the correct string to display for the time
def getTimeString(currentDatetime):
	returnString = ""
	if (len(str(currentDatetime.hour)) == 1):
		returnString += ("0%i" % (currentDatetime.hour))
	else:
		returnString += ("%i" % (currentDatetime.hour))
	returnString += ":"
	if (len(str(currentDatetime.minute)) == 1):
		returnString += ("0%i" % (currentDatetime.minute))
	else:
		returnString += ("%i" % (currentDatetime.minute))
	returnString += ":"
	if (len(str(currentDatetime.second)) == 1):
		returnString += ("0%i" % (currentDatetime.second))
	else:
		returnString += ("%i" % (currentDatetime.second))
	return returnString

#Method to get correct string to display for the date
def getDateString(currentDatetime):
	returnString = ("%i-" % (currentDatetime.year))
	if (len(str(currentDatetime.month)) == 1):
		returnString += ("0%i" % (currentDatetime.month))
	else:
		returnString += ("%i" % (currentDatetime.month))
	returnString += "-"
	if (len(str(currentDatetime.day)) == 1):
		returnString += ("0%i" % (currentDatetime.day))
	else:
		returnString += ("%i" % (currentDatetime.day))
	return returnString

datetimeQueue = queue.Queue(5)
dateFlagQueue = queue.Queue(1)
dateFlagQueue.put(dt.datetime.now())
firstDateFlag = True

#Method used by worker thread to get new datetime when needed
def updateDatetime(datetimeQueue):
	while True:
		if (datetimeQueue.qsize() == 0):
			datetimeQueue.put(dt.datetime.now())
			print("Updated")
		else:
			time.sleep(1)

#Method used by worker thread to display new time when necessary
def displayTime(datetimeQueue, dateFlagQueue):
	while True:
		if (datetimeQueue.qsize() != 0):
			print("GettingTime")
			newTime = getTimeString(datetimeQueue.get(0))
			datetimeQueue.task_done()
			lblTime.configure(text=newTime)
			if (newTime[0:1] == 0) and (newTime[3:4] == 0) and (newTime[6:7] == 0):
				dateFlagQueue.put(dt.datetime.now())
		else:
			time.sleep(0.1)

#Method used by worker thread to display new date when necessary
def displayDate(datetimeQueue, dateFlagQueue, firstDateFlag):
	while True:
		if (dateFlagQueue.qsize() != 0) or (firstDateFlag == True):
			print("GettingDate")
			newDate = getDateString(dateFlagQueue.get(0))
			dateFlagQueue.task_done()
			firstDateFlag = False
			lblDate.configure(text=newDate)
		else:
			time.sleep(1)

#Create worker threads
datetimeUpdater = threading.Thread(target=updateDatetime, args=(datetimeQueue,))
datetimeUpdater.setDaemon(True)
timeDisplayer = threading.Thread(target=displayTime, args=(datetimeQueue,dateFlagQueue))
timeDisplayer.setDaemon(True)
dateDisplayer = threading.Thread(target=displayDate, args=(datetimeQueue,dateFlagQueue,firstDateFlag))
dateDisplayer.setDaemon(True)

#Start worker threads
datetimeUpdater.start()
timeDisplayer.start()
dateDisplayer.start()


##Displays top bar with date and time
#currentDateTime = dt.datetime.now()
##Gets the string for the current date
#if (len(str(currentDateTime.month)) == 1):
#    if (len(str(currentDateTime.day)) == 1):
#        dateBarString = "%i-0%i-0%i" % (currentDateTime.year, currentDateTime.month, currentDateTime.day)
#    else:
#        dateBarString = "%i-0%i-%i" % (currentDateTime.year, currentDateTime.month, currentDateTime.day)
#else:
#    if (len(str(currentDateTime.day)) == 1):
#        dateBarString = "%i-%i-0%i" % (currentDateTime.year, currentDateTime.month, currentDateTime.day)
#    else:
#        dateBarString = "%i-%i-%i" % (currentDateTime.year, currentDateTime.month, currentDateTime.day)
##TODO - Add dynamic time
#timeBarString = "%i:%i" % (currentDateTime.hour, currentDateTime.minute)


##Gets and displays image of CPU use per core
#processor_info.getCPUInfo()
#cpu_info_image = ImageTk.PhotoImage(Image.open('processor_info_percpu_usage.png'))
#cpu_info = tk.Canvas(root, width=650, height=300, bg='#636363', highlightthickness=0).place(x=0, y=45)

root.mainloop()
