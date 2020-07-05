import psutil
import numpy as np

def getWholeCPULoad():
	CPULoad = psutil.cpu_percent(interval=None)
	return CPULoad

def getPerCoreCPULoad():
	CPULoad = psutil.cpu_percent(interval=None, percpu=True)
	return CPULoad
