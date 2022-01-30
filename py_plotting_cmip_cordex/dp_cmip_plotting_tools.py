#!/usr/bin/env python3

import os
import pandas as pd
from scattertable import scattertable
import numpy as np
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import markers


def subtract_era(datadi, era5di, file_dict,r, model_name):
     ''' maxtrix hist - matrix era5
     hist is a matrix, ERA5 just one value '''

     for parameter in file_dict.keys():
        df_name = file_dict[parameter][0]
        MIP = file_dict[parameter][1][:]
        var = file_dict[parameter][2][:]      
        timeslice=file_dict[parameter][5]
        reg = file_dict[parameter][3][:]
        sce = file_dict[parameter][4][:]
        vartitel=file_dict[parameter][6]
        kind=file_dict[parameter][7]
            
     FileName=df_name+MIP[0]+'_'+r+'_'+sce[0]+timeslice+var[0]+'.csv'
     print(FileName)
     FileEra= df_name+MIP[1]+'_'+r+'_'+sce[1]+timeslice+var[1]+'.csv'
     print(FileEra)
     InFile=os.path.join(datadi,FileName)
     InEra=os.path.join(era5di,FileEra)
     print('InEra:',era5di)
     dfhist=pd.read_csv(InFile,index_col='model_member')
     df_era5 =pd.read_csv(InEra ,index_col='model_member')   

     dfdiffm=pd.DataFrame()
     colm=['ANN','DJF','MAM','JJA','SON']
          
     for c in range(5):
         diff=pd.DataFrame()
         col=colm[c]
         value=df_era5.iloc[0][col]
         print('value= ', value)
         dfhist.loc[dfhist[col]> 1e+19 ] = np.nan
         diff=dfhist[col] - value
         if var[1] == 'tp':
             # change unit to mm/day
             value=value * 86400             
             diff=(dfhist[col] * 86400) - value
             print('value= ', value)
             print('precipitation')
             if kind == '%':
                 diff=diff * (100 / value)
         dfdiffm=pd.concat([dfdiffm,diff],axis=1,join='outer',sort=False)
     dfdiffm.columns = colm

     # Alphabethical Order
     dfdiffm=dfdiffm.sort_index()
     # MEAN diff
     dfdiffmm=dfdiffm.copy()
     dfdiffmm.loc['MEAN']=dfdiffmm.mean(numeric_only=True, axis=0)
     #
     if MIP[0] == 'CMIP5':
          t2=pd.DataFrame()
          for i in model_name:
               t=dfdiffm.loc[(dfdiffm.index == i)]
               t2=pd.concat([t2,t],axis=0)
          t2m=t2.copy()
          t2m.loc['MEAN-CMIP5-CORDEX']=t2m.mean(numeric_only=True, axis=0)      
          EC=t2m.loc[(t2m.index == 'MEAN-CMIP5-CORDEX')]
          
          # append to dfdiffmm
          dfdiffmm=pd.concat([dfdiffmm,EC],axis=0)
        
     return dfdiffmm


def add_mean_hm(InData,MIP,model_name):
    ''' add MEAN per month or season over all models for heatmap'''
  
    InDatam=InData.copy()
    InDatam.loc['MEAN']=InDatam.mean(numeric_only=True, axis=0)
     #
    if MIP == 'CMIP5':
        t2=pd.DataFrame()
        for i in model_name:
            t=InDatam.loc[(InDatam.index == i)]
            t2=pd.concat([t2,t],axis=0)
        t2m=t2.copy()
        t2m.loc['MEAN-CMIP5-CORDEX']=t2m.mean(numeric_only=True, axis=0)
          #print(t2m)
        EC=t2m.loc[(t2m.index == 'MEAN-CMIP5-CORDEX')]
          # append 
        InDatam=pd.concat([InDatam,EC],axis=0)
     
    #print(InDatam)
    return InDatam


def add_mean(df):
    ''' mean over df.Scenario '''
    
    MeanData=pd.DataFrame()
    for s in df['Scenario'].unique():
        print(s)
        sel=df.loc[(df['Scenario'] == s)]
        selm=sel.copy()
        selm.loc['MEAN']=selm.mean(numeric_only=True, axis=0)
        selm.at['MEAN','experiment'] = 'MEAN'
        selm.at['MEAN','Scenario'] = s
        MeanData=pd.concat([MeanData,selm],axis=0)
    
    dfm=MeanData.loc[(MeanData['experiment'] == 'MEAN')]
    print(dfm)
    return dfm

# ******************************************************************      
# ToDo die add columns in eine funktion zusammen fassen irgendwie
# ******************************************************************

