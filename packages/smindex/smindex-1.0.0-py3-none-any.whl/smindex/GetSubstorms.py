import numpy as np
from . import Globals
from .ReadSubstorms import ReadSubstorms

def GetSubstorms(Date=None):
	'''
	Return a list of substorms
	
	Inputs
	======
	Date : None or int or [int,int]
		If None - all substorms will be returned.
		If a single integer date is suppplied then only substorms 
		from that date will be returned.
		If a 2-element array-like object with start and end dates is 
		supplied then all dates within that range will be returned.
		
	Returns
	=======
	out : numpy.recarray
		Substorm list
	'''
	
	if Globals.Substorms is None:
		Globals.Substorms = ReadSubstorms()
	
	out = Globals.Substorms
	
	if Date is None:
		pass
	elif np.size(Date) == 1:
		use = np.where(out.Date == Date)[0]
		out = out[use]
	elif np.size(Date) == 2:
		use = np.where((out.Date >= Date[0]) & (out.Date <= Date[1]))[0]
		out = out[use]
	
	return out
