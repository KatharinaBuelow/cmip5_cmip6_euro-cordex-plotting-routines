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
from dp_cmip_plotting_tools import scatter_plot , scatter_plot_cordex, add_column_for_plot_cmip_cordex, add_column_for_plot_cordex

'''
This program makes scatterplots for different ensembles 
for each scenario and timeslice:
a) CMIP5 and CORDEX
b) CMIP5 and CMIP6
'''
#-------------------
# Select Variable
#------------------

var1_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', '%', (-70,70), 'pro','pro_diff_pr_'],}
#var1_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', 'mm/day', (-1.5,1.5), 'mm', 'diff_pr_'],}

#var2_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', (-2 , 11),('MED','CEU','NEU'),60],}
var2_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', (-2 , 10),('BI','IP','FR','ME','SC','AL','MD','EA'),80],}

#Deuschland
#var1_dict = {'Precipitation':[r'$\Delta$' +' Niederschlag', 'pr', '%', (-60,60), 'pro','pro_diff_pr_'],}
#var2_dict = {'Temperature':[r'$\Delta$' +' Temperatur', 'tas', 'K', (-2 , 10),('deutschland',), 60],}

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
# Make Outputdir and
# Select, if you want to plot CMIP5 & CORDEX or CMIP5 & CMIP6
#
# cmip5-cordex:
#
#plotdir=workdir.replace('py_plotting_cmip_cordex','SCATTER/plots_cordex')
#ensemble='EURO-CORDEX'
#
# cmip5-cmip6:
#
plotdir=workdir.replace('py_plotting_cmip_cordex','SCATTER/plots')
ensemble='CMIP6'

if not os.path.exists(plotdir):
    os.makedirs(plotdir)
print(' ')
print('Output will be stored in : ', plotdir)

#-----------------------------------------------
# nothing needs to be changed below:
#----------------------------------------------
# 

rcp = ['rcp26', 'rcp45', 'rcp85']
ssp = ['ssp126','ssp245','ssp585']

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
        for r in range(len(rcp)):
            print('scenario:', rcp[r],ssp[r])
            for time in range(len(timeslice)):
                print(timeslice[time])
                timen=timeslice[time].replace('_',' ')
                title= rcp[r].upper()+' '+reg.upper()+' '+seas+' '+timeslicep[time]+' - '+timehistp
                print(title)
                # infile, concat dataframe
                FileName5='df_CMIP5_'+seas+'_'+regions[i]+'_'+rcp[r]+'_'+timeslice[time]+'.csv'
                print(FileName5)
                if ensemble == 'EURO-CORDEX':
                    FileName6='df_'+ensemble+'_'+seas+'_'+regions[i]+'_'+rcp[r]+'_'+timeslice[time]+'.csv'
                else: 
                    FileName6='df_'+ensemble+'_'+seas+'_'+regions[i]+'_'+ssp[r]+'_'+timeslice[time]+'.csv'
                print(FileName6)
                InFile5=os.path.join(datadir,FileName5)
                InFile6=os.path.join(datadir,FileName6)
                PlotName='CMIP5_'+ensemble+'_'+var2+'_'+var1+'_'+version+'_'+regions[i]+'_'+seas+'_'+rcp[r]+'_'+ssp[r]+'_'+timeslice[time]+'.png'
                if ensemble == 'EURO-CORDEX':
                    PlotName='CMIP5_'+ensemble+'_'+var2+'_'+var1+'_'+version+'_'+regions[i]+'_'+seas+'_'+rcp[r]+'_'+timeslice[time]+'.png'
                OutFile=os.path.join(plotdir,PlotName)
                if ensemble == 'EURO-CORDEX':
                    df5 = pd.read_csv(InFile5)
                    InData5=add_column_for_plot_cmip_cordex(df5)
                    df6 = pd.read_csv(InFile6)
                    InData6=add_column_for_plot_cordex(df6)
                    df=pd.DataFrame()
                    df=pd.concat([InData6,InData5],axis=0)
                    InData6=pd.DataFrame()
                    InData5=pd.DataFrame()
                else:
                    InData5 = pd.read_csv(InFile5)
                    InData6 = pd.read_csv(InFile6) 
                    df=pd.DataFrame()
                    df=pd.concat([InData6,InData5],axis=0)
                
                x_column=xcoln+timen
                if xcoln == 'diff_pr_':
                    df[x_column]=df[x_column]*86400 # needed to plot mm, data is in kg m-2s-1
                y_column='diff_tas_'+timen
                if ensemble == 'EURO-CORDEX':
                    print('EURO-CORDEX')
                    print(x_column)
                    print(y_column)
                    scatter_plot_cordex(df, x_column, y_column, rcp[r], var1_dict, var2_dict, OutFile, title)
                else:
                    scatter_plot(df, x_column, y_column, rcp[r], ssp[r], var1_dict, var2_dict, OutFile, title)
                    

   

