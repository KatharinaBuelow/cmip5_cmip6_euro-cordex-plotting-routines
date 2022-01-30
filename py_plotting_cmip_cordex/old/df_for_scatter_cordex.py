#!/usr/bin/env python3

'''
 open dataframe and sort for Scatter plots

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
                for exp in df['experiment_id'].unique(): 
                    for time in ('1981-01-01 to 2010-12-31',):
                        dfhist=convert_to_df_time(df, mip, mask, season, time, exp)
                        print(mask)
                        print(exp)
                        print(season)
                        print(df['experiment_id'])
                        print(dfhist)
                    for time in ('2036-01-01 to 2065-12-31','2070-01-01 to 2099-12-31'):
                        dfsce=convert_to_df_time(df, mip, mask, season, time, exp)
                        print(dfsce)
                    # join historical and Scenario
                        dfsce=pd.concat([dfsce,dfhist],axis=1,join='inner',sort=False)
                        print('concat ')
                        print(dfsce)
                            # substract scenario - historical 
                        for var in ('tas','pr'):
                            col_name_hist=var+'_1981-01-01 to 2010-12-31'
                            col_name=var+'_'+time
                            col_diff='diff_'+var+'_'+time
                            dfsce[col_diff]= dfsce[col_name] - dfsce[col_name_hist]
                            if var == 'pr':
                                col_diff_pro='pro_diff_'+var+'_'+time
                                dfsce[col_diff_pro]= dfsce[col_diff] * (100 / dfsce[col_name_hist])
                            # save dfsce for plotting
                            # it should contain modelname, mip, rcp, time, tas_hist, tas_sc, tas_diff, pr_hist,pr_sc,pr_diff, rsds ......
                            timen=time.replace(' ','_')
                            # add basics again:
                        dfsce['project_id'] = mip
                        dfsce['mask'] = mask
                        dfsce['season'] = season
                        dfsce['experiment_id'] = exp
                        dfsce['time_bounds'] = time
                                                 
                        dfname=Outdatadir+'df_'+mip+'_'+season+'_'+mask +'_'+ exp+'_'+timen+'.csv'
                        print('Output will be in =', dfname)
                        dfsce.to_csv(dfname,index='model_member')
             
if __name__ == "__main__":
    Infile='EUR-11_CORDEX_rcp26-rcp45-rcp85_tas-pr_PRUDENCE_landonly_seasonal_fldmean.csv'   
    #Infile='EUR-11_CORDEX_rcp26-rcp45-rcp85_tas-pr_SREX-AR6-NEU-CEU-MED_landonly_seasonal_fldmean.csv'

    datadir='/work/ch0636/g300047/dataprocessing_cmip5_cmip6/INPUT_DATA/'
    filename=datadir+Infile
    Outdatadir='/work/ch0636/g300047/dataprocessing_cmip5_cmip6/SCATTER/data/'

    main(filename,Outdatadir)