def add_column_for_plot(df):
    ''' add column for CMIP-mini-ensembel ...'''
    
    eurocordex = scattertable('cordex-gcm')
    cmip6_lbc = scattertable('cmip6-gcm-lbc')
    
    # Create column with names, which equal the names in list CMIP5-CORDEX :
    df['model_member_experiment_id'] = df['model_member'].str.cat(df['experiment_id'],sep="_")  
    df['experimentn'] = df['model_member_experiment_id'].map(eurocordex)
    df['experiment1'] = [x if x == 'CMIP5-CORDEX' else z for x,z in zip(df['experimentn'],df['project_id'])]
    # clean up
    df.drop(['experimentn'], inplace=True, axis=1)
    
    # A simulation of the CMIP5-CORDEX ensemble is also a memebr of CMIP5 Ensemble and needs to added again
    sel=df.loc[(df['experiment1'] == 'CMIP5-CORDEX')]
    sel=sel.replace({'experiment1':'CMIP5-CORDEX'},{'experiment1':'CMIP5'}, regex=True)
    dfn=df.append(sel)
    

    # CMIP6: Create column with names , which equal the names in list CMIP6-LBC :
    dfn['experimentn'] = dfn['model_member_experiment_id'].map(cmip6_lbc)
    dfn['experiment'] = [x if x == 'CMIP6-LBC' else z for x,z in zip(dfn['experimentn'],dfn['experiment1'])]
    # clean up
    dfn.drop(['experimentn'], inplace=True, axis=1)
    dfn.drop(['experiment1'], inplace=True, axis=1)

    # the runs which are in the Ensemble with LBC are also in the ensemble of CMIP, so they have to occure twice
    sel=dfn.loc[(dfn['experiment'] == 'CMIP6-LBC')]
    sel=sel.replace({'experiment':'CMIP6-LBC'},{'experiment':'CMIP6'}, regex=True)
    df=dfn.append(sel)

    df['xcategory']=df['experiment'].str.cat(df['experiment_id'],sep="-")
    return(df)

def add_column_for_plot_season(df):
    ''' add column for CMIP-mini-ensembel ...'''
    
    eurocordex = scattertable('cordex-gcm')
    cmip6_lbc = scattertable('cmip6-gcm-lbc')
    
    # CMIP5: Create column with names , which equal the names in list CORDEX_GCM /cmip6-gcm-lbc :
    df['model_member_experiment_id'] = df['model_member'].str.cat(df['experiment_id'],sep="_")  
    df['experimentn'] = df['model_member_experiment_id'].map(eurocordex)
    df['experiment1'] = [x if x == 'CMIP5-CORDEX' else z for x,z in zip(df['experimentn'],df['project_id'])]
    # clean up
    df.drop(['experimentn'], inplace=True, axis=1)
    # the runs which are in the Ensemble with LBC are also in the ensemble of CMIP, so they have to occure twice
    sel=df.loc[(df['experiment1'] == 'CMIP5-CORDEX')]
    sel['experiment1']= 'CMIP5'
    dfn=df.append(sel)
    # CMIP6: Create column with names , which equal the names in list CORDEX_GCM /cmip6-gcm-lbc :
    dfn['experimentn'] = dfn['model_member_experiment_id'].map(cmip6_lbc)
    dfn['experiment'] = [x if x == 'CMIP6-LBC' else z for x,z in zip(dfn['experimentn'],dfn['experiment1'])]
    # clean up
    dfn.drop(['experimentn'], inplace=True, axis=1)
    dfn.drop(['experiment1'], inplace=True, axis=1)
    # the runs which are in the Ensemble with LBC are also in the ensemble of CMIP, so they have to occure twice
    sel=dfn.loc[(dfn['experiment'] == 'CMIP6-LBC')]
    sel['experiment']= 'CMIP6'
    df=dfn.append(sel)
    df['xcategory']=df['season'].str.cat(df['experiment'],sep="-")
    return(df)


def add_column_for_plot_cordex(df):
    ''' the CORDEX name of GCM and RCM needs to be splitt first'''
    # CORDEX
    df_tmp= df['model_member'].str.split(pat="_",expand=True)
    column_name=['RCM','GCMn','CORDEX','member']
    df_tmp.columns = column_name
    df=pd.concat([df,df_tmp],axis=1)
    df['GCM']=df['GCMn'].str.cat(df['member'],sep="_")
    
    #replace project_id with rcm name
    df=df.drop(['project_id'], axis=1)
    df=df.drop(['GCMn'], axis=1)
    df=df.drop(['CORDEX'], axis=1)
    df=df.drop(['member'], axis=1)
    df['project_id']=df['RCM']
    # sometimes the same model has a different name
    df['project_id'].replace('CLMcom-BTU-CCLM4-8-17','CLMcom-CCLM4-8-17',inplace=True) 
    df['project_id'].replace('IPSL-INERIS-WRF381P','IPSL-WRF381P',inplace=True) 
    # this looks silly, but some institutes have two names and some on
    df['GCM'].replace('CNRM-CERFACS-CNRM-CM5_r1i1p1','CNRM-CM5_r1i1p1', inplace=True)
    df['GCM'].replace('MIROC-MIROC5_r1i1p1','MIROC5_r1i1p1', inplace=True)
    df['GCM'].replace('NCC-NorESM1-M_r1i1p1','NorESM1-M_r1i1p1', inplace=True)
    df['GCM'].replace('CCCma-CanESM2_r1i1p1','CanESM2_r1i1p1', inplace=True)
    df['GCM'].replace('MPI-M-MPI-ESM-LR_r1i1p1','MPI-ESM-LR_r1i1p1', inplace=True)
    df['GCM'].replace('MPI-M-MPI-ESM-LR_r2i1p1','MPI-ESM-LR_r2i1p1', inplace=True)
    df['GCM'].replace('MPI-M-MPI-ESM-LR_r3i1p1','MPI-ESM-LR_r3i1p1', inplace=True)
    df['GCM'].replace('IPSL-IPSL-CM5A-LR_r1i1p1','IPSL-CM5A-LR_r1i1p1', inplace=True)
    df['GCM'].replace('IPSL-IPSL-CM5A-MR_r1i1p1','IPSL-CM5A-MR_r1i1p1', inplace=True)
    df['GCM'].replace('NOAA-GFDL-GFDL-ESM2G_r1i1p1','GFDL-ESM2G_r1i1p1', inplace=True)
    df['GCM'].replace('ICHEC-EC-EARTH_r12i1p1','EC-EARTH_r12i1p1', inplace=True)
    df['GCM'].replace('ICHEC-EC-EARTH_r1i1p1','EC-EARTH_r1i1p1', inplace=True)
    df['GCM'].replace('ICHEC-EC-EARTH_r3i1p1','EC-EARTH_r3i1p1', inplace=True)
    df['GCM'].replace('MOHC-HadGEM2-ES_r1i1p1','HadGEM2-ES_r1i1p1', inplace=True)
    return(df)


