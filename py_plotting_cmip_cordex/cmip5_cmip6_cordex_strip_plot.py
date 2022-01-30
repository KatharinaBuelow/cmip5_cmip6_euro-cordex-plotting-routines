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
from dp_cmip_plotting_tools import strip_plot_cc

#-------------------
# Select Variable
#-------------------

#var_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', '%', (-80,80),
#                             ('NEU','CEU','MED') ,'pro_diff_pr_'],}
#var_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', 'mm/day', (-1.2,1.2), 
#                             ('NEU','CEU','MED'), 'diff_pr_'],}
#var_dict = {'Precipitation':[r'$\Delta$' +' Niederschlag', 'pr', '%', (-60,60),
#                             ('deutschland',) ,'pro_diff_pr_'],}
#var_dict = {'Precipitation':[r'$\Delta$' +' Niederschlag', 'pr', 'mm/day', (-1,1),
#                             ('deutschland',) ,'diff_pr_'],}

#var_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', (-2 , 11),
#                           ('NEU','CEU','MED'),'diff_tas_']}

var_dict = {'Temperature':[r'$\Delta$' +' Temperatur', 'tas', 'K', (-2 , 10),
                           ('deutschland',),'diff_tas_']}

    
print(os.getcwd())
workdir=os.getcwd()
#-------------------------------------------
# Select input data and output directory
#-------------------------------------------
#
# This program requires, that the data files exist
# which can be calculated with Creat_df_for_plots.py
#
datadir=workdir.replace('py_plotting_cmip_cordex','SCATTER/data')
print(' ')
print('datafile is read from: ', datadir)
#
# Make Outputdir
#
plotdir=workdir.replace('py_plotting_cmip_cordex','STRIPPLOT/plots')
if not os.path.exists(plotdir):
    os.makedirs(plotdir)
print(' ')
print('Output will be stored in : ', plotdir)

#-----------------------------------------------
# nothing needs to be changed below:
#----------------------------------------------
mip=['CMIP5','CMIP6','EURO-CORDEX']
timehist  =  '1981-01-01_to_2010-12-31'
timeslice = ['2036-01-01_to_2065-12-31',
	     '2070-01-01_to_2099-12-31',
             ]
timehistp  =  '(1981 to 2010)'
timeslicep = ['(2036 to 2065)',
              '(2070 to 2099)',
              ]
    
seasons = ('JJA','DJF','ANN', 'MAM', 'SON')

# Variable 
for parameter in var_dict.keys():
    var = var_dict[parameter][1]
    einheit = var_dict[parameter][2]
    regions=var_dict[parameter][4]
    ycoln = var_dict[parameter][5]
                                
for seas in seasons:
    print(seas)
    for time in range(len(timeslice)):
        print(timeslice[time])
        for i in range(len(regions)):
            print('region: ',regions[i])
            df=pd.DataFrame()
            for m in range(len(mip)):
                if mip[m] != 'CMIP6':
                    sce = ['rcp26','rcp45','rcp85']
                else:
                    sce = ['ssp126','ssp245','ssp370','ssp585']
                for r in range(len(sce)):
                    print('scenario:', sce[r])
                    timean=timeslice[time].replace('_',' ')    
                    # infile, concat dataframe
                    FileName='df_'+mip[m]+'_'+seas+'_'+regions[i]+'_'+sce[r]+'_'+timeslice[time]+'.csv'
                    print(FileName)
                    InFile=os.path.join(datadir,FileName)
                    InData = pd.read_csv(InFile)                
                    df=pd.concat([df,InData],axis=0)
                y_column=ycoln+timean
            if ycoln == 'diff_pr_':
                df[y_column]=df[y_column]*86400 # needed to plot mm, data is in kg m-2s-1
            dfname='df_'+regions[i]
            # There is definitly a better method, which I just do not know at the moment:
            print(df.shape)
            if dfname == 'df_deutschland':
                dataframes=[df,] 

            if dfname == 'df_NEU':
                df_NEU=df
                print(dfname,' : ',df_NEU.shape)
            if dfname == 'df_CEU':
                df_CEU=df
                print(dfname,' : ',df_CEU.shape)
            if dfname == 'df_MED':
                df_MED=df
                print(dfname,' : ',df_MED.shape)
        if dfname == 'df_deutschland':
            dataframes=[df,]
            PlotName=ycoln+'deutschland_'+seas+'_'+timeslice[time]+'_cmip+cordex.png'
        else:
            dataframes=[df_NEU,df_CEU,df_MED]   
            PlotName=ycoln+'SREX_'+seas+'_'+timeslice[time]+'_cmip+cordex.png'
        title= seas+' '+timeslicep[time]+' - '+timehistp
        print(title)
        OutFile=os.path.join(plotdir,PlotName)
        strip_plot_cc(dataframes, y_column, var_dict, OutFile, title)

    
   

