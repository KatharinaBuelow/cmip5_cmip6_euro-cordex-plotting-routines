#! /usr/bin/python
# coding: utf-8
import numpy
import glob
import matplotlib.pyplot as plt
import subprocess
import os
from matplotlib import markers
from scattertable import scattertable
import pandas as pd
import seaborn as sns

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
       
def add_column_for_plot(df,rcp):
    ''' add column for color ...'''

    eurocordex = scattertable('cordex-gcm')
    rcpeurocordex = scattertable('rcp-cordex-gcm')
    #Create column with names , which equal the names in list CORDEX_GCM :
    df['model_member_experiment_id'] = df['model_member'].str.cat(df['experiment_id'],sep="_")
    df['experimentn'] = df['model_member_experiment_id'].map(eurocordex)
    df['experiment'] = [x if x == 'CMIP5-CORDEX' else z for x,z in zip(df['experimentn'],df['project_id'])]
    # clean up
    df.drop(['experimentn'], axis=1)

    # if all scenarios are plotted, the color of CORDEX should not change
    print('rcp fuer if =',rcp)
    if rcp != 'all':
        #print('gehe in if schleife')rcpeurocordex ist doch unnoetig?
        #df['experimentnn'] = df['model_member_experiment_id'].map(rcpeurocordex)
        df['experimentnn'] = df['model_member_experiment_id'].map(eurocordex)
        df['experimentnnn'] = df['experiment_id'].str.cat(df['experimentnn'],sep="-")
        df['Scenario'] = [x if x == 'CMIP5-CORDEX' else z for x,z in zip(df['experimentnn'],df['experiment_id'])]
        df['Scenario'] = [z if x == 'CMIP5-CORDEX' else y for x,y,z in zip(df['experimentnn'],df['experiment_id'],df['experimentnnn'])]
        
        print (df['Scenario'])
        # clean up
        print('hier')
        df.drop(['experimentnn'], axis=1)
        df.drop(['experimentnnn'], axis=1)
        # needs to be fixed
    else:
        df['Scenario'] = df['experiment_id']
    
    return(df)


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

    add_column_for_plot(df,rcp)
    dfm=add_mean(df)

    df2=df.loc[(df['experiment'] == 'CMIP5-CORDEX')]
    colors = scattertable('colors')
    marker = scattertable('marker') 
    
    # this is a dirty solution
    # edgecolor does not take a dict (I think)
    print('rcp=', rcp)
    # vielleicht
    #edgecolor=colors.get(rcp)
    edgecolor="none"
   
    # rename column (nicer in plot)
    #df.rename({'experiment_id' : 'Scenario'},axis=1, inplace=True)
    df.rename({'experiment' : 'Experiment'},axis=1, inplace=True)
    df2.rename({'experiment' : 'Experiment'},axis=1, inplace=True)
    dfm.rename({'experiment' : 'Experiment'},axis=1, inplace=True)
    df=pd.concat([df,dfm],axis=0) # only to get the symbol in the legend

    # Achsen
    xname=varlongname1+' ['+einheit1+']'
    yname=varlongname2+' ['+einheit2 +']'
    #reihe={'EURO-CORDEX','ssp126','rcp26'}
    #fig = plt.gcf() 
    #fig.set_size_inches(6,6)   #(12, 8)
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
    plt.title(title, color='k', fontsize=12) #, y=1.08)
    #handles, labels = ax.get_legend_handles_labels()
    #ax.legend(handles=handles[1:], labels=labels[1:])
    #plt.legend(loc='best')#'upper right') 
    #plt.show ()
    print('Plot will be : ',OutFile)
    plt.savefig(OutFile, bbox_inches="tight")    
                  
    return

     
def main(filename, columns, var1_dict, var2_dict):
    ''' collect, what you want to plot '''

    rcp = ['rcp26', 'rcp45', 'rcp85']
    ssp = ['ssp126','ssp245','ssp585']

    timehist  =  '1981-01-01_to_2010-12-31'
    timeslice = ['2036-01-01_to_2065-12-31',
		 '2070-01-01_to_2099-12-31', 
                 ]
    timehistp  =  '(1981 to 2010)'
    timeslicep = ['(2036 to 2065)',
		 '(2070 to 2099)', 
                 ]
    
    seasons = ('JJA','DJF','ANN', 'MAM', 'SON')

    # Variable 1 pr
    for parameter in var1_dict.keys():
        var1 = var1_dict[parameter][1]
        einheit1 = var1_dict[parameter][2]
        version = var1_dict[parameter][4]
        xcoln = var1_dict[parameter][5]

    # Variable 2 tas
    for parameter in var2_dict.keys():
        var2 = var2_dict[parameter][1]
        einheit2 = var2_dict[parameter][2]
        regions=var2_dict[parameter][4]
        print('regions: ',regions)


    for i in range(len(regions)):
        print('region: ',regions[i])
        reg=regions[i]
        reg=reg.replace('CEU','WCE')
        for seas in seasons:
            print('season:',seas)
            for r in range(len(rcp)):
                print('scenario:', rcp[r],ssp[r])
                for time in range(len(timeslice)):
                    print(timeslice[time])
                    timen=timeslice[time].replace('_',' ')
                    title= reg.upper()+' '+seas+' '+timeslicep[time]+' - '+timehistp
                    print(title)
                    # infile, concat dataframe
                    FileName5='df_CMIP5_'+seas+'_'+regions[i]+'_'+rcp[r]+'_'+timeslice[time]+'.csv'
                    print(FileName5)
                    FileName6='df_CMIP6_'+seas+'_'+regions[i]+'_'+ssp[r]+'_'+timeslice[time]+'.csv'
                    print(FileName6)
                    InFile5=os.path.join(datadi,FileName5)
                    InFile6=os.path.join(datadi,FileName6)
                    PlotName='CMIP5_CMIP6_'+var2+'_'+var1+'_'+version+'_'+regions[i]+'_'+seas+'_'+rcp[r]+'_'+ssp[r]+'_'+timeslice[time]+'.png'
                    OutFile=os.path.join(plotdi,PlotName)
                    
                    InData5 = pd.read_csv(InFile5)
                    InData6 = pd.read_csv(InFile6) 
                    df=pd.DataFrame()
                    df=pd.concat([InData6,InData5],axis=0)
                    x_column=xcoln+timen
                    if xcoln == 'diff_pr_':
                        df[x_column]=df[x_column]*86400 # needed to plot mm, data is in kg m-2s-1
                    y_column='diff_tas_'+timen
                    scatter_plot(df, x_column, y_column, rcp[r], ssp[r], var1_dict, var2_dict, OutFile, title)
                    
if __name__ == "__main__":

    #var1_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', '%', (-70,70), 'pro','pro_diff_pr_'],}
    var1_dict = {'Precipitation':[r'$\Delta$' +' Precipitation', 'pr', 'mm/day', (-1.5,1.5), 'mm', 'diff_pr_'],}
    var2_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', (-2 , 11),('MED','CEU','NEU'),60],}
   # var2_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', (-2 , 10),('BI','IP','FR','ME','SC','AL','MD','EA'),80],}
    #var2_dict = {'Temperature':[r'$\Delta$' +' Temperature', 'tas', 'K', (-2 , 10),('deutschland',), 80],}


    datadi='/work/ch0636/g300047/dataprocessing_cmip5_cmip6/SCATTER/data/'      
    plotdi='/work/ch0636/g300047/dataprocessing_cmip5_cmip6/SCATTER/plots-D-test/'
	
    main(datadi, plotdi, var1_dict, var2_dict)


