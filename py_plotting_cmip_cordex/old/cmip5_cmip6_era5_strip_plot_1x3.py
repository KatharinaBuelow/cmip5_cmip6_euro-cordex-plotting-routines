#! /usr/bin/python
# coding: utf-8
import numpy as np
import glob
import matplotlib.pyplot as plt
import subprocess
import os
from matplotlib import markers
from scattertable2 import scattertable
import pandas as pd
import seaborn as sns

def minMaxP(x):
    ''' caluclates statistical values of the whole datafram (need to be float)'''
    return pd.Series(index=['min','P50','max'],data=[x.min(),x.quantile(0.5),x.max()])

def make_table_muell(dataframes, ycoln, var_dict, OutDataFile):
# funktioniert nicht
    for n in range(len(dataframes)):
        df=dataframes[n]
        df=add_column_for_plot(df)
        reg=df['mask'].unique()
        name=reg[0]
        print('Tabel fuer :', name ,' and ', ycoln)
        for i in df['xcategory'].unique():
            sel=df.loc[(df['xcategory'] == i)]
            sel1=sel[ycoln]
            print( sel1 )
            #ft=sel1.apply(minMaxP)
            #rint(dft)
        return

def make_table(dataframes, ycoln, var_dict, OutDataFile):
    
    for n in range(len(dataframes)):
        df=dataframes[n]
        df=add_column_for_plot(df)
        reg=df['mask'].unique()
        name=reg[0]
        print('Tabel fuer :', name ,' and ', ycoln)
        print('Minimum')
        print(name, df.groupby(by=['xcategory'])[ycoln].min())
        print('Median')
        print(name, df.groupby(by=['xcategory'])[ycoln].quantile(0.5))
        print('Maximum')
        print(name, df.groupby(by=['xcategory'])[ycoln].max())
# to do
# wie kann ich es speichern

       
    return

def add_column_for_plot(df):
    ''' add column for CMIP-mini-ensembel ...'''
    
    eurocordex = scattertable('cordex-gcm')
    cmip6_lbc = scattertable('cmip6-gcm-lbc')
    
    # CMIP5: Create column with names , which equal the names in list CORDEX_GCM /cmip6-gcm-lbc :
    df['model_member_experiment_id'] = df['model_member'].str.cat(df['experiment_id'],sep="_")  
    df['experimentn'] = df['model_member_experiment_id'].map(eurocordex)
    df['experiment1'] = [x if x == 'CMIP5-EURO-CORDEX' else z for x,z in zip(df['experimentn'],df['project_id'])]
    # clean up
    df.drop(['experimentn'], inplace=True, axis=1)
    # the runs which are in the Ensemble with LBC are also in the ensemble of CMIP, so they have to occure twice
    sel=df.loc[(df['experiment1'] == 'CMIP5-EURO-CORDEX')]
    sel['experiment1']= 'CMIP5'
    dfn=df.append(sel)
    # CMIP5-EURO-CORDEX was just a too long name
    dfn['experiment1']= ['CMIP5-CORDEX' if x=='CMIP5-EURO-CORDEX' else x for x in dfn['experiment1']]
    
    # CMIP6: Create column with names , which equal the names in list CORDEX_GCM /cmip6-gcm-lbc :
    #print(dfn['model_member_experiment_id'])
    dfn['experimentn'] = dfn['model_member_experiment_id'].map(cmip6_lbc)
    dfn['experiment'] = [x if x == 'CMIP6-LBC' else z for x,z in zip(dfn['experimentn'],dfn['experiment1'])]
    #print('df_experiment =', dfn['experiment'].unique())
    # clean up
    dfn.drop(['experimentn'], inplace=True, axis=1)
    dfn.drop(['experiment1'], inplace=True, axis=1)
    # the runs which are in the Ensemble with LBC are also in the ensemble of CMIP, so they have to occure twice
    sel=dfn.loc[(dfn['experiment'] == 'CMIP6-LBC')]
    sel['experiment']= 'CMIP6'
    df=dfn.append(sel)
    
    df['xcategory']=df['season'].str.cat(df['experiment'],sep="-")
    return(df)


