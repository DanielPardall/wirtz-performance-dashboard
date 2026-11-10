from dash import Dash, html, dcc, Output, Input, State, ctx
import visualizations as vz
import json
import os

# --- Configuração ---
player_name = "Florian Wirtz"
comp_id = 9
season_id = 281
data_path = "./data"
matches_path = os.path.join(data_path, "matches", str(comp_id), f"{season_id}.json")
with open(matches_path, encoding='utf-8') as f:
    matches = json.load(f)
match_ids = [m['match_id'] for m in matches]

# --- Gerar visualizações ---
apresentacao = vz.apresentar_jogador(player_name=player_name, image_path="assets/Wirtz.jpg", data_path=data_path)
passes_sucesso, passes_erro = vz.get_pass_data_plotly(player_name, comp_id, season_id, data_path)
fig_pizza = vz.plot_pizza_passes(passes_sucesso, passes_erro)
fig_direcao = vz.plot_direcao_passes(player_name, comp_id, season_id, data_path)
fig_len = vz.plot_pass_length(player_name, comp_id, season_id, data_path)
fig_passes_all = vz.plot_passes_combined(passes_sucesso, passes_erro)
fig_passes_success = vz.plot_passes_success_only(passes_sucesso)
fig_passes_error = vz.plot_passes_error_only(passes_erro)
fig_key_passes = vz.plot_key_passes(player_name, comp_id, season_id, data_path)
fig_assists = vz.plot_goal_assists(player_name, comp_id, season_id, data_path)
fig_xg_bubbles = vz.plot_xg_bubble_shots(match_ids, player_name, data_path)
G, node_sizes, edge_widths, node_colors, pass_counts, pair_passes = vz.get_pass_network_data(match_ids, data_path)
fig_pass_network = vz.plot_pass_network(G, node_sizes, edge_widths, node_colors, pass_counts, pair_passes)
fig_shot_resume = vz.shot_resume(match_ids, player_name, data_path)
fig_dribbles_all = vz.dribbles_all(player_name="Florian Wirtz", data_path="./data", comp_id=9, season_id=281)
fig_dribbles_sucess = vz.dribbles_sucess(player_name="Florian Wirtz", data_path="./data", comp_id=9, season_id=281)
fig_dribbles_failed = vz.dribbles_failed(player_name="Florian Wirtz", data_path="./data", comp_id=9, season_id=281)
fig_dribbles_nutmeg_sucess = vz.dribbles_nutmeg_sucess(player_name="Florian Wirtz", data_path="./data", comp_id=9, season_id=281)
fig_dribbles_nutmeg_failed = vz.dribbles_nutmeg_failed(player_name="Florian Wirtz", data_path="./data", comp_id=9, season_id=281)
fig_pie_dribbles = vz.plot_dribble_success_donut("Florian Wirtz", 9, 281, "./data")
fig_pie_nutmeg = vz.plot_nutmeg_success_donut("Florian Wirtz", 9, 281, "./data")


# Remates com hover
with open(matches_path, encoding='utf-8') as f:
    matches = json.load(f)
match_ids = [m['match_id'] for m in matches]
match_dict = vz.get_match_id_name_dict(matches_path)
fig_remates_hover = vz.plot_shots_plotly_with_hover(match_ids, player_name, data_path, match_dict)

# --- App ---
app = Dash(__name__)

server = app.server

