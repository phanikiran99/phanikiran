#dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#import plots
import geo
#import base64
import os
import flask
import pathlib
import helper  # local
import random
#import sqlite3
import base64

#from test_scripts import firstRow, secondRow

cat = [{'label':'All','value':'All'}]  #categories
titles= [{'label':'All','value':'All'}] #titles
arti_list = [] #articles formatted
artiList = helper.retriveArticlesList(['All'],['All'])  #all article list dict

cov_filename = 'static/covidWorld.png' # replace with your own image
encoded_image_cov = base64.b64encode(open(cov_filename, 'rb').read())


def createContainer(title,descr,date,cat,link,imgLink):
    clr = random.choice(['#FFFF99','#FF9966','#CCFF99'])
    imgFile = imgLink
    encodedImage = base64.b64encode(open(imgFile, 'rb').read())
    cont  = html.Div(
                    [
                    html.H6(title),
                    html.P(descr),
                    html.P('Created: ' +str(date)),
                    html.P('Category: '+str(cat)),
                    html.A(
                    html.Img(src='data:image/png;base64,{}'.format(encodedImage.decode()), style={
                                    "height": "70px",
                                    "width": "auto",
                                    "margin-bottom": "0px",
                                }),
                    href=link),
                    html.Div(
                    [
                        html.A(
                            html.Button("Go", id="learn-more-button"),
                            href=link,
                        )
                    ],
                    className="one-half column",
                    id="button",
                ),
                    
                    ],
                    className="mini_container", style={'box-shadow': '2px 2px 2px '+clr+';'},
                    ),
    return cont



for arti in artiList:
#    print(arti[0],arti[3])
    cat.append({'label':arti[3],'value':arti[3]})
    titles.append({'label':arti[0],'value':arti[0]})
    
    arti_list.append(html.Div(
                    [
                    html.H6(arti[0]),
                    html.P(arti[1]),
                    html.P('Created: ' +str(arti[2])),
                    html.P('Category: '+str(arti[3])),
                    html.Div(
                    [
                        html.A(
                            html.Button("Go", id="learn-more-button"),
                            href=arti[4],
                        )
                    ],
                    className="one-half column",
                    id="button",
                ),
                    
                    ],
                    className="mini_container",
                    ),)

#print (cat,titles)
filteredArt = arti_list   
    
#print(cat,titles)
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()



geo.saveImages();

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

########### Initiate the app
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__,suppress_callback_exceptions=True)
server = app.server
app.title="Phanikiran Siddineni"

   

layout_index = html.Div([
            dcc.Store(id="aggregate_data"),
            # empty Div to trigger javascript file for graph resizing
            html.Div(id="output-clientside"),
            html.Div(
                [
                    
                        html.A(
                        html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("bitmap.png"),
                                id="plotly-image",
                                style={
                                    "height": "80px",
                                    "width": "auto",
                                    "margin-bottom": "0px",
                                },
                            ),
                                    
                        ],
                        className="column col-md-4",
                        style={'textAligh':'center'}
                    ),
                    href='/'),
                    
                     html.Div([html.Div(html.H6("Filter Articles By Category/Title"),style={'text-align':'center'},id='filter-text'),
                        html.Div([html.Div([html.H6("Category")],className='col-md-2 text-right'),
                                  html.Div([dcc.Dropdown(options=cat,multi=True,id='cat-filter')],className="col-md-3"),
                                  html.Div([html.H6("Title")],className='col-md-2 text-right'),
                                  html.Div([dcc.Dropdown(options=titles,multi=True,id='title-filter')],
                                            className="col-md-4"),],),
    #                    html.Div([html.H6("Title"),dcc.Dropdown(options=titles,multi=True),],className="col-md-6"),
                          
                          ],className='col-md-12'),
                                        
                ],
                id="header",
                className="row flex-display fixed-top",
                style={"margin-bottom": "25px"},
            ),
        
                        html.Div([
                        html.Div([], className='row container-display'), 
                        html.Div([], className='row container-display'),], id='output-filter-div',),
                         
                        
    ])
