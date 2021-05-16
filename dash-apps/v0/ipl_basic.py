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


 


dropdown =  dbc.FormGroup(
        [
            dbc.Label("Team", html_for="dropdown"),
            dcc.Dropdown(
                id="team-filter",
                options=[
                        {"label": team, "value": team}
                        for team in teams_list
                    ],
                value=teams_list[0]
            ),
        ]
    )
form = dbc.Card(
    [
        dbc.Row(),
        dbc.Row(
            [ 
                dbc.Col(md=2 ),
                dbc.Col(dbc.Form([dropdown]),md=6 )
            ]
        )
    ]
)




table = dbc.Card(
    [
    dbc.Row(
        [
            dbc.Col(html.Div("Total Matches Played :"),md=8),
            dbc.Col(html.Div(id='total-matches'),md=2)
        ],style={'marginLeft':'10 px'}
    ),
    html.Hr(),
    dbc.Row(
        [
            dbc.Col(html.Div("Total Matches Won :"),md=8),
            dbc.Col(html.Div(id='total-won'),md=2)
        ]
    ),
    html.Hr(),
    dbc.Row(
        [
            dbc.Col(html.Div("Winning % : "),md=8),
            dbc.Col(html.Div(id='winning-percent'),md=2)
        ]
    )
    ]
)

tab1_content= dbc.Card(
    [
        dbc.Row(
            [
                #dbc.Col(md=2),
                dbc.Col(form, md=6),
                #dbc.Col(md=2)
            ],justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(table,md=4)
            ],
            justify="center"
        ),
        html.H3('Yearly Stats 📈'),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="team-matches"), md=4),
                dbc.Col(dcc.Graph(id="team-wins"), md=4),
                dbc.Col(dcc.Graph(id="team-wins-percent"), md=4)
            ],
            align="center",
        ),
        html.H3('Team-Wise Stats 📈'),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="team-matches-twise"), md=4),
                dbc.Col(dcc.Graph(id="team-won-twise"), md=4),
                dbc.Col(dcc.Graph(id="team-win-percent-twise"), md=4)
            ],
            align="center",
        )
    ]
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)
tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Team Performance"),
        dbc.Tab(tab2_content, label="Player Performance"),
        dbc.Tab(
            "This tab's content is never seen", label="Tab 3", disabled=True
        ),
    ]
)
app.layout = dbc.Container(
    [
        html.H1("IPL Analytics 🏆"),
        html.Hr(),
        tabs
    ],
    fluid=True
)
@app.callback(
    Output('total-matches', "children"),
    Input("team-filter", "value")
)
def team_total_matches(team):
    return get_grand_total(team,'match')

@app.callback(
    Output('total-won', "children"),
    Input("team-filter", "value")
)
def team_total_wins(team):
    return get_grand_total(team,'winner')

@app.callback(
    Output('winning-percent', "children"),
    Input('total-matches', "children"),
    Input('total-won', "children"),
)
def wins_percent(total,won):
    return str(round(won*100/total))+'%'


@app.callback(
    Output("team-matches", "figure"),
    Input("team-filter", "value")
)
def team_matches_year(team):
    a=get_yearly_total(team,'match')
    a=pd.DataFrame(a)
    a=a.reset_index().rename(columns={0:'matches_played'})
    fig = px.bar(a, x='year', y='matches_played',title=f'Matches Played by {team}')
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
    fig = px.bar(a, x='year', y='matches_won',title=f'Matches Won by {team}')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    return fig

@app.callback(
    Output("team-wins-percent", "figure"),
    Input("team-filter", "value")
)
def team_wins_percent(team):
    a=get_yearly_total(team,'match')
    b=get_yearly_total(team,'win')
    c=(b*100/a).fillna(0).apply(round)
    a=pd.DataFrame(c)
    a=a.reset_index().rename(columns={0:'win%'})
    fig = px.bar(a, x='year', y='win%',title=f'% Won by {team}')
    
    return fig
@app.callback(
    Output("team-matches-twise", "figure"),
    Input("team-filter", "value")
)
def matches_team_wise(team):
    a=get_team_wise_total(team,'match')
    a=pd.DataFrame(a)
    a=a.reset_index().rename(columns={'index':'team',0:'matches_played'})
    fig = px.bar(a.sort_values(by='matches_played'), y='team',x='matches_played',title=f'Matches played by {team}')
    fig.update_layout(
    autosize=False,
    width=400,
    height=300,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
        )
    )
    return fig

@app.callback(
    Output("team-won-twise", "figure"),
    Input("team-filter", "value")
)   
def wins_team_wise(team):
    a=get_team_wise_total(team,'winner')
    a=pd.DataFrame(a)
    a=a.reset_index().rename(columns={'index':'team',0:'matches_won'})
    fig = px.bar(a.sort_values(by='matches_won'), y='team', x='matches_won',title=f'Matches Won by {team}')
    fig.update_layout(
    autosize=False,
    width=400,
    height=300,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
        )
    )
    return fig

@app.callback(
    Output("team-win-percent-twise", "figure"),
    Input("team-filter", "value")
)  
def win_percent_team_wise(team):
    a=get_team_wise_total(team,'match')
    b=get_team_wise_total(team,'win')
    c=(b*100/a).fillna(0).apply(round)
    a=pd.DataFrame(c)
    a=a.reset_index().rename(columns={'index':'team',0:'win%'})
    
    fig = px.bar(a.sort_values(by='win%'), y='team', x='win%',title=f'% Won by {team}')
    
    fig.update_layout(
    autosize=False,
    width=400,
    height=300,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
        )
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)