app.layout = html.Div(style={'fontFamily': 'Arial', 'paddingLeft': '30px', 'paddingRight': '30px', 'paddingBottom': '40px'}, children=[
    html.Div(
        children=[
            html.Span("Performance Overview | ", style={
                'fontWeight': 'normal',
                'fontSize': '24px'  
            }),
            html.Span("Florian Wirtz", style={
                'fontWeight': 'bold',
                'fontSize': '35px'  
            }),
            html.Span(" | 1. Bundesliga 2023/24", style={
                'fontWeight': 'normal',
                'fontSize': '24px'  
            })
        ],
        style={
            'backgroundColor': '#171B26',
            'color': 'white',
            'textAlign': 'center',
            'padding': '20px 0',
            'marginBottom': '20px',
            'letterSpacing': '1px'
        }
    ),

    html.Hr(style={
        'border': 'none',
        'borderTop': '2px solid solid rgba(189, 31, 48, 0.3)',
        'margin': '30px 0 20px 0',
        'width': '90%',
        'marginLeft': 'auto',
        'marginRight': 'auto'
    }),

    # Introdução visualmente mais apelativa
    html.Div([
        html.H2("Season Overview", style={
            'textAlign': 'center',
            'color': '#333333',
            'fontSize': '26px',
            'marginBottom': '14px',
            'letterSpacing': '0.5px'
        }),
        html.Div([
            html.P([
                html.Span("Florian Wirtz had an outstanding 2023/24 season, helping Bayer Leverkusen win their "),
                html.B("first"),
                html.Span(" Bundesliga title. With consistent performances throughout the year, he was named "),
                html.B("Bundesliga Player of the Season"),
                html.Span(".")
            ], style={
                'marginBottom': '18px',
                'textAlign': 'justify',
                'textJustify': 'inter-word'
            }),
            html.P("This dashboard highlights his key contributions in passing, shooting, positioning and overall impact during the campaign.", style={
                'marginBottom': '0',
                'textAlign': 'justify',
                'textJustify': 'inter-word'
            }),
        ], style={
            'color': '#333',
            'fontSize': '17px',
            'lineHeight': '1.5',
            'maxWidth': '800px',
            'margin': '0 auto',
            'padding': '0 18px'
        })
    ], style={
        'backgroundColor': '#f4f4f4',
        'padding': '35px 28px',
        'borderRadius': '12px',
        'width': '80%',
        'margin': '0 auto 10px auto',
        'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.06)',
        'border': '0.1px solid #171B26'
    }),

    html.Nav([
        html.A("Player Profile", href="#player-profile", className="nav-link"),
        html.A("Attribute Summary", href="#attribute-summary", className="nav-link"),
        html.A("Player Comparison", href="#comparison", className="nav-link"),
        html.A("Action Heatmap", href="#heatmap", className="nav-link"),
        html.A("Passing", href="#passing", className="nav-link"),
        html.A("Shooting", href="#shooting", className="nav-link"),
        html.A("Dribbling", href="#dribbling", className="nav-link"),
        html.A("Team Passing", href="#team-passing", className="nav-link"),
        
    ],
    id="nav-bar",
    style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'gap': '20px',
        'padding': '8px',
        'position': 'sticky',
        'top': '0',
        'backgroundColor': 'rgb(23, 27, 38, 0.9)',
        'zIndex': '1000',
        'borderBottom': '1px solid #444',
        'borderRadius': '4px',
        'width': '70%',
        'marginLeft': 'auto',
        'marginRight': 'auto',
        'transition': 'transform 0.3s ease'
    }),



    # Outra pequena linha abaixo
    html.Hr(id = "player-profile", style={
        'border': 'none',
        'borderTop': '2px solid solid rgba(189, 31, 48, 0.3)',
        'margin': '20px 0 30px 0',
        'width': '90%',
        'marginLeft': 'auto',
        'marginRight': 'auto'
    }),

    html.Div([
        dcc.Graph(figure=apresentacao, style={
            'width': '63.5%',
            'margin': '0 auto',
            'padding': '0'
        }, config={'displayModeBar': False})
    ], style={'marginBottom': '40px'}),

    html.Hr(id = "attribute-summary", style={
        'border': 'none',
        'borderTop': '1px solid #ccc',
        'margin': '40px 0'
    }),

    html.H2("Player Performance Metrics (per 90 mins)", style={'textAlign': 'center'}),
    html.Div([
        
        html.Div([
            html.H4("Defensive Metrics"),
            html.Ul([
                html.Li([html.B("Tackles: "), "When the player successfully challenges and wins the ball."], style={'marginBottom': '10px'}),
                html.Li([html.B("Ball Recoveries: "), "Recovering possession of a loose or uncontrolled ball."], style={'marginBottom': '10px'}),
                html.Li([html.B("Pressures: "), "Applying pressure to an opponent in possession."], style={'marginBottom': '10px'})
            ]),
            html.H4("Attacking Metrics"),
            html.Ul([
                html.Li([html.B("Goals: "), "Number of goals scored."], style={'marginBottom': '10px'}),
                html.Li([html.B("Shots: "), "Total shot attempts toward goal."], style={'marginBottom': '10px'}),
                html.Li([html.B("Expected Goals (xG): "), "Expected goals from shot attempts"], style={'marginBottom': '10px'})
            ]),
            html.H4("Build-up & Creative Metrics"),
            html.Ul(id="comparison", children=[
                html.Li([html.B("Completed Passes: "), "Total number of successful passes completed."], style={'marginBottom': '10px'}),
                html.Li([html.B("Progressive Passes: "), "Passes moving the ball significantly forward (≥25m)."], style={'marginBottom': '10px'}),
                html.Li([html.B("Assists: "), "Passes leading directly to a goal."], style={'marginBottom': '10px'}),
                html.Li([html.B("Key Passes: "), "Passes leading to a shot attempt."], style={'marginBottom': '10px'}),
                html.Li([html.B("Successful Dribbles: "), "Dribbles where the player beats the defender."], style={'marginBottom': '10px'})
            ])
        ], className='hover-reveal', style={'width': '28%', 'paddingLeft': '0px', 'fontSize': '12px', 'textAlign': 'justify', 'textJustify': 'inter-word', 'lineHeight': '1.4', 'maxWidth': '280px', 'marginTop': '10px'}),
        
        
        html.Div([
            html.Img(id="radar-img", src="/assets/radar_wirtz.png", style={  
                "marginTop": "15px",
                "marginBottom": "10px"
            }),

            html.Div([
                html.Div("Compare with", style={
                    'backgroundColor': 'white',
                    'padding': '10px 12px',
                    'borderRight': '1px solid #ccc',
                    'borderRadius': '6px 0 0 6px',
                    'color': '#555',
                    'fontSize': '15px',
                    'whiteSpace': 'nowrap',
                    'display': 'flex',
                    'alignItems': 'center'
                }),

                html.Div([
                    dcc.Dropdown(
                        id='player-compare-dropdown',
                        options=[
                            {'label': "Antoine Griezmann", 'value': 'wirtz_griezmann.png'},
                            {'label': "Lionel Messi", 'value': 'wirtz_messi.png'},
                            {'label': "Amine Adli", 'value': 'wirtz_adli.png'},
                            {'label': "Victor Boniface", 'value': 'wirtz_boniface.png'},
                            {'label': "Neymar Junior", 'value': 'wirtz_neymar.png'},
                            {'label': "Kylian Mbappé", 'value': 'wirtz_mbappe.png'},
                            {'label': "Ousmane Dembélé", 'value': 'wirtz_dembele.png'}
                        ],
                        placeholder="Select...",
                        style={
                            'width': '100%',
                            'border': 'none',
                            'fontSize': '15px'
                        },
                        clearable=True
                    )
                ], style={
                    'flexGrow': '1',
                    'display': 'flex',
                    'alignItems': 'center'
                })

            ], style={
                'display': 'flex',
                'width': '360px',
                'margin': '20px auto',
                'border': '1px solid #ccc',
                'borderRadius': '6px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'backgroundColor': 'white'
            })
        ], style={"textAlign": "center"}),

    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'width': '80%', 'padding': '0px'}),

    html.Hr(id= "heatmap", style={
        'border': 'none',
        'borderTop': '1px solid #ccc',
        'margin': '40px 0'
    }),

    html.H2("Season Action Density Map", style={'textAlign': 'center', 'marginBottom': '35px'}),

    html.Div([

        html.Div([
            html.Img(src="/assets/heatmap.png", style={
                'width': '100%', 'borderRadius': '12px',
                'boxShadow': '0px 4px 12px rgba(0, 0, 0, 0)'
            })
        ], style={
            'width': '60%',
            'margin': '0 auto',
            'position': 'relative',
            'marginRight': '30px'  
        }),

        html.Div([
            html.P(["This visualization captures the spatial density of all on-field events involving Florian Wirtz throughout the season, including both ", html.B("on-ball"), " and ",  html.B("off-ball actions"), "."], style={'marginBottom': '18px'}),
            html.P(["The heat intensity indicates areas of higher activity, with a clear emphasis on the left attacking corridor."], style={'marginBottom': '18px'}),
            html.P([
                "The ", html.B("median event location"),
                ", shown directly on the pitch, aligns with his typical positioning in the role of a ",
                html.B("Left Attacking Midfielder"), "."
            ], style={'marginBottom': '18px'})
        
        ], className='hover-reveal', style={
            'width': '17%',
            'fontSize': '13px',
            'textAlign': 'justify',
            'textJustify': 'inter-word',
            'lineHeight': '1.4',
            'maxWidth': '320px',
            'marginLeft': '0px',
            'marginTop': '14px'
        })

    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'flex-start',
        'marginBottom': '0px'
    }),

    html.Hr(id="passing", style={
        'border': 'none',
        'borderTop': '1px solid #ccc',
        'margin': '40px 0'
    }),

    html.H2("Season Passing Performance", style={'textAlign': 'center'}),
    html.Div([
        dcc.RadioItems(
            id='pass-type-selector',
            options=[
                {'label': 'All Passes', 'value': 'all'},
                {'label': 'Successful Passes', 'value': 'success'},
                {'label': 'Unsuccessful Passes', 'value': 'error'}
            ],
            value='all',
            labelStyle={'display': 'inline-block', 'marginRight': '20px'},
            style={"textAlign": "center", 'marginBottom': '0px'}
        )
    ]),

    html.Div([
        dcc.RadioItems(
            id='sub-success-type-selector',
            options=[
                {'label': 'All Successful Passes', 'value': 'success_all'},
                {'label': 'Key Passes', 'value': 'key'},
                {'label': 'Assists', 'value': 'assists'}
            ],
            value='success_all',
            labelStyle={'display': 'inline-block', 'marginRight': '20px'},
            style={'textAlign': 'center'}
        )
    ], id='sub-pass-options', style={
        'textAlign': 'center',
        'marginTop': '0px',
        'marginBottom': '0px',
        'minHeight': '28px',     
        'overflow': 'hidden',
        'visibility': 'hidden'
    }),

    html.Div([
        html.Span("Successful", style={
            'color': '#1F77B4',
            'marginRight': '10px',
            'fontWeight': 'bold'
        }),
        html.Span("|", style={'marginRight': '10px'}),
        html.Span("Unsuccessful", style={
            'color': '#D62728',
            'fontWeight': 'bold'
        })
    ], style={
        'textAlign': 'center',
        'marginTop': '10px',  
        'marginBottom': '5px',
        'fontSize': '18px'
    }),

    html.Div([
        html.Div([
            html.Div([
                dcc.Loading(
                    id='loading-pass-map',
                    type='default',
                    children=dcc.Graph(
                        id='pass-map-plotly',
                        figure=fig_passes_all,
                        style={
                            'width': '580px',
                            'height': '480px',
                            'margin': '0',
                            'padding': '0'
                        },
                        config={'displayModeBar': False}
                    
                    ), style={'marginLeft': '400px'}
                )
            ], style={
                'flex': '0 0 auto',
                'marginRight': '30px'
            }),

            html.Div([
                dcc.Loading(
                    id='loading-pizza',
                    type='default',
                    children=dcc.Graph(
                        figure=fig_pizza,
                        style={'height': '200px', 'marginBottom': '8px'},
                        config={'displayModeBar': False}
                    )
                ),
                dcc.Loading(
                    id='loading-direction',
                    type='default',
                    children=dcc.Graph(
                        figure=fig_direcao,
                        style={'height': '220px', 'marginBottom': '8px'},
                        config={'displayModeBar': False}
                    )
                ),
                dcc.Loading(
                    id='loading-length',
                    type='default',
                    children=dcc.Graph(
                        figure=fig_len,
                        style={'height': '220px'},
                        config={'displayModeBar': False}
                    )
                )
            ], style={
                'flex': '0 0 auto',
                'width': '310px',
                'paddingTop': '30px',
                'marginLeft': '400px'
            })
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'alignItems': 'flex-start',
            'gap': '10px'
        })
    ], style={
        'width': '100%',
        'paddingLeft': '50px',  
        'boxSizing': 'border-box',
        'marginTop': '-10px',
        'marginBottom': '30px'
    }),

    html.Div([
        html.P([
            "This section visualizes ", html.B("all passes"), " made by the player throughout the season, colored by outcome."
            ]),
        html.P([
            "Each pass includes hover info with the ", html.B("match, body part, height, and length"),
            ". ", html.B("Key passes"), " (those that lead directly to a shot) and ", html.B("assists"),
            " also display the receiving player."
        ]),
        html.P([
            "The player showed a ", html.B("high success rate (83.8%)"), 
            ". ", html.B("Unsuccessful"), " passes are mostly found near the opponent’s penalty area, while ", html.B("successful"), " ones are more dispersed, especially in the attacking midfield."
        ]),
        html.P([
            html.B("Forward passes"), " are the least frequent and most error-prone, likely due to tighter defensive coverage. ",
            html.B("Long passes"), " (over 25 meters) also show a higher failure rate, reflecting the natural difficulty of executing longer-range deliveries accurately."
        ])
    ], className='pass-info'),


    html.Hr(id="shooting", style={
        'border': 'none',
        'borderTop': '1px solid #ccc',
        'margin': '40px 0'
    }),

   html.H2("Shot Placement and Finishing Outcome Distribution", style={'textAlign': 'center'}),
    html.Div([], style={'marginBottom': '26px'}),
    # Botão centralizado entre o título e a visualização
    html.Div([
        html.Button("Shot Summary", id="open-modal", className="hover-grow-button", n_clicks=0, style={
            'backgroundColor': '#171B26',
            'color': 'white',
            'border': 'none',
            'padding': '6px 12px',
            'borderRadius': '4px',
            'fontSize': '13px',
            'cursor': 'pointer',
            'margin': '10px auto',
            'display': 'block'
        })
    ]),

    # Secção principal: texto + gráfico
    html.Div([

        # Texto explicativo à esquerda
        html.Div([
            html.P([
                "This visualization displays all shots taken by the player throughout the season that ",
                html.B("crossed the end line towards goal"),
                ", categorized by outcome."
            ], style={'marginBottom': '18px'}),
            html.P([
                html.B("Each marker is interactive:"),
                " Double-clicking the plot zooms out to reveal all attempts. Hovering shows details such as the match, body part used, and shot height (in meters)."
            ], style={'marginBottom': '18px'}),
            html.P([
                "Clicking the ",
                html.B("Shot Summary"),
                " button opens a circular breakdown showing the percentage of shots in each outcome category."
            ], style={'marginBottom': '18px'}),
                        
            html.P([
                html.B("Note:"),
                " While the projection offers an intuitive view of shot placement and finishing, positional data may include minor ",
                html.B("inaccuracies"),
                "."
            ], style={'marginBottom': '18px'})
        ], className='hover-reveal', style={
            'width': '15%',
            'fontSize': '13px',
            'textAlign': 'justify',
            'textJustify': 'inter-word',
            'lineHeight': '1.4',
            'maxWidth': '360px',
            'marginRight': '30px',
            'marginTop': '-80px'
        }),

        # Gráfico e modal à direita
        html.Div([
            dcc.Graph(
                figure=fig_remates_hover,
                style={'width': '100%', 'marginLeft': '-300px', 'padding': '0'},
                config={'displayModeBar': False}
            ),

            html.Div([
                html.Div([

                    # Linha superior do modal com título e botão de fechar
                    html.Div([
                        html.Div(style={'width': '30px'}),  # espaço à esquerda
                        html.H4("Shot Summary", style={'textAlign': 'center', 'flexGrow': 1, 'margin': '0'}),
                        html.Button("×", id="close-modal", n_clicks=0, style={
                            'fontSize': '22px',
                            'border': 'none',
                            'background': 'none',
                            'cursor': 'pointer'
                        }),
                    ], style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'space-between',
                        'padding': '8px 8px 0px 8px'
                    }),

                    # Gráfico dentro do modal
                    dcc.Graph(
                        id="custom-modal-graph",
                        figure=fig_shot_resume,
                        style={'height': '520px', 'marginTop': '10px'},
                        config={'displayModeBar': False}
                    )

                ], style={
                    'backgroundColor': 'white',
                    'padding': '10px',
                    'borderRadius': '8px',
                    'width': '80%',
                    'maxWidth': '800px',
                    'boxShadow': '0 4px 12px rgba(0,0,0,0.2)'
                })
            ], id='modal', style={
                'display': 'none',
                'position': 'fixed',
                'top': 0,
                'left': 0,
                'width': '100%',
                'height': '100%',
                'backgroundColor': 'rgba(0,0,0,0.5)',
                'zIndex': 9999,
                'justifyContent': 'center',
                'alignItems': 'center'
            }, n_clicks=0)

        ], style={'width': '56.7%'})

    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'flex-start',
        'marginBottom': '40px',
        'padding': '0px'
    }),

    html.Hr(style={
        'border': 'none',
        'borderTop': '1px solid #ccc',
        'margin': '40px 0'
    }),

    html.H2("Expected Goals (xG) and Finishing Outcomes Map", style={'textAlign': 'center', 'marginBottom': '7px'}),

    html.Div([

        # Visualização (lado esquerdo)
        html.Div([
            dcc.Graph(figure=fig_xg_bubbles, style={
                'width': '100%', 'borderRadius': '12px',
                'boxShadow': '0px 4px 12px rgba(0, 0, 0, 0)',
                'padding': '0', 'margin': '0 auto'
            }, config={'displayModeBar': False})
        ], style={
            'width': '65%',
            'margin': '0 auto',
            'position': 'relative',
            'marginLeft': '370px'
        }),

        # Texto (lado direito)
        html.Div([
            html.P("This visualization displays all shots taken by the player throughout the season, including those that were blocked before crossing the end line.", style={'marginBottom': '18px'}),
            html.P([
                html.B("Expected Goals (xG): "),
                "A statistical metric estimating the likelihood of a goal being scored, based on the shot’s characteristics, including location, angle, and type."
            ], style={'marginBottom': '-13px'}),

            html.P([
                html.B("Total xG"), 
                ": represents the total xG value from all shot attempts."
            ], style={'marginBottom': '18px'}),

            html.P([
                "The map highlights that all shot attempts were made in the opponent’s half, with the most distant one recording an ",
                html.B("xG of 0.03"),
                ". The shot with the highest xG value (",
                html.B("0.78"),
                ") resulted from a ",
                html.B("penalty kick"),
                ", which reflects the typically high scoring probability in those situations."
            ], style={'marginBottom': '18px'})
        ], className='hover-reveal', style={
            'width': '17%',
            'fontSize': '13px',
            'textAlign': 'justify',
            'textJustify': 'inter-word',
            'lineHeight': '1.4',
            'maxWidth': '320px',
            'marginLeft': '0px',
            'marginRight': '50px',
            'marginTop': '40px'
        })

    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'flex-start',
        'marginBottom': '0px'
    }),

    html.Hr(id= "dribbling", style={
        'border': 'none',
        'borderTop': '1px solid #ccc',
        'margin': '40px 0'
    }),


    html.H2("Season Dribbling Performance", style={'textAlign': 'center'}),

    # Seletor principal (All, Successful, Unsuccessful)
    html.Div([
        dcc.RadioItems(
            id='dribble-type-selector',
            options=[
                {'label': 'All Dribbles', 'value': 'all'},
                {'label': 'Successful Dribbles', 'value': 'success'},
                {'label': 'Unsuccessful Dribbles', 'value': 'fail'}
            ],
            value='success',
            labelStyle={'display': 'inline-block', 'marginRight': '20px'},
            style={"textAlign": "center", 'marginBottom': '0px'}
        )
    ]),

    # Sub-seletor (apenas se Success ou Fail)
    html.Div([
        dcc.RadioItems(
            id='sub-dribble-type-selector',
            options=[
                {'label': 'All Successful Dribbles', 'value': 'success_all'},
                {'label': 'Nutmegs', 'value': 'success_nutmeg'}
            ],
            value='success_all',
            labelStyle={'display': 'inline-block', 'marginRight': '20px'},
            style={'textAlign': 'center'}
        )
    ], id='sub-dribble-options', style={
        'textAlign': 'center',
        'marginTop': '0px',
        'marginBottom': '0px',
        'minHeight': '28px',
        'overflow': 'hidden',
        'visibility': 'visible'
    }),

    # Legenda
    html.Div([
        html.Span("Successful", style={
            'color': '#1F77B4',
            'marginRight': '10px',
            'fontWeight': 'bold'
        }),
        html.Span("|", style={'marginRight': '10px'}),
        html.Span("Unsuccessful", style={
            'color': '#D62728',
            'fontWeight': 'bold'
        })
    ], style={
        'textAlign': 'center',
        'marginTop': '10px',
        'marginBottom': '5px',
        'fontSize': '18px'
    }),

    # Gráficos
    html.Div([
        html.Div([
            dcc.Graph(
                id='dribble-map-plotly',
                figure=fig_dribbles_sucess,
                style={'width': '580px', 'height': '480px', 'margin': '0', 'padding': '0'},
                config={'displayModeBar': False}
            )
        ], style={'flex': '0 0 auto', 'marginRight': '30px'}),

        html.Div([
            dcc.Graph(
                id='dribble-pie-all',
                figure=fig_pie_dribbles,
                style={'height': '250px', 'marginBottom': '60px'},
                config={'displayModeBar': False}
            ),
            dcc.Graph(
                id='dribble-pie-nutmeg',
                figure=fig_pie_nutmeg,
                style={'height': '250px'},
                config={'displayModeBar': False}
            )
        ], style={
            'flex': '0 0 auto',
            'width': '310px',
            'paddingTop': '65px',
            'marginLeft': '400px'
        })
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'flex-start',
        'gap': '10px',
        'width': '100%',
        'paddingLeft': '50px',
        'marginLeft': '30px',
        'boxSizing': 'border-box',
        'marginTop': '0px',
        'marginBottom': '30px'
    }),

    html.Div([], style={'marginBottom': '90px'}),

    html.Div([
        html.P([
            "This section visualizes ", html.B("all dribbles"), " attempted by the player throughout the season, colored by outcome."
        ]),
        html.P([
            "A dribble is defined as ", html.B("an attempt by a player to beat an opponent while retaining possession"), 
            ". Blue markers indicate successful dribbles, and red markers show unsuccessful ones."
        ]),
        html.P([
            "Circles represent ", html.B("standard dribbles"), ", while stars represent ", html.B("nutmegs"), 
            ", dribbles where the ball was played between the opponent’s legs, a move often seen as especially skillful and eye-catching."
        ]),
        html.P([
            "Each dribble includes hover information showing the ", html.B("match"), ", ", html.B("outcome"),
            ", whether it was a ", html.B("nutmeg"), ", ", html.B("overrun"), " (ball passed the defender into another player's possession), ",
            html.B("no touch"), " (the player allowed the ball to run past without touching it), and if it was done ", html.B("under pressure"),
            " from an opponent."
        ])
    ], className='dribble-info'),


    html.Div([], style={'marginBottom': '10px'}),

    html.Hr(id = "team-passing", style={
        'border': 'none',
        'borderTop': '1px solid #ccc',
        'margin': '40px 0'
    }),


    html.H2("Team Passing Network", style={'textAlign': 'center', 'marginBottom': '10px'}),

    html.Div([

        # Texto explicativo no lado esquerdo
        html.Div([
            html.P([
                "This passing network visualizes the most frequent connections among the 11 players with the highest ",
                html.B("total minutes played"), " throughout the season."
            ], style={'marginBottom': '18px'}),

            html.P([
                "Each player is positioned according to the team’s ",
                html.B("official position designation"),
                ", which reflects the typical tactical role and area they occupy within the team’s structured setup."
            ], style={'marginBottom': '18px'}),


            html.P([
                "For deeper insight into the passing dynamics, hover near the center of any connecting line to view the number of passes exchanged between the two players."
            ], style={'marginBottom': '18px'}),

        ], className='hover-reveal', style={
            'width': '13%',
            'fontSize': '13px',
            'textAlign': 'justify',
            'textJustify': 'inter-word',
            'lineHeight': '1.4',
            'maxWidth': '360px',
            'marginRight': '30px',
            'marginTop': '40px'
        }),

        # Visualização no lado direito
        html.Div([
            dcc.Graph(figure=fig_pass_network, style={
                'width': '100%', 'marginLeft': '-150px', 'padding': '0'
            }, config={'displayModeBar': False})
        ], style={'width': '73%'})

    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'flex-start',
        'marginBottom': '0px',
        'padding': '0px'
    }),


    html.Hr(style={
        'border': 'none',
        'borderTop': '1px solid #ccc',
        'margin': '40px 0'
    }),

    html.Div("↑", id="scroll_top", n_clicks=0, className="scroll-button"),

    html.Footer([
        html.Div([
            html.P("© 2025 | Dashboard developed by Daniel Monteiro", style={
                'margin': '0',
                'color': 'white',
                'fontSize': '17.5px',
                'lineHeight': '1.8'  
            }),
            html.P([
                html.Span("Contacts: ", style={'fontWeight': 'bold'}),
                "Daniel Monteiro (uc2021248878@student.uc.pt)"
            ], style={
                'margin': '4px 0',
                'color': 'white',
                'fontSize': '13px',
                'lineHeight': '1.8'
            }),
            html.P([html.Span("Data source: ", style={'fontWeight': 'bold'}), "Hudl StatsBomb open data"], style={
                'margin': '0',
                'color': 'white',
                'fontSize': '13px',
                'lineHeight': '1.8'
            })
        ], style={
            'textAlign': 'center',
            'padding': '20px',
            'maxWidth': '1000px',
            'margin': '0 auto'
        })
    ], style={
        'backgroundColor': '#171B26',
        'marginTop': '40px'
    })

])

