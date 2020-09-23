# -*- coding: utf-8 -*-
#@todo:work in progress

import pandas as pd
import requests
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from plotly.subplots import make_subplots
from math import ceil

stateapi = 'https://api.covid19india.org/states_daily.json'
stateData = requests.get(stateapi).json()
stateDf = pd.DataFrame(stateData['states_daily'])

rows = ceil(round(len(stateDf.columns)-3)/5)
cols =5

trends =  make_subplots(rows=rows,cols=cols)
rw=1
cl=1

for col in stateDf.columns:
    if col not in('tt','status','date'):        
        temp_dat = stateDf[stateDf['status'] == 'Confirmed'][[col,'date']]
        #print(rw,' ',cl)
        try:
            trends.add_trace(go.Scatter(x=temp_dat['date'],y=temp_dat[col],name=col.upper()),row=rw,col=cl)
            trends.update_layout(height=900, width=1200, title_text="States Data",showlegend=True,xaxis=dict(
                        autorange=True,
                        showgrid=False,
                        ticks='',
                        showticklabels=False
                        ),
                        yaxis=dict(
                                autorange=True,
                                showgrid=False,
                                ticks='',
                                showticklabels=False
                                ))

            if rw < 5:
                rw = rw+1
            else:
                rw=1
                cl=cl+1
        except:
            pass
        
        
trends.show();

plot(trends)