def add_column_for_plot_cmip_cordex(df):
    ''' add column for color ...'''

    eurocordex = scattertable('cordex-gcm')      
    #Create column with names , which equal the names in list CORDEX_GCM :
    df['model_member_experiment_id'] = df['model_member'].str.cat(df['experiment_id'],sep="_")
    df['experimentn'] = df['model_member_experiment_id'].map(eurocordex)
    df['GCM'] = [z if x == 'CMIP5-CORDEX' else y for x,y,z in zip(df['experimentn'],df['project_id'],df['model_member'])]
    df=df.drop(['experimentn'], axis=1)
    return(df)


def add_column_for_plot_rcp(df,rcp):
    ''' add column for color ...'''

    eurocordex = scattertable('cordex-gcm')
        
    # Create column with names , which equal the names in list CORDEX_GCM :
    # this will eventually determine the shape
    df['model_member_experiment_id'] = df['model_member'].str.cat(df['experiment_id'],sep="_")
    df['experimentn'] = df['model_member_experiment_id'].map(eurocordex)
    df['experiment'] = [x if x == 'CMIP5-CORDEX' else z for x,z in zip(df['experimentn'],df['project_id'])]
    
    # if all scenarios are plotted, the color of CORDEX should not change see else
    print('rcp fuer if =',rcp)
    if rcp != 'all':
        #df['experimentnn'] = df['model_member_experiment_id'].map(eurocordex)
        #df['experimentnnn'] = df['experiment_id'].str.cat(df['experimentnn'],sep="-")
        df['experimentnnn'] = df['experiment_id'].str.cat(df['experimentn'],sep="-")
        df['Scenario'] = [x if x == 'CMIP5-CORDEX' else z for x,z in zip(df['experimentn'],df['experiment_id'])]
        #df['Scenario'] = [z if x == 'CMIP5-CORDEX' else y for x,y,z in zip(df['experimentn'],df['experiment_id'],df['experimentnnn'])]
        # clean up        
        df.drop(['experimentnnn'], axis=1)
        
    else:
        df['Scenario'] = df['experiment_id']       
        #Kevin: 3 special models pickt for Kevin, geht auch einfacher
        #kevin=scattertable('cmip6-gcm-lbc-kevin')
        #kevin2=scattertable('cmip6-gcm-lbc-kevin2')
        #df['experimentnk'] = df['model_member_experiment_id'].map(kevin) #kevin
        #df['experimentnk2'] = df['model_member_experiment_id'].map(kevin2) #kevin
        #df['Scenario'] = [z if x == 'ssp370_LBC' else y for x,y,z in zip(df['experimentnk2'],df['experiment_id'],df['experimentnk'])]
        
    # clean up
    df=df.drop(['experimentn'], axis=1)
    return(df)


def plot_heatmap_season_1x3(reg,dataframes, plotname, var_dict,plot_titel, model_name, model_mean):
    
    print ('reg: ', reg)
    for parameter in var_dict.keys():
        Einheit = var_dict[parameter][0]
        # y-range:
        lim_min = var_dict[parameter][1][0]
        lim_max = var_dict[parameter][1][1]
        color = var_dict[parameter][2]

        format = var_dict[parameter][3] #fmt=".1f"
    for s in range(0,len(reg)):
        print('shape: ',dataframes[s].shape)
        
    # figsize is important, make a reasonable choice

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(25,7))
    
    #First
    df=dataframes[0]
    mask = df.isna()
    
    ax1=sns.heatmap(df.T, mask=mask.T, ax=ax1, square=True, annot=True,fmt=format, annot_kws={"size": 8}, 
                   cmap=color,cbar_kws=dict(pad=0.003,shrink= 1,label= Einheit,),vmin=lim_min, vmax=lim_max,linewidths=0.5, linecolor='white' ,xticklabels=False, yticklabels=True)
    ax1.set_facecolor('lightgrey')
    ax1.tick_params(bottom=False) ## other options are left,right and top
    ax1.set_ylabel(reg[0])    
    ax1.set_xlabel(' ')
    ax1.set_title(plot_titel, color='k', fontsize=12)
    #Second
    df=dataframes[1]
    mask = df.isna()

    ax2=sns.heatmap(df.T, mask=mask.T, ax=ax2, square=True, annot=True,fmt=format, annot_kws={"size": 8}, 
                   cmap=color,cbar_kws=dict(pad=0.003,shrink= 1,label= Einheit),vmin=lim_min, vmax=lim_max,linewidths=0.5, linecolor='white' ,xticklabels=False, yticklabels=True)
    
    ax2.set_facecolor('lightgrey')
    ax2.tick_params(bottom=False)
    ax2.set_ylabel('WCE')  #reg[1])    
    ax2.set_xlabel(' ')
    
    #Third
    df=dataframes[2]
    mask = df.isna()

    ax3=sns.heatmap(df.T, mask=mask.T,ax=ax3, square=True, annot=True,fmt=format, annot_kws={"size": 8}, 
                   cmap=color,cbar_kws=dict(pad=0.003,shrink= 1,label= Einheit), vmin=lim_min, vmax=lim_max,linewidths=0.5, linecolor='white' ,xticklabels=True, yticklabels=True)
    # no cbar: cbar=False
    ax3.set_facecolor('lightgrey')
    ax3.set_ylabel(reg[2])    
    ax3.set_xlabel(' ')
    plt.tight_layout()

    for label in ax3.get_xticklabels():
        if label.get_text() in model_name:
            #label.set_size(13)
            label.set_weight("bold")
            label.set_color("red")
    
    for label in ax3.get_xticklabels():
        if label.get_text() in model_mean:
            label.set_weight("bold")
            
    
    print('hier ist der file:' ,plotname)
    #plt.show()
    plt.savefig(plotname, bbox_inches="tight")

    return


