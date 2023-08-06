import numpy as np
from .ReadBinary import ReadBinary
from . import Globals

def GetIndices(Year):
	'''
	Read the SuperMAG indices.
	
	Inputs
	======
	Year : int
		This should either be an integer year or a 2 element array-like
		object containing start and end years
		
	Returns
	=======
	data : numpy.recarray
		Object containing SuperMAG indices
	
	'''
	
	#list the years
	if np.size(Year) == 1:
		yrs = np.array([Year]).flatten()
	elif np.size(Year) == 2:
		yrs = np.arange(Year[0],Year[1]+1)
	else:
		yrs = np.array([Years]).flatten()
	ny = yrs.size
	
	#determine the length of the output array
	n = 0
	for i in range(0,ny):
		n += ReadBinary(yrs[i],size=True)
		
	#create the output array
	data = np.recarray(n,dtype=Globals.idtype)
	
	#fill it
	p = 0
	for i in range(0,ny):
		tmp = ReadBinary(yrs[i])
		data[p:p+tmp.size] = tmp
		p += tmp.size
		
	return data
