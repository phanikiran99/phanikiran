# -*- coding: utf-8 -*-
#plotly
import plotly.graph_objects as go
#data
import pandas as pd
import numpy as np
#api
import requests

from dateutil import parser
import dash_html_components as html

#import math

# get the data
api = 'https://api.covid19india.org/data.json'
resp = requests.get(api)

stateapi = 'https://api.covid19india.org/states_daily.json'
stateData = requests.get(stateapi).json()
stateDf = pd.DataFrame(stateData['states_daily'])
confirmed_trend = stateDf[stateDf['status'] == 'Confirmed']
recovered_trend = stateDf[stateDf['status'] == 'Recovered']


state_ut = list(set(confirmed_trend.columns) - set(['status','tt','date']))


caseTimeSeries = pd.DataFrame(resp.json()['cases_time_series'])  # timeseries data
stateWise = pd.DataFrame(resp.json()['statewise']) # statewise
tested = pd.DataFrame(resp.json()['tested']) # test statistics



eventTimeline ={'What':['First Case - 30th January <br>','LockDown 1.0 - 25th March <br>100 Cases/day','2.0 Extended<br> 1000 cases/day ',
                        '3.0 extended<br> 2.5k Cases/day','4.0 extended<br> 5K/day ',
                        'Unlock 1.0 on June 1st <br> <b>7k Cases/Day','Unlock 2.0 <br> 15k/Day<br>','Unlock 4.0 <br> ~90k Cases/Day'],
'When':['30 January','25 March','14 April','01 May','17 May','01 June','01 July','01 Sept']}

delta = []
for value in eventTimeline['When']:
  delta.append((parser.parse(value) - parser.parse('30 January')).days)
eventTimeline['delta'] = delta


#total statistics, Daily Cases trends 
fig = go.Figure()

fig.add_trace(go.Scatter(x=caseTimeSeries['date'], y=caseTimeSeries['totalconfirmed'], name='Total Confirmed',marker_color='LightGrey'))
fig.add_trace(go.Scatter(x=caseTimeSeries['date'], y=caseTimeSeries['totalrecovered'], name='Total Recovered',marker_color='LightGrey'))
fig.add_trace(go.Scatter(x=caseTimeSeries['date'], y=caseTimeSeries['totalconfirmed'].map(int)-(caseTimeSeries['totalrecovered'].map(int)+ caseTimeSeries['totaldeceased'].map(int))
                                          , name='Total Active',marker_color='#E7717D',mode='lines+text'))
fig.add_trace(go.Scatter(x=caseTimeSeries['date'], y=caseTimeSeries['totaldeceased'], name='Total Deceased',marker_color='LightGrey'))
#fig.add_trace(go.Bar(x=caseTimeSeries['date'], y=caseTimeSeries['dailyconfirmed'], name='Daily Confirmed'))


fig.add_annotation(x=caseTimeSeries['date'].iloc[-1],
                   y=caseTimeSeries['totalconfirmed'].map(int).max(),
                   text='Confirmed')

fig.add_annotation(x=caseTimeSeries['date'].iloc[-1],
                   y=caseTimeSeries['totalrecovered'].map(int).max(),
                   text='Recovered')

fig.add_annotation(x=caseTimeSeries['date'].iloc[-1],
                   y=caseTimeSeries['totaldeceased'].map(int).max(),
                   text='Deceased')

fig.add_annotation(x=caseTimeSeries['date'].iloc[-1],
                   y=(caseTimeSeries['totalconfirmed'].map(int)-(caseTimeSeries['totalrecovered'].map(int)+ caseTimeSeries['totaldeceased'].map(int))).iloc[-1],
                   text='Active',font={'color':'Crimson'})

fig.add_annotation(x=(caseTimeSeries['date'].iloc[-100]),
                   y=caseTimeSeries['totalconfirmed'].map(int).max()/1.6,
                   text=str(caseTimeSeries['totalconfirmed'].map(int).max()) + ' Total',
                   font=dict(
            
            size=64,
            color="#E7717D"
            ))

fig.add_annotation(x=(caseTimeSeries['date'].iloc[-100]),
                   y=caseTimeSeries['totalconfirmed'].map(int).max(),
                   text=str(caseTimeSeries['totalrecovered'].map(int).max()) + ' Recoverd',
                   font=dict(
            
            size=32,
            color="#AFD275"
            ))

fig.update_annotations(dict(
            xref="x",
            yref="y",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-20
))
fig.update_layout(barmode='stack',xaxis_showgrid=False, yaxis_showgrid=False, plot_bgcolor='#FFF',showlegend=False,hovermode='x')
fig.update_layout(title='Covid19 Timeline in India', height=400)

figText = html.Div(['People Infected as on ', html.B(str(caseTimeSeries['date'].iloc[-1])) , 
                    html.H3(' = ' + str(caseTimeSeries['totalconfirmed'].map(int).max()), style={'color': 'LightBlue'}),
                    
                    html.P(['Out of which ', html.H4(str((caseTimeSeries['totalconfirmed'].map(int)-(caseTimeSeries['totalrecovered'].map(int)+ caseTimeSeries['totaldeceased'].map(int))).iloc[-1]), style={'color': 'Crimson'})])
                    , ' Are still Infected & ' ,html.H4(str(caseTimeSeries['totalrecovered'].map(int).iloc[-1]), style={'color': 'green'}), ' have been cured and Discharged',
                    html.P(['Morality Rate ', html.H5(str((round(caseTimeSeries['totaldeceased'].map(int).iloc[-1]*100/caseTimeSeries['totalconfirmed'].map(int).iloc[-1],2))))]),
                    ],
                    
                )

