import numpy as np
from .ListFiles import ListFiles
from .ReadSMIFile import ReadSMIFile
import os
from . import Globals
from .ReadBinary import ReadBinary
import RecarrayTools as RT

opts = {	'overwrite' : 'o',
			'skip' : 's',
			'merge' : 'm'}

def ConvertData(files=None,Overwrite='ask'):
	'''
	Convert SuperMAG ASCII files to a binary format which is fast to read
	
	
	'''
	
	#list the files
	if files is None:
		files = ListFiles(Globals.DataPath+'download/')
	else:
		files = np.array([files]).flatten()
		nf = np.size(files)
		exists = np.zeros(nf,dtype='bool')
		for i in range(0,nf):
			exists[i] = os.path.isfile(files[i])
		if not exists.any():
			print('None of these files can be found')
			return
		use = np.where(exists)[0]
		files = files[use]
	nf = files.size
	print('Found {:d} files...'.format(nf))
	
	#read each file in and save as a temp file
	years = []
	tmpnames = np.zeros(nf,dtype='object')
	for i in range(0,nf):
		print('Converting file {0} of {1}'.format(i+1,nf))
		#get the basename
		bname = os.path.basename(files[i])
		
		#output name and path
		tname = Globals.tmpdir + bname + '.bin'
		tmpnames[i] = tname
		
		#convert the data
		data,s = ReadSMIFile(files[i])
		
		#save if successful
		if s:
			RT.SaveRecarray(data,tname,Progress=True)
			
			#store the unique years
			ud = np.unique(data.Date//10000)
			years.append(ud)
		else:
			print('Reading file {:s} failed')
			years.append(np.array([]))

	#list existing year files
	_,efiles = ListFiles(Globals.bindir,ReturnNames=True)
	eyears = np.array([np.int32(e[:4]) for e in efiles])
		
	#get the list of years in the new files
	nyears = np.concatenate(years)
	uyears,cyears = np.unique(nyears,return_counts=True)
		
	#now to either merge/replace/skip with existing files
	for i in range(0,uyears.size):
		print('Combining year {:04d}'.format(uyears[i]))
		#look for new files with the same years
		use = np.zeros(nf,dtype='bool')
		for j in range(0,nf):
			use[j] = uyears[i] in years[j]
		use = np.where(use)[0]
		
		#count up the number of records
		n = 0
		for j in range(0,use.size):
			n += ReadBinary(tmpnames[use[j]],size=True)
		
		#create recarray
		ndata = np.recarray(n,dtype=Globals.idtype)
		
		#fill it
		p = 0
		for j in range(0,use.size):
			tmp = ReadBinary(tmpnames[use[j]])
			ndata[p:p+tmp.size] = tmp
			p += tmp.size
		
		oname = Globals.bindir + '{:04d}.bin'.format(uyears[i])
		
		#check if this date exists in binary folder already
		if uyears[i] in eyears:
			okeys = list(opts)
			oopts = ['o','s','m']
			if Overwrite in okeys:
				opt = opts[Overwrite]
			elif Overwrite in oopts:
				opt = Overwrite
			else:
				#ask
				opt = ''
				while not opt in oopts:
					print('Data already exists for the year {:04d}'.format(uyears[i]))
					opt = input('merge/skip/overwrite? (m/s/o): ')
			
			if opt == 'o':
				srt = np.argsort(ndata.utc)
				ndata = ndata[srt]
				RT.SaveRecarray(ndata,oname,Progress=True)
			elif opt == 'm':
				edata = ReadBinary(uyears[i])
				
				data = RT.JoinRecarray(ndata,edata)
				srt = np.argsort(data.utc)
				data = data[srt]
				
				_,ind = np.unique(data.utc,return_index=True)
				data = data[ind]
				
				RT.SaveRecarray(data,oname,Progress=True)
		else:
			srt = np.argsort(ndata.utc)
			ndata = ndata[srt]
			RT.SaveRecarray(ndata,oname,Progress=True)
			
	#remove temp files
	for t in tmpnames:
		os.system('rm -v '+t)
			
