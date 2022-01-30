#! /usr/bin/python
# coding: utf-8
import numpy as np
import glob
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
from dp_cmip_plotting_tools import add_mean_hm,  plot_heatmap_sce_1x3, rename


''' make heatmaps for each season average over 30 years
    collect, what you want to plot
    3 Scenarios per region and per time_slice and per variable '''
#-------------------------------------------
#
# This program requires, that the data files exist
# which can be calculated with Create_df_for_heatmap.py
#
#------------------------------
# select variable
#-------------------------------

var_dict = {'Precipitation':['['+r'$\Delta$' +' Precipitation mm/day'+']', (-1.5,1.5),'PuOr','.1f'],}
#var_dict = {'Precipitation':['['+r'$\Delta$' +' Precipitation %'+']', (-70,70),'PuOr','.0f'],}
#var_dict = {'Temperature':['['+r'$\Delta$' +' Kelvin'+']', (-9,9),'seismic','.1f'],}
#var_dict = {'SNOW':['['+r'$\Delta$' +' mm'+']', (-70,70),'RdBu','.0f'],}
#var_dict = {'Radiation':['['+r'$\Delta$' +' W / m**2'+']', (-30,30),'PiYG_r','.0f'],}
    
#---------------------------    
# select file dictionary
#--------------------------

