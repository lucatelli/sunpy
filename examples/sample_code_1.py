#!/usr/bin/env python
"""  A very simple examle script to download, open, and plot an image
     from the Illustris Image host site.

     Author:  P. Torrey (ptorrey@mit.edu) 1/24/15

     Update:  P. Torrey (ptorrey@mit.edu) 6/21/15 
		w/ suggestions from Geferson Lucatelli and Connor Bottrell
"""

import numpy as np
import os
# The two lines below make it possible for people to sit in the examples directory and run the scripts.
import sys
sys.path.append('../..')
import sunpy.sunpy__load as sunpy__load		# 
import sunpy.sunpy__plot as sunpy__plot


my_api = "enter your own api key here !!!"
dl_base='http://www.illustris-project.org'

try:
    # Depending on the NumPy version, the line below can raise a TypeError even if the file is
    # present.  The try/except block enables us to try loadtxt calls that work for more NumPy
    # versions.
    try: 
        catalog = np.loadtxt('directory_catalog_135.txt',
                             dtype={'names'  : ('subdirs', 'galaxy_numbers', 'galaxy_masses'),
                                    'formats': ('S3', 'i10', 'f8')})
    except TypeError:
        catalog = np.loadtxt('directory_catalog_135.txt',
                             dtype={'names'  : ('subdirs', 'galaxy_numbers', 'galaxy_masses'),
                                    'formats': ('S3', 'i8', 'f8')})
except IOError:  
    # If we don't already have the file, we have to download it and try again.
    os.system("wget "+dl_base+"/files/directory_catalog_135.txt")
    try:
        catalog = np.loadtxt('directory_catalog_135.txt',
                             dtype={'names'  : ('subdirs', 'galaxy_numbers', 'galaxy_masses'),
                                    'formats': ('S3', 'i10','f8')})
    except TypeError:
        catalog = np.loadtxt('directory_catalog_135.txt',
                             dtype={'names'  : ('subdirs', 'galaxy_numbers', 'galaxy_masses'),
                                    'formats': ('S3', 'i8','f8')})


all_subdirs = catalog['subdirs']
all_galnrs  = catalog['galaxy_numbers']

for index,galnr in enumerate(all_galnrs[:1]):
    cmd = 'wget --content-disposition --header="API-Key: '+my_api+'" "'+dl_base+ \
	'/api/Illustris-1/snapshots/135/subhalos/'+str(galnr)+  \
	'/stellar_mocks/broadband.fits"'
    
    if( not (os.path.isfile("./broadband_"+str(galnr)+".fits")) ):
	os.system(cmd) 
    filename = "./broadband_"+str(galnr)+".fits"

    # retrieve the image.  Could be used for non-parametric fitting, plotting, etc.
    image = sunpy__load.load_broadband_image(filename,band='B_Johnson.res')

    # plot an SDSS gri band idealized image
    sunpy__plot.plot_sdss_gri(filename, savefile='./sdss_gri_'+str(galnr)+'.png')

    os.remove("./"+filename)

