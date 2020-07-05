import tkinter as tk
import time
import datetime as dt
import threading
import queue
import CPUInfo
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

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

#Queue and flags variables needed
datetimeQueue = queue.Queue(5)
dateFlagQueue = queue.Queue(1)
dateFlagQueue.put(dt.datetime.now())
firstDateFlag = True

#Method used by worker thread to get new datetime when needed
def updateDatetime(datetimeQueue):
	while True:
		if (datetimeQueue.qsize() == 0):
			datetimeQueue.put(dt.datetime.now())
		else:
			time.sleep(1)

#Method used by worker thread to display new time when necessary
def displayTime(datetimeQueue, dateFlagQueue):
	while True:
		if (datetimeQueue.qsize() != 0):
			newTime = getTimeString(datetimeQueue.get(0))
			datetimeQueue.task_done()
			lblTime.configure(text=newTime)
			#If new day, update date
			if (newTime[0:1] == 0) and (newTime[3:4] == 0) and (newTime[6:7] == 0):
				dateFlagQueue.put(dt.datetime.now())
		else:
			time.sleep(0.1)

#Method used by worker thread to display new date when necessary
def displayDate(datetimeQueue, dateFlagQueue, firstDateFlag):
	while True:
		if (dateFlagQueue.qsize() != 0) or (firstDateFlag == True):
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


##Section of code that makes dynamic graph of whole CPU usage
#Queue and flag variables needed
wholeCPUUsageQueue = queue.Queue(20)
for b in range(20):
	wholeCPUUsageQueue.put(0)
wholeCPUUsageFlagQueue = queue.Queue(1)

#Uses pyplot to make figure and axis of subplot
figWholeCPUUsage, axWholeCPUUsage = plt.subplots(1,1)
#Change figure settings
figWholeCPUUsage.set_facecolor('#bfbfbf')
figWholeCPUUsage.set_figwidth(6.5)
figWholeCPUUsage.set_figheight(3)
figWholeCPUUsage.set_dpi(100)
#Change axis settings
axWholeCPUUsage.axis(ymin=0, ymax=100, xmin=0, xmax=20)
axWholeCPUUsage.set_facecolor('#bfbfbf')
#Get values for base graph, plot on axes
firstTimexVals = np.arange(20)
firstTimeyVals = []
for a in range(wholeCPUUsageQueue.qsize()):
				firstTimeyVals.append(wholeCPUUsageQueue.get(a))
				wholeCPUUsageQueue.put(firstTimeyVals[a])
axWholeCPUUsage.plot(firstTimexVals, firstTimeyVals)

#Makes canvas on which the figure is drawn, places in tk instance
fctaWholeCPUUsage = FigureCanvasTkAgg(figWholeCPUUsage, root)
fctaWholeCPUUsage.draw()
fctaWholeCPUUsage.get_tk_widget().place(x=0,y=44)

#Method used by worker to update figure values
def updateWholeCPUUsage(wholeCPUUsageQueue, wholeCPUUsageFlagQueue):
	while True:
		if (wholeCPUUsageFlagQueue.qsize() == 0):
			temp = wholeCPUUsageQueue.get(0)
			newUsage = CPUInfo.getWholeCPULoad()
			wholeCPUUsageQueue.put(newUsage)
			wholeCPUUsageFlagQueue.put(True)
		else:
			time.sleep(1)

#Method used by worker thread to display new figure
def displayWholeCPUUsage(wholeCPUUsageQueue, wholeCPUUsageFlagQueue, axWholeCPUUsage, fctaWholeCPUUsage):
	while True:
		xVals = np.arange(20)
		if (wholeCPUUsageFlagQueue.qsize() != 0):
			#Get y values
			yVals = []
			for a in range(wholeCPUUsageQueue.qsize()):
				#Since .get() removes from queue, I need to add back instantly
				yVals.append(wholeCPUUsageQueue.get(a))
				wholeCPUUsageQueue.put(yVals[a])
			#Clear current plot
			axWholeCPUUsage.clear()
			#Plot new values
			axWholeCPUUsage.plot(xVals,yVals)
			#Set axis settings
			axWholeCPUUsage.axis(ymin=0, ymax=100, xmin=0, xmax=20)
			axWholeCPUUsage.set_facecolor('#bfbfbf')
			#Recreate FCTA, clear renderer, place again -- no clue why it works but it does
			fctaWholeCPUUsage = FigureCanvasTkAgg(figWholeCPUUsage, root)
			fctaWholeCPUUsage.get_renderer().clear()
			fctaWholeCPUUsage.get_tk_widget().place(x=0,y=44)
			#Clear flag that signifies display update is needed
			temp = wholeCPUUsageFlagQueue.get(0)
		else:
			time.sleep(0.2)

#Create worker threads
figWholeCPUUsageUpdater = threading.Thread(target=updateWholeCPUUsage, args=(wholeCPUUsageQueue, wholeCPUUsageFlagQueue))
figWholeCPUUsageUpdater.setDaemon(True)
figWholeCPUUsageDisplayer = threading.Thread(target=displayWholeCPUUsage, args=(wholeCPUUsageQueue, wholeCPUUsageFlagQueue, axWholeCPUUsage, fctaWholeCPUUsage))
figWholeCPUUsageDisplayer.setDaemon(True)

#Start worker threads
figWholeCPUUsageUpdater.start()
figWholeCPUUsageDisplayer.start()


root.mainloop()
