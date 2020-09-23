import pandas as pd
#import numpy as np
import requests

from helper import dict
# -*- coding: utf-8 -*-
api = 'https://api.covid19india.org/states_daily.json'
resp = requests.get(api)

stateDf = pd.DataFrame(resp.json()['states_daily'])
state_ut = list(set(stateDf.columns) - set(['status','tt','date']))

dict = dict


transformedDf = pd.DataFrame()

# transformedDf.columns = ['Count','Status','date','State']
transformedDf = stateDf[['ap','status','date']]
transformedDf['State'] = dict['ap']
transformedDf.columns = ['Count','Status','date','State']


for state in set(state_ut)-set('ap'):
  print ('Processing {}'.format(state))
  tempDf = pd.DataFrame()
  tempDf = stateDf[[state,'status','date']]
  tempDf.columns = ['Count','Status','date']
  tempDf['State'] = dict[state]
  print (tempDf.head(2))
  transformedDf = transformedDf.append(tempDf)
  
  
transformedDf.to_excel('CovidStateTrend.xlsx',index=False)