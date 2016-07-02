# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 01:54:57 2016

@author: Bora
"""

import numpy as np
from netCDF4 import Dataset
def HDD(set_point):
    mean_data=Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/mean_'+str(set_point)+'.nc','r')
    max_data=Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/max_'+str(set_point)+'.nc','r')
    min_data=Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/min_'+str(set_point)+'.nc','r')
    point2_data=Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/mean_2point_'+str(set_point)+'.nc','r')
    
    long = np.array(mean_data.variables['longitude'][:],dtype=np.float32) #Defining the variables in the netcdf file and assigning them 
    lats = np.array(max_data.variables ['latitude'][:],dtype=np.float32)
    time = np.array(min_data.variables ['time'][:],dtype=np.float32)
    mean_temp = np.array(mean_data.variables ['temp'][:],dtype=np.float32)
    max_temp = np.array(max_data.variables ['temp'][:],dtype=np.float32)
    min_temp = np.array(min_data.variables ['temp'][:],dtype=np.float32)
    point_2_temp= np.array(point2_data.variables ['temp'][:],dtype=np.float32)
    for i in mean_data.variables:
        print([i,mean_data.variables[i].units,mean_data.variables[i].shape])
    
    for i in range (len(time)):
       for j in range (len(lats)):
           for k in range (len(long)):
               if (mean_temp[i][j][k]>0.0):
                   mean_temp[i][j][k] =0.0
               if (max_temp[i][j][k]>0.0):
                   max_temp[i][j][k] =0.0
               if (min_temp[i][j][k]>0.0):
                   min_temp[i][j][k] =0.0
               if (point_2_temp[i][j][k]>0.0):
                   point_2_temp[i][j][k] =0.0
    mean_t2m= np.empty((len(lats),len(long)), dtype=np.float32)
    max_t2m= np.empty((len(lats),len(long)), dtype=np.float32)
    min_t2m= np.empty((len(lats),len(long)), dtype=np.float32)
    point_2_t2m=np.empty((len(lats),len(long)), dtype=np.float32)
    for i in range (365):
        mean_t2m = mean_t2m+mean_temp[i]
        max_t2m = max_t2m+max_temp[i]
        min_t2m = min_t2m+min_temp[i]
        point_2_t2m=point_2_t2m+point_2_temp[i]
    mean_data.close()
    max_data.close()
    min_data.close()
    point2_data.close()
    cmplgrp = Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/HDD_'+str(set_point)+'.nc', mode='w', format='NETCDF3_CLASSIC')
    cmplgrp.close()
    
    cmplgrp = Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/HDD_'+str(set_point)+'.nc','a')
    
    lat= cmplgrp.createDimension('latitude', 241)
    lon= cmplgrp.createDimension('longitude', 480)
    
    latitudes= cmplgrp.createVariable('latitude',np.float32,('latitude',))
    longitudes=cmplgrp.createVariable('longitude',np.float32,('longitude',))
    temp_mean= cmplgrp.createVariable('t2m_mean',np.short,('latitude','longitude',))
    temp_min= cmplgrp.createVariable('t2m_min',np.short,('latitude','longitude',))
    temp_max= cmplgrp.createVariable('t2m_max',np.short,('latitude','longitude',))
    temp_2point=cmplgrp.createVariable('t2m_2point',np.short,('latitude','longitude',))
    
    import time
    cmplgrp.history = 'Created ' + time.ctime(time.time())
    cmplgrp.Conventions = 'CF-1.6'
    
    latitudes.long_name = 'latitude'
    latitudes.units = 'degrees_north'
    
    longitudes.units = 'degrees_east'
    longitudes.long_name='longitude'
    
    temp_mean.long_name = '2 meter mean temperature averages for 20 years'
    temp_mean.units = 'K'
    temp_mean.scale_factor = 1
    temp_mean.add_offset=0
    temp_mean.fill_value=-32767
    temp_mean.missing_value = -32767
    
    temp_min.long_name = '2 meter min temperature averages for 20 years'
    temp_min.units = 'K'
    temp_min.scale_factor = 1
    temp_min.add_offset=0
    temp_min.fill_value=-32767
    temp_min.missing_value = -32767
    
    temp_max.long_name = '2 meter max temperature averages for 20 years'
    temp_max.units = 'K'
    temp_max.scale_factor = 1
    temp_max.add_offset=0
    temp_max.fill_value=-32767
    temp_max.missing_value = -32767
    
    temp_2point.long_name = '2 meter max temperature averages for 20 years'
    temp_2point.units = 'K'
    temp_2point.scale_factor = 1
    temp_2point.add_offset=0
    temp_2point.fill_value=-32767
    temp_2point.missing_value = -32767
    
    latitudes[:]= lats
    longitudes[:]=long
    temp_mean[:]=mean_t2m
    temp_min[:]=min_t2m
    temp_max[:]=max_t2m
    temp_2point[:]=point_2_t2m
    
    
    cmplgrp.close()
    
    


        
