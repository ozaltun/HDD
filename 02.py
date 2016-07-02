# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 19:45:45 2016

@author: Bora
"""
"""
    This code is tailored especially for reanalysis data from ERA-Interim.  The code would need to be altered if
    the dataset was going to change.  If bigger datasets are used from ERA-Interim, depending on the number of 
    leap years added the code would need to be changed.  The main idea is taking out the temperature data for 
    February 29th directly, creating a code that is not flexible to change.  It is also important to note that this code is 
    currently incomplete.  The data is extracted but the requrired code for creating a new netCDF file is currently not inside this document.
"""
"""This initial section involves extracting the data from the dataset in hand."""
import numpy as np
from netCDF4 import Dataset
nc=Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/01.nc','r')
for i in nc.variables:
    print ([i,nc.variables[i].units,nc.variables[i].shape])
lons = np.array(nc.variables['longitude'][:],dtype=np.float32)
lats = np.array(nc.variables ['latitude'][:],dtype=np.float32)
time_0 = np.array(nc.variables ['time'][:],dtype=np.float32)
temperature_0 = np.array(nc.variables['t2m'][:],dtype=np.float32)
""" This next section creates an empty array in order for us to be able to reallocate the sections that we want from our original dataset.  The 'for' loops take the sections of the original dataset that don't involve any data for February 29th."""
time_new=np.empty([29200],dtype=np.float32)
temperature_new = np.empty([29200,241,480],dtype=np.float32)
for i in range(236):
    temperature_new[i]=temperature_0[i]
    time_new[i]=time_0[i]
for i in range(236,6076):
    temperature_new[i]=temperature_0[i+4]
    time_new[i]=time_0[i+4]
for i in range(6076,11916):
    temperature_new[i]=temperature_0[i+8]
    time_new[i]=time_0[i+8]
for i in range(11916,17756):
    temperature_new[i]=temperature_0[i+12]
    time_new[i]=time_0[i+12]
for i in range(17756,23596):
    temperature_new[i]=temperature_0[i+16]
    time_new[i]=time_0[i+16]
for i in range(23596,29200):
    temperature_new[i]=temperature_0[i+20]
    time_new[i]=time_0[i+20]

try:nc.close()
except: pass
cmplgrp = Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/03.nc', mode='w', format='NETCDF3_CLASSIC')
cmplgrp.close()

cmplgrp = Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/03.nc','a')

time_1= cmplgrp.createDimension('time', None)
lat= cmplgrp.createDimension('latitude', 241)
lon= cmplgrp.createDimension('longitude', 480)

times= cmplgrp.createVariable('time',np.int32,('time',))
latitudes= cmplgrp.createVariable('latitude',np.float32,('latitude',))
longitudes=cmplgrp.createVariable('longitude',np.float32,('longitude',))
temp= cmplgrp.createVariable('t2m',np.short,('time','latitude','longitude',))
#crs = cmplgrp.createVariable('crs','i4')

import time
cmplgrp.history = 'Created ' + time.ctime(time.time())
cmplgrp.Conventions = 'CF-1.6'

latitudes.long_name = 'latitude'
latitudes.units = 'degrees_north'

longitudes.units = 'degrees_east'
longitudes.long_name='longitude'

times.long_name = 'time'
times.units = 'days since 2000-1-1 0:0:0'
times.calendar='noleap'



temp.long_name = '2 meter temperature averages for 20 years'
temp.units = 'K'
temp.scale_factor = 0.0019682440842811303
temp.add_offset=0
temp.fill_value=-32767
temp.missing_value = -32767


times[:]=times_new
latitudes[:]= lats
longitudes[:]=lons
temp[:]=temperature_new


cmplgrp.close()