def rename(reg):
    print('replace:',reg)
    reg=reg.replace('1','BI') # prudence regions are sometimes only Numbers
    reg=reg.replace('2','IP')
    reg=reg.replace('3','FR')
    reg=reg.replace('4','ME')
    reg=reg.replace('5','SC')
    reg=reg.replace('6','AL')
    reg=reg.replace('7','MD')
    reg=reg.replace('8','EA')
    reg=reg.replace('CEU','WCE') # central Europe CEU has changed its name WCE
    print ('reg=',reg)
    
    return reg


def plot_heatmap_sce_1x3(sce, dataframes, plotname, var_dict,plot_titel, model_name, dt):

    #Name df
    for parameter in var_dict.keys():
        Einheit = var_dict[parameter][0]
        # y-range:
        lim_min = var_dict[parameter][1][0]
        lim_max = var_dict[parameter][1][1]
        color = var_dict[parameter][2]

        format = var_dict[parameter][3] #fmt=".1f"

    for s in range(0,len(sce)):
        print('shape: ',dataframes[s].shape)
        
    # figsize is important, make a reasonable choice
    if dt == 'mon':
         fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(30,10))
    else:
         fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(25,7)) 
   
    #First
    df=dataframes[0]
    mask = df.isna()
    
    im=sns.heatmap(df.T, mask=mask.T, ax=ax1, square=True, annot=True,fmt=format, annot_kws={"size": 6}, 
                   cmap=color,cbar_kws=dict(pad=0.003,shrink= 1,label= Einheit,),vmin=lim_min, vmax=lim_max,linewidths=0.5, linecolor='white' ,xticklabels=False, yticklabels=True)
    ax1.set_facecolor('lightgrey')
    ax1.tick_params(bottom=False) ## other options are left,right and top
    ax1.set_ylabel(sce[0])    
    ax1.set_xlabel(' ')
    ax1.set_title(plot_titel, color='k', fontsize=12)
    #ax1.text(32,-0.5,Einheit)
    #Second
    df=dataframes[1]
    mask = df.isna()

    ax2=sns.heatmap(df.T, mask=mask.T, ax=ax2, square=True, annot=True,fmt=format, annot_kws={"size": 6}, 
                   cmap=color,cbar_kws=dict(pad=0.003,shrink= 1,label= Einheit),vmin=lim_min, vmax=lim_max,linewidths=0.5, linecolor='white' ,xticklabels=False, yticklabels=True)
    
    ax2.set_facecolor('lightgrey')
    ax2.tick_params(bottom=False)
    ax2.set_ylabel(sce[1])    
    ax2.set_xlabel(' ')
    
    #Third
    df=dataframes[2]
    mask = df.isna()

    ax3=sns.heatmap(df.T, mask=mask.T,ax=ax3, square=True, annot=True,fmt=format, annot_kws={"size": 6}, 
                   cmap=color,cbar_kws=dict(pad=0.003,shrink= 1,label= Einheit), vmin=lim_min, vmax=lim_max,linewidths=0.5, linecolor='white' ,xticklabels=True, yticklabels=True)
    # no cbar: cbar=False
    ax3.set_facecolor('lightgrey')
    ax3.set_ylabel(sce[2])    
    ax3.set_xlabel(' ')
    plt.tight_layout()

    model_mean=("MEAN","MEAN-CMIP5-CORDEX")

    for label in ax3.get_xticklabels():
        if label.get_text() in model_name: #== "MPI-ESM-LR_r3i1p1":
        #label.set_size(13)
            label.set_weight("bold")
            label.set_color("red")

    for label in ax3.get_xticklabels():
        if label.get_text() in model_mean:
            label.set_weight("bold")
   

    print('hier ist der file:' ,plotname)
    #plt.show()
    plt.savefig(plotname, bbox_inches="tight")

    return


