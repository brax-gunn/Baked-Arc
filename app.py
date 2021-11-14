import dash
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

import dash_bootstrap_components as dbc

df = pd.read_csv('Bakery.csv')
df['Date'] = df['DateTime'].str.split(' ').str[0]
df = df.drop('DateTime',axis='columns')


items_list = []
for item in df['Items'].unique():
    items_list.append({'label':str(item),'value':item})


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.GRID]) 
app.title = 'Baked-Arc'

emptyFig = go.Figure(
    data=None,
    layout=go.Layout(
            paper_bgcolor='#644141',
            plot_bgcolor='#644141',
            font_family="Courier New",
            font_color="white",
            title_font_family="Glory",
            title_font_color="white",
            legend_title_font_color="white"
        )
)
emptyFig.update_layout(
    xaxis={"visible": False},
    yaxis={"visible": False},
    annotations= [
                        {
                            "text": "🥺 No data found",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {
                                "size": 28
                            }
                        }
                    ]
)


app.layout = html.Div([
    html.Img(src=('/assets/BAKED-ARC.png'),style={'width':'100%'}),
	
    html.Hr(),

    # Date Analysis
    html.H1('Time Based Analysis (All Products)'),
    dbc.Row([
        dbc.Col(
            dcc.DatePickerRange(
                id='graph1-dateRangePicker',
                display_format='DD-MM-YYYY',
                min_date_allowed='2016-01-11',
                max_date_allowed='2017-12-03',
                initial_visible_month='2016-01-11',
            ),
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph1-1',),
        ),
        dbc.Col(
            dcc.Graph(id='graph1-2',),
        )
    ]),
    # Date + Product
    html.H1('Time + Product Based Analyis'),  
    dbc.Row([
        dbc.Col(
            dcc.DatePickerRange(
                id='graph2-dateRangePicker',
                display_format='DD-MM-YYYY',
                min_date_allowed='2016-01-11',
                max_date_allowed='2017-12-03',
                initial_visible_month='2016-01-11',
                
            ),
        ),
        dbc.Col(
            dcc.Dropdown(
                id='graph2-productList',
                options=items_list,
                multi=True,
                clearable=False,
                placeholder='Select an Item(s)'
            ),
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph2',),
        )
    ]),

    # Product Only
    html.H1('Product Based Analysis (All Time)'),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='graph3-productName',
                options=items_list,
                clearable=False,
                placeholder='Select an Item',
                style={
                    'width':'50%'
                }
            ),
        ),
    ],),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph3-1',),
        ),
        dbc.Col(
            dcc.Graph(id='graph3-2',),
        )
    ])

],style={'width':'70%','margin-left':'15%','padding':'20px'})







@app.callback(Output('graph1-1','figure'),
                [
                    Input('graph1-dateRangePicker','start_date'),
                    Input('graph1-dateRangePicker','end_date'),
                ]
             )
def update_graph11(start_date,end_date):
    global df
    global emptyFig
    if( (start_date==None) or (end_date==None) ):
        return emptyFig
    else:
        df_graph11 = df[ ( df['Date']>=start_date)& (df['Date']<=end_date )]
        df_graph11 = df_graph11.groupby(['Items']).size().reset_index(name='Sales')
        df_graph11 = df_graph11.sort_values(by=['Sales'],ascending=False)
        df_graph11 = df_graph11.head(5)

        x_values = df_graph11['Items']
        y_values = df_graph11['Sales']
        
        data = [
            go.Bar(
                x=x_values,
                y=y_values,
                opacity=0.7,
            )
        ]
        

        fig = go.Figure(
            data=data,
            layout=go.Layout(
                title='Top 5 Items Sold',
                xaxis={'title':'Item Name ->'},
                yaxis={'title':'Total Items Sold ->'},
                paper_bgcolor='#644141',
                plot_bgcolor='#644141',
                font_family="Courier New",
                font_color="white",
                title_font_family="Glory",
                title_font_color="white",
                legend_title_font_color="white"
                
            )
        )
        fig.update_layout(template='plotly_dark')
        return fig


@app.callback(Output('graph1-2','figure'),
                [
                    Input('graph1-dateRangePicker','start_date'),
                    Input('graph1-dateRangePicker','end_date'),
                ]
             )
