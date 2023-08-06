import numpy as np
import os

#try and find the SMINDEX_PATH variable - this is where data will be stored
ModulePath = os.path.dirname(__file__)+'/'
try:
	DataPath = os.getenv('SMINDEX_PATH')+'/'
	
	#if this is successful - now check whether the subdirectories exist
	dlddir = DataPath + 'download/'
	bindir = DataPath + 'binary/'
	tmpdir = DataPath + 'temp/'
	subdir = DataPath + 'substorms/'
	if not os.path.isdir(dlddir):
		os.system('mkdir -pv '+dlddir)
	if not os.path.isdir(bindir):
		os.system('mkdir -pv '+bindir)
	if not os.path.isdir(tmpdir):
		os.system('mkdir -pv '+tmpdir)
	if not os.path.isdir(subdir):
		os.system('mkdir -pv '+subdir)
except:
	print('Please set SMINDEX_PATH environment variable')
	DataPath = ''

#this is the data type for the recarray which will store the indices
#The regional SME,SMU,SML indices are centred on a 3-hour MLT range 
#equal to the index + 0.5 - i.e. SMEr[12] corresponds to 11:00 - 14:00 MLT)
#Regional versions of SMR are centered on a 6 hour MLT window, 
#i.e. SMR00 corresponds to 21:00 to 03:00 MLT
idtype = [	('Date','int32'),			#Date in the format yyyymmdd
			('ut','float32'),			#Time in hours since the start of the day
			('utc','float64'),			#Continuous time since 1950 (in hours)
			('SME','float32'),			#Global SME index
			('SML','float32'),			#Global SML index
			('SMU','float32'),			#Global SMU index
			('MLTSML','float32'),			#Global SML index MLT
			('MLTSMU','float32'),			#Global SMU index MLT
			('MLATSML','float32'),			#Global SML index Latitude
			('MLATSMU','float32'),			#Global SMU index Latitude
			('SMEr','float32',(24,)),	#Regional SME index 
			('SMLr','float32',(24,)),	#Regional SML index
			('SMUr','float32',(24,)),	#Regional SMU index
			('SMR','float32'),			#Global SMR index
			('SMR00','float32'),		#SMR near midnight
			('SMR06','float32'),		#SMR near dawn
			('SMR12','float32'),		#SMR near noon
			('SMR18','float32')]		#SMR near dusk
			
#this dtype is to store the substorm lists
sdtype = [	('Date','int32'),			#Date in the format yyyymmdd
			('ut','float32'),			#Time in hours since the start of the day
			('utc','float64'),			#Continuous time since 1950 (in hours)
			('MLT','float32'),			#Magnetic Local Time
			('MLat','float32'),			#Mag latitude
			('GLon','float32'),			#Geo Longitude
			('GLat','float32'),			#Geo Latitude
			('Source','U6')]			#Substorm list it came from:
										#	NG2011 - Newell and Gjerloev 2011
										#	F2015 - Forsyth 2015
										#	OG2020 - Ohtani and Gjerloev 2020
										#	F04F06 - Frey et al 2004 and 2006
										#	L2010 - Liou 2010

#this is where the substorm list will be stored in memory
Substorms = None
