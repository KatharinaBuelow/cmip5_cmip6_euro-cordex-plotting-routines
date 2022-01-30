#!/usr/bin/env python3

'''
 open large dataframe and sort into smaller dataframes for plotting

'''

import os
import pandas as pd
from dp_cmip_tools import replace_mask_name, convert_to_df_time , save_df

Inputfiles=('CMIP6_ssp_tas-pr-rsds-snw-snc_seasonal_NG.csv',
            'CMIP5_rcp_tas-pr-rsds-snw-snc_seasonal_NG.csv',                
            'CMIP6_ssp_tas-pr-rsds-snw-snc_seasonal_PRUDENCE.csv',
            'CMIP5_rcp_tas-pr-rsds-snw-snc_seasonal_PRUDENCE.csv',          
            'CMIP6_ssp_tas-pr-rsds-snw-snc_seasonal_SREX_NEU_CEU_MED.csv',
            'CMIP5_rcp_tas-pr-rsds-snw-snc_seasonal_SREX_NEU_CEU_MED.csv',  
            'EUR-11_CORDEX_rcp26-rcp45-rcp85_tas-pr_PRUDENCE_landonly_seasonal_fldmean.csv')  
             
#Inputfiles=('EUR-11_CORDEX_rcp26-rcp45-rcp85_tas-pr_SREX-AR6-NEU-CEU-MED_landonly_seasonal_fldmean.csv',)

#Inputfiles=('EUR-11_CORDEX_rcp26-rcp45-rcp85_tas-pr-rsds-snw_NG_landonly_seasonal_fldmean.csv',)

print(os.getcwd())
workdir=os.getcwd()
#
# Select input data and output directory
#
Inputdir=workdir.replace('py_plotting_cmip_cordex','INPUT_DATA')
print(' ')
print('datafile is read from: ', Inputdir)

# Make Outputdir

Outdatadir=workdir.replace('py_plotting_cmip_cordex','SCATTER/data')
if not os.path.exists(Outdatadir):
    os.makedirs(Outdatadir)
print(' ')
print('Output will be stored in : ', Outdatadir)

for Infile in Inputfiles:
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
    for mip in df['project_id'].unique():
        for mask in df['mask'].unique():
            for season in df['season'].unique():
                if mip != 'EURO-CORDEX':
                    for exp in ('historical',):
                        for time in ('1981-01-01 to 2010-12-31',):
                            dfhist=convert_to_df_time(df, mip, mask, season, time, exp)
                            #save dfhist for plotting
                            save_df(Outdatadir,dfhist,time,mip,mask,season,exp)
                for exp in df['experiment_id'].unique():
                    if mip == 'EURO-CORDEX':
                        for time in ('1981-01-01 to 2010-12-31',):
                            dfhist=convert_to_df_time(df, mip, mask, season, time, exp)
                            save_df(Outdatadir,dfhist,time,mip,mask,season,exp)
                    if exp != 'historical': 
                        for time in ('2036-01-01 to 2065-12-31','2070-01-01 to 2099-12-31'):
                            dfsce=convert_to_df_time(df, mip, mask, season, time, exp)
                            # join historical and Scenario
                            dfsce=pd.concat([dfsce,dfhist],axis=1,join='inner',sort=False)
                            # substract scenario - historical 
                            for var in ('tas','pr'):
                                col_name_hist=var+'_1981-01-01 to 2010-12-31'
                                col_name=var+'_'+time
                                col_diff='diff_'+var+'_'+time
                                dfsce[col_diff]= dfsce[col_name] - dfsce[col_name_hist]
                                if var == 'pr':
                                    col_diff_pro='pro_diff_'+var+'_'+time
                                    dfsce[col_diff_pro]= dfsce[col_diff] * (100 / dfsce[col_name_hist])
                            
                            save_df(Outdatadir,dfsce,time,mip,mask,season,exp)
                            


             