def strip_plot(dataframes, y_column, var_dict, OutDataFile, OutFile, title):

    # Variable
    for parameter in var_dict.keys():
        varlongname = var_dict[parameter][0]
        var = var_dict[parameter][1]
        print(parameter, varlongname, var)
        einheit = var_dict[parameter][2]
        ymin = var_dict[parameter][3][0]
        ymax = var_dict[parameter][3][1]
        #funktioniert nochnicht
        ctable= var_dict[parameter][7]
        
        print('y_column = ', y_column)
        
    # hat nicht funktionier muss noch eingebaut werden
    #colors = scattertable('colors')
    #print (colors)
       
    my_t= {'ANN-CMIP6':'tab:red',
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
    my_c= {'ANN-CMIP6':'tab:brown',
           'ANN-CMIP6-LBC':'xkcd:gold',
           'ANN-CMIP5':'xkcd:green',
           'ANN-CMIP5-CORDEX':'xkcd:lime',
           'DJF-CMIP6':'tab:brown',
           'DJF-CMIP6-LBC':'xkcd:gold',
           'DJF-CMIP5':'xkcd:green',
           'DJF-CMIP5-CORDEX':'xkcd:lime',
           'MAM-CMIP6':'tab:brown',
           'MAM-CMIP6-LBC':'xkcd:gold',
           'MAM-CMIP5':'xkcd:green',
           'MAM-CMIP5-CORDEX':'xkcd:lime',
           'JJA-CMIP6':'tab:brown',
           'JJA-CMIP6-LBC':'xkcd:gold',
           'JJA-CMIP5':'xkcd:green',
           'JJA-CMIP5-CORDEX':'xkcd:lime',
           'SON-CMIP6':'tab:brown',
           'SON-CMIP6-LBC':'xkcd:gold',
           'SON-CMIP5':'xkcd:green',
           'SON-CMIP5-CORDEX':'xkcd:lime'
           }

    
    print('my_c : ',my_c)
    yname=varlongname+' ['+einheit +']'
    print('')
    print('')
    print('Uebergabe der dataframes:')
    print('')
    for s in range(0,3):
        print('shape: ',dataframes[s].shape)
    #fig = plt.figure(figsize=(12, 8))  #6,6

    fig, axs= plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True, figsize=(12,10)) #(12,18))
   
    xorder=['ANN-CMIP6', 'ANN-CMIP6-LBC', 'ANN-CMIP5', 'ANN-CMIP5-CORDEX', 'DJF-CMIP6',
             'DJF-CMIP6-LBC','DJF-CMIP5','DJF-CMIP5-CORDEX','MAM-CMIP6','MAM-CMIP6-LBC', 
             'MAM-CMIP5','MAM-CMIP5-CORDEX','JJA-CMIP6','JJA-CMIP6-LBC', 'JJA-CMIP5',
             'JJA-CMIP5-CORDEX','SON-CMIP6', 'SON-CMIP6-LBC', 'SON-CMIP5', 'SON-CMIP5-CORDEX']
    
    df1=dataframes[0]
    
    df1=add_column_for_plot(df1)
    reg1=df1['mask'].unique()
    name1=reg1[0]
    print('Bild fuer :', name1)
    print(df1['xcategory'],df1[y_column])
    axs[0]=sns.stripplot(x='xcategory', y=y_column, data=df1,dodge=True, color='black',alpha=0.7, jitter=0.3, size=3, order=xorder,ax=axs[0])
    axs[0]=sns.boxplot(x='xcategory', y=y_column, data=df1, whis=np.inf, palette=my_c,order=xorder, boxprops=dict(alpha=1),ax=axs[0])
    axs[0].tick_params(bottom=False)
    axs[0].grid(True)
    axs[0].set_ylim(ymin,ymax)
    axs[0].axhline(0, color='black', lw=1.5)
    axs[0].tick_params(axis='y', labelsize=12)
    #plt.tick_params(axis='x', labelsize=12)
    #plt.xticks(rotation=90)
    axs[0].set_ylabel(name1+' '+yname,fontsize=12)
    axs[0].set_xlabel(' ')#xname,fontsize=12)
    axs[0].set_title(title, color='k', fontsize=12) 

    # 2.
    df2=dataframes[1]
    df2=add_column_for_plot(df2)
    reg2=df2['mask'].unique()
    name2=reg2[0]
    name2='WCE'
    print('Bild fuer :', name2)
    axs[1]=sns.stripplot(x='xcategory', y=y_column, data=df2,dodge=True, color='black',alpha=0.7, jitter=0.3, size=3, order=xorder,ax=axs[1])
    axs[1]=sns.boxplot(x='xcategory', y=y_column, data=df2, whis=np.inf, palette=my_c,order=xorder, boxprops=dict(alpha=1),ax=axs[1])
    axs[1].tick_params(bottom=False)
    axs[1].grid(True)
    axs[1].set_ylim(ymin,ymax)
    axs[1].axhline(0, color='black', lw=1.5)
    axs[1].tick_params(axis='y', labelsize=12)
    #plt.tick_params(axis='x', labelsize=12)
    #plt.xticks(rotation=90)
    axs[1].set_ylabel(name2+' '+yname,fontsize=12)
    axs[1].set_xlabel(' ')#xname,fontsize=12)

    # 3.    
    df3=dataframes[2]
    df3=add_column_for_plot(df3)
       
    axs[2]=sns.stripplot(x='xcategory', y=y_column, data=df3 ,dodge=True, color='black',alpha=0.7, jitter=0.3, size=3, order=xorder,ax=axs[2])
    axs[2]=sns.boxplot(x='xcategory', y=y_column, data=df3 , whis=np.inf, palette=my_c,order=xorder, boxprops=dict(alpha=1),ax=axs[2])
    reg3=df3['mask'].unique()
    name3=reg3[0]
    print('Bild fuer :', name3)
    axs[2].grid(True)
    axs[2].set_ylim(ymin,ymax)
    axs[2].axhline(0, color='black', lw=1.5)
    axs[2].tick_params(axis='y', labelsize=12)
    axs[2].tick_params(axis='x', labelsize=12, rotation=90)
    #ax3.set_xticks(rotation=90)
    axs[2].set_ylabel(name3+' '+yname,fontsize=12)
    axs[2].set_xlabel('')#xname,fontsize=12)
    print(df3)
    print('Plot will be : ',OutFile)
    plt.savefig(OutFile, bbox_inches='tight')    

    return


