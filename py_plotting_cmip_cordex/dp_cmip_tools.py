#!/usr/bin/env python3

import os
import pandas as pd


def subtract_two(dfhist,dfsce,var, version):
    ''' maxtrix scen - matrix hist'''

    dfdiff = pd.DataFrame()
    dfdiff = dfsce - dfhist
    if var == 'pr' and version == 'rel':
        print('precipitation')
        dfdiff = dfdiff * (100 / dfhist)

    if var == 'pr' and version == 'abs':
        print('precipitation in mm')
        dfdiff=dfdiff*86400  #mm/day
  
    return dfdiff


def replace_mask_name(df):
    ''' Prudence masks have number and changed into short names'''

    df['mask'] = df['mask'].str.replace('1','BI')
    df['mask'] = df['mask'].str.replace('2','IP')
    df['mask'] = df['mask'].str.replace('3','FR')
    df['mask'] = df['mask'].str.replace('4','ME')
    df['mask'] = df['mask'].str.replace('5','SC')
    df['mask'] = df['mask'].str.replace('6','AL')
    df['mask'] = df['mask'].str.replace('7','MD')
    df['mask'] = df['mask'].str.replace('8','EA')
    return df

def convert_to_df_time(df, mip, mask, season, time, experiment):
    ''' creates individual df and sorts value to index=model_member'''
    ''' used for scatter plots'''
   
    dft=pd.DataFrame()
    for var in ('tas','pr'):
        sel = df.loc[ (df['project_id'] == mip) & 
                      (df['mask'] == mask) & 
                      (df['variable'] == var) & 
                      (df['season'] == season) &
                      (df['time_bounds'] == time) &
                      (df['experiment_id'] == experiment) ]
        
        # rename index with model name
        sel.index=sel['model_member']
        # column name of variable selected
        col_name=var+'_'+time
        # rename column
        sel.columns = [col_name if x=='mean' else x for x in sel.columns]
        # concat columns to new dataframe
        dft=pd.concat([dft,sel[col_name]],axis=1,join='outer',sort=False)
        dft.index.name = 'model_member'
        
    return dft   


def convert_to_df_time_fh(df, mip, mask, time, experiment,var,dt):     
    ''' creates individual df and sorts value to index=model_member''' 
    ''' for plotting heatmap, colums are month or season)'''
    
    dft=pd.DataFrame()  

    # This is not pretty, but I need the month/season in the correct order
    if dt == 'seasonal':
        season=('ANN', 'DJF','MAM','JJA', 'SON')
    
    if dt == 'monthly':
        season=('Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec')
    for seas in season:         
        sel = df.loc[ (df['project_id'] == mip) &
                      (df['mask'] == mask) & 
                      (df['variable'] == var) &
                      (df['time_bounds'] == time) &
                      (df['season'] == seas) &
                      (df['experiment_id'] == experiment) ]         
        # rename index with model name         
        sel.index=sel['model_member']         
        # column name of variable selected         
        col_name=seas         
        # rename column         
        sel.columns = [col_name if x=='mean' else x for x in sel.columns]  
        # concat columns to new dataframe         
        dft=pd.concat([dft,sel[col_name]],axis=1,join='outer',sort=False)
    return dft   



def save_df(Outdatadir,df,time,mip,mask,season,exp):
    '''
    This save a data frame with some additiona information
    '''
    timen=time.replace(' ','_')
    # add basics again:
    df['project_id'] = mip
    df['mask'] = mask
    df['season'] = season
    df['experiment_id'] = exp
    df['time_bounds'] = time
                                                 
    outname='df_'+mip+'_'+season+'_'+mask +'_'+ exp+'_'+timen+'.csv'
    dfname=os.path.join(Outdatadir,outname)
    print('Output will be in =', dfname)
    df.to_csv(dfname,index='model_member')
    #index_label='model_member'
    return