def scatter_plot_cordex(df, x_column, y_column, rcp, var1_dict, var2_dict, OutFile, title):

    # Variable 1
    for parameter in var1_dict.keys():
        varlongname1 = var1_dict[parameter][0]
        var1 = var1_dict[parameter][1]
        print(parameter, varlongname1, var1)
        einheit1 = var1_dict[parameter][2]
        xmin = var1_dict[parameter][3][0]
        xmax = var1_dict[parameter][3][1]
	
    # Variable 2
    for parameter in var2_dict.keys():
        varlongname2 = var2_dict[parameter][0]
        var2 = var2_dict[parameter][1]
        print(parameter, varlongname2, var2)
        einheit2 = var2_dict[parameter][2]
        ymin = var2_dict[parameter][3][0]
        ymax = var2_dict[parameter][3][1]
        size = var2_dict[parameter][5]

    df2=df.loc[(df['GCM'] == 'CMIP5')]
    df1=df.loc[(df['GCM'] != 'CMIP5')]
    colors = scattertable('colors-cordex')
    marker = scattertable('marker-rcm') 
    edgecolor="none"
   
    # rename column (nicer in plot)
    df1.rename({'project_id' : 'Model'},axis=1, inplace=True)
    df2.rename({'project_id' : 'Model'},axis=1, inplace=True)

    # Achsen
    xname=varlongname1+' ['+einheit1+']'
    yname=varlongname2+' ['+einheit2 +']'
    fig = plt.figure(figsize=(6, 6))
    
    sns.scatterplot(x=x_column, y=y_column, data=df2, hue=df2.GCM,style=df2.Model, markers=marker, s=size, palette=colors, edgecolor=edgecolor, alpha=0.5, legend=False)
    sns.scatterplot(x=x_column, y=y_column, data=df1, hue=df1.GCM,style=df1.Model, markers=marker, s=size, palette=colors, edgecolor=edgecolor, alpha=0.75, legend='auto')  
        
    plt.grid(True)
    plt.ylim(ymin,ymax)
    plt.xlim(xmin,xmax)
    plt.axhline(0, color='black', lw=1.5)
    plt.axvline(0, color='black', lw=1.5)
    plt.tick_params(axis='y', labelsize=12)
    plt.tick_params(axis='x', labelsize=12)
    plt.ylabel(yname,fontsize=12)
    plt.xlabel(xname,fontsize=12)
    plt.title(title, color='k', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05,1),loc=2) # legend out side
    print('Plot will be : ',OutFile)
    plt.savefig(OutFile, bbox_inches="tight")    
                  
    return


def scatter_plot(df, x_column, y_column, rcp, ssp, var1_dict, var2_dict, OutFile, title):

    # Variable 1
    for parameter in var1_dict.keys():
        varlongname1 = var1_dict[parameter][0]
        var1 = var1_dict[parameter][1]
        print(parameter, varlongname1, var1)
        einheit1 = var1_dict[parameter][2]
        xmin = var1_dict[parameter][3][0]
        xmax = var1_dict[parameter][3][1]
	
    # Variable 2
    for parameter in var2_dict.keys():
        varlongname2 = var2_dict[parameter][0]
        var2 = var2_dict[parameter][1]
        print(parameter, varlongname2, var2)
        einheit2 = var2_dict[parameter][2]
        ymin = var2_dict[parameter][3][0]
        ymax = var2_dict[parameter][3][1]
        size = var2_dict[parameter][5]
       
    add_column_for_plot_rcp(df,rcp)
    dfm=add_mean(df)

    df2=df.loc[(df['experiment'] == 'CMIP5-CORDEX')]
    colors = scattertable('colors')
    marker = scattertable('marker') 
    edgecolor="none"
   
    # rename column (nicer in plot)
    df.rename({'experiment' : 'Experiment'},axis=1, inplace=True)
    df2.rename({'experiment' : 'Experiment'},axis=1, inplace=True)
    dfm.rename({'experiment' : 'Experiment'},axis=1, inplace=True)
    df=pd.concat([df,dfm],axis=0) # only to get the symbol in the legend

    # Achsen
    xname=varlongname1+' ['+einheit1+']'
    yname=varlongname2+' ['+einheit2 +']'
    fig = plt.figure(figsize=(6, 6))
    print('this will be plottet: ',dfm)
    sns.scatterplot(x=x_column, y=y_column, data=df, hue=df.Scenario,style=df.Experiment, markers=marker, s=size, palette=colors, edgecolor=edgecolor, alpha=0.75, legend='auto')  
    sns.scatterplot(x=x_column, y=y_column, data=df2, hue=df2.Scenario,style=df2.Experiment, markers=marker, s=140, palette=colors, edgecolor=edgecolor, legend=False)
    sns.scatterplot(x=x_column, y=y_column, data=dfm, hue=dfm.Scenario,style=dfm.Experiment, markers=marker, s=100, palette=colors, edgecolor='xkcd:black', legend=False)
        
    plt.grid(True)
    plt.ylim(ymin,ymax)
    plt.xlim(xmin,xmax)
    plt.axhline(0, color='black', lw=1.5)
    plt.axvline(0, color='black', lw=1.5)
    plt.tick_params(axis='y', labelsize=12)
    plt.tick_params(axis='x', labelsize=12)
    plt.ylabel(yname,fontsize=12)
    plt.xlabel(xname,fontsize=12)
    plt.title(title, color='k', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05,1),loc=2) # legend out side
    print('Plot will be : ',OutFile)
    plt.savefig(OutFile, bbox_inches="tight")    
                  
    return


