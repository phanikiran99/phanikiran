# -*- coding: utf-8 -*-
# dict of state names to shortcuts
import dash_core_components as dcc
import dash_html_components as html
import plots
import geo
import base64
import sqlite3
#import app
import articles

def retriveArticlesList(cat=['All_1'],title=['All_1']):
    cat.append('All_1')
    cat.append('All_2')  # Dummy appends so sqlite will not fail
    title.append('All_1')
    title.append('All_2') # on single element traverse
    print (cat, title)
    conn = None
    try:
        conn = sqlite3.connect('static/entries.db')
    except:
        print ('unable to connect')
    cur = conn.cursor()
    if ('All' in cat and 'All' in title):
        sql= 'select * from entry_list'
    elif (len(cat) == 0 or 'All' in cat) and len(title) != 0:
        sql = 'select * from entry_list where entry in {}'.format(tuple(title)) 
        
    elif (len(title) == 0 or 'All' in title) and len(cat) != 0:
        sql = 'select * from entry_list where category in {}'.format(tuple(cat)) 
        
    elif ('All' in title and 'All' in cat):
        sql = 'select * from entry_list'
        
    else:
        sql = 'select * from entry_list where entry in {} and category in {}'.format(tuple(title),tuple(cat))
        
    print (sql)    
    cur.execute(sql)
    rows = cur.fetchall()
    article_list = []
    for row in rows:
        article_list.append(row)   
    
    return article_list

dict = {'an': 'Andaman & Nicobar Island',
 'ap': 'Andhra Pradesh',
 'ar': 'Arunanchal Pradesh',
 'as': 'Assam',
 'br': 'Bihar',
 'ch': 'Chandigarh',
 'ct': 'Chhattisgarh',
 'dd': 'Dadara & Nagar Havelli',
 'dl': 'NCT of Delhi',
 'dn': 'Daman & Diu',
 'ga': 'Goa',
 'gj': 'Gujarat',
 'hp': 'Himachal Pradesh',
 'hr': 'Haryana',
 'jh': 'Jharkhand',
 'jk': 'Jammu & Kashmir',
 'ka': 'Karnataka',
 'kl': 'Kerala',
 'la': '',
 'ld': 'Lakshadweep',
 'mh': 'Maharashtra',
 'ml': 'Meghalaya',
 'mn': 'Manipur',
 'mp': 'Madhya Pradesh',
 'mz': 'Mizoram',
 'nl': 'Nagaland',
 'or': 'Odisha',
 'pb': 'Puducherry',
 'py': 'Punjab',
 'rj': 'Rajasthan',
 'sk': 'Sikkim',
 'tg': 'Telangana',
 'tn': 'Tamil Nadu',
 'tr': 'Tripura',
 'tt': '',
 'up': 'Uttar Pradesh',
 'ut': 'Uttarakhand',
 'wb': 'West Bengal',
 'un': 'Unknown'}


#geo.saveImages();

fig  = plots.fig  # trend line
fig2 = plots.fig2 # doubling rate
fig3 = plots.fig3
fig4 = plots.fig4

rec_filename = 'static/recovery.png' # replace with your own image
encoded_image_rec = base64.b64encode(open(rec_filename, 'rb').read())


act_filename = 'static/active.png' # replace with your own image
encoded_image_act = base64.b64encode(open(act_filename, 'rb').read())    

states_options = [{'label':i[1],'value':i[0]} for i in dict.items()]

title_filename  ='assets/bitmap.png'
encoded_image_logo = base64.b64encode(open(title_filename,'rb').read())


