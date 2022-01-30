#! /usr/bin/python
# coding: utf-8
import numpy as np
import glob
import matplotlib.pyplot as plt
import subprocess
import os
from matplotlib import markers
from scattertable import scattertable
import pandas as pd
import seaborn as sns
from dp_cmip_plotting_tools import scatter_plot

#-------------------
# Select Variable
#------------------

#var1_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', '%', (-70,70), 'pro','pro_diff_pr_'],}
#var1_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', 'mm/day', (-1.5,1.5), 'mm', 'diff_pr_'],}
#deutsch
var1_dict = {'Precipitation':[r'$\Delta$' +' Niederschlag', 'pr', '%', (-70,70), 'pro','pro_diff_pr_'],}
#var2_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', (-2 , 11),('MED','CEU','NEU'),60],}
var2_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', (-2 , 10),('BI','IP','FR','ME','SC','AL','MD','EA'),80],}
#var2_dict = {'Temperature':[r'$\Delta$' +' Temperatur', 'tas', 'K', (-2 , 10),('deutschland',), 80],}

#-----------------------------------------
#  collect, what you want to plot '''
#----------------------------------------
sce = ['rcp26','rcp45','rcp85']
#sce = ['ssp119','ssp126','ssp245','ssp370','ssp434','ssp460','ssp585']
mip='CMIP5'
#mip='CMIP6'


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
plotdir=workdir.replace('py_plotting_cmip_cordex','SCATTER/plots_all_scenarios')
if not os.path.exists(plotdir):
    os.makedirs(plotdir)
print(' ')
print('Output will be stored in : ', plotdir)

#----------------------------------------------
# nothing needs to be changed after this
#----------------------------------------------

timehist  =  '1981-01-01_to_2010-12-31'
timeslice = ['2036-01-01_to_2065-12-31',
	     '2070-01-01_to_2099-12-31',
             ]
timehistp  =  '(1981 to 2010)'
timeslicep = ['(2036 to 2065)',
	      '(2070 to 2099)',
              ]
    
seasons = ('JJA','DJF','ANN', 'MAM', 'SON')

# Variable 1 pr
for parameter in var1_dict.keys():
    var1 = var1_dict[parameter][1]
    einheit1 = var1_dict[parameter][2]
    version = var1_dict[parameter][4]
    xcoln = var1_dict[parameter][5]

# Variable 2 tas
for parameter in var2_dict.keys():
    var2 = var2_dict[parameter][1]
    einheit2 = var2_dict[parameter][2]
    regions=var2_dict[parameter][4]
    print('regions: ',regions)

for i in range(len(regions)):
    print('region: ',regions[i])
    reg=regions[i]
    reg=reg.replace('CEU','WCE')
    for seas in seasons:
        print('season:',seas)
        for time in range(len(timeslice)):
            print(timeslice[time])
            df=pd.DataFrame()
            for r in range(len(sce)):
                print('scenario:', sce[r])
                timen=timeslice[time].replace('_',' ')
                title= reg.upper()+' '+seas+' '+timeslicep[time]+' - '+timehistp
                print(title)
                # infile, concat dataframe
                FileName='df_'+mip+'_'+seas+'_'+regions[i]+'_'+sce[r]+'_'+timeslice[time]+'.csv'
                print(FileName)
                InFile=os.path.join(datadir,FileName)
                PlotName=mip+'_'+var2+'_'+var1+'_'+version+'_'+regions[i]+'_'+seas+'_'+timeslice[time]+'.png'
                OutFile=os.path.join(plotdir,PlotName)
                InData = pd.read_csv(InFile)                
                df=pd.concat([df,InData],axis=0)
            PlotName='test.png'
            x_column=xcoln+timen
            if xcoln == 'diff_pr_':
                df[x_column]=df[x_column]*86400 # needed to plot mm, data is in kg m-2s-1
            y_column='diff_tas_'+timen
            scatter_plot(df, x_column, y_column,'all','all', var1_dict, var2_dict, OutFile, title)
                    
