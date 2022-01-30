#!/usr/bin/env python3
#
# converts a recursive pyspatem dict of monthly 30 year means to a dataframe 
# for plotting a heatmap
# it works for annual cycle and seasoanl files
# 
#
import os
import pandas as pd
from pprint import pprint
import pickle

from dp_cmip_tools import replace_mask_name, convert_to_df_time_fh

def main(filename, Outdatadir, variables, dt):
    
    # read dataframe
    with open(filename, "r") as file:
        print('open file: ',filename)
        df = pd.read_csv(file)
    
    df['model_member'] = df['project_id'] #df['model_id'].str.cat(df['ensemble_member'],sep="_")
    df['mask'] = df['mask'].apply(str)
    # planed are plots for each region, exp, time-slice,var
    for mip in df['project_id'].unique():
        for mask in df['mask'].unique():
            for exp in ('Observation',):
                print('for ',mip, mask,exp, var, dt, ': create df_hist:') 
                for time in ('1981-01-01 to 2010-12-31',):
                    # eobs has mean and spread in the dataframe
                    print(df)
                    sel=df.loc[(df['ensemble_member'] == 'mean')]
                    print(sel)
                    print(mip,var,mask,time)
                    dfhist=convert_to_df_time_fh(sel, mip, mask, time, exp, var, dt)
                    timen=time.replace(' ','_')
                    Outfile='df_'+mip+'_'+mask +'_'+ exp+'_'+timen+'_'+var+'.csv'
                    dfname=os.path.join(Outdatadir,Outfile)
                    print('Output will be in =', dfname)
                    dfhist.to_csv(dfname,index='model_member',na_rep='NaN')

                    # if pr save two files one additional in mm
                    if var == 'rr': 
                        dfhistn=dfhist * 86400
                        Outfile='df_'+mip+'_'+mask +'_'+ exp+'_'+'1981-01-01_to_2010-12-31'+'_'+var+'_mm.csv'
                        dfname=os.path.join(Outdatadir,Outfile)
                        print('Output will be in =', dfname)
                        dfhistn.to_csv(dfname,index='model_member',na_rep='NaN')                              

if __name__ == "__main__":

    #variables=('2t','ssrd','tp','snd')
    
    Infiles=('v20.0e_E-OBS_O-b-s-e-r-v-a-t-i-o-n_tg-rr_PRUDENCE_landonly_seasonal_fldmean.csv',
             'v20.0e_E-OBS_O-b-s-e-r-v-a-t-i-o-n_tg-rr_SREX-AR6-CEU-MED-NEU_landonly_seasonal_fldmean.csv')


    datadir='/work/ch0636/g300047/dataprocessing_cmip5_cmip6/INPUT_DATA_EOBS/'
    Outdatadir='/work/ch0636/g300047/dataprocessing_cmip5_cmip6/HEATMAP/data/EOBS'

    try:
        os.makedirs(Outdatadir)
    except FileExistsError:
    # directory already exists
        pass

    for Infile in Infiles:
        filename=os.path.join(datadir+Infile)
        var='tg'  #'rr'
        print(var)
        seas=Infile.split('_')[6]
        print(seas)
        main(filename, Outdatadir, var, seas)
