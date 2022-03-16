from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = (pd.read_csv("games.csv")
      .dropna()
      .loc[lambda x: x.Year_of_Release >= 2000]
      .astype({
          'Year_of_Release': int
          , 'Platform': 'category'
          , 'Genre': 'category'
          , 'Rating': 'category'
      })
      .loc[lambda x: x.User_Score != 'tbd']
      .astype({
          'User_Score': float
      })
     )
genres_values = list(df.Genre.unique())
ratings_values = list(df.Rating.unique()), 

app.layout = html.Div(children=[
    html.Div(
        children=[html.H3(
            children='Динамика состояния игровой индустрии',
            ),
            ]),
    html.Hr(),
    html.Div(children=[
        html.Div(children=[
            html.P("На дашбордах ниже представлены:")
            , html.Ul(children=[
                html.Li(children='статистика по количеству выпущенных игр за выбранный период времени'),
                html.Li(children='распределение выпущенных игр по Платформам'),
                html.Li(children='статистика оценок зрителей и критиков')
                ])
            ], style={'padding': 5, 'flex': 1}),
        html.Div(children=[
            html.P("Используя имеющиеся фильтры можно ограничить данные:")
            , html.Ul(children=[
                html.Li('по жанрам, в которых выпущены игры'),
                html.Li('по рейтингу контента'),
                html.Li('по годам выпуска')
                ])
            ], style={'padding': 5, 'flex': 1}),

        ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Hr(),

    html.Div([
        html.Div(children=[
            html.Label('Фильтр жанров, в которых выпущены игры'),
            dcc.Dropdown(
                options=genres_values,
                multi=True,
                value=genres_values)),
                id='genre_filter'),
            ], style={'padding': 5, 'flex': 1}),

        html.Div(children=[
            html.Label('Фильтр рейтингов'),
            dcc.Dropdown(
                options=ratings_values,
                multi=True,
                value=ratings_values,
                id='rating_filter'),
            ], style={'padding': 5, 'flex': 1})
        ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Hr(),

    html.Div([
        html.Div(
            html.Label("Количество выпушенных игр с учетом установленных фильтров")
            ,id='text1'
            , style={'padding': 5, 'flex': 1}),
        html.Div([]
            , style={'padding': 5, 'flex': 1})
        ], style={
            'display': 'flex'
            , 'flex-direction': 'row'
            , 'align-items': 'center'
            , 'justify-content': 'center'}
        ),

    html.Div([
        html.Div(children=[
            dcc.Graph(id='stacked_area_plot')
            ], style={'padding': 5, 'flex': 1}),
        html.Div(children=[
            dcc.Graph(id='scatter_plot')
            ], style={'padding': 5, 'flex': 1})
        ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Hr(),

    html.Div([
        html.Div(children=[
            html.Label('Интервал годов выпуска'),
            dcc.RangeSlider(
                step=None,
                marks={int(i): str(i) for i in sorted(list(df.Year_of_Release.unique()))},
                value=[int(df.Year_of_Release.unique().min()), int(df.Year_of_Release.unique().max())],
                id='years_slider'
                )
            ], style={'padding': 5, 'flex': 1}),
        html.Div(style={'padding': 5, 'flex': 1})
        ], style={'display': 'flex', 'flex-direction': 'row'}),
    ])


@app.callback(
        Output('stacked_area_plot', 'figure'),
        Input('years_slider', 'value'),
        Input('genre_filter', 'value'),
        Input('rating_filter', 'value')
        )
def update_figure(
        selected_years
        , selected_genres
        , selected_ratings
        ):

    years = [df.Year_of_Release.min(), df.Year_of_Release.max()] if selected_years is None else selected_years
    genres = [list(df.Genre.unique())] if selected_genres is None else selected_genres
    ratings = [list(df.Rating.unique())] if selected_ratings is None else selected_ratings

    filtered_df = (df
            .loc[(df.Year_of_Release >= years[0]) & (df.Year_of_Release <= years[1])]
            .loc[df.Genre.isin(genres)]
            .loc[df.Rating.isin(ratings)]
           )

    fig = px.area(
            (filtered_df
                .groupby(['Platform', 'Year_of_Release'])
                .agg(
                    count_of_issue=pd.NamedAgg(column='Name', aggfunc='count')
                    )
                .reset_index()
                )
            , x='Year_of_Release'
            , y='count_of_issue'
            , color='Platform'
            )
    fig.update_layout(transition_duration=300)

    return fig

@app.callback(
        Output('scatter_plot', 'figure'),
        Input('years_slider', 'value'),
        Input('genre_filter', 'value'),
        Input('rating_filter', 'value')
        )
def update_figure(
        selected_years
        , selected_genres
        , selected_ratings
        ):

    years = [df.Year_of_Release.min(), df.Year_of_Release.max()] if selected_years is None else selected_years
    genres = [list(df.Genre.unique())] if selected_genres is None else selected_genres
    ratings = [list(df.Rating.unique())] if selected_ratings is None else selected_ratings

    filtered_df = (df
            .loc[(df.Year_of_Release >= years[0]) & (df.Year_of_Release <= years[1])]
            .loc[df.Genre.isin(genres)]
            .loc[df.Rating.isin(ratings)]
           )

    fig = px.scatter(filtered_df,
            x='User_Score',
            y='Critic_Score',
            color='Genre',
            )
    fig.update_layout(transition_duration=300)

    return fig

@app.callback(
        Output('text1', 'children'),
        Input('years_slider', 'value'),
        Input('genre_filter', 'value'),
        Input('rating_filter', 'value')
        )
def calculate_issuses(
        selected_years
        , selected_genres
        , selected_ratings
        ):

    years = [df.Year_of_Release.min(), df.Year_of_Release.max()] if selected_years is None else selected_years
    genres = [list(df.Genre.unique())] if selected_genres is None else selected_genres
    ratings = [list(df.Rating.unique())] if selected_ratings is None else selected_ratings

    filtered_df = (df
            .loc[(df.Year_of_Release >= years[0]) & (df.Year_of_Release <= years[1])]
            .loc[df.Genre.isin(genres)]
            .loc[df.Rating.isin(ratings)]
           )
    label = html.Label("Количество выпушенных игр с учетом установленных фильтров")
    block = html.Div(
            children=[filtered_df.shape[0]]
            , style = {
                'width': '100%'
                , 'display': 'flex'
                , 'align-items': 'center'
                , 'justify-content': 'center'
                , 'color': 'blue'
                })

    return label, block


if __name__ == '__main__':
    app.run_server(debug=True)
