#!/usr/bin/env python3

'''
 open dataframe and sort for Scatterplots , Stripplots or Boxplots

'''

import os
import pandas as pd
from pprint import pprint
import pickle
from dp_cmip_tools import replace_mask_name, convert_to_df_time


def main(filename, Outdatadir):

    # read dataframe
    with open(filename, "r") as file:
        df = pd.read_csv(file)
    
    # convert mean column to numerics
    df['mask'] = df['mask'].apply(str)
    replace_mask_name(df)

    print (df['mask'])
    # planed are plots for each region, season, exp, time-slice
    for mip in df['project_id'].unique():
        for mask in df['mask'].unique():
            for season in df['season'].unique(): 
                for exp in ('historical',):
                    print('for ',mip, mask, season,': create df_hist:') 
                    for time in ('1981-01-01 to 2010-12-31',):
                        dfhist=convert_to_df_time(df, mip, mask, season, time, exp)              
                        # it should contain modelname, mip, rcp, time, tas_hist, tas_sc, tas_diff, pr_hist,pr_sc,pr_diff, rsds ......
                        timen=time.replace(' ','_')
                        # add basics again:
                        dfhist['project_id'] = mip
                        dfhist['mask'] = mask
                        dfhist['season'] = season
                        dfhist['experiment_id'] = exp
                        dfhist['time_bounds'] = time
                                                 
                        dfname=Outdatadir+'df_'+mip+'_'+season+'_'+mask +'_'+ exp+'_'+timen+'.csv'
                        print('Output will be in =', dfname)
                        dfhist.to_csv(dfname,index='model_member')
             
if __name__ == "__main__":
    #Infile='CMIP5_rcp_tas-pr-rsds-snw-snc_seasonal_NG.csv'       
    #Infile='CMIP5_rcp_tas-pr-rsds-snw-snc_seasonal_SREX_NEU_CEU_MED.csv'  
    #Infile='CMIP6_ssp_tas-pr-rsds-snw-snc_seasonal_PRUDENCE.csv'
    #Infile='CMIP5_rcp_tas-pr-rsds-snw-snc_seasonal_PRUDENCE.csv' 
    #Infile='CMIP6_ssp_tas-pr-rsds-snw-snc_seasonal_NG.csv'                
    Infile='CMIP6_ssp_tas-pr-rsds-snw-snc_seasonal_SREX_NEU_CEU_MED.csv'


    datadir='/work/ch0636/g300047/dataprocessing_cmip5_cmip6/INPUT_DATA/'
    filename=datadir+Infile
    Outdatadir='/work/ch0636/g300047/dataprocessing_cmip5_cmip6/SCATTER/data/'

    main(filename,Outdatadir)