def sub_era(df,era5di,region,timehist):
    Era_tp='df_ERA5_'+region+'_Reanalysis_'+timehist+'_tp.csv'
    Era_2t='df_ERA5_'+region+'_Reanalysis_'+timehist+'_2t.csv'
    print(Era_tp)
    print(Era_2t)
    InEra_tp=os.path.join(era5di,Era_tp)
    InEra_2t=os.path.join(era5di,Era_2t)
    df_era5_tp=pd.read_csv(InEra_tp ,index_col='model_member')
    df_era5_2t=pd.read_csv(InEra_2t ,index_col='model_member')
    
    dfdiff=pd.DataFrame()
    print('size of df= ',df.shape)
    colm=['ANN','DJF','MAM','JJA','SON']
    for c in range(5):
         col=colm[c]
         valueT=df_era5_2t.iloc[0][col]
         valueP=df_era5_tp.iloc[0][col]
         print('value= ', valueT, valueP)
         sel=df.loc[(df['season'] == col)]
         sel['diff_tas'] = sel['tas_1981-01-01 to 2010-12-31']-valueT
         sel['diff_pr'] = (sel['pr_1981-01-01 to 2010-12-31']-valueP)*86400 # change unit [mm/day]
         sel['pro_diff_pr'] = (sel['pr_1981-01-01 to 2010-12-31']-valueP)*100/valueP # [%]
         # nur die season wieder hinter einander
         dfdiff=pd.concat([sel,dfdiff],axis=0)
    print('size of diff= ',dfdiff.shape)
    return(dfdiff)



