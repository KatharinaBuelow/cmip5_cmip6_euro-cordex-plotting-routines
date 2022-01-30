#!/usr/bin/env python3
#
# converts a recursive pyspatem dict of monthly 30 year means to a dataframe 
# for plotting a heatmap
# it works for annual cycle and seasoanl files
# 
#

#!/usr/bin/env python3

'''
 open large dataframe and sort into smaller dataframes for plotting
 sorting ERA5 data for Heatmap plots, alle seasons in one file

'''

import os
import pandas as pd
from dp_cmip_tools import replace_mask_name, convert_to_df_time_fh, subtract_two

variables=('tas','rsds','pr','snw')

Inputfiles = ('CMIP5_rcp_tas-pr-rsds-snw-snc_seasonal_NG.csv',
              'CMIP5_rcp_tas-pr-rsds-snw-snc_seasonal_SREX_NEU_CEU_MED.csv',
              'CMIP6_ssp_tas-pr-rsds-snw-snc_seasonal_PRUDENCE.csv', 
              'CMIP5_rcp_tas-pr-rsds-snw-snc_seasonal_PRUDENCE.csv', 
              'CMIP6_ssp_tas-pr-rsds-snw-snc_seasonal_NG.csv', 
              'CMIP6_ssp_tas-pr-rsds-snw-snc_seasonal_SREX_NEU_CEU_MED.csv', 
              'CMIP5_rcp_tas-pr-rsds-snw-snc_monthly_NG.csv', 
              'CMIP5_rcp_tas-pr-rsds-snw-snc_monthly_SREX_NEU_CEU_MED.csv',
              'CMIP6_ssp_tas-pr-rsds-snw-snc_monthly_PRUDENCE.csv',
              'CMIP5_rcp_tas-pr-rsds-snw-snc_monthly_PRUDENCE.csv',
              'CMIP6_ssp_tas-pr-rsds-snw-snc_monthly_NG.csv',
              'CMIP6_ssp_tas-pr-rsds-snw-snc_monthly_SREX_NEU_CEU_MED.csv')

print('working directory: ',os.getcwd())
workdir=os.getcwd()

# Select input data and output directory

Inputdir=workdir.replace('py_plotting_cmip_cordex','INPUT_DATA')
print(' ')
print('datafile is read from: ', Inputdir)

for Infile in Inputfiles:
    dt=Infile.split('_')[3]
    print(dt)
    mip=Infile.split('_')[0]
    print(mip)
    filename=os.path.join(Inputdir,Infile)
        
    # Make Outputdir
    Outdatadir=workdir.replace('py_plotting_cmip_cordex','HEATMAP/data/'+mip+'/'+dt)
    if not os.path.exists(Outdatadir):
        os.makedirs(Outdatadir)
    print(' ')
    print('Output will be stored in : ', Outdatadir)
    
    # read dataframe
    with open(filename, "r") as file:
        print('open file: ',filename)
        df = pd.read_csv(file)
    print(df)
    #
    df['mask'] = df['mask'].apply(str)
    replace_mask_name(df)
 
    # little adjustment of the df for plotting
    # model_id and realisation in one colomn, it is easier to handle for plotting
    
    for mip in df['project_id'].unique():
        if mip == 'CMIP6':
            df['model_id'] = df['model_id'].str.split('_').str[0]
    df['model_id'] = df['model_id'].str.upper()
    df['model_member'] = df['model_id'].str.cat(df['ensemble_member'],sep="_")
    
    # planed are plots for each region, exp, time-slice, var

    for mip in df['project_id'].unique():
        for mask in df['mask'].unique():
            for var in variables:
                for exp in ('historical',):
                    print('for ',mip, mask,exp, var,': create df_hist:') 
                    for time in ('1981-01-01 to 2010-12-31',):
                        dfhist=convert_to_df_time_fh(df, mip, mask, time, exp, var, dt)
                        timen=time.replace(' ','_')
                        Outfile='df_'+mip+'_'+mask +'_'+ exp+'_'+timen+'_'+var+'.csv'
                        dfname=os.path.join(Outdatadir,Outfile)
                        print('Output will be in =', dfname)
                        
                        dfhist.to_csv(dfname,index_label='model_member',na_rep='NaN')

                for exp in df['experiment_id'].unique():
                    if exp != 'historical':
                        print('for ', mip, mask, exp, var,': create scenario:') 
                        for time in ('2036-01-01 to 2065-12-31','2070-01-01 to 2099-12-31'):
                            dfsce=convert_to_df_time_fh(df, mip, mask, time, exp, var, dt)
                            timen=time.replace(' ','_')
                            Outfile='df_'+mip+'_'+mask +'_'+ exp+'_'+timen+'_'+var+'.csv'
                            dfname=os.path.join(Outdatadir,Outfile)
                            print('Output will be in =', dfname)
                            dfsce.to_csv(dfname,index_label='model_member',na_rep='NaN')
                            # subtract historical and Scenario                       
                            dfsced=subtract_two(dfhist,dfsce,var,'rel')
                            timen=time.replace(' ','_')
                            Outfile='df_diff_'+mip+'_'+mask +'_'+ exp+'_'+timen+'_minus_1981-01-01_to_2010-12-31'+'_'+var+'.csv'
                            dfname=os.path.join(Outdatadir,Outfile)
                            print('Output will be in =', dfname)
                            dfsced.to_csv(dfname,index_label='model_member',na_rep='NaN')

                            # if pr save two files one additional in mm
                            if var == 'pr': 
                                dfsceda=subtract_two(dfhist,dfsce,var,'abs') 
                                timen=time.replace(' ','_')
                                Outfile='df_diff_'+mip+'_'+mask +'_'+ exp+'_'+timen+'_minus_1981-01-01_to_2010-12-31'+'_'+var+'_mm.csv'
                                dfname=os.path.join(Outdatadir,Outfile)
                                print('Output will be in =', dfname)
                                dfsceda.to_csv(dfname,index_label='model_member',na_rep='NaN')
                                dfhistn=dfhist * 86400
                                Outfile='df_'+mip+'_'+mask +'_'+ exp+'_'+'1981-01-01_to_2010-12-31'+'_'+var+'_mm.csv'
                                dfname=os.path.join(Outdatadir,Outfile)
                                print('Output will be in =', dfname)
                                dfhistn.to_csv(dfname,index_label='model_member',na_rep='NaN')                              

   