# --- Callbacks ---
@app.callback(
    Output("radar-img", "src"),
    Input("player-compare-dropdown", "value")
)
def update_radar_image(selected_player_img):
    return f"/assets/{selected_player_img}" if selected_player_img else "/assets/radar_wirtz.png"

@app.callback(
    Output("sub-pass-options", "style"),
    Input("pass-type-selector", "value")
)
def toggle_sub_options(pass_type):
    return {
        'textAlign': 'center',
        'marginTop': '0px',
        'marginBottom': '0px',
        'minHeight': '28px',
        'overflow': 'hidden',
        'visibility': 'visible' if pass_type == 'success' else 'hidden'
    }

@app.callback(
    Output('modal', 'style'),
    Input('open-modal', 'n_clicks'),
    Input('close-modal', 'n_clicks'),
    Input('modal', 'n_clicks'),
    State('modal', 'style')
)
def toggle_modal(n_open, n_close, n_bg_click, current_style):
    triggered = ctx.triggered_id

    if triggered == 'open-modal':
        return {**current_style, 'display': 'flex'}
    elif triggered in ['close-modal', 'modal']:
        return {**current_style, 'display': 'none'}
    return current_style

@app.callback(
    Output("radar-img", "style"),
    Input("player-compare-dropdown", "value")
)
def adjust_radar_size(selected):
    if selected:
        return {
            "width": "79%",  
            "marginTop": "10px",
            "marginBottom": "10px",
            "marginLeft": "auto",
            "marginRight": "auto"
        }
    else:
        return {
            "width": "85%",  
            "marginLeft": "25px",
            "marginTop": "15px",
            "marginBottom": "10px"
        }

