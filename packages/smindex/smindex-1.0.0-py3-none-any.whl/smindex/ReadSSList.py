import numpy as np
from . import Globals
import PyFileIO as pf
import DateTimeTools as TT

def _RemoveSSHeader(lines):
	'''
	Remove the header from the file and find the column labels.
	
	Inputs
	======
	lines : numpy.ndarray
		Numpy array of strings from the file
	
	Returns
	=======
	lines : numpy.ndarray
		Array of strings containing just the data
	source : str
		String which denotes which method these substorms are from
	
	'''
	#find the data and the header
	nl = lines.size
	for i in range(0,nl):
		if lines[i][0:6] == '<year>':
			header = lines[:i]
			lines = lines[i+1:]
			break
	
	#scan the header for the following names
	auths = {	'Frey' : 'F04F06',
				'Othani' : 'OG2020',
				'Newell' : 'NG2011',
				'Liou' : 'L2010',
				'Forsyth' : 'F2015' }
	keys = list(auths.keys())
	source = ''
	for h in header:
		for k in keys:
			if k in h:
				source = auths[k]
				break
		if source != '':
			break
			
	
	return lines,source
	

def ReadSSList(fname):
	'''
	Reads a substorm list provided by SuperMAG
	
	Inputs
	======
	fname : str
		Name and full path of file to read
	
	Returns
	=======
	data : numpy.recarray
		Substorm list
	
	'''
	
	#firstly read in the file
	lines = pf.ReadASCIIFile(fname)
	
	#remove the header
	lines,source = _RemoveSSHeader(lines)
	n = lines.size
	
	#now create output recarray
	data = np.recarray(n,dtype=Globals.sdtype)
	
	#separate each line
	s = np.array([l.split() for l in lines])
	
	#get dates and times
	yr = np.int32(s[:,0])
	mn = np.int32(s[:,1])
	dy = np.int32(s[:,2])
	hh = np.int32(s[:,3])
	mm = np.int32(s[:,4])
	data.Date = TT.DateJoin(yr,mn,dy)
	data.ut = TT.HHMMtoDec(hh,mm)
	data.utc = TT.ContUT(data.Date,data.ut)
	
	#fill the rest of the fields
	data.Source[:] = source
	data.MLT = np.float32(s[:,5])
	data.MLat = np.float32(s[:,6])
	data.GLon = np.float32(s[:,7])
	data.GLat = np.float32(s[:,8])

	return data