#    return layout_index

#layout_index = home_layout()
 
covid_layout = helper.covid_layout
common_layout = helper.common_layout
covtab_layout = helper.covtab_layout
    
blog_layout = html.Div([
    html.H2('Blog'),
    #dcc.Dropdown(
    #    id='page-2-dropdown',
    #    options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
    #    value='LA'
    #),
    #html.Div(id='page-2-display-value'),
    #html.Br(),
    dcc.Link('Navigate to "/"', href='/'),
    html.Br(),
    dcc.Link('Navigate to "/covid19india"', href='/covid19'),
])    
# index layout
                        

app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    layout_index,
    covid_layout,
    blog_layout,
    common_layout,
    covtab_layout,
    helper.dokkaseetamma_layout
    
])    

# Index callbacks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/covid19":
        return covid_layout
    elif pathname == "/blog":
        return blog_layout
    elif pathname == "/common":
        return common_layout
    elif pathname == "/covtab":
        return covtab_layout
    elif pathname == "/dokkaSeetammaGaaru":
        return helper.dokkaseetamma_layout
    elif pathname =='/':
        return layout_index


@app.callback(Output(component_id='output-filter-div',component_property='children'),
              [Input(component_id='cat-filter', component_property='value'), 
               Input(component_id='title-filter', component_property='value')]) 
def filter_artiList(cat=[], title=[]):
    print ('Filtering articles by -{} & {}'.format(cat,title))
    cnt = 0
#    othCnt =0
    row=0
    othRowCnt  =0
    itemList = {}
    itemList[row] = []

    filteredArti=[]
#    print (cat)
    filtered = []
#    print('ArtiList -', artiList)
    if (title == None  and cat==None):
        filtered = artiList
#        print ( 'No filter')
    elif (title == None and cat != None):
        filtered = helper.retriveArticlesList(cat,['All'])
    elif(title != None and cat== None):
        filtered = helper.retriveArticlesList(['All'],title)
    else:
        filtered = helper.retriveArticlesList(cat,title)
            
    filtered = list(set(filtered))
    for arti in filtered*20:
        cnt = cnt + 1
        if cnt < 6:
            itemList[row].append(createContainer(arti[0],arti[1],arti[2],arti[3],arti[4],arti[5]))
#        print('add {} to {} row'.format(arti[0],row+1))
            if cnt == 6:
                row =row +1
                itemList[row] = []
        else:
#            othCnt = tot - 6        
            othRowCnt = othRowCnt + 1
            if othRowCnt == 8:
                othRowCnt = 0
                row = row+1
                itemList[row] =[]
            itemList[row].append(createContainer(arti[0],arti[1],arti[2],arti[3],arti[4],arti[5]))
#    print (itemList.keys(), itemList[0])    
    firstRow  = html.Div([html.Div([
                        html.Div(
                                html.Img(
                                src=app.get_asset_url("image823.png"),
                                id="plotly-image",
                                style={
                                    "height": "180px",
                                    "width": "auto",
                                    "margin-bottom": "0px",
    #                                "align-content":"center",
                                    "textAlign":"center",
                                },
                            ),style={"textAlign":"center",},
                            ),
                        html.H4("Phanikiran Siddineni",
                                style={"margin-bottom": "0px", "text-align":"center"},
                                ),
                        html.H6("Engineer, Love to Code, Draw, Capture, Read, Write, Analyze", 
                                style={"margin-top": "0px", "text-align":"center"}
                                ),
                          ],className='pretty-container col-md-3'),
                        itemList[0][0][0],itemList[0][1][0],
                        itemList[0][2][0],itemList[0][3][0],itemList[0][4][0],itemList[0][5][0],
                        ],
                        className="row container-display col-md-12")
    secondRow = html.Div([item[0] for item in itemList[1]],
                     className="row container-display col-md-12")

    filteredArti = [html.Div([firstRow], className='row container-display'), 
                        html.Div([secondRow], className='row container-display'),
                        ]
    return filteredArti


                    
@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)
    

if __name__ == '__main__':
    app.run_server()