def strip_plot_cc(dataframes, y_column, var_dict, OutFile, title):

    # Variable
    for parameter in var_dict.keys():
        varlongname = var_dict[parameter][0]
        var = var_dict[parameter][1]
        print(parameter, varlongname, var)
        einheit = var_dict[parameter][2]
        ymin = var_dict[parameter][3][0]
        ymax = var_dict[parameter][3][1]
       
    my_c= {'CMIP6-ssp245': 'tab:cyan',
           'CMIP6-LBC-ssp245': 'tab:cyan', 
           'CMIP5-rcp45': 'tab:blue',
           'CMIP5-CORDEX-rcp45': 'tab:blue',
           'EURO-CORDEX-rcp45': 'xkcd:lightblue',
           'CMIP6-ssp126': 'tab:olive',  
           'CMIP6-LBC-ssp126': 'tab:olive',
           'CMIP5-rcp26': 'tab:green',
           'CMIP5-CORDEX-rcp26': 'tab:green',
           'EURO-CORDEX-rcp26': 'xkcd:lime', 
           'CMIP6-ssp370': 'tab:red', 
           'CMIP6-LBC-ssp370': 'tab:red', 
           'CMIP6-ssp585': 'tab:pink',
           'CMIP6-LBC-ssp585': 'tab:pink',
           'CMIP5-rcp85': 'tab:purple',
           'CMIP5-CORDEX-rcp85': 'tab:purple',
           'EURO-CORDEX-rcp85': 'xkcd:magenta'}

    yname=varlongname+' ['+einheit +']'
    print('')
    print('')
    print('Uebergabe der dataframes:')
    print('')
    print('How many dataframes: ',len(dataframes))
    if len(dataframes) == 1:
        print('shape: ',dataframes[0].shape)  
    
        fig = plt.figure(figsize=(12, 6))
        xorder=['CMIP6-ssp126', 'CMIP6-LBC-ssp126', 'CMIP5-rcp26', 'CMIP5-CORDEX-rcp26', 'EURO-CORDEX-rcp26',
            'CMIP6-ssp245', 'CMIP6-LBC-ssp245', 'CMIP5-rcp45', 'CMIP5-CORDEX-rcp45', 'EURO-CORDEX-rcp45',
            'CMIP6-ssp585', 'CMIP6-LBC-ssp585', 'CMIP5-rcp85', 'CMIP5-CORDEX-rcp85', 'EURO-CORDEX-rcp85',
            'CMIP6-ssp370' ,'CMIP6-LBC-ssp370']
    
        df1=dataframes[0]
        df1=add_column_for_plot(df1)
        reg=df1['mask'].unique()
        name1=reg[0]
        print('Bild fuer :', name1)
        sns.stripplot(x='xcategory', y=y_column, data=df1,dodge=True, color='black',alpha=0.7, jitter=0.3, size=4, order=xorder)
        sns.boxplot(x='xcategory', y=y_column, data=df1, whis=np.inf, palette=my_c,order=xorder, boxprops=dict(alpha=.8))
        plt.tick_params(bottom=False)
        plt.grid(True)
        plt.ylim(ymin,ymax)
        plt.axhline(0, color='black', lw=1.5)
        plt.tick_params(axis='y', labelsize=12)
        plt.tick_params(axis='x', labelsize=12, rotation=90)
        plt.ylabel(yname,fontsize=12)
        plt.xlabel(' ')#xname,fontsize=12)
        plt.title(name1.upper()+' '+title, color='k', fontsize=12) 
    else:
        for s in range(0,3):
            print('shape: ',dataframes[s].shape)
        fig, axs= plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True, figsize=(12,10)) #(12,18))
        xorder=['CMIP6-ssp126', 'CMIP6-LBC-ssp126', 'CMIP5-rcp26', 'CMIP5-CORDEX-rcp26', 'EURO-CORDEX-rcp26',
            'CMIP6-ssp245', 'CMIP6-LBC-ssp245', 'CMIP5-rcp45', 'CMIP5-CORDEX-rcp45', 'EURO-CORDEX-rcp45',
            'CMIP6-ssp585', 'CMIP6-LBC-ssp585', 'CMIP5-rcp85', 'CMIP5-CORDEX-rcp85', 'EURO-CORDEX-rcp85',
            'CMIP6-ssp370' ,'CMIP6-LBC-ssp370']
        df1=dataframes[0]
        df1=add_column_for_plot(df1)
        reg=df1['mask'].unique()
        name1=reg[0]
        print('Bild fuer :', name1)
        axs[0]=sns.stripplot(x='xcategory', y=y_column, data=df1,dodge=True, color='black',alpha=0.7, jitter=0.3, size=4, order=xorder,ax=axs[0])
        axs[0]=sns.boxplot(x='xcategory', y=y_column, data=df1, whis=np.inf, palette=my_c,order=xorder, boxprops=dict(alpha=.8),ax=axs[0])
        axs[0].tick_params(bottom=False)
        axs[0].grid(True)
        axs[0].set_ylim(ymin,ymax)
        axs[0].axhline(0, color='black', lw=1.5)
        axs[0].tick_params(axis='y', labelsize=12)
        axs[0].set_ylabel(name1+' '+yname,fontsize=12)
        axs[0].set_xlabel(' ')
        axs[0].set_title(title, color='k', fontsize=12) 
        # 2.
        df2=dataframes[1]
        df2=add_column_for_plot(df2)
        reg2=df2['mask'].unique()
        name2=reg2[0]
        print('Bild fuer :', name2)
        axs[1]=sns.stripplot(x='xcategory', y=y_column, data=df2,dodge=True, color='black',alpha=0.7, jitter=0.3, size=4, order=xorder,ax=axs[1])
        axs[1]=sns.boxplot(x='xcategory', y=y_column, data=df2, whis=np.inf, palette=my_c,order=xorder, boxprops=dict(alpha=.8),ax=axs[1])
        axs[1].tick_params(bottom=False)
        axs[1].grid(True)
        axs[1].set_ylim(ymin,ymax)
        axs[1].axhline(0, color='black', lw=1.5)
        axs[1].tick_params(axis='y', labelsize=12)
        axs[1].set_ylabel(name2+' '+yname,fontsize=12)
        axs[1].set_xlabel(' ')
        # 3.    
        df3=dataframes[2]
        df3=add_column_for_plot(df3)
        axs[2]=sns.stripplot(x='xcategory', y=y_column, data=df3,dodge=True, color='black',alpha=0.7, jitter=0.3, size=4, order=xorder,ax=axs[2])
        axs[2]=sns.boxplot(x='xcategory', y=y_column, data=df3, whis=np.inf, palette=my_c,order=xorder, boxprops=dict(alpha=.8),ax=axs[2])
        reg3=df3['mask'].unique()
        name3=reg3[0]
        print('Bild fuer :', name3)
        axs[2].grid(True)
        axs[2].set_ylim(ymin,ymax)
        axs[2].axhline(0, color='black', lw=1.5)
        axs[2].tick_params(axis='y', labelsize=12)
        axs[2].tick_params(axis='x', labelsize=12, rotation=90)
        axs[2].set_ylabel(name3+' '+yname,fontsize=12)
        axs[2].set_xlabel('')
    
    print('Plot will be : ',OutFile)
    plt.savefig(OutFile, bbox_inches='tight')    

    return