@app.callback(
    Output("pass-map-plotly", "figure"),
    Input("pass-type-selector", "value"),
    Input("sub-success-type-selector", "value")
)
def update_pass_map(main_selection, sub_selection):
    if main_selection == 'all':
        return fig_passes_all
    elif main_selection == 'success':
        if sub_selection == 'key':
            return fig_key_passes
        elif sub_selection == 'assists':
            return fig_assists
        else:
            return fig_passes_success
    elif main_selection == 'error':
        return fig_passes_error

@app.callback(
    Output('sub-dribble-type-selector', 'options'),
    Output('sub-dribble-type-selector', 'value'),
    Output('dribble-map-plotly', 'figure'),
    Input('dribble-type-selector', 'value'),
    Input('sub-dribble-type-selector', 'value')
)
def update_dribble_graphs(dribble_type, sub_type):
    if dribble_type == 'success':
        sub_options = [
            {'label': 'All Successful Dribbles', 'value': 'success_all'},
            {'label': 'Nutmegs', 'value': 'success_nutmeg'}
        ]
        default = sub_type if sub_type in ['success_all', 'success_nutmeg'] else 'success_all'
        fig_map = fig_dribbles_sucess if default == 'success_all' else fig_dribbles_nutmeg_sucess

    elif dribble_type == 'fail':
        sub_options = [
            {'label': 'All Unsuccessful Dribbles', 'value': 'fail_all'},
            {'label': 'Nutmegs', 'value': 'fail_nutmeg'}
        ]
        default = sub_type if sub_type in ['fail_all', 'fail_nutmeg'] else 'fail_all'
        fig_map = fig_dribbles_failed if default == 'fail_all' else fig_dribbles_nutmeg_failed

    else:  # dribble_type == 'all'
        sub_options = []
        default = None
        fig_map = fig_dribbles_all

    return sub_options, default, fig_map


@app.callback(
    Output("sub-dribble-options", "style"),
    Input("dribble-type-selector", "value")
)
def toggle_dribble_sub_options(main_type):
    return {
        'textAlign': 'center',
        'marginTop': '0px',
        'marginBottom': '0px',
        'minHeight': '28px',
        'overflow': 'hidden',
        'visibility': 'visible' if main_type in ['success', 'fail'] else 'hidden'
    }


# --- Run ---
if __name__ == '__main__':
    app.run(debug=True)
