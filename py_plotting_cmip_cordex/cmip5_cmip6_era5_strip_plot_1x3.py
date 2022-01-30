#! /usr/bin/python
# coding: utf-8
import numpy as np
import glob
import matplotlib.pyplot as plt
import subprocess
import os
from matplotlib import markers
import pandas as pd
import seaborn as sns
from dp_cmip_plotting_tools import strip_plot_historical, sub_era

#-------------------
# Select Variable
#------------------

#var_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', '%', 
#                             (-100,100),('NEU','CEU','MED') ,'pro_diff_pr', 'Precipitation'],}
var_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', 'mm/day', 
                             (-2.2,2.2), ('NEU','CEU','MED'), 'diff_pr','Precipitation'],}
#var_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', 
#                           (-10 , 10),('NEU','CEU','MED'),'diff_tas', 'Temperatur','my_t']}

print(os.getcwd())
workdir=os.getcwd()
#-------------------------------------------
# Select input data and output directory
#-------------------------------------------
#
# This program requires, that the data files exist
# which can be calculated with Creat_df_for_plots.py
#
era5dir=workdir.replace('py_plotting_cmip_cordex','HEATMAP/data/ERA5/')
datadir=workdir.replace('py_plotting_cmip_cordex','SCATTER/data')
print(' ')
print('datafile is read from: ', datadir)
print('ERA5 datafile is read from: ', era5dir)
#
# Make Outputdir
#
plotdir=workdir.replace('py_plotting_cmip_cordex','STRIPPLOT/plots_historical')
if not os.path.exists(plotdir):
    os.makedirs(plotdir)
print(' ')
print('Output will be stored in : ', plotdir)

#-----
# collect, what you want to plot '''
#-----
mip=['CMIP5','CMIP6'] #,'EURO-CORDEX']
timehist  =  '1981-01-01_to_2010-12-31'
timehistp  =  '(1981 to 2010)'
seasons = ('JJA','DJF','ANN', 'MAM', 'SON')
sce =('historical',)


#-----------------------------------------------
# nothing needs to be changed below:
#----------------------------------------------
# Variable 
for parameter in var_dict.keys():
    var = var_dict[parameter][1]
    einheit = var_dict[parameter][2]
    regions=var_dict[parameter][4]
    ycoln = var_dict[parameter][5]
    titlevar = var_dict[parameter][6]
    print('regions: ',regions)
                                 
for i in range(len(regions)):
    print('region: ',regions[i])
    df=pd.DataFrame()
    for m in range(len(mip)):
        print(m)
        for s in range(len(seasons)):
            timean=timehist.replace('_',' ')    
            # infile, concat dataframe
            FileName='df_'+mip[m]+'_'+seasons[s]+'_'+regions[i]+'_'+sce[0]+'_'+timehist+'.csv'
            InFile=os.path.join(datadir,FileName)
            InData = pd.read_csv(InFile)
            df=pd.concat([df,InData],axis=0)
        
    dfname='df_'+regions[i]
    if dfname == 'df_NEU':
        df_NEU=sub_era(df,era5dir,'NEU',timehist)
        print(dfname,' : ',df_NEU.shape)
    if dfname == 'df_CEU':
        df_CEU=sub_era(df,era5dir,'CEU',timehist)
        print(dfname,' : ',df_CEU.shape)
    if dfname == 'df_MED':
        df_MED=sub_era(df,era5dir,'MED',timehist)
        print(dfname,' : ',df_MED.shape)

dataframes=[df_NEU,df_CEU,df_MED]        
title= timehistp+' '+titlevar +' Bias to ERA5'
PlotName=ycoln+'_SREX_'+timehist+'_cmip-era5.png'
OutFile=os.path.join(plotdir,PlotName)
OutDataFile=os.path.join(plotdir.replace('plots','data'),PlotName.replace('png','csv'))
#-------------
# make plot:
#---------------
print('das wird gelesen')
print(df_NEU)
strip_plot_historical(dataframes, ycoln, var_dict, OutDataFile, OutFile, title)
       
           

