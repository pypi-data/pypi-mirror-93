import numpy as np
from . import Globals
import DateTimeTools as TT
import PyFileIO as pf

def _RemoveHeader(lines):
	'''
	Remove the header from the file and find the column labels.
	
	Inputs
	======
	lines : numpy.ndarray
		Numpy array of strings from the file
	
	Returns
	=======
	columnstr : str
		String containing the column names
	lines : numpy.ndarray
		Array of strings containing just the data
	
	'''
	nl = lines.size
	for i in range(0,nl):
		if lines[i][0:6] == '<year>':
			columnstr = lines[i]
			lines = lines[i+1:]
			break
	return columnstr,lines
	
def _NameColumns(columnstr):
	'''
	Return a list of the column names contained in the file.
	
	Inputs
	======
	columnstr : str
		String contaiing the names of the columns in theformat of the SM
		data file
	
	
	Returns
	=======
	columns : str
		Array of column names
	'''
	
	#remove unwanted characters
	s = columnstr.replace('<','').replace('>','').replace('(nT)','').replace('(deg.)','').replace('(hrs)','').replace(' ','').replace('\n','')
	
	#separate
	columns = s.split('\t')
	
	return columns


def _DataDict(columns,lines):
	'''
	Create a dictionary from the text.
	
	Inputs
	======
	colums : str
		Array of strings containing the names of the fields stored in
		the file.
	lines : numpy.ndarray
		Lines from the file only containing data.
	
	Returns
	=======
	data : dict
		Dictionary containing data.
	'''
	
	#convert the lines of ascii to a 2D array of floats
	flts = np.array([np.float32(l.split('\t')) for l in lines])
	
	#change bad values ot NaN
	bad = np.where(flts > 999990)
	flts[bad] = np.nan
	
	#now add to the dictionary
	dct = {}
	
	for i,c in enumerate(columns):
		if c in ['year', 'month', 'day','hour', 'min', 'sec',]:
			dct[c] = np.int32(flts[:,i])
		else:
			dct[c] = flts[:,i]
	return dct
	
def _DataRecarray(dct):
	'''
	Convert the data dictionary to a nice numpy.recarray
	
	Inputs
	======
	dct : dict
		Dictionary containing data
		
	Returns
	=======
	data : numpy.recarray
		
	
	'''

	#date and time first
	Date = TT.DateJoin(dct['year'],dct['month'],dct['day'])
	ut = TT.HHMMtoDec(dct['hour'],dct['min'],dct['sec'])
	utc = TT.ContUT(Date,ut)
	
	#create output recarray
	data = np.recarray(Date.size,dtype=Globals.idtype)
	data.fill(np.nan)
	
	#fill in the date and time fields
	data.Date = Date
	data.ut = ut
	data.utc = utc
	
	#now fill in the other fields
	cols = list(dct.keys())
	names = data.dtype.names
	for c in cols:
		if c in names:
			data[c] = dct[c]
		elif 'r' in c:
			a,b = c.split('r')
			a = a + 'r'
			
			if a in names:
				b = np.int32(b)
				data[a][:,b] = dct[c]

	return data
	
def ReadSMIFile(fname):
	'''
	This function will attempt to read the contents of a SuperMAG index
	data file. For best results when downloading SM indices, please 
	select the following options: SME U/L, SME, SME MLT, SME MLAT, 
	SME LT, SMU LT, SML LT, SMR, SMR LT
	
	Place the downloaded file into SMINDEX_PATH/download/
	
	Inputs
	======
	fname : str
		The full name and path to the file.
	
	Returns
	=======
	data : numpy.recarray
		Record array containing data (see Globals.idtype for field info)
	success : bool
		True or False, depending on whether reading the file was 
		successful.
	
	'''
	
	#set success to False
	success = False
	
	try:
		#read the file in
		lines = pf.ReadASCIIFile(fname)

		#extract data and column header
		columns,lines = _RemoveHeader(lines)

		#split column names
		columns = _NameColumns(columns)

		#get data dictionary
		dct = _DataDict(columns,lines)

		#convert to recarray
		data = _DataRecarray(dct)

		success = True
	except:
		print('Reading file failed: {:s}'.format(fname))
		data = np.recarray(0,dtype=Globals.idtype)
	
	return data,success
