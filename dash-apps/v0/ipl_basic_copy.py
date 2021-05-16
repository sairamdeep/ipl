import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import plotly.express as px

import dash_bootstrap_components as dbc
import plotly.graph_objs as go

#### Total Matches 
def get_gp_match_result(filter_='Chennai Super Kings',col='batting_team',gp_col=[],metric='total_matches'):
    return team_matches[team_matches[col]==filter_].groupby(gp_col)[metric].sum()

def get_gp_winner_result(filter_='Chennai Super Kings',col='winner',gp_col=[],metric='total_wins'):
    return team_wins[team_wins[col]==filter_].groupby(gp_col)[metric].sum()

def get_grand_total(filter_='Chennai Super Kings',key='match'):
    if key=='match':
        return get_gp_match_result(filter_,'batting_team','batting_team','total_matches').apply(int).values[0]
    else:
        return get_gp_winner_result(filter_,'winner','winner','total_wins').apply(int).values[0]

def get_yearly_total(filter_='Chennai Super Kings',key='match'):
    if key=='match':
        return get_gp_match_result(filter_,'batting_team',['batting_team','year'],'total_matches').unstack(1).apply(int)
    else:
        return get_gp_winner_result(filter_,'winner',['winner','year'],'total_wins').unstack(1).apply(int)


def get_team_wise_total(filter_='Chennai Super Kings',key='match'):
    if key=='match':
        return get_gp_match_result(filter_,'batting_team',['batting_team'],[x for x in teams_list if x!=filter_]).apply(int)
    else:
        return get_gp_winner_result(filter_,'winner',['winner'],[x for x in teams_list if x!=filter_]).apply(int)
    
def get_yearly_team_wise_total(filter_='Chennai Super Kings',key='match'):
    if key=='match':
        return get_gp_match_result(filter_,'batting_team',['year'],[x for x in teams_list if x!=filter_])
    else:
        return get_gp_winner_result(filter_,'winner',['year'],[x for x in teams_list if x!=filter_])
    
def get_team_profile(filter_='Chennai Super Kings'):
    return


team_matches=pd.read_csv('E:/projects/iitm/data/team_matches_NSO.csv')
team_wins=pd.read_csv('E:/projects/iitm/data/team_wins_NSO.csv')

teams_list=list(team_matches.batting_team.unique())


app = app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "IPL DashBoard"

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Select Team"),
                dcc.Dropdown(
                    id="team-filter",
                    options=[
                        {"label": team, "value": team}
                        for team in teams_list
                    ],
                    value=teams_list[0],
                    clearable=False,
                ),
            ]
        )
    ]
)


app.layout = dbc.Container(
    [
        html.H1("IPL Analytics 🏆"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
            ],
            style={'textAlign': 'center'}
        ),
    ],
    fluid=True,
)


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🏆", className="header-emoji"),
                html.H1(
                    children="IPL Analytics", className="header-title"
                ),
                html.P(
                    children="Analyzing the IPL data"
                    " between 2008 and 2020",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="team-matches",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="team-wins",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("team-matches", "figure"),
    Input("team-filter", "value")
)
def team_matches_year(team):
    a=get_yearly_total(team,'match')
    a=pd.DataFrame(a)
    a=a.reset_index().rename(columns={0:'matches_played'})
    fig = px.bar(a, x='year', y='matches_played',title=f'Matches Played by {team} yearly')
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    #fig.set_title(f'Matches Played by {team} yearly')
    return fig
@app.callback(
    Output("team-wins", "figure"),
    Input("team-filter", "value")
)
def team_matches_won(team):
    a=get_yearly_total(team,'winner')
    a=pd.DataFrame(a)
    a=a.reset_index().rename(columns={0:'matches_won'})
    fig = px.bar(a, x='year', y='matches_won',title=f'Matches Won by {team} yearly')
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    return fig
if __name__ == "__main__":
    app.run_server(debug=True)