import helper
import dash_html_components as html
import dash_core_components as dcc


artiList = helper.retriveArticlesList() 
artiList = artiList * 22
tot = len(artiList)

print (tot)
cat = [{'label':'All','value':'All'}]  #categories
titles= [{'label':'All','value':'All'}] #titles
arti_list = [] #articles formatted

cnt = 0
othCnt =0
row=0
othRowCnt  =0
itemList = {}
itemList[row] = []
import random

def createContainer(title,descr,date,cat,link):
    clr = random.choice(['#EFC050','White'])
    cont  = html.Div(
                    [
                    html.H6(title),
                    html.P(descr),
                    html.P('Created: ' +str(date)),
                    html.P('Category: '+str(cat)),
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
                    className="mini_container", style={'background-color':clr},
                    ),
    return cont

for arti in artiList:
    cnt = cnt + 1
    print(cnt, arti[0],arti[3])
    cat.append({'label':arti[3],'value':arti[3]})
    titles.append({'label':arti[0],'value':arti[0]})
    
    if cnt < 6:
        itemList[row].append(createContainer(arti[0],arti[1],arti[2],arti[3],arti[4]))
#        print('add {} to {} row'.format(arti[0],row+1))
        if cnt == 6:
            row =row +1
            itemList[row] = []
    else:
        othCnt = tot - 6
        
        othRowCnt = othRowCnt + 1
        if othRowCnt == 8:
            othRowCnt = 0
            row = row+1
            itemList[row] =[]
        itemList[row].append(createContainer(arti[0],arti[1],arti[2],arti[3],arti[4]))
#        print('add {} to {} row'.format(arti,row+1))


firstRow  = html.Div([html.Div([
                        html.Div(
                                html.Img(
                                src=("image823.png"),
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
                          ],className='pretty-container col-md-3'),itemList[0][0][0],itemList[0][1][0],
                        itemList[0][2][0],itemList[0][3][0],itemList[0][4][0],itemList[0][5][0],],
                        className="row container-display col-md-12",style={'background-color':'#FEFFFF'})
secondRow = html.Div([item[0] for item in itemList[1]],
                     className="row container-display col-md-12",style={'background-color':'#FEFFFF'})
                                                              
#print (firstRow, secondRow)                                                