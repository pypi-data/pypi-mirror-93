import numpy as np
from .ListFiles import ListFiles
from . import Globals
import RecarrayTools as RT
import os
from .ReadSSList import ReadSSList
from .ReadSubstorms import ReadSubstorms


def UpdateSubstorms():
	'''
	Update the list of substorms stored in $SMINDEX_PATH/Substorms.bin
	
	'''
	
	#list the files
	files = ListFiles(Globals.subdir)
	nf = files.size
	print('Found {:d} files...'.format(nf))
	
	#read each file
	tmpdata = []
	n = 0
	for i in range(0,nf):
		print('Reading file {0} of {1}'.format(i+1,nf))
		try:
			tmp = ReadSSList(files[i])
			tmpdata.append(tmp)
			n += tmp.size
		except:
			print('Something went wrong whilst reading file {:s}'.format(files[i]))
	
	#now create the output data object
	print('Found {:d} substorms'.format(n))
	data = np.recarray(n,dtype=Globals.sdtype)
	
	#fill it
	p = 0
	for t in tmpdata:
		data[p:p+t.size] = t
		p += t.size
		
	#check if we have an existing substorm binary
	print('Checking for existing list')
	edata = ReadSubstorms()
	
	if not edata is None:
		print('Combining substorms and removing duplicates')
		#combine objects
		data = RT.JoinRecarray(edata,data)
		print('Total {:d} substorms'.format(n))
		
		#this is a bit hacky, but I don't want to get rid of the subtorms
		#that appear twice in two or more different lists - so I will
		#use a string for each date,time and source
		fmt = '{:08d}-{:6.3f}-{:s}'
		ustr = np.array([fmt.format(data[i].Date,data[i].ut,data[i].Source) for i in range(0,data.size)])
		
		u,i = np.unique(ustr,return_index=True)
		data = data[i]
		
		print('Reduced to {:d} substorms'.format(n))
				
	#sort everything
	srt = np.argsort(data.utc)
	data = data[srt]
		
	#now save it
	fname = Globals.DataPath + 'Substorms.bin'
	print('Saving file {:s}'.format(fname))
	RT.SaveRecarray(data,fname)