def strip_plot_historical(dataframes, y_column, var_dict, OutDataFile, OutFile, title):
    # Variable
    for parameter in var_dict.keys():
        varlongname = var_dict[parameter][0]
        var = var_dict[parameter][1]
        einheit = var_dict[parameter][2]
        ymin = var_dict[parameter][3][0]
        ymax = var_dict[parameter][3][1]

#---------------
# colors
#--------------
# Temperature 
    if var == 'tas':
       my_c= {'ANN-CMIP6':'tab:red',
              'ANN-CMIP6-LBC':'tab:pink',
              'ANN-CMIP5':'tab:blue',
              'ANN-CMIP5-CORDEX':'tab:cyan',
              'DJF-CMIP6':'tab:red',
              'DJF-CMIP6-LBC':'tab:pink',
              'DJF-CMIP5':'tab:blue',
              'DJF-CMIP5-CORDEX':'tab:cyan',
              'MAM-CMIP6':'tab:red',
              'MAM-CMIP6-LBC':'tab:pink',
              'MAM-CMIP5':'tab:blue',
              'MAM-CMIP5-CORDEX':'tab:cyan',
              'JJA-CMIP6':'tab:red',
              'JJA-CMIP6-LBC':'tab:pink',
              'JJA-CMIP5':'tab:blue',
              'JJA-CMIP5-CORDEX':'tab:cyan',
              'SON-CMIP6':'tab:red',
              'SON-CMIP6-LBC':'tab:pink',
              'SON-CMIP5':'tab:blue',
              'SON-CMIP5-CORDEX':'tab:cyan'
              }