def main(filename, era5di, columns, var_dict):
    ''' collect, what you want to plot '''

    mip=['CMIP5','CMIP6'] #,'EURO-CORDEX']

    timehist  =  '1981-01-01_to_2010-12-31'
    timeslice = ['2036-01-01_to_2065-12-31',
		 '2070-01-01_to_2099-12-31', 
                ]
    timehistp  =  '(1981 to 2010)'
    timeslicep = ['(2036 to 2065)',
		 '(2070 to 2099)', 
                 ]
    
    seasons = ('JJA','DJF','ANN', 'MAM', 'SON')
    sce =('historical',)

   # Variable 
    for parameter in var_dict.keys():
        var = var_dict[parameter][1]
        einheit = var_dict[parameter][2]
        regions=var_dict[parameter][4]
        ycoln = var_dict[parameter][5]
        titlevar = var_dict[parameter][6]
        print('regions: ',regions)
                                 
    for i in range(len(regions)):
        print('region: ',regions[i])
        df=pd.DataFrame()
        for m in range(len(mip)):
            print(m)
            for s in range(len(seasons)):
                print('season:', seasons[s])
                timean=timehist.replace('_',' ')    
                # infile, concat dataframe
                FileName='df_'+mip[m]+'_'+seasons[s]+'_'+regions[i]+'_'+sce[0]+'_'+timehist+'.csv'
                print(FileName)
                InFile=os.path.join(datadi,FileName)
                InData = pd.read_csv(InFile)
                df=pd.concat([df,InData],axis=0)
        
        dfname='df_'+regions[i]
        if dfname == 'df_NEU':
            df_NEU=sub_era(df,era5di,'NEU',timehist)
            print(dfname,' : ',df_NEU.shape)
        if dfname == 'df_CEU':
            df_CEU=sub_era(df,era5di,'CEU',timehist)
            print(dfname,' : ',df_CEU.shape)
        if dfname == 'df_MED':
            df_MED=sub_era(df,era5di,'MED',timehist)
            print(dfname,' : ',df_MED.shape)

    dataframes=[df_NEU,df_CEU,df_MED]        
    title= timehistp+' '+titlevar +' Bias to ERA5'
    print(title)
    PlotName=ycoln+'_SREX_'+timehist+'_cmip-era5.png'
    OutFile=os.path.join(plotdi,PlotName)
    OutDataFile=os.path.join(plotdi.replace('plots','data'),PlotName.replace('png','csv'))
    # hier plotten
    strip_plot(dataframes, ycoln, var_dict, OutDataFile, OutFile, title)
    make_table(dataframes, ycoln, var_dict, OutDataFile)   
           
if __name__ == '__main__':
    
    #does not make sense to do pr % bias for MED:
    #var_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', '%', (-100,100),('NEU','CEU','MED') ,'pro_diff_pr', 'Precipitation'],}
    var_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', 'mm/day', (-2.2,2.2), ('NEU','CEU','MED'), 'diff_pr','Precipitation','my_p'],}
    #var_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', (-10 , 10),('NEU','CEU','MED'),'diff_tas', 'Temperatur','my_t']}
    #var2_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', (-2 , 10),('BI','IP','FR','ME','SC','AL','MD','EA'),40,],}

    #var2_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', (-2 , 10),('deutschland',),40],}


    datadi='/work/ch0636/g300047/dataprocessing_cmip5_cmip6/SCATTER/data/'	
    plotdi='/work/ch0636/g300047/dataprocessing_cmip5_cmip6/STRIPPLOT/plots/'
    era5di='/work/ch0636/g300047/dataprocessing_cmip5_cmip6/HEATMAP/data/ERA5/'

    main(datadi, era5di, plotdi, var_dict)
