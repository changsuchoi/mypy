import os
from astropy.io import fits

files = glob.glob('Calib*.fits')
files.sort()

def puthdr(inim, hdrkey, hdrval, hdrcomment=''):
	from astropy.io import fits
	hdr		=	fits.getheader(inim)
	fits.setval(inim, hdrkey, value=hdrval, comment=hdrcomment)
	comment     = inim+'\t'+'('+hdrkey+'\t'+str(hdrval)+')'


def dateobs(i):

  dateobsstr=fits.getheader(i)['DATE-OBS']
  if len(dateobsstr) < 12 :
    print(i, 'DATE-OBS string is short, make new string')
    timeobsstr=fits.getheader(i)['TIME-OBS']
    newdateobs=dateobsstr+'T'+timeobsstr
    print(i, newdateobs)
    puthdr(i,'DATE-OBS',newdateobs)
  else : print(i,'is OK.', dateobsstr)



for i in files : dateobs(i)
