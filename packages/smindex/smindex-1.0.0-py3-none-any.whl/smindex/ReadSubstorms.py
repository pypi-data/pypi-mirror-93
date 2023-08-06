import numpy as np
from . import Globals
import RecarrayTools as RT
import os

def ReadSubstorms():
	'''
	Read the substorm list created by the function "UpdateSubstorms"
	
	Returns
	=======
	data : numpy.recarray
		Data object containing the list of substorms
	
	'''
	#get the file name
	fname = Globals.DataPath + 'Substorms.bin'	
	
	#check it exists
	if not os.path.isfile(fname):
		print('No substorm list found - please run smindex.UpdateSubstorms()')
		return None
	
	return RT.ReadRecarray(fname,Globals.sdtype)
	