# Precipitation
    if var == 'pr': 
       my_c= {'ANN-CMIP6': 'xkcd:lime',
              'ANN-CMIP6-LBC': 'xkcd:gold',
              'ANN-CMIP5': 'xkcd:green',
              'ANN-CMIP5-CORDEX':'xkcd:lime',
              'DJF-CMIP6':'xkcd:lime',
              'DJF-CMIP6-LBC':'xkcd:gold',
              'DJF-CMIP5':'xkcd:green',
              'DJF-CMIP5-CORDEX':'xkcd:lime',
              'MAM-CMIP6':'xkcd:lime',
              'MAM-CMIP6-LBC':'xkcd:gold',
              'MAM-CMIP5':'xkcd:green',
              'MAM-CMIP5-CORDEX':'xkcd:lime',
              'JJA-CMIP6':'xkcd:lime',
              'JJA-CMIP6-LBC':'xkcd:gold',
              'JJA-CMIP5':'xkcd:green',
              'JJA-CMIP5-CORDEX':'xkcd:lime',
              'SON-CMIP6':'xkcd:lime',
              'SON-CMIP6-LBC':'xkcd:gold',
              'SON-CMIP5':'xkcd:green',
              'SON-CMIP5-CORDEX':'xkcd:lime'
              }

    yname=varlongname+' ['+einheit +']'

    for s in range(0,3):
        print('shape: ',dataframes[s].shape)

    fig, axs= plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True, figsize=(12,10))
   
    xorder=['ANN-CMIP6', 'ANN-CMIP6-LBC', 'ANN-CMIP5', 'ANN-CMIP5-CORDEX', 'DJF-CMIP6',
             'DJF-CMIP6-LBC','DJF-CMIP5','DJF-CMIP5-CORDEX','MAM-CMIP6','MAM-CMIP6-LBC', 
             'MAM-CMIP5','MAM-CMIP5-CORDEX','JJA-CMIP6','JJA-CMIP6-LBC', 'JJA-CMIP5',
             'JJA-CMIP5-CORDEX','SON-CMIP6', 'SON-CMIP6-LBC', 'SON-CMIP5', 'SON-CMIP5-CORDEX']
    
    df1=dataframes[0] 
    print('hier:','xcategory') 
    print(df1)
    print('hier=',df1[y_column])
    df1=add_column_for_plot_season(df1)
    print('xorder',df1)
    reg1=df1['mask'].unique()
    name1=reg1[0]
    axs[0]=sns.stripplot(x='xcategory', y=y_column, data=df1,dodge=True, color='black',alpha=0.7, jitter=0.3, size=3, order=xorder,ax=axs[0])
    axs[0]=sns.boxplot(x='xcategory', y=y_column, data=df1, whis=np.inf, palette=my_c,order=xorder, boxprops=dict(alpha=1),ax=axs[0])
    axs[0].tick_params(bottom=False)
    axs[0].grid(True)
    axs[0].set_ylim(ymin,ymax)
    axs[0].axhline(0, color='black', lw=1.5)
    axs[0].tick_params(axis='y', labelsize=12)
    axs[0].set_ylabel(name1+' '+yname,fontsize=12)
    axs[0].set_xlabel(' ')
    axs[0].set_title(title, color='k', fontsize=12) 

    # 2.
    df2=dataframes[1]
    df2=add_column_for_plot_season(df2)
    reg2=df2['mask'].unique()
    name2=reg2[0]
    name2='WCE'
    axs[1]=sns.stripplot(x='xcategory', y=y_column, data=df2,dodge=True, color='black',alpha=0.7, jitter=0.3, size=3, order=xorder,ax=axs[1])
    axs[1]=sns.boxplot(x='xcategory', y=y_column, data=df2, whis=np.inf, palette=my_c,order=xorder, boxprops=dict(alpha=1),ax=axs[1])
    axs[1].tick_params(bottom=False)
    axs[1].grid(True)
    axs[1].set_ylim(ymin,ymax)
    axs[1].axhline(0, color='black', lw=1.5)
    axs[1].tick_params(axis='y', labelsize=12)
    axs[1].set_ylabel(name2+' '+yname,fontsize=12)
    axs[1].set_xlabel(' ')

    # 3.    
    df3=dataframes[2]
    df3=add_column_for_plot_season(df3)       
    axs[2]=sns.stripplot(x='xcategory', y=y_column, data=df3 ,dodge=True, color='black',alpha=0.7, jitter=0.3, size=3, order=xorder,ax=axs[2])
    axs[2]=sns.boxplot(x='xcategory', y=y_column, data=df3 , whis=np.inf, palette=my_c,order=xorder, boxprops=dict(alpha=1),ax=axs[2])
    reg3=df3['mask'].unique()
    name3=reg3[0]
    axs[2].grid(True)
    axs[2].set_ylim(ymin,ymax)
    axs[2].axhline(0, color='black', lw=1.5)
    axs[2].tick_params(axis='y', labelsize=12)
    axs[2].tick_params(axis='x', labelsize=12, rotation=90)
    axs[2].set_ylabel(name3+' '+yname,fontsize=12)
    axs[2].set_xlabel('')
    print('Plot will be : ',OutFile)
    plt.savefig(OutFile, bbox_inches='tight')    

    return

def sub_era(df,era5di,region,timehist):
    Era_tp='df_ERA5_'+region+'_Reanalysis_'+timehist+'_tp.csv'
    Era_2t='df_ERA5_'+region+'_Reanalysis_'+timehist+'_2t.csv'
    
    InEra_tp=os.path.join(era5di,Era_tp)
    InEra_2t=os.path.join(era5di,Era_2t)
    df_era5_tp=pd.read_csv(InEra_tp ,index_col='model_member')
    df_era5_2t=pd.read_csv(InEra_2t ,index_col='model_member')
    
    dfdiff=pd.DataFrame()
    
    colm=['ANN','DJF','MAM','JJA','SON']
    for c in range(5):
         col=colm[c]
         valueT=df_era5_2t.iloc[0][col]
         valueP=df_era5_tp.iloc[0][col]
         print('value ERA5= ', valueT, valueP)
         sel=df.loc[(df['season'] == col)]
         sel['diff_tas'] = sel['tas_1981-01-01 to 2010-12-31']-valueT
         sel['diff_pr'] = (sel['pr_1981-01-01 to 2010-12-31']-valueP)*86400 # change unit [mm/day]
         sel['pro_diff_pr'] = (sel['pr_1981-01-01 to 2010-12-31']-valueP)*100/valueP # [%]
         # nur die season wieder hinter einander
         dfdiff=pd.concat([sel,dfdiff],axis=0)
    
    return(dfdiff)
