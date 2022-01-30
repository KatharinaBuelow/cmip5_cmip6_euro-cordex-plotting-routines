#! /usr/bin/python
# coding: utf-8
import numpy as np
import glob
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
from dp_cmip_plotting_tools import subtract_era, plot_heatmap_season_1x3


''' plots 3 heatmaps (each SRES region NEU, WCE, MED) for timeslice and variable
collect, what you want to plot '''

#------------------------------
# select variable
#-------------------------------

var_dict = {'Precipitation':['['+r'$\Delta$' +' mm/day'+']', (-1.5,1.5),'PuOr','.1f'],}
#var_dict = {'Temperature':['['+r'$\Delta$' +' Kelvin'+']', (-9,9),'seismic','.1f'],}
#var_dict = {'SNOW':['['+r'$\Delta$' +' mm'+']', (-70,70),'RdBu','.0f'],}
#var_dict = {'Radiation':['['+r'$\Delta$' +' W / m**2'+']', (-50,50),'PiYG_r','.0f'],}

#---------------------------    
# select file dictionary
#--------------------------

#---------------
# CMIP5
#---------------
#file_dict = {'File':['df_' , ('CMIP5','ERA5'),('pr','tp'), ('NEU','CEU','MED'), ('historical','Reanalysis') ,('_1981-01-01_to_2010-12-31_'),'mean precipitation bias [mm/day]','mm',],}
#file_dict = {'File':['df_' , ('CMIP5','ERA5'),('tas','2t'), ('NEU','CEU','MED'), ('historical','Reanalysis') ,('_1981-01-01_to_2010-12-31_'),'mean temperature bias [K]','K',],}
#file_dict = {'File':['df_' , ('CMIP5','ERA5'),('snw','snd'), ('NEU','CEU','MED'), ('historical','Reanalysis') ,('_1981-01-01_to_2010-12-31_'),'mean swe bias [mm]','mm',],}
#file_dict = {'File':['df_' , ('CMIP5','ERA5'),('rsds','ssrd'), ('NEU','CEU','MED'), ('historical','Reanalysis') ,('_1981-01-01_to_2010-12-31_'),'mean radiation (rsds) bias [w/m**2]','w',],}

#----------------------
# CMIP6
#----------------------
file_dict = {'File':['df_' , ('CMIP6','ERA5'),('pr','tp'), ('NEU','CEU','MED'), ('historical','Reanalysis') ,('_1981-01-01_to_2010-12-31_'),'mean precipitation bias [mm/day]','mm',],}
#file_dict = {'File':['df_' , ('CMIP6','ERA5'),('tas','2t'), ('NEU','CEU','MED'), ('historical','Reanalysis') ,('_1981-01-01_to_2010-12-31_'),'mean temperature bias [K]','K',],}
#file_dict = {'File':['df_' , ('CMIP6','ERA5'),('snw','snd'), ('NEU','CEU','MED'), ('historical','Reanalysis') ,('_1981-01-01_to_2010-12-31_'),'mean swe bias [mm]','mm',],}
#file_dict = {'File':['df_' , ('CMIP6','ERA5'),('rsds','ssrd'), ('NEU','CEU','MED'), ('historical','Reanalysis') ,('_1981-01-01_to_2010-12-31_'),'mean radiation (rsds) bias [w/m**2]','w',],}

#--------------------------
# Directory
#--------------------------
print(os.getcwd())
workdir=os.getcwd()
#-------------------------------------------
# Select input data and output directory
#-------------------------------------------
#
# files
for parameter in file_dict.keys():
     df_name = file_dict[parameter][0]
     MIP = file_dict[parameter][1][:]
     var = file_dict[parameter][2][:]      
     timeslice=file_dict[parameter][5]
     reg = file_dict[parameter][3][:]
     sce = file_dict[parameter][4][:]
     vartitel=file_dict[parameter][6]

print(MIP)
# This program requires, that the data files exist
# which can be calculated with Create_df_for_heatmaps.py
#
era5di=workdir.replace('py_plotting_cmip_cordex','HEATMAP/data/ERA5/')
datadi=workdir.replace('py_plotting_cmip_cordex','HEATMAP/data/'+MIP[0]+'/seasonal/')
print(' ')
print('datafile is read from: ', datadi)
#
# Make Outputdir
#
plotdi=workdir.replace('py_plotting_cmip_cordex','HEATMAP/plots_era5')
if not os.path.exists(plotdi):
    os.makedirs(plotdi)
print(' ')
print('Output will be stored in : ', plotdi)


#-----------------------------------------------
# nothing needs to be changed below:
#----------------------------------------------
    
# EURO-CORDEX: dick
model_name=("CNRM-CM5_r1i1p1", "GFDL-ESM2G_r1i1p1", "HADGEM2-ES_r1i1p1",
            "MPI-ESM-LR_r1i1p1", "MPI-ESM-LR_r2i1p1", "MPI-ESM-LR_r3i1p1",
            "NORESM1-M_r1i1p1", "EC-EARTH_r1i1p1",  
            "EC-EARTH_r12i1p1","IPSL-CM5A-LR_r1i1p1","IPSL-CM5A-MR_r1i1p1",
            "CANESM2_r1i1p1", "MIROC5_r1i1p1",
            "ACCESS-CM2_r1i1p1f1","CMCC-ESM2_r1i1p1f1",
            "CESM2_r11i1p1f1", "CMCC-CM2-SR5_r1i1p1f1",
            "CNRM-CM6-1_r1i1p1f2", "CNRM-ESM2-1_r1i1p1f2",
            "CANESM5_r1i1p1f1", "EC-EARTH3-VEG_r1i1p1f1",
            "HADGEM3-GC31-LL_r1i1p1f3", "HADGEM3-GC31-MM_r1i1p1f3",
            "IPSL-CM6A-LR_r1i1p1f1", "MIROC6_r1i1p1f1",
            "MIROC-ES2L_r1i1p1f2", "MPI-ESM1-2-HR_r1i1p1f1",
            "MPI-ESM1-2-LR_r1i1p1f1", "MRI-ESM2-0_r1i1p1f1",
            "NORESM2-LM_r1i1p1f1","NORESM2-MM_r1i1p1f1", 
            "TAIESM1_r1i1p1f1","UKESM1-0-LL_r1i1p1f2")
    
model_mean=("MEAN","MEAN-CMIP5-CORDEX")
        
    
    #das sollte besser gehen, mit eine Schleife, klapt aber irgendwie gerade nicht:
    #for r in range(len(reg)):
    #    dfdiff_reg[r]=subtract_era(datadi,era5di,file_dict,reg[r])
    #Ersatz:
print('NEU')
dfdiff_NEU=subtract_era(datadi,era5di,file_dict,'NEU',model_name)
print('CEU')
dfdiff_CEU=subtract_era(datadi,era5di,file_dict,'CEU',model_name)
print('MED')
dfdiff_MED=subtract_era(datadi,era5di,file_dict,'MED',model_name)
      

PlotName=df_name+MIP[0]+'_'+MIP[1]+'_'+reg[0]+'_'+reg[1]+'_'+reg[2]+'_'+sce[0]+timeslice+var[0]+'_mean.png'
tt=timeslice.replace('_',' ')
plot_titel= MIP[0]+' - '+MIP[1]+', '+vartitel+' '+tt
OutFile=os.path.join(plotdi,PlotName)
                            
dataframes=[dfdiff_NEU,dfdiff_CEU,dfdiff_MED]
plot_heatmap_season_1x3(reg,dataframes,OutFile,var_dict,plot_titel,model_name,model_mean)
                    
