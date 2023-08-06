import numpy as np
import RecarrayTools as RT
from . import Globals


def ReadBinary(f,size=False):
	'''
	Read a binary file containing supermag indices.
	
	Inputs
	======
	f : str or int
		In the case f is and integer - it should be a year and will read
		the saved data file in $SMINDEX_PATH/binary/yyyy.bin
		Otherwise it should be a string containing the full path to a
		specific binary file.
	size : bool	
		If True, only the number of records will be returned.
		
	Returns
	=======
	data : numpy.recarray
	OR
	n : int
	
	
	'''
	
	if isinstance(f,str):
		#specific file
		fname = f
	else:
		#we have a year (in theory)
		fname = Globals.bindir + '{:04d}.bin'.format(f)
	
	#read the data
	if size:
		F = open(fname,'rb')
		out = np.fromfile(F,dtype='int32',count=1)[0]
		F.close()
	else:
		out = RT.ReadRecarray(fname,Globals.idtype)
	
	return out
