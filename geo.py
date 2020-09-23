# -*- coding: utf-8 -*-
import pandas as pd
from geopandas import GeoSeries, GeoDataFrame, read_file
from shapely.geometry import Point
import helper
import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from plotly.tools import mpl_to_plotly

def saveImages():
    print ('savingImages')
    geoData = read_file(r'static/Admin2.shp')
    geoList = geoData.sort_values(by='ST_NM').ST_NM.unique()
    
    stateapi = 'https://api.covid19india.org/states_daily.json'
    stateData = requests.get(stateapi).json()
    stateDf = pd.DataFrame(stateData['states_daily'])
    
    stateDfConfirmed = stateDf[stateDf['status'] == 'Confirmed'].fillna(0).replace('',0)
    stateDfRecovered = stateDf[stateDf['status'] == 'Recovered'].fillna(0).replace('',0)
    stateDfDeceased = stateDf[stateDf['status'] =='Deceased'].fillna(0).replace('',0)
    
    stateTotalConfirmed =[] 
    stateTotalDeceased =[]
    stateTotalRecovered =[]
    listStates = []
    for col in stateDf:
        if col not in ['date','status']:
            listStates.append(col)
    #         print (col)
            stateTotalConfirmed.append(np.sum(stateDfConfirmed[col].apply(lambda x: int(x))))
            stateTotalDeceased.append(np.sum(stateDfDeceased[col].apply(lambda x: int(x))))
            stateTotalRecovered.append(np.sum(stateDfRecovered[col].apply(lambda x:int(x))))
            
    data = {'State':listStates, 'Confirmed':stateTotalConfirmed, 'Deceased':stateTotalDeceased, 'Recovered':stateTotalRecovered}
    
    fullData  = pd.DataFrame(data=data)
    fullData['Decease%'] = round((fullData['Deceased']/fullData['Confirmed'])*100,2)
    fullData['Recover%'] = round((fullData['Recovered']/fullData['Confirmed'])*100,2)
    fullData['Active%'] = round(((fullData['Confirmed'] -(fullData['Recovered']+fullData['Deceased']))/fullData['Confirmed'])*100,2)
    
    dict ={}
    for i,_ in enumerate(listStates):
        try:
            dict[_] = geoList[i]
        except IndexError:
            dict[_] = ""
            
    dict = helper.dict
    fullData['ST_NM'] = fullData['State'].map(dict)
    geoFullData  = geoData.merge(fullData[['Decease%','ST_NM','Recover%','Active%']], on='ST_NM', how='outer')
    geoFullData = geoFullData.dropna(subset=['geometry'])
    geoFullData['coords'] = geoFullData['geometry'].apply(lambda x: x.representative_point().coords[:])
    geoFullData['coords'] = [coords[0] for coords in geoFullData['coords']]
    #fig = plt.figure()
    
    
    #fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True, sharey=True)
    geoFullData.plot( figsize=(12,7), column='Active%', legend=True,cmap='RdYlGn_r');
    for idx, row in geoFullData.iterrows():
        plt.annotate(s=row['Active%'],xy=row['coords'], horizontalalignment='center')
     
    plt.title('Active Cases Per 100 People Infected -'+str(dt.datetime.now()));
    plt.savefig('static/active.png')
    
    geoFullData.plot(figsize=(12,7), column='Recover%', legend=True,cmap='RdYlGn');
    for idx, row in geoFullData.iterrows():
        plt.annotate(s=row['Recover%'],xy=row['coords'], horizontalalignment='center')
     
    plt.title('Recoveries Per 100 People Infected- '+str(dt.datetime.now()));
    plt.savefig('static/recovery.png')
    
if __name__ == '__main__':
    saveImages()
    




