# scamp astrometry for astrometry.net result file
# first version 2020.3.18 Changsu Choi
# function scamp_net(i) 2020.3.26
# header remove astrometry.net head and add scamp .head 2020.3.26 
# refering to
# https://github.com/mommermi/2017Spring_Astroinformatics
# To do : 



import os
import astropy.io.fits as fits
import glob
import astropy.io.ascii as ascii
import subprocess

codedirec   = '/data7/changsu/code/astrom/astromtest/'
seconfig    = codedirec+'astrom.sex'
separam     = codedirec+'astrom.par'
scampconfig = codedirec+'astrom.scamp'

# input file name
#i = 'Calibrated-LOAO-NGC3367-20180707-034519-R-60.fits'
#i = 'Calibrated-MCD30inch-NGC3367-20181220-115218-R-60.fits'

os.system('ls *.fits')
#imlist		= glob.glob(input('image to process\t: '))
imlist		= glob.glob('Calib*.fits')
imlist.sort()
for img in imlist: print(img)

def scamp_net(i):
	newname='sa'+i
	os.system('cp '+i+' '+newname)
	iname = i.split('.')[0] 
	# source extractor
	secom = 'sex '+i+' -c '+seconfig+' -PARAMETERS_NAME '+separam+' -CATALOG_NAME '+iname+'.ldac'
	seout = subprocess.getoutput(secom)

	line1 = [s for s in seout.split('\n') if 'RMS' in s]
	line2 = [s for s in seout.split('\n') if 'Objects: detected' in s]
	# skymed, skysig = float(line1[0].split('Background:')[1].split('RMS:')[0]), float(line1[0].split('RMS:')[1].split('/')[0])
	nobj, nse      = float(line2[0].split('Objects: detected ')[1].split('/')[0]), float(line2[0].split('Objects: detected ')[1].split('sextracted')[1])
	print('sextractor working ...')
	print('detected',nobj,'sextracted',nse)

	# scamp
	print('scamp working ...')
	scampcom='scamp -c '+scampconfig+' '+iname+'.ldac'+' -ASTREF_CATLOG 2MASS' 
	scampout=subprocess.getoutput(scampcom)
	line1=[s for s in scampout.split('\n') if 'cont.' in s]
	contnum = scampout.split(line1[0])[1].split('\n')[1].split(' ')[11]    
	contnum = scampout.split(line1[0])[1].split('\n')[1].split('"')[1].split(' ')[3]
	print('cont.',contnum) 
	# merging header
	print(i, newname)
	newhead = open(iname+'.head', 'r').readlines()
	hdu = fits.open(newname, mode='update', verify='silentfix',
                    ignore_missing_end=True)

	for m in range(len(hdu[0].header)):  
		if hdu[0].header[m] == '--Start of Astrometry.net WCS solution--': 
			n=m 
			print(n) 

	del hdu[0].header[n:]
	for line in newhead:
	        key = line[:8].strip()
	        try:
	            value = float(line[10:30].replace('\'', ' ').strip())
	        except ValueError:
	            value = line[10:30].replace('\'', ' ').strip()
	        comment = line[30:].strip()
	        if key.find('END') > -1:
	            break
	        hdu[0].header[key] = (str(value), comment)

	hdu.flush()
	print(i,' is done.')




#f=open('scamp_net_result.txt','w')
for i in range(len(imlist)) : 
	scamp_net(imlist[i])
	print(i+1, 'of', str(len(imlist)) )
#f.close()
#hdr1.fromTxtFile('astromtest.head')
#hdr1.extend(fits.Header.fromtextfile(iname+'.head'), update=True, update_first=True)
#hdr1.fromtextfile('astromtest.head',update=True,update_first=True)
#fits.writeto('a'+inim,fits.getdata(inim),hdr1)