def update_graph12(start_date,end_date):
    global df
    global emptyFig
    if( (start_date==None) or (end_date==None) ):
        return emptyFig
    else:
        df_graph12 = df[ ( df['Date']>=start_date)& (df['Date']<=end_date )]
        df_graph12 = df_graph12.groupby(['Items']).size().reset_index(name='Sales')
        df_graph12 = df_graph12.sort_values(by=['Sales'],ascending=False)
        df_graph12 = df_graph12.tail(5)

        x_values = df_graph12['Items']
        y_values = df_graph12['Sales']
        
        data = [
            go.Bar(
                x=x_values,
                y=y_values,
                opacity=0.7,
            )
        ]

        fig = go.Figure(
            data=data,
            layout=go.Layout(
                title='Bottom 5 Items Sold',
                xaxis={'title':'Item Name ->'},
                yaxis={'title':'Total Items Sold ->'},
                paper_bgcolor='#644141',
                plot_bgcolor='#644141',
                font_family="Courier New",
                font_color="white",
                title_font_family="Glory",
                title_font_color="white",
                legend_title_font_color="white"
            )
        )   
        fig.update_layout(template='plotly_dark')
        return fig

@app.callback(Output('graph2','figure'),
                [
                    Input('graph2-productList','value'),
                    Input('graph2-dateRangePicker','start_date'),
                    Input('graph2-dateRangePicker','end_date'),
                ]
             )
def update_graph2(product_list,start_date,end_date):
    global df
    global emptyFig
    if( (product_list==None) or (start_date==None) or (end_date==None) or len(product_list)==0 ):
        return emptyFig
    else:
        df_graph2 = df.groupby(['Items','Date',]).size().reset_index(name='Sales')
        df_graph2 = df_graph2[ ( df_graph2['Date']>=start_date)& (df_graph2['Date']<=end_date )]
        
        traces=[]
        for item in product_list:
            print(item)
            
            x_values = df_graph2[ df_graph2['Items']==item ]['Date']
            y_values = df_graph2[ df_graph2['Items']==item ]['Sales']
            
            
            traces.append(
                go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode='lines+markers',
                    opacity=0.7,
                    marker = {'size':10},
                    name=item
                )
            )

        fig = go.Figure(
            data=traces,
            layout=go.Layout(
                title='Products + Date Analysis',
                xaxis={'title':'Date ->'},
                yaxis={'title':'Total Product Sold ->'},
                paper_bgcolor='#644141',
                plot_bgcolor='#644141',
                font_family="Courier New",
                font_color="white",
                title_font_family="Glory",
                title_font_color="white",
                legend_title_font_color="white"
            )
        )
        fig.update_layout(template='plotly_dark')
        return fig


@app.callback(Output('graph3-1','figure'),
                [
                    Input('graph3-productName','value'),
                ]
             )
def update_graph31(product_name):
    global df
    global emptyFig
    if( (product_name==None) or (product_name=='') ):
        return emptyFig
    else:
        df_graph31 = df.groupby(['Items','Daypart',]).size().reset_index(name='Sales')
        df_graph31 = df_graph31[ df_graph31['Items']==product_name ]

        x_values = df_graph31['Daypart']
        y_values = df_graph31['Sales']
        
        data = [
            go.Bar(
                x=x_values,
                y=y_values,
                opacity=0.7,
            )
        ]
        

        fig = go.Figure(
            data=data,
            layout=go.Layout(
                title='Products Analysis',
                xaxis={'title':'Day Time ->'},
                yaxis={'title':'Total Product Sold ->'},
                paper_bgcolor='#644141',
                plot_bgcolor='#644141',
                font_family="Courier New",
                font_color="white",
                title_font_family="Glory",
                title_font_color="white",
                legend_title_font_color="white"
            )
        )
        fig.update_layout(template='plotly_dark')
        return fig


@app.callback(Output('graph3-2','figure'),
                [
                    Input('graph3-productName','value'),
                ]
             )
def update_graph32(product_name):
    global df
    global emptyFig
    if( (product_name==None) or (product_name=='') ):
        return emptyFig
    else:
        df_graph32 = df.groupby(['Items','DayType',]).size().reset_index(name='Sales')
        df_graph32 = df_graph32[ df_graph32['Items']==product_name ]

        x_values = df_graph32['DayType']
        y_values = df_graph32['Sales']
        
        data = [
            go.Pie(
                labels=x_values,
                values=y_values,
                opacity=0.7,
            )
        ]
        

        fig = go.Figure(
            data=data,
            layout=go.Layout(
                title='Products Analysis',
                xaxis={'title':'Day Time ->'},
                yaxis={'title':'Total Product Sold ->'},
                paper_bgcolor='#644141',
                plot_bgcolor='#644141',
                font_family="Courier New",
                font_color="white",
                title_font_family="Glory",
                title_font_color="white",
                legend_title_font_color="white"
            )
        )
        fig.update_layout(template='plotly_dark')
        return fig




if __name__ == '__main__':
    app.run_server()