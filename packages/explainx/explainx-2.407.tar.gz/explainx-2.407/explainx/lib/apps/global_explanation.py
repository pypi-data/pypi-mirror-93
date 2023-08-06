from imports import *
from plotly_graphs import *
from plotly_css import *
from app import app

def global_explanation(original_variables):
    
    layout =  html.Div(children=[
        

                            html.Div([
                                dcc.Loading([
                                    html.Div([
                                    dcc.Dropdown(
                                            id='xaxis-column-test-2',
                                            options=[{'label': i, 'value': i} for i in original_variables[1]],
                                            value=original_variables[1],
                                            clearable=False
                                        )
                                    ], style={'display':'none'})]),
                                html.Div([
                                    html.H4('Aggregate Feature Importance',
                                            style=style5),
                                    html.P(
                                        'Feature importance assign a score to input features based on how useful they are at predicting a target variable. ',
                                        style=style6)
                                    ,
                                    dcc.Loading(
                                        id="loading-1",
                                        type="circle",
                                        children = [
                                            html.Div([
                                                html.Div([
                                                    html.H5(id="global_message_1")
                                                ], className="insights_div_1"),
                                                html.Div(dcc.Graph(id="global_feature_importance"), className="aggregate_imp"),
                                           
                                            ])
                                        ],
                                
                                        # children=dbc.Row([
                                        #         dbc.Col(html.Div(dcc.Graph(id="global_feature_importance")), width=8),
                                        #         dbc.Col([
                                        #                 html.Div([
                                        #                 html.H4("Insights"),
                                        #                 html.P(id='global_message_1')
                                        #                 ])
                                        #             ])
                                        #         ])

                                    )
                                    , ], style=style7,
                                ),

                                html.Div([
                                    html.H4('Global Feature Impact',
                                            style=style8),
                                    html.P(
                                        'Feature impact identifies which features (also known as columns or inputs) in a dataset have the greatest positive or negative effect on the outcomes of a machine learning model.',
                                        style=style9),
                                    dcc.Loading(
                                        id="loading-2",
                                        type="circle",
                                        children=dbc.Row(
                                            [
                                                dbc.Col(html.Div(dcc.Graph(id='global_feature_impact',
                                                                        style={'marginLeft': 50, 'marginTop': 0,
                                                                                'height': '500px'})), width=8),
                                                dbc.Col(
                                                    [
                                                      
                                                        html.Div([
                                                            html.H4("How the overall model behavior was determined"),
                                                            html.P(id='message_1'),
                                                            html.P(id='message_2'),
                                                            html.P(id='message_3')
                                                        ]

                                                        )]
                                                )

                                            ])

                                    )

                                ],
                                    style=style10,
                                ),
                            ],

                                style=style11
                            )
                        ], style={'height': '400'})
    return layout
