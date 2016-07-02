# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 13:44:19 2016

@author: Bora
"""
import numpy as np
from netCDF4 import Dataset
nc=Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/03.nc','r')
def mean(time_0,x,y,n,set_point):# n is the periods in a day.
    """
        This next section extracts the data from the global_temperature.nc dataset which is the file downloaded
        from ERA-interim's website.  It initially prints out the variables, units, and their shapes.  Then extracts
        their longitute and latitude, and time variables.
    """
    for i in nc.variables:
            print ([i,nc.variables[i].units,nc.variables[i].shape])
    long = np.array(nc.variables['longitude'][:],dtype=np.float32) #Defining the variables in the netcdf file and assigning them 
    lats = np.array(nc.variables ['latitude'][:],dtype=np.float32)
    time = np.array(nc.variables ['time'][:],dtype=np.float32)
    """
        This section is here to define some of the input parameters.  'time_0' is an input variable for the mean
        function that represents the initial starting year of the dataset being used.  'x', and 'y' are the time
        periods that want to be analyzed.  It is there to create a subset of the dataset at hand.  'n' represents 
        the number of temperature values there are in a certain day.
    """

    x_new=((x%time_0)*(n*365)) #Finding the number of years from the base data (which is from 1996-2015)
    y_new=((y%time_0)*(n*365))
    number_of_years=y-x
    time_period=time[x_new:y_new] # Creating an array with the time period specified
    temperature = np.array(nc.variables['temp'][x_new:y_new][:][:],dtype=np.float32)
    
    temperature_new= np.empty((len(time_period)/n, len(lats),len(long)), dtype=np.float32)
    for i in range(len(temperature_new)):   
        temperature_new[i]= (np.sum(temperature[(i*n):((i+1)*n)],axis=0))/4
    temperature_mean=np.empty((365,len(lats),len(long)), dtype=np.float32)
    for i in range(365):
        for j in range(number_of_years):
            temperature_mean[i]= temperature_new[i+365*j]+temperature_mean[i]
    temperature_mean=temperature_mean/number_of_years
    temperature_mean = np.subtract(temperature_mean,(273.16+set_point))
    time_for_mean=np.arange(1,366,1)
    nc.close()
    
    data4mean= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/mean_'+str(set_point)+'.nc', 'w', format='NETCDF4')
    data4mean.close()
    
    data4mean= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/mean_'+str(set_point)+'.nc', 'a')
    
    time= data4mean.createDimension('time', None)
    lat= data4mean.createDimension('lat', 241)
    lon= data4mean.createDimension('lon', 480)
    
    times= data4mean.createVariable('time','f4',('time',))
    latitudes= data4mean.createVariable('latitude','f4',('lat',))
    longitudes=data4mean.createVariable('longitude','f4',('lon',))
    temp= data4mean.createVariable('temp','f4',('time','lat','lon',))
    
    import time
    data4mean.description = 'Mean Temperature values from 1996-2016 excluding February 29th'
    data4mean.source= 'netCDF4 python'
    data4mean.history= 'Created' +time.ctime(time.time())
    latitudes.units= 'degrees north'
    longitudes.units= 'degrees east'
    temp.units = 'K'
    times.units = 'days in a gregorian calendar'
    
    latitudes[:]= lats
    longitudes[:]=long
    times[:]= time_for_mean
    temp[:]= temperature_mean
    data4mean.close()
    
    new_data= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/mean_'+str(set_point)+'.nc', 'r')
    for i in new_data.variables:
        print([i,new_data.variables[i].units,new_data.variables[i].shape])
    new_data.close()
from netCDF4 import Dataset
def max(time_0,x,y,n,set_point):# n is the periods in a day.
    nc=Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/03.nc','r')
    for i in nc.variables:
            print ([i,nc.variables[i].units,nc.variables[i].shape])
    long = np.array(nc.variables['longitude'][:],dtype=np.float32) #Defining the variables in the netcdf file and assigning them 
    lats = np.array(nc.variables ['latitude'][:],dtype=np.float32)
    time = np.array(nc.variables ['time'][:],dtype=np.float32)

    x_new=((x%time_0)*(n*365)) #Finding the number of years from the base data (which is from 1996-2015)
    y_new=((y%time_0)*(n*365))
    number_of_years=y-x
    time_period=time[x_new:y_new] # Creating an array with the time period specified
    temperature = np.array(nc.variables['temp'][x_new:y_new][:][:],dtype=np.float32)
    
    temperature_new= np.empty((len(time_period)/n, len(lats),len(long)), dtype=np.float32)
    for i in range(len(temperature_new)):   
        temperature_new[i]= np.max(temperature[(i*n):((i+1)*n)],axis=0)
    temperature_max=np.empty((365,len(lats),len(long)), dtype=np.float32)
    for i in range(365):
        for j in range(number_of_years):
            temperature_max[i]= temperature_new[i+365*j]+temperature_max[i]
    temperature_max=temperature_max/number_of_years
    temperature_max = np.subtract(temperature_max,(273.16+set_point))
    
    time_for_max=np.arange(1,366,1)
    nc.close()
    
    data4max= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/max_'+str(set_point)+'.nc', 'w', format='NETCDF4')
    data4max.close()
    
    data4max= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/max_'+str(set_point)+'.nc', 'a')
    
    time= data4max.createDimension('time', None)
    lat= data4max.createDimension('lat', 241)
    lon= data4max.createDimension('lon', 480)
    
    times= data4max.createVariable('time','f4',('time',))
    latitudes= data4max.createVariable('latitude','f4',('lat',))
    longitudes=data4max.createVariable('longitude','f4',('lon',))
    temp= data4max.createVariable('temp','f4',('time','lat','lon',))
    
    import time
    data4max.description = 'Max Temperature values from 1996-2016 excluding February 29th'
    data4max.source= 'netCDF4 python'
    data4max.history= 'Created' +time.ctime(time.time())
    latitudes.units= 'degrees north'
    longitudes.units= 'degrees east'
    temp.units = 'K'
    times.units = 'days in a gregorian calendar'
    
    latitudes[:]= lats
    longitudes[:]=long
    times[:]= time_for_max
    temp[:]= temperature_max
    data4max.close()
    
    new_data= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/max_'+str(set_point)+'.nc', 'r')
    for i in new_data.variables:
        print([i,new_data.variables[i].units,new_data.variables[i].shape])
    new_data.close()
from netCDF4 import Dataset
def min(time_0,x,y,n,set_point):# n is the periods in a day.
    nc=Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/03.nc','r')
    for i in nc.variables:
            print ([i,nc.variables[i].units,nc.variables[i].shape])
    long = np.array(nc.variables['longitude'][:],dtype=np.float32) #Defining the variables in the netcdf file and assigning them 
    lats = np.array(nc.variables ['latitude'][:],dtype=np.float32)
    time = np.array(nc.variables ['time'][:],dtype=np.float32)

    x_new=((x%time_0)*(n*365)) #Finding the number of years from the base data (which is from 1996-2015)
    y_new=((y%time_0)*(n*365))
    number_of_years=y-x
    time_period=time[x_new:y_new] # Creating an array with the time period specified
    temperature = np.array(nc.variables['temp'][x_new:y_new][:][:],dtype=np.float32)
    
    temperature_new= np.empty((len(time_period)/n, len(lats),len(long)), dtype=np.float32)
    for i in range(len(temperature_new)):   
        temperature_new[i]= np.min(temperature[(i*n):((i+1)*n)],axis=0)
    temperature_min=np.empty((365,len(lats),len(long)), dtype=np.float32)
    for i in range(365):
        for j in range(number_of_years):
            temperature_min[i]= temperature_new[i+365*j]+temperature_min[i]
    temperature_min=temperature_min/number_of_years
    temperature_min = np.subtract(temperature_min,(273.16+set_point))
    time_for_min=np.arange(1,366,1)
    nc.close()
    
    data4min= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/min_'+str(set_point)+'.nc', 'w', format='NETCDF4')
    data4min.close()
    
    data4min= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/min_'+str(set_point)+'.nc', 'a')
    
    time= data4min.createDimension('time', None)
    lat= data4min.createDimension('lat', 241)
    lon= data4min.createDimension('lon', 480)
    
    times= data4min.createVariable('time','f4',('time',))
    latitudes= data4min.createVariable('latitude','f4',('lat',))
    longitudes=data4min.createVariable('longitude','f4',('lon',))
    temp= data4min.createVariable('temp','f4',('time','lat','lon',))
    
    import time
    data4min.description = 'Min Temperature values from 1996-2016 excluding February 29th'
    data4min.source= 'netCDF4 python'
    data4min.history= 'Created' +time.ctime(time.time())
    latitudes.units= 'degrees_north'
    longitudes.units= 'degrees_east'
    temp.units = 'K'
    times.units = 'days in a gregorian calendar'
    
    latitudes[:]= lats
    longitudes[:]=long
    times[:]= time_for_min
    temp[:]= temperature_min
    data4min.close()
    
    new_data= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/min_'+str(set_point)+'.nc', 'r')
    for i in new_data.variables:
        print([i,new_data.variables[i].units,new_data.variables[i].shape])
    new_data.close()
from netCDF4 import Dataset
def two_point_average(time_0,x,y,n,set_point):# n is the periods in a day.
    nc=Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/03.nc','r')
    for i in nc.variables:
            print ([i,nc.variables[i].units,nc.variables[i].shape])
    long = np.array(nc.variables['longitude'][:],dtype=np.float32) #Defining the variables in the netcdf file and assigning them 
    lats = np.array(nc.variables ['latitude'][:],dtype=np.float32)
    time = np.array(nc.variables ['time'][:],dtype=np.float32)

    x_new=((x%time_0)*(n*365)) #Finding the number of years from the base data (which is from 1996-2015)
    y_new=((y%time_0)*(n*365))
    number_of_years=y-x
    time_period=time[x_new:y_new] # Creating an array with the time period specified
    temperature = np.array(nc.variables['temp'][x_new:y_new][:][:],dtype=np.float32)
    
    temperature_new= np.empty((len(time_period)/n, len(lats),len(long)), dtype=np.float32)
    for i in range(len(temperature_new)):   
        temperature_new[i]= (np.min(temperature[(i*n):((i+1)*n)],axis=0)+np.max(temperature[(i*n):((i+1)*n)],axis=0))/2
    temperature_2_point=np.empty((365,len(lats),len(long)), dtype=np.float32)
    for i in range(365):
        for j in range(number_of_years):
            temperature_2_point[i]= temperature_new[i+365*j]+temperature_2_point[i]
    temperature_2_point=temperature_2_point/number_of_years
    temperature_2_point = np.subtract(temperature_2_point,(273.16+set_point))
    time_for_min=np.arange(1,366,1)
    nc.close()
    
    data4_2mean= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/mean_2point_'+str(set_point)+'.nc', 'w', format='NETCDF4')
    data4_2mean.close()
    
    data4_2mean= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/mean_2point_'+str(set_point)+'.nc', 'a')
    
    time= data4_2mean.createDimension('time', None)
    lat= data4_2mean.createDimension('lat', 241)
    lon= data4_2mean.createDimension('lon', 480)
    
    times= data4_2mean.createVariable('time','f4',('time',))
    latitudes= data4_2mean.createVariable('latitude','f4',('lat',))
    longitudes=data4_2mean.createVariable('longitude','f4',('lon',))
    temp= data4_2mean.createVariable('temp','f4',('time','lat','lon',))
    
    import time
    data4_2mean.description = 'Min Temperature values from 1996-2016 excluding February 29th'
    data4_2mean.source= 'netCDF4 python'
    data4_2mean.history= 'Created' +time.ctime(time.time())
    latitudes.units= 'degrees_north'
    longitudes.units= 'degrees_east'
    temp.units = 'K'
    times.units = 'days in a gregorian calendar'
    
    latitudes[:]= lats
    longitudes[:]=long
    times[:]= time_for_min
    temp[:]= temperature_2_point
    data4_2mean.close()
    
    new_data= Dataset('/Users/Bora/Desktop/REU/Bond/DDCode/mean_2point_'+str(set_point)+'.nc', 'r')
    for i in new_data.variables:
        print([i,new_data.variables[i].units,new_data.variables[i].shape])
    new_data.close()


