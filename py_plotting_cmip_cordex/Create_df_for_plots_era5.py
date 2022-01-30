#!/usr/bin/env python3

'''
 open large dataframe and sort into smaller dataframes for plotting
 sorting ERA5 data for Heatmap plots, alle seasons in one file

'''

import os
import pandas as pd
from dp_cmip_tools import replace_mask_name, convert_to_df_time_fh , save_df

Inputfiles=('IFS_ERA5_R-e-a-n-a-l-y-s-i-s_2t_NG_landonly_seasonal_fldmean.csv',
            'IFS_ERA5_R-e-a-n-a-l-y-s-i-s_2t_PRUDENCE_landonly_seasonal_fldmean.csv',
            'IFS_ERA5_R-e-a-n-a-l-y-s-i-s_2t_SREX-AR6-NEU-CEU-MED_landonly_seasonal_fldmean.csv',
            'IFS_ERA5_R-e-a-n-a-l-y-s-i-s_tp_NG_landonly_seasonal_fldmean.csv',
            'IFS_ERA5_R-e-a-n-a-l-y-s-i-s_tp_PRUDENCE_landonly_seasonal_fldmean.csv',
            'IFS_ERA5_R-e-a-n-a-l-y-s-i-s_tp_SREX-AR6-NEU-MED-CEU_landonly_seasonal_fldmean.csv')

print(os.getcwd())
workdir=os.getcwd()
#
# Select input data and output directory
#
Inputdir=workdir.replace('py_plotting_cmip_cordex','INPUT_DATA_ERA5')
print(' ')
print('datafile is read from: ', Inputdir)

# Make Outputdir

Outdatadir=workdir.replace('py_plotting_cmip_cordex','HEATMAP/data/ERA5')
if not os.path.exists(Outdatadir):
    os.makedirs(Outdatadir)
print(' ')
print('Output will be stored in : ', Outdatadir)

for Infile in Inputfiles:
    var=Infile.split('_')[3]
    print(var)
    dt=Infile.split('_')[6]
    print(dt)

    filename=os.path.join(Inputdir,Infile)
    print(' ')
    print(' File which is processed:')
    print(Infile)

    # read dataframe
    with open(filename, "r") as file:
        df = pd.read_csv(file)
    
    # prudence regions are numbers from 1 to 8 and get new abbreviations
    df['mask'] = df['mask'].apply(str)
    replace_mask_name(df)

    # planed are plots for each region, season, exp, time-slice
    df['model_member'] = df['project_id']
    for mip in df['project_id'].unique():
        for mask in df['mask'].unique(): 
            for exp in ('Reanalysis',):
                for time in ('1981-01-01 to 2010-12-31',):
                    dfhist=convert_to_df_time_fh(df, mip, mask, time, exp, var, dt)
                    timen=time.replace(' ','_')
                    Outfile='df_'+mip+'_'+mask +'_'+ exp+'_'+timen+'_'+var+'.csv'
                    dfname=os.path.join(Outdatadir,Outfile)
                    print('Output will be in =', dfname)
                    dfhist.to_csv(dfname,index='model_member',na_rep='NaN')

                    # if pr save two files one additional in mm
                    if var == 'tp': 
                        dfhistn=dfhist * 86400
                        Outfile='df_'+mip+'_'+mask +'_'+ exp+'_'+'1981-01-01_to_2010-12-31'+'_'+var+'_mm.csv'
                        dfname=os.path.join(Outdatadir,Outfile)
                        print('Output will be in =', dfname)
                        dfhistn.to_csv(dfname,index='model_member',na_rep='NaN')  

                            


             