# unit of precipitation needs to be adjusted either mm/day or % and pr or pr_mm
#-----------
# CMIP5
#------------
# Precipitation
#file_dict = {'File':['df_diff_', 'CMIP5', 'pr_mm', ('deutschland',), ('rcp26','rcp45','rcp85') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean precipitation change [mm/day]',],}   
file_dict = {'File':['df_diff_' , 'CMIP5','pr_mm', ('CEU','NEU','MED'), ('rcp26','rcp45','rcp85') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean precipitation change [mm/day]',],}
#file_dict = {'File':['df_diff_' , 'CMIP5','pr_mm', ('1','2','3','4','5','6','7','8'), ('rcp26','rcp45','rcp85') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean precipitation change [mm/day]',],}

#Temperature
#file_dict = {'Temperature':['df_diff_' , 'CMIP5','tas', ('CEU','NEU','MED'), ('rcp26','rcp45','rcp85') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean temperature change [K]',],}
#file_dict = {'Temperature':['df_diff_' , 'CMIP5','tas', ('1','2','3','4','5','6','7','8'), ('rcp26','rcp45','rcp85') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean temperature change [K]',],}
#file_dict = {'Temperature':['df_diff_' , 'CMIP5','tas', ('deutschland',), ('rcp26','rcp45','rcp85') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean temperature change [K]',],}

# snow
#file_dict = {'Snow':['df_diff_' , 'CMIP5','snw', ('CEU','NEU','MED'),  ('rcp26','rcp45','rcp85') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean swe change [mm]',],}
#file_dict = {'Snow':['df_diff_' , 'CMIP5','snw', ('1','2','3','4','5','6','7','8'), ('rcp26','rcp45','rcp85'), ('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean swe change [mm]',],}
#file_dict = {'Snow':['df_diff_' , 'CMIP5','snw', ('deutschland',), ('rcp26','rcp45','rcp85'), ('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean swe change [mm]',],}

# Radiaton
#file_dict = {'Radiation':['df_diff_' , 'CMIP5','rsds', ('CEU','NEU','MED'), ('rcp26','rcp45','rcp85'), ('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean radiation change [w/m**2]',],}
#file_dict = {'Radiation':['df_diff_' , 'CMIP5','rsds', ('1','2','3','4','5','6','7','8'), ('rcp26','rcp45','rcp85'), ('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean radiation change [w/m**2]',],}
#file_dict = {'Radiation':['df_diff_' , 'CMIP5','rsds', ('deutschland',), ('rcp26','rcp45','rcp85'), ('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean radiation change [w/m**2]',],}

#----------------------
# CMIP6
#----------------------
# Precipitation
# var precipitation in mm/day file_dict needs to be changed from pr to pr_mm 
#file_dict = {'File':['df_diff_' , 'CMIP6','pr_mm', ('CEU','NEU','MED'), ('ssp126','ssp245','ssp585') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean precipitation change [mm/day]',],}
#file_dict = {'File':['df_diff_' , 'CMIP6','pr', ('1','2','3','4','5','6','7','8'), ('ssp126','ssp245','ssp585') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean precipitation change [%]',],}
#file_dict = {'File':['df_diff_', 'CMIP6', 'pr', ('deutschland',), ('ssp126','ssp245','ssp585') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean precipitation change [%]',],}

# Temperature
#file_dict = {'Temperature':['df_diff_' , 'CMIP6','tas', ('CEU','NEU','MED'), ('ssp126','ssp245','ssp585') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean temperature change [K]',],}
#file_dict = {'Temperature':['df_diff_' , 'CMIP6','tas', ('1','2','3','4','5','6','7','8'), ('ssp126','ssp245','ssp585') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean temperature change [K]',],}
#file_dict = {'Temperature':['df_diff_' , 'CMIP6','tas', ('deutschland',), ('ssp126','ssp245','ssp585') ,('_2036-01-01_to_2065-12-31','_2070-01-01_to_2099-12-31'),'_minus_1981-01-01_to_2010-12-31_','mean temperature change [K]',],}


print(os.getcwd())
workdir=os.getcwd()
#-----------------------------------------------
# nothing needs to be changed below:
#----------------------------------------------

for parameter in file_dict.keys():
    df_name = file_dict[parameter][0]
    MIP = file_dict[parameter][1]
    var = file_dict[parameter][2]
        
    print(parameter, df_name, MIP, var)
    timeslice=file_dict[parameter][4][:]
    reg = file_dict[parameter][3][:]
    sce = file_dict[parameter][4][:]
    timeslice=file_dict[parameter][5][:]
    hist=file_dict[parameter][6]
    vartitel=file_dict[parameter][7]
    print(parameter,reg,sce)

dt='season'
datadi=workdir.replace('py_plotting_cmip_cordex','HEATMAP/data/'+MIP+'/seasonal/')
print(' ')
print('datafile is read from: ', datadi)
#
# Make Outputdir
#
plotdi=workdir.replace('py_plotting_cmip_cordex','HEATMAP/plots/seasonal/')
if not os.path.exists(plotdi):
    os.makedirs(plotdi)
print(' ')
print('Output will be stored in : ', plotdi)


model_name=("CNRM-CM5_r1i1p1", "GFDL-ESM2G_r1i1p1", "HADGEM2-ES_r1i1p1",
            "MPI-ESM-LR_r1i1p1", "MPI-ESM-LR_r2i1p1", "MPI-ESM-LR_r3i1p1",
            "NORESM1-M_r1i1p1", "EC-EARTH_r1i1p1",  
            "EC-EARTH_r12i1p1", "IPSL-CM5A-LR_r1i1p1","IPSL-CM5A-MR_r1i1p1",
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


for region in range(len(reg)):
    print('region: ', reg[region])
        
    for time in range(len(timeslice)):
        print(timeslice[time])
        
        # I do not like the next line, how can InData be flexible?-------
            
        FileName=df_name+MIP+'_'+reg[region]+'_'+sce[0]+timeslice[time]+hist+var+'.csv'                  
        InFile=os.path.join(datadi,FileName)
        InData1=pd.read_csv(InFile,index_col='model_member')
        InData1m=add_mean_hm(InData1,MIP,model_name)

        FileName=df_name+MIP+'_'+reg[region]+'_'+sce[1]+timeslice[time]+hist+var+'.csv'                  
        InFile=os.path.join(datadi,FileName)
        InData2=pd.read_csv(InFile,index_col='model_member')
        InData2m=add_mean_hm(InData2,MIP,model_name)
            
        FileName=df_name+MIP+'_'+reg[region]+'_'+sce[2]+timeslice[time]+hist+var+'.csv'                  
        InFile=os.path.join(datadi,FileName)
        InData3=pd.read_csv(InFile,index_col='model_member')
        InData3m=add_mean_hm(InData3,MIP,model_name)
        # ---------------------------------------
        reg_name=reg[region]
        reg_name=rename(reg_name)
        PlotName=df_name+MIP+'_'+reg_name+'_'+sce[0]+'_'+sce[1]+'_'+sce[2]+timeslice[time]+hist+var+'.png'
        tt=timeslice[time].replace('_',' ')
        th=hist.replace('_',' ')
        plot_titel= MIP+': '+reg_name.upper()+', '+vartitel+' '+tt+' '+th
        OutFile=os.path.join(plotdi,PlotName)
                            
        dataframes=[InData1m,InData2m,InData3m]
        plot_heatmap_sce_1x3(sce,dataframes,OutFile,var_dict,plot_titel,model_name,dt)
                    