def getHeaderTop(title):
    headerTop = html.Div(
                    [
                        
                            html.A(
                            html.Div(
                            [
                                html.Img(
                                    src=('data:image/png;base64,{}'.format(encoded_image_logo.decode())),
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
                        
                         html.Div(html.H4(title), className='col-md-8 text-right'),
                                            
                    ],
                    id="header",
                    className="row flex-display fixed-top col-md-12",
                    style={"margin-bottom": "25px"},
                )
    return headerTop
    
                            

def commonLayout(layoutTitle='Title',numFilters=2,filter1Name='Filter1',
                 filter2Name='Filter2',
                 filter1Options=[{}], filter2Options=[{}], figList=[],footNotes=html.Div(),additionalDiv=''):
    """
    Parameters : layoutTitle = Title of the page
    numfilters = Total number of filters - supports two filters
    filter'n'Name = name of filters
    filter'n'Options = options for dropdown values
    figlist - list of lists with id, fig object, Text description of figure
    """
    if numFilters > 0:
    # prepare for filter area
        filterArea  =  html.Div([html.H5(filter1Name,className='col-md-2'),
                      html.Div([dcc.Dropdown(options=filter1Options,multi=True,value='ap')]
                    ,className='col-md-4'),
                    html.H5(filter2Name,className='col-md-2'),
                      html.Div([dcc.Dropdown(options=filter2Options,multi=True,value='ap')]
                    ,className='col-md-4'),]
                ,className='row container-display pretty_container col-md-12')       
        # prepare for plots
    else:
        filterArea = html.Div()
    figureArea = []
    for i,fig in enumerate(figList):
        if i%2 == 0:
            figureArea.append(html.Div([html.Div([dcc.Graph(id=fig[0], figure=fig[1])], className='pretty_container col-md-10'),
                                        html.Div([html.P(fig[2])], className='pretty_container col-md-2 text-left')], 
                                        className='row container-display col-md-12',style={'background-color':''}))
        else:
            figureArea.append(html.Div([html.Div([html.P(fig[2])], className='pretty_container col-md-2 text-right'),
                                        html.Div([dcc.Graph(id=fig[0], figure=fig[1])], className='pretty_container col-md-10'),
                                        ], 
                                        className='row container-display col-md-12',style={'background-color':''}))
    
    figureArea.append(additionalDiv)
    figureArea.append(html.Div([html.Div([html.H4('Browse More Articles <YTC>',)], className='pretty_container col-md-10'),
                                        html.Div([footNotes], className='pretty_container col-md-2 text-left')], 
                                        className='row container-display col-md-12',style={'background-color':''}))
    
    
    updatedLayout = html.Div(children=[
            getHeaderTop(layoutTitle),
#        html.Div(html.H4(layoutTitle),className='row pretty_container col-md-12 container-fluid center'),
        filterArea,
        html.Div(figureArea),
        
        ]
        )
    
    return updatedLayout



common_layout = commonLayout(layoutTitle='Covid19 India EDA Short analysis on How India is dealing with Covid19',numFilters=2,filter1Name='State',
                 filter2Name='Filter2',
                 filter1Options=states_options,
                 filter2Options=[{'label':'1','value':'1'},{'label':'2','value':'2'}], 
                 figList=[['test',fig,plots.figText],['test2',fig4,plots.fig4Text],['test3',fig2,plots.fig2Text]])

footNotesCovid = html.Div([html.Div(html.A(' /DataSource/ ', href='http://api.covid19india.org', target='_blank')),
                           html.Div(html.A(' /References/ ',href='#')),
                           html.Div(html.A(' /Back to Home/ ',href='/'))])
additionalDivCovid = html.Div([
    html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image_act.decode())),
    ],
    className='pretty_container col-md-6'),
    html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image_rec.decode())),
            ],
            className='pretty_container col-md-6'),
            ],
    className='row container-display col-md-12'),

covid_layout = commonLayout(layoutTitle='Covid19 India EDA Short analysis on How India is dealing with Covid19',numFilters=0,
                 figList=[['test',fig,plots.figText],['test2',fig4,plots.fig4Text],['test3',fig2,plots.fig2Text]],
                 footNotes =footNotesCovid,additionalDiv=html.Div())



covtab_layout = html.Div(children=[html.Div([getHeaderTop('Covid 19 Offline Analysis Using Tableau')],),
                                   html.Iframe(src="https://public.tableau.com/views/Covid19InIndia/Indiatotal?:language=en-GB&:display_count=y&:origin=viz_share_link:showVizHome=no&:embed=true showVizHome=no&:embed=true"
                                     ,width='100%', height="655"
                                     ),
                                    html.Div([html.Div([html.H4('Browse More Articles <YTC>',)], className='pretty_container col-md-10'),
                                        html.Div([footNotesCovid], className='pretty_container col-md-2 text-left')], 
                                        className='row container-display col-md-12',style={'background-color':''})
        ],className='pretty_container col-md-12 container-fluid'),
                
footNotesSeetamma = html.Div([html.Div(html.A(' /Reference 1/ ', href=articles.references[0], target='_blank')),
                           html.Div(html.A(' /Reference 2/ ',href=articles.references[0], target ='_blank')),
                           html.Div(html.A(' /Back to Home/ ',href='/'))])

dokkaseetamma_layout =  html.Div(children=[html.Div([getHeaderTop(articles.titledokkaSeetammaGaaru)],),
                                   html.Div(articles.dokkaSeetammaGaaru
                                     
                                     ),
                                    html.Div([html.Div([html.H4('Browse More Articles <YTC>',)], className='pretty_container col-md-10'),
                                        html.Div([footNotesSeetamma], className='pretty_container col-md-2 text-left')], 
                                        className='row container-display col-md-12',style={'background-color':''})
        ],className='pretty_container col-md-12 container-fluid'),