#Doubling Rate
pctChange = pd.DataFrame({'date':caseTimeSeries['date'],'totalconfirmed':caseTimeSeries['totalconfirmed'],'pct_change':caseTimeSeries['totalconfirmed'].map(int).pct_change().mul(100).round(2)})
pctChange['cumul_pct'] = pctChange['pct_change'].cumsum()
p=1
rates = []
for i in range(100):
  if p > caseTimeSeries['totalconfirmed'].map(int).max():
    break
  else:
    rates.append(p)
    p = p *2

def doubling_rate(lst):
  # rates = rates
  tf = []
  for val in lst:
    try:
      if val >= rates[0]:
        # print (val, rates[0])
        rates.pop(0)
        
        tf.append(True)
      else:
        tf.append(False)
    except IndexError:
      # print (rates,len(rates))
      # print ('exception')
      tf.append(False)
  return tf

pctChange['double'] = doubling_rate(pctChange['totalconfirmed'].map(int))
pctChangenoDup = pctChange.drop_duplicates('cumul_pct',keep='last')
pctChangenoDup['double'] = doubling_rate(pctChange.drop_duplicates('cumul_pct',keep='last')['cumul_pct'])
doublingData = pctChange[pctChange['double']]
doublingData['doubleRate'] = doublingData.reset_index()['index'].diff().fillna(0).to_list()

fig2 = go.Figure()
fig2.add_trace(go.Bar(x=doublingData['date'],y=doublingData['doubleRate'], name='DoublingRate of Cases'))

#fig2.add_trace(go.Scatter(x=doublingData['date'],y=doublingData['totalconfirmed'].map(int).map(np.log), name='Total Cases LogScale'))
fig2.update_traces(marker_color='#FF9966',marker_line_color='#CCFF99',marker_line_width=1.5)
fig2.add_trace(go.Scatter(x=doublingData['date'],y=doublingData['doubleRate'], name='DoublingRate of Cases', marker_color='#E7717D'))
fig2.update_layout(hovermode='x',title='Doubling Rate of Cases in India ' + str(doublingData['doubleRate'].iloc[-1]),plot_bgcolor='#FFF',showlegend=False)

fig2.add_annotation(x=10, y=15, text=str(doublingData['doubleRate'].iloc[-1]) + ' Doubling Rate', font=dict(
            size=32,
            color="#AFD275"
            ))                   
fig2Text = 'This plot depicts the doubling rate trend of cases Related to Covid, Increasing trend depicts the decreasing Covid Cases'


fig3 = go.Figure()
for col in confirmed_trend.columns:
  if col in state_ut:
    fig3.add_trace(go.Scatter(x=confirmed_trend['date'], 
                              y= confirmed_trend[col].map(int).cumsum().values -recovered_trend[col].map(int,abs).cumsum().values,
                              name=col, mode='lines+markers',
                              #marker={'size':confirmed_trend[col].map(int,abs).apply(lambda x: 0 if x <0 else x/100).values}
                              ))
  else:
    pass
fig3.update_layout(title='State Wise Active Cases trend',hovermode='x',showlegend=False, plot_bgcolor='#FFF')


fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=caseTimeSeries['date'], y=caseTimeSeries['dailyconfirmed'], name='Confirmed',marker_color='DarkOrange'))
fig4.add_trace(go.Scatter(x=caseTimeSeries['date'], y=caseTimeSeries['dailyrecovered'], name='Recovered',marker_color='DarkBlue'))

  
fig4.add_annotation(x=eventTimeline['delta'][0]+15,
                     y=3000,
                     text=eventTimeline['What'][0])


fig4.add_annotation(x=eventTimeline['delta'][1],
                     y=16000,
                     text=eventTimeline['What'][1])

fig4.add_annotation(x=eventTimeline['delta'][2],
                     y=45000,
                     text=eventTimeline['What'][2])


fig4.add_annotation(x=eventTimeline['delta'][3],
                     y=75000,
                     text=eventTimeline['What'][3])

fig4.add_annotation(x=eventTimeline['delta'][4],
                     y=90000,
                     text=eventTimeline['What'][4])


fig4.add_annotation(x=eventTimeline['delta'][5],
                     y=20000,
                     text=eventTimeline['What'][5])

fig4.add_annotation(x=eventTimeline['delta'][6]-15,
                     y=40000,
                     text=eventTimeline['What'][6])

fig4.add_annotation(x=eventTimeline['delta'][7]-2,
                     y=100000,
                     text=eventTimeline['What'][7])

fig4.add_annotation(x=caseTimeSeries['date'].iloc[-1],
                   y=caseTimeSeries['dailyconfirmed'].map(int).max(),
                   text='Daily Confirmed', font={'color':'Crimson'})

fig4.add_annotation(x=caseTimeSeries['date'].iloc[-1],
                   y=caseTimeSeries['dailyrecovered'].map(int).max(),
                   text='DailyRecovered',font={'color':'LightGreen'})


fig4.update_annotations(dict(
            xref="x",
            yref="y",
            showarrow=True,
            arrowhead=8,
            ax=0,
            ay=-2
))
fig4.update_layout(barmode='stack',xaxis_showgrid=False, yaxis_showgrid=False, plot_bgcolor='#FFF',showlegend=False,hovermode='x')
fig4.update_layout(title='Covid19 Daily Timeline - India',height=400,font=dict(
        family="Helvetica",
        size=12,
        color="Black"
    ))

fig4Text = "We can say the cases were coming down and We are progressing towards recovery only when the recoveries/day were continuosly are greater than confirmed cases/day"