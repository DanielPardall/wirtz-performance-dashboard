# -*- coding: utf-8 -*-

# IMPORTS
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.patches import Arc, Circle, Polygon
from matplotlib.colors import Normalize
from pandas import json_normalize
import json
from PIL import Image
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from sklearn.preprocessing import MinMaxScaler
import networkx as nx
from matplotlib import cm, colors


# --- Constantes ---
player_name = "Florian Wirtz"
DATA_PATH = "./data"
comp_id, season_id = 9, 281

PLAYER_NAMES = [
    "Lukáš Hrádecký", "Granit Xhaka", "Alejandro Grimaldo García", "Jonathan Tah",
    "Florian Wirtz", "Jeremie Frimpong", "Jonas Hofmann", "Edmond Fayçal Tapsoba",
    "Exequiel Alejandro Palacios", "Victor Okoh Boniface", "Robert Andrich"
]

# Coordenadas dos jogadores
CUSTOM_POSITIONS = {
    "Lukáš Hrádecký": (11, 40),
    "Jonathan Tah": (28, 27),
    "Edmond Fayçal Tapsoba": (28, 53),
    "Alejandro Grimaldo García": (46, 70),
    "Jeremie Frimpong": (46, 10),
    "Robert Andrich": (46, 40),
    "Granit Xhaka": (60, 26),
    "Exequiel Alejandro Palacios": (60, 54),
    "Jonas Hofmann": (82, 19),
    "Florian Wirtz": (82, 61),
    "Victor Okoh Boniface": (93, 40),
}

def draw_pitch(ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))

    # Contorno do campo
    ax.plot([0, 0], [0, 80], color='black')        # Lateral esquerda
    ax.plot([0, 120], [80, 80], color='black')     # Linha superior
    ax.plot([120, 120], [80, 0], color='black')    # Lateral direita
    ax.plot([120, 0], [0, 0], color='black')       # Linha inferior

    # Linha de meio campo
    ax.plot([60, 60], [0, 80], color='black')

    # Círculo central
    ax.add_patch(Circle((60, 40), 9.15, color='black', fill=False))
    ax.add_patch(Circle((60, 40), 0.3, color='black'))  # marca do centro

    # Áreas grandes
    ax.plot([0, 18], [18, 18], color='black')
    ax.plot([18, 18], [18, 62], color='black')
    ax.plot([0, 18], [62, 62], color='black')

    ax.plot([120, 102], [18, 18], color='black')
    ax.plot([102, 102], [18, 62], color='black')
    ax.plot([102, 120], [62, 62], color='black')

    # Arcos da área
    ax.add_patch(Arc((12, 40), width=18.3, height=18.3, angle=0, theta1=310, theta2=50, color='black'))
    ax.add_patch(Arc((108, 40), width=18.3, height=18.3, angle=180, theta1=310, theta2=50, color='black'))

    # Áreas pequenas
    ax.plot([0, 6], [30, 30], color='black')
    ax.plot([6, 6], [30, 50], color='black')
    ax.plot([6, 0], [50, 50], color='black')

    ax.plot([120, 114], [30, 30], color='black')
    ax.plot([114, 114], [30, 50], color='black')
    ax.plot([114, 120], [50, 50], color='black')

    # Marcas de penálti
    ax.add_patch(Circle((12, 40), radius=0.3, color='black'))
    ax.add_patch(Circle((108, 40), radius=0.3, color='black'))

    # Balizas
    ax.plot([0, 0], [36, 44], color='black', linewidth=4)
    ax.plot([120, 120], [36, 44], color='black', linewidth=4)

    # Configurações do gráfico
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 80)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    # direção ataque
    ax.annotate(
        '', xy=(68, -3), xytext=(52, -3),
        arrowprops=dict(
            arrowstyle='-|>', 
            lw=2.2,
            color='black',
            shrinkA=0, shrinkB=0, 
            mutation_scale=25    
        ),
        annotation_clip=False
    )

    return ax

def draw_pitch_plotly_dribble():
    fig = go.Figure()

    # Contorno do campo
    fig.add_shape(type="rect", x0=0, y0=0, x1=120, y1=80, line=dict(color="black", width=2))

    # Linha de meio campo
    fig.add_shape(type="line", x0=60, y0=0, x1=60, y1=80, line=dict(color="black", width=2))

    # Círculo central
    center_circle = go.Scatter(
        x=[60 + 9.15 * np.cos(t) for t in np.linspace(0, 2 * np.pi, 200)],
        y=[40 + 9.15 * np.sin(t) for t in np.linspace(0, 2 * np.pi, 200)],
        mode='lines',
        line=dict(color='black', width=2),
        showlegend=False,
        hoverinfo="skip"
    )
    fig.add_trace(center_circle)

    fig.add_trace(go.Scatter(x=[60], y=[40], mode='markers',
                             marker=dict(color='black', size=6),
                             showlegend=False,
                             hoverinfo="skip"))

    # Áreas grandes
    fig.add_shape(type="rect", x0=0, y0=18, x1=18, y1=62, line=dict(color="black", width=2))
    fig.add_shape(type="rect", x0=102, y0=18, x1=120, y1=62, line=dict(color="black", width=2))

    # Arcos das áreas (esquerda)
    arc_left = []
    for angle in np.radians(np.linspace(310, 410, 200)):
        x = 12 + (18.3 / 2) * np.cos(angle)
        y = 40 + (18.3 / 2) * np.sin(angle)
        arc_left.append((x, y))
    fig.add_trace(go.Scatter(x=[pt[0] for pt in arc_left], y=[pt[1] for pt in arc_left],
                             mode="lines", line=dict(color="black", width=2),
                             showlegend=False, hoverinfo="skip"))

    # Arcos das áreas (direita)
    arc_right = []
    for angle in np.radians(np.linspace(130, 230, 200)):
        x = 108 + (18.3 / 2) * np.cos(angle)
        y = 40 + (18.3 / 2) * np.sin(angle)
        arc_right.append((x, y))
    fig.add_trace(go.Scatter(x=[pt[0] for pt in arc_right], y=[pt[1] for pt in arc_right],
                             mode="lines", line=dict(color="black", width=2),
                             showlegend=False, hoverinfo="skip"))

    # Áreas pequenas
    fig.add_shape(type="rect", x0=0, y0=30, x1=6, y1=50, line=dict(color="black", width=2))
    fig.add_shape(type="rect", x0=114, y0=30, x1=120, y1=50, line=dict(color="black", width=2))

    # Marcas de penálti
    fig.add_trace(go.Scatter(x=[12, 108], y=[40, 40], mode='markers',
                             marker=dict(color='black', size=6),
                             showlegend=False,
                             hoverinfo="skip"))

    # Balizas
    fig.add_shape(type="line", x0=0, y0=36, x1=0, y1=44, line=dict(color="black", width=4))
    fig.add_shape(type="line", x0=120, y0=36, x1=120, y1=44, line=dict(color="black", width=4))

    sx, sy = 52, -3  # início
    ex, ey = 68, -3  # fim

    # Linha da seta
    fig.add_trace(go.Scatter(
        x=[sx, ex], y=[sy, ey],
        mode='lines',
        line=dict(color='black', width=2.2),
        hoverinfo='skip',
        showlegend=False
    ))

    # Ponta (triângulo customizado)
    dx = ex - sx
    dy = ey - sy
    norm = np.sqrt(dx**2 + dy**2)
    ux, uy = dx / norm, dy / norm

    arrow_length = 1.5  # controla o comprimento da seta
    head_base = 0.9     # controla a largura

    tip = (ex, ey)
    left = (ex - arrow_length * ux + head_base * uy,
            ey - arrow_length * uy - head_base * ux)
    right = (ex - arrow_length * ux - head_base * uy,
             ey - arrow_length * uy + head_base * ux)

    fig.add_trace(go.Scatter(
        x=[tip[0], left[0], right[0], tip[0]],
        y=[tip[1], left[1], right[1], tip[1]],
        fill='toself',
        fillcolor='black',
        line=dict(color='black'),
        mode='lines',
        hoverinfo='skip',
        showlegend=False
    ))
    
    fig.add_annotation(
        x=59.5, y=-4,
        text="Attack Direction",
        showarrow=False,
        font=dict(size=12),
        xanchor='center',
        yanchor='top'
    )
    
    # Configurações finais
    fig.update_layout(
        xaxis=dict(range=[0, 122], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-5, 85], showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
        plot_bgcolor='white',
        margin=dict(l=0, r=0, t=0, b=0),
        width=1000,
        height=700
    )
    
    fig.add_annotation(
        x=6.6,
        y=-3.2,
        text="Dribble Type:",
        showarrow=False,
        font=dict(size=14, color="black", family="Helvetica", weight='bold')
    )

    fig.add_trace(go.Scatter(
        x=[15],
        y=[-3.2],
        mode="markers",
        marker=dict(size=12, color='white', symbol='circle', line=dict(color='black', width=1)),
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.add_annotation(
        x=16.5,
        y=-3.1,
        text="Normal",
        showarrow=False,
        font=dict(size=13, color="black"),
        xanchor='left'
    )

    fig.add_trace(go.Scatter(
        x=[27],
        y=[-3.2],
        mode="markers",
        marker=dict(size=14, color='white', symbol='star', line=dict(color='black', width=1)),
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.add_annotation(
        x=29,
        y=-3.1,
        text="Nutmeg",
        showarrow=False,
        font=dict(size=13, color="black"),
        xanchor='left'
    )

    return fig

def draw_pitch_plotly():
    fig = go.Figure()

    # Contorno do campo
    fig.add_shape(type="rect", x0=0, y0=0, x1=120, y1=80, line=dict(color="black", width=2))

    # Linha de meio campo
    fig.add_shape(type="line", x0=60, y0=0, x1=60, y1=80, line=dict(color="black", width=2))

    # Círculo central
    center_circle = go.Scatter(
        x=[60 + 9.15 * np.cos(t) for t in np.linspace(0, 2 * np.pi, 200)],
        y=[40 + 9.15 * np.sin(t) for t in np.linspace(0, 2 * np.pi, 200)],
        mode='lines',
        line=dict(color='black', width=2),
        showlegend=False,
        hoverinfo="skip"
    )
    fig.add_trace(center_circle)

    fig.add_trace(go.Scatter(x=[60], y=[40], mode='markers',
                             marker=dict(color='black', size=6),
                             showlegend=False,
                             hoverinfo="skip"))

    # Áreas grandes
    fig.add_shape(type="rect", x0=0, y0=18, x1=18, y1=62, line=dict(color="black", width=2))
    fig.add_shape(type="rect", x0=102, y0=18, x1=120, y1=62, line=dict(color="black", width=2))

    # Arcos das áreas (esquerda)
    arc_left = []
    for angle in np.radians(np.linspace(310, 410, 200)):
        x = 12 + (18.3 / 2) * np.cos(angle)
        y = 40 + (18.3 / 2) * np.sin(angle)
        arc_left.append((x, y))
    fig.add_trace(go.Scatter(x=[pt[0] for pt in arc_left], y=[pt[1] for pt in arc_left],
                             mode="lines", line=dict(color="black", width=2),
                             showlegend=False, hoverinfo="skip"))

    # Arcos das áreas (direita)
    arc_right = []
    for angle in np.radians(np.linspace(130, 230, 200)):
        x = 108 + (18.3 / 2) * np.cos(angle)
        y = 40 + (18.3 / 2) * np.sin(angle)
        arc_right.append((x, y))
    fig.add_trace(go.Scatter(x=[pt[0] for pt in arc_right], y=[pt[1] for pt in arc_right],
                             mode="lines", line=dict(color="black", width=2),
                             showlegend=False, hoverinfo="skip"))

    # Áreas pequenas
    fig.add_shape(type="rect", x0=0, y0=30, x1=6, y1=50, line=dict(color="black", width=2))
    fig.add_shape(type="rect", x0=114, y0=30, x1=120, y1=50, line=dict(color="black", width=2))

    # Marcas de penálti
    fig.add_trace(go.Scatter(x=[12, 108], y=[40, 40], mode='markers',
                             marker=dict(color='black', size=6),
                             showlegend=False,
                             hoverinfo="skip"))

    # Balizas
    fig.add_shape(type="line", x0=0, y0=36, x1=0, y1=44, line=dict(color="black", width=4))
    fig.add_shape(type="line", x0=120, y0=36, x1=120, y1=44, line=dict(color="black", width=4))

    sx, sy = 52, -3  # início
    ex, ey = 68, -3  # fim

    # Linha da seta
    fig.add_trace(go.Scatter(
        x=[sx, ex], y=[sy, ey],
        mode='lines',
        line=dict(color='black', width=2.2),
        hoverinfo='skip',
        showlegend=False
    ))

    # Ponta (triângulo customizado)
    dx = ex - sx
    dy = ey - sy
    norm = np.sqrt(dx**2 + dy**2)
    ux, uy = dx / norm, dy / norm

    arrow_length = 1.5  # controla o comprimento da seta
    head_base = 0.9     # controla a largura

    tip = (ex, ey)
    left = (ex - arrow_length * ux + head_base * uy,
            ey - arrow_length * uy - head_base * ux)
    right = (ex - arrow_length * ux - head_base * uy,
             ey - arrow_length * uy + head_base * ux)

    fig.add_trace(go.Scatter(
        x=[tip[0], left[0], right[0], tip[0]],
        y=[tip[1], left[1], right[1], tip[1]],
        fill='toself',
        fillcolor='black',
        line=dict(color='black'),
        mode='lines',
        hoverinfo='skip',
        showlegend=False
    ))

    fig.add_annotation(
        x=59.5, y=-4,
        text="Attack Direction",
        showarrow=False,
        font=dict(size=12),
        xanchor='center',
        yanchor='top'
    )
    
    # Configurações finais
    fig.update_layout(
        xaxis=dict(range=[0, 122], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-5, 85], showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
        plot_bgcolor='white',
        margin=dict(l=0, r=0, t=0, b=0),
        width=1000,
        height=700
    )

    return fig

def get_pass_data_plotly(player_name, comp_id, season_id, data_path="./data"):
    matches_path = os.path.join(data_path, 'matches', str(comp_id), f'{season_id}.json')
    with open(matches_path, encoding='utf-8') as f:
        matches = json.load(f)
    match_ids = [m['match_id'] for m in matches]

    passes_sucesso = []
    passes_erro = []
    match_dict = {m['match_id']: f"{m['home_team']['home_team_name']} vs {m['away_team']['away_team_name']}" for m in matches}

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f'{match_id}.json'), encoding='utf-8') as f:
                events = json.load(f)
            df = json_normalize(events, sep='_')
            df_player = df[(df['player_name'] == player_name) & (df['type_name'] == 'Pass')]

            for _, row in df_player.iterrows():
                start = row.get("location")
                end = row.get("pass_end_location")

                if not isinstance(start, list) or not isinstance(end, list):
                    continue

                start_x, start_y = start[0], 80 - start[1]
                end_x, end_y = end[0], 80 - end[1]
                body_part = row.get("pass_body_part_name", 'Unknown')
                match_name = match_dict.get(match_id, f"Match {match_id}")
                height = row.get("pass_height_name", "Unknown")
                length = row.get("pass_length", "N/A")
                if isinstance(length, (int, float)):
                    length = round(length, 2)
                else:
                    length = "N/A"

                hover_text = f"Match: {match_name}<br>Body part: {body_part}<br>Height: {height}<br>Length: {length} meters"

                if pd.isna(row.get("pass_outcome_name")):
                    passes_sucesso.append(((start_x, start_y), (end_x, end_y), hover_text))
                else:
                    passes_erro.append(((start_x, start_y), (end_x, end_y), hover_text))
        except:
            continue

    return passes_sucesso, passes_erro

def _add_pass_arrows(fig, pass_list, color, alpha=0.7):
    rgba = f"rgba{(*colors.to_rgba(color)[:3], alpha)}"
    
    for (sx, sy), (ex, ey), hover in pass_list:
        fig.add_trace(go.Scatter(
            x=[sx, ex], y=[sy, ey],
            mode='lines',
            line=dict(color=rgba, width=1.5),
            text=[hover, hover],
            hoverinfo='text',
            showlegend=False
        ))

        dx = ex - sx
        dy = ey - sy
        norm = np.sqrt(dx**2 + dy**2)
        if norm == 0:
            continue
        ux, uy = dx / norm, dy / norm
        arrow_length = 0.75
        head_base = 0.42
        tip = (ex, ey)
        left = (ex - arrow_length * ux + head_base * uy, ey - arrow_length * uy - head_base * ux)
        right = (ex - arrow_length * ux - head_base * uy, ey - arrow_length * uy + head_base * ux)

        fig.add_trace(go.Scatter(
            x=[tip[0], left[0], right[0], tip[0]],
            y=[tip[1], left[1], right[1], tip[1]],
            fill='toself',
            fillcolor=rgba,
            line=dict(color=rgba),
            mode='lines',
            hoverinfo='skip',
            showlegend=False
        ))

def plot_key_passes(player_name, comp_id, season_id, data_path):
    from pandas import json_normalize
    import matplotlib.colors as mcolors

    passes_chave = []
    matches_path = os.path.join(data_path, 'matches', str(comp_id), f'{season_id}.json')
    with open(matches_path, encoding='utf-8') as f:
        matches = json.load(f)
    match_ids = [m['match_id'] for m in matches]

    match_dict = {m['match_id']: f"{m['home_team']['home_team_name']} vs {m['away_team']['away_team_name']}" for m in matches}

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f'{match_id}.json'), encoding='utf-8') as f:
                events = json.load(f)
            df = json_normalize(events, sep='_')
            df_player = df[(df['player_name'] == player_name) & (df['type_name'] == 'Pass')]

            for _, row in df_player.iterrows():
                if row.get("pass_shot_assist") is not True:
                    continue
                start = row.get("location")
                end = row.get("pass_end_location")
                if not isinstance(start, list) or not isinstance(end, list):
                    continue
                start_x, start_y = start[0], 80 - start[1]
                end_x, end_y = end[0], 80 - end[1]
                hover = (
                    f"Match: {match_dict.get(match_id)}<br>"
                    f"Recipient: {row.get('pass_recipient_name', 'Unknown')}<br>"
                    f"Body part: {row.get('pass_body_part_name', 'Unknown')}<br>"
                    f"Height: {row.get('pass_height_name', 'Unknown')}<br>"
                    f"Length: {round(row.get('pass_length', 'N/A'), 2)} meters"
                )
                passes_chave.append(((start_x, start_y), (end_x, end_y), hover))
        except:
            continue

    fig = draw_pitch_plotly()
    _add_pass_arrows(fig, passes_chave, '#1F77B4')
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(range=[-7, 85], showgrid=False, zeroline=False, visible=False),
        xaxis=dict(showgrid=False, zeroline=False, visible=False)
    )
    return fig

def plot_goal_assists(player_name, comp_id, season_id, data_path):
    from pandas import json_normalize
    import matplotlib.colors as mcolors

    assistencias = []
    matches_path = os.path.join(data_path, 'matches', str(comp_id), f'{season_id}.json')
    with open(matches_path, encoding='utf-8') as f:
        matches = json.load(f)
    match_ids = [m['match_id'] for m in matches]

    match_dict = {m['match_id']: f"{m['home_team']['home_team_name']} vs {m['away_team']['away_team_name']}" for m in matches}

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f'{match_id}.json'), encoding='utf-8') as f:
                events = json.load(f)
            df = json_normalize(events, sep='_')
            df_player = df[(df['player_name'] == player_name) & (df['type_name'] == 'Pass')]

            for _, row in df_player.iterrows():
                if row.get("pass_goal_assist") is not True:
                    continue
                start = row.get("location")
                end = row.get("pass_end_location")
                if not isinstance(start, list) or not isinstance(end, list):
                    continue
                start_x, start_y = start[0], 80 - start[1]
                end_x, end_y = end[0], 80 - end[1]
                hover = (
                    f"Match: {match_dict.get(match_id)}<br>"
                    f"Recipient: {row.get('pass_recipient_name', 'Unknown')}<br>"
                    f"Body part: {row.get('pass_body_part_name', 'Unknown')}<br>"
                    f"Height: {row.get('pass_height_name', 'Unknown')}<br>"
                    f"Length: {round(row.get('pass_length', 'N/A'), 2)} meters"
                )
                assistencias.append(((start_x, start_y), (end_x, end_y), hover))
        except:
            continue

    fig = draw_pitch_plotly()
    _add_pass_arrows(fig, assistencias, '#1F77B4')  
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(range=[-7, 85], showgrid=False, zeroline=False, visible=False),
        xaxis=dict(showgrid=False, zeroline=False, visible=False)
    )
    return fig

def plot_passes_combined(passes_sucesso, passes_erro):
    fig = draw_pitch_plotly()
    _add_pass_arrows(fig, passes_sucesso, '#1F77B4', alpha=0.55)
    _add_pass_arrows(fig, passes_erro, '#D62728', alpha=0.55)

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(range=[-7, 85], showgrid=False, zeroline=False, visible=False),
        xaxis=dict(showgrid=False, zeroline=False, visible=False)
    )
    return fig

def plot_passes_success_only(passes_sucesso):
    fig = draw_pitch_plotly()
    _add_pass_arrows(fig, passes_sucesso, '#1F77B4', alpha=0.55)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(range=[-7, 85], showgrid=False, zeroline=False, visible=False),
        xaxis=dict(showgrid=False, zeroline=False, visible=False)
    )
    return fig

def plot_passes_error_only(passes_erro):
    fig = draw_pitch_plotly()
    _add_pass_arrows(fig, passes_erro, '#D62728', alpha=0.55)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(range=[-7, 85], showgrid=False, zeroline=False, visible=False),
        xaxis=dict(showgrid=False, zeroline=False, visible=False)
    )
    return fig

def draw_vertical_half_pitch():
    fig = go.Figure()

    fig.add_shape(type="rect", x0=0, y0=0, x1=80, y1=60, line=dict(color="black", width=2))
    fig.add_shape(type="rect", x0=18, y0=42, x1=62, y1=60, line=dict(color="black", width=2))
    fig.add_shape(type="rect", x0=30, y0=54, x1=50, y1=60, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=36, y0=60, x1=44, y1=60, line=dict(color="black", width=4))
    
    fig.add_trace(go.Scatter(x=[40], y=[0], mode="markers", marker=dict(size=6, color="black"), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[40], y=[48], mode="markers", marker=dict(size=6, color="black"), showlegend=False, hoverinfo="skip"))

    # Penalty arc (rotated ellipse)
    arc_angles = np.linspace(310, 360, 300, endpoint=False).tolist() + np.linspace(0, 50, 300).tolist()
    arc_x, arc_y = [], []
    for angle in arc_angles:
        theta = np.radians(angle)
        x = (18.3 / 2) * np.cos(theta)
        y = (18.3 / 2) * np.sin(theta)
        x_rot = x * np.cos(np.radians(270)) - y * np.sin(np.radians(270))
        y_rot = x * np.sin(np.radians(270)) + y * np.cos(np.radians(270))
        arc_x.append(40 + x_rot)
        arc_y.append(48 + y_rot)

    fig.add_trace(go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color="black", width=2), showlegend=False, hoverinfo="skip"))

    # Half circle
    theta_vals = np.linspace(0, np.pi, 200)
    mid_arc_x = 40 + 9.15 * np.cos(theta_vals)
    mid_arc_y = 0 + 9.15 * np.sin(theta_vals)
    fig.add_trace(go.Scatter(x=mid_arc_x, y=mid_arc_y, mode='lines', line=dict(color='black', width=2), showlegend=False, hoverinfo="skip"))

    fig.update_layout(
        xaxis=dict(range=[0, 80], visible=False),
        yaxis=dict(range=[-3, 62], visible=False, scaleanchor="x", scaleratio=1),
        margin=dict(l=0, r=0, t=0, b=22),  # Reduz top, mantém bottom
        plot_bgcolor="white",
        width=700,
        height=640
    )
    return fig

def plot_xg_bubble_shots(match_ids, player_name, data_path):
    fig = draw_vertical_half_pitch()
    total_goals = 0
    total_xg = 0
    total_shots = 0
    all_shots = []

    match_dict = {}
    with open(os.path.join(data_path, 'matches', '9', '281.json'), encoding='utf-8') as f:
        matches = json.load(f)
        for m in matches:
            match_dict[m['match_id']] = f"{m['home_team']['home_team_name']} vs {m['away_team']['away_team_name']}"

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f'{match_id}.json'), encoding='utf-8') as f:
                events = json.load(f)
            df = json_normalize(events, sep='_')
            shots = df[(df['player_name'] == player_name) & (df['type_name'] == 'Shot')]

            for _, row in shots.iterrows():
                loc = row.get('location')
                if not isinstance(loc, list) or len(loc) < 2:
                    continue
                x, y = loc[0], loc[1]
                if x < 60:
                    continue

                xg = float(row.get('shot_statsbomb_xg', 0))
                is_goal = row.get('shot_outcome_name') == 'Goal'
                body_part = row.get('shot_body_part_name', 'Unknown')
                shot_type = row.get('shot_type_name', 'Unknown')
                match_name = match_dict.get(match_id, f"Match {match_id}")

                color = 'red' if is_goal else 'orange'

                all_shots.append({
                    'x': 80 - y,
                    'y': x - 60,
                    'xg': xg,
                    'color': color,
                    'hover': f"xG: {xg:.2f}<br>{'Goal' if is_goal else 'Shot'}<br>Match: {match_name}<br>Body part: {body_part}<br>Type: {shot_type}"
                })

                total_shots += 1
                total_xg += xg
                if is_goal:
                    total_goals += 1

        except:
            continue

    def xg_to_radius(xg, max_radius=40, min_radius=10):
        return min_radius + (max_radius - min_radius) * (xg ** 0.9)

    for shot in all_shots:
        fig.add_trace(go.Scatter(
            x=[shot['x']],
            y=[shot['y']],
            mode='markers',
            marker=dict(
                size=xg_to_radius(shot['xg']),
                color=shot['color'],
                line=dict(color='black', width=1.2),
                opacity=0.8
            ),
            hoverinfo='text',
            hovertext=shot['hover'],
            showlegend=False
        ))

    # 4. Estatísticas anotadas
    xg_per_shot = total_xg / total_shots if total_shots else 0
    base_y = 5.5
    spacing = 3.8
    stats_annotations = [
        dict(x=4, y=base_y + spacing * 4, text=f"<b>Summary</b>", showarrow=False, font=dict(size=16, color="black", family="Helvetica"), xanchor='left'),
        dict(x=4, y=base_y + spacing * 3, text=f"Goals: <b>{total_goals}</b>", showarrow=False, font=dict(size=16, color="black", family="Helvetica"), xanchor='left'),
        dict(x=4, y=base_y + spacing * 2, text=f"Total xG: <b>{total_xg:.2f}</b>", showarrow=False, font=dict(size=16, color="black", family="Helvetica"), xanchor='left'),
        dict(x=4, y=base_y + spacing, text=f"Shots: <b>{total_shots}</b>", showarrow=False, font=dict(size=16, color="black", family="Helvetica"), xanchor='left'),
        dict(x=4, y=base_y, text=f"TotalxG/Shot: <b>{xg_per_shot:.2f}</b>", showarrow=False, font=dict(size=16, color="black", family="Helvetica"), xanchor='left'),
    ]

    # 5. Legenda e bolinhas de xG
    fig.add_trace(go.Scatter(
        x=[11],
        y=[-3],
        mode="markers",
        marker=dict(size=18, color='orange', line=dict(color='black', width=1.5)),
        showlegend=False,
        hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=[18],
        y=[-3],
        mode="markers",
        marker=dict(size=18, color='red', line=dict(color='black', width=1.5)),
        showlegend=False,
        hoverinfo="skip"
    ))

    # 2. Adiciona as anotações restantes com texto
    legend_annotations = [
        dict(x=9, y=-3, text="Outcome:", showarrow=False,
             font=dict(size=14, color="black", family="Helvetica", weight='bold'), xanchor='right'),

        dict(x=14, y=-3, text="Shot", showarrow=False,
             font=dict(size=14, color="black", family="Helvetica")),

        dict(x=21.1, y=-3, text="Goal", showarrow=False,
             font=dict(size=14, color="black", family="Helvetica")),

        dict(x=52, y=-3, text="xG Value:", showarrow=False,
             font=dict(size=14, color="black", family="Helvetica", weight='bold'), xanchor='right')
    ]


    xg_examples = [0.1, 0.4, 0.7, 1.0]
    x_positions = [53.5, 60, 67, 74.9]
    text_positions = [56, 63, 70.5, 78.9]
    for xg, x_pos, text_pos in zip(xg_examples, x_positions, text_positions):
        fig.add_trace(go.Scatter(
            x=[x_pos],
            y=[-3],
            mode='markers',
            marker=dict(
                size=xg_to_radius(xg),
                color='white',
                line=dict(color='black', width=1.2),
                opacity=0.8
            ),
            showlegend=False,
            hoverinfo="skip"
        ))
        legend_annotations.append(
            dict(x=text_pos, y=-3, text=f"{xg}", showarrow=False, font=dict(size=14, color="black", family="Helvetica"))
        )

    # 6. Atualizar layout
    fig.update_layout(annotations=stats_annotations + legend_annotations)

    return fig

def plot_pizza_passes(passes_sucesso, passes_erro):
    success_count = len(passes_sucesso)
    error_count = len(passes_erro)

    df_pie = pd.DataFrame({
        'Result': ['Successful', 'Unsuccessful'],
        'Count': [success_count, error_count]
    })

    fig_pie = px.pie(
        df_pie,
        names='Result',
        values='Count',
        color='Result',
        hole=0.35,
        color_discrete_map={
            'Successful': '#1F77B4',
            'Unsuccessful': '#D62728'
        }
    )

    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent',
        textfont_size=10,
        hovertemplate='%{label}<br>%{value} passes<br>%{percent}'
    )

    fig_pie.update_layout(
        title='Pass Success Rate',
        title_font_size=13,
        showlegend=False,
        template='plotly_white',
        margin=dict(t=30, b=10, l=10, r=10),
        height=180,
        font=dict(size=12)
    )

    return fig_pie

def apresentar_jogador(player_name="Florian Wirtz", image_path="assets/Wirtz.jpg", data_path="./data"):
    img = Image.open(image_path)
    data = data_path
    
    # Dados para visualização
    nome_jogador = player_name
    dados_esquerda = {
        "21 years": "Age",
        "Germany": "Nationality",
        "Bayer Leverkusen": "Team",
        "Left Attacking Midfield": "Position"
    }
    dados_direita = {
        "32": "Matches",
        "2383": "Minutes Played",
        "11": "Goals",
        "10": "Assists"
    }
    # Criar figura
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0.505], y=[0.94],
        text=f"<b><span style='font-size:32px;'>{nome_jogador}</span></b>",
        mode="text",
        textfont=dict(size=32, color="black", family="Helvetica"),
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.add_layout_image(
        dict(
            source=img,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.47,
            sizex=0.75,
            sizey=0.7,
            xanchor="center",
            yanchor="middle",
            sizing="contain",
            opacity=1,
            layer="below"
        )
    )

    y_positions = np.linspace(0.73, 0.2, len(dados_esquerda))

    for (valor, chave), y in zip(dados_esquerda.items(), y_positions):
        fig.add_trace(go.Scatter(
            x=[0.13], y=[y],
            text=f"<b><span style='font-size:18px;'>{valor}</span></b><br><span style='font-size:17px;'>{chave}</span>",
            mode="text",
            textfont=dict(size=18, color="black", family="Helvetica"),
            showlegend=False,
            hoverinfo="skip"
        ))

    for (valor, chave), y in zip(dados_direita.items(), y_positions):
        fig.add_trace(go.Scatter(
            x=[0.88], y=[y],
            text=f"<b><span style='font-size:18px;'>{valor}</span></b><br><span style='font-size:17px;'>{chave}</span>",
            mode="text",
            textfont=dict(size=18, color="black", family="Helvetica"),
            showlegend=False,
            hoverinfo="skip"
        ))

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[0, 1]),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=0, r=0, t=0, b=0),
        width=900,
        height=500
    )
    
    return fig

def plot_direcao_passes(player_name, comp_id, season_id, data_path="./data"):
    passes = []
    matches_path = os.path.join(data_path, 'matches', str(comp_id), f'{season_id}.json')
    with open(matches_path, encoding='utf-8') as f:
        matches = json.load(f)
    match_ids = [m['match_id'] for m in matches]

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f'{match_id}.json'), encoding='utf-8') as f:
                events = json.load(f)
            df = json_normalize(events, sep='_')
            df_passes = df[(df['player_name'] == player_name) & (df['type_name'] == 'Pass')][['pass_angle', 'pass_outcome_name']].dropna(subset=['pass_angle'])
            passes.append(df_passes)
        except:
            continue

    df_passes = pd.concat(passes, ignore_index=True)

    def classify_pass_direction(angle):
        if -2*np.pi/3 <= angle <= -np.pi/3 or np.pi/3 <= angle <= 2*np.pi/3:
            return 'Lateral'
        elif -np.pi/3 < angle < np.pi/3:
            return 'Forward'
        else:
            return 'Backward'

    df_passes['Direction'] = df_passes['pass_angle'].apply(classify_pass_direction)
    df_passes['Result'] = df_passes['pass_outcome_name'].apply(lambda x: 'Successful' if pd.isna(x) else 'Unsuccessful')

    counts_dir = df_passes.groupby(['Direction', 'Result']).size().reset_index(name='count')
    pivot_dir = counts_dir.pivot(index='Direction', columns='Result', values='count').fillna(0)

    colors = {'Successful': '#1F77B4', 'Unsuccessful': '#D62728'}

    fig_dir = go.Figure()
    fig_dir.update_layout(
        showlegend=False  # <-- Isto tem que vir ANTES de adicionar os traços
    )
    for result in ['Unsuccessful', 'Successful']:
        fig_dir.add_trace(go.Bar(
            x=pivot_dir.index,
            y=pivot_dir[result],
            marker_color=colors[result],
            customdata=[[f"{(v / pivot_dir.loc[cat].sum()) * 100:.1f}%", result]
                        for cat, v in zip(pivot_dir.index, pivot_dir[result])],
            hovertemplate='%{customdata[1]}<br>%{y} passes<br>%{x}<br>%{customdata[0]}',
            width=0.5,
            showlegend=False  # desativa legenda se não precisa
        ))
    fig_dir.update_traces(name='', selector=dict(type='bar'))
    fig_dir.update_layout(
        title='Pass Direction',
        title_font_size=13,
        xaxis_title='',
        yaxis_title='',
        legend_title='',
        barmode='stack',
        bargap=0.05,  # Minimiza espaço entre barras
        xaxis_title_standoff=10,
        template='plotly_white',
        margin=dict(t=30, b=30, l=20, r=10),
        height=200,
        font=dict(size=12),
        showlegend=False,
    )

    return fig_dir

def create_goal_post_plotly():
    fig = go.Figure()

    # Estrutura principal
    fig.add_shape(type='line', x0=32, y0=0, x1=48, y1=0, line=dict(color='lightgray', width=2))
    fig.add_shape(type='line', x0=36, y0=0, x1=36, y1=2.67, line=dict(color='black'))
    fig.add_shape(type='line', x0=44, y0=0, x1=44, y1=2.67, line=dict(color='black'))
    fig.add_shape(type='line', x0=36, y0=2.67, x1=44, y1=2.67, line=dict(color='black'))

    # Parte traseira
    fig.add_shape(type='line', x0=35.9, y0=0, x1=35.9, y1=2.75, line=dict(color='black'))
    fig.add_shape(type='line', x0=44.1, y0=0, x1=44.1, y1=2.75, line=dict(color='black'))
    fig.add_shape(type='line', x0=35.9, y0=2.75, x1=44.1, y1=2.75, line=dict(color='black'))

    # Linhas de profundidade
    fig.add_shape(type='line', x0=36, y0=2.67, x1=36.3, y1=2.58, line=dict(color='gray'))
    fig.add_shape(type='line', x0=36.3, y0=2.58, x1=36.7, y1=0.8, line=dict(color='gray'))
    fig.add_shape(type='line', x0=36.7, y0=0.8, x1=36, y1=0, line=dict(color='gray'))

    fig.add_shape(type='line', x0=44, y0=2.67, x1=43.7, y1=2.58, line=dict(color='gray'))
    fig.add_shape(type='line', x0=43.7, y0=2.58, x1=43.3, y1=0.8, line=dict(color='gray'))
    fig.add_shape(type='line', x0=43.3, y0=0.8, x1=44, y1=0, line=dict(color='gray'))
    fig.add_shape(type='line', x0=36.7, y0=0.8, x1=43.3, y1=0.8, line=dict(color='gray'))

    fig.add_shape(type='line', x0=26, y0=0, x1=54, y1=0, line=dict(color='lightgray', width=2))

    fig.update_layout(
        width=900,
        height=500,
        xaxis=dict(range=[34.8, 45.3], visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[0, 3], visible=False),
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=0)
    )
    return fig

def get_match_id_name_dict(matches_path):
    with open(matches_path, encoding='utf-8') as f:
        matches = json.load(f)

    match_dict = {}
    for m in matches:
        match_id = m['match_id']
        home = m['home_team']['home_team_name']
        away = m['away_team']['away_team_name']
        match_dict[match_id] = f"{home} vs {away}"
    return match_dict

def plot_shots_plotly_with_hover(match_ids, player_name, data_path, match_dict):
    fig = create_goal_post_plotly()

    shot_styles = {
        'Goal': {'color': '#2CA02C', 'symbol': 'x'},
        'Off T': {'color': '#9467BD', 'symbol': 'x'},
        'Post': {'color': '#FF7F0E', 'symbol': 'x'},
        'Saved': {'color': '#D62728', 'symbol': 'x'},
        'Saved to Post': {'color': '#1F77B4', 'symbol': 'x'},
    }

    display_names = {
        'Goal': 'Goal',
        'Off T': 'Off Target',
        'Post': 'Post',
        'Saved': 'Saved',
        'Saved to Post': 'Saved to Post'
    }

    for outcome, style in shot_styles.items():
        xs, ys, labels = [], [], []
        for match_id in match_ids:
            try:
                with open(os.path.join(data_path, 'events', f'{match_id}.json'), encoding='utf-8') as f:
                    events = json.load(f)
                df = json_normalize(events, sep='_')
                shots = df[(df['player_name'] == player_name) &
                           (df['type_name'] == 'Shot') &
                           (df['shot_outcome_name'] == outcome)]

                for _, row in shots.iterrows():
                    loc = row.get('shot_end_location')
                    body_part = row.get('shot_body_part_name', 'Unknown')
                    if not isinstance(loc, list) or len(loc) < 3:
                        continue
                    x = loc[1]
                    y = loc[2]
                    match_name = match_dict.get(match_id, f"Match ID {match_id}")
                    xs.append(x)
                    ys.append(y)
                    labels.append(
                        f"<b>{display_names[outcome]}</b><br>{match_name}<br>Body part: {body_part}<br>Height: {y:.2f} meters"
                    )
            except Exception as e:
                print(f"Erro no jogo {match_id}: {e}")
                continue

        fig.add_trace(go.Scatter(
            x=xs,
            y=ys,
            mode='markers',
            marker=dict(color=style['color'], size=8, symbol=style['symbol']),
            name=display_names[outcome],
            hovertext=labels,
            hoverinfo="text"
        ))

    fig.update_layout(
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.99,
            font=dict(size=10)
        ),
        xaxis=dict(fixedrange=False),
        yaxis=dict(range=[1, 2.45], fixedrange=False),  # Zoom ON
        dragmode="zoom",
        margin=dict(t=30, b=0, l=10, r=10),  # b=5 -> mínimo espaço em baixo
        height=400
    )

    return fig

def plot_pass_length(player_name, comp_id, season_id, data_path="./data"):
    matches_path = os.path.join(data_path, 'matches', str(comp_id), f'{season_id}.json')
    with open(matches_path, encoding='utf-8') as f:
        matches = json.load(f)
    match_ids = [m['match_id'] for m in matches]

    passes_len = []
    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f'{match_id}.json'), encoding='utf-8') as f:
                events = json.load(f)
            df = json_normalize(events, sep='_')
            df_passes = df[
                (df['player_name'] == player_name) & 
                (df['type_name'] == 'Pass')
            ][['pass_length', 'pass_outcome_name']].dropna(subset=['pass_length'])
            passes_len.append(df_passes)
        except:
            continue

    df_passes_len = pd.concat(passes_len, ignore_index=True)

    def classify_pass_length(length):
        if length <= 10:
            return '0–10m'
        elif length <= 25:
            return '10–25m'
        else:
            return '>25m'

    df_passes_len['Length Category'] = df_passes_len['pass_length'].apply(classify_pass_length)
    df_passes_len['Result'] = df_passes_len['pass_outcome_name'].apply(lambda x: 'Successful' if pd.isna(x) else 'Unsuccessful')

    counts_len = df_passes_len.groupby(['Length Category', 'Result']).size().reset_index(name='count')
    pivot_len = counts_len.pivot(index='Length Category', columns='Result', values='count').fillna(0)
    pivot_len = pivot_len.reindex(['0–10m', '10–25m', '>25m'])

    colors = {'Successful': '#1F77B4', 'Unsuccessful': '#D62728'}

    fig_len = go.Figure()
    fig_len.update_layout(
        showlegend=False  # <-- Isto tem que vir ANTES de adicionar os traços
    )
    for result in ['Unsuccessful', 'Successful']:
        fig_len.add_trace(go.Bar(
            x=pivot_len.index,
            y=pivot_len[result],
            marker_color=colors[result],
            customdata=[[f"{(v / pivot_len.loc[cat].sum()) * 100:.1f}%", result]
                        for cat, v in zip(pivot_len.index, pivot_len[result])],
            hovertemplate='%{customdata[1]}<br>%{y} passes<br>%{x}<br>%{customdata[0]}',
            width=0.5,
            showlegend=False  # desativa legenda se não precisa
        ))
    fig_len.update_traces(name='', selector=dict(type='bar'))
    fig_len.update_layout(
        title='Pass Length',
        title_font_size=13,
        xaxis_title='',
        yaxis_title='',
        legend_title='',
        barmode='stack',
        bargap=0.05,  # Minimiza espaço entre barras
        template='plotly_white',
        margin=dict(t=30, b=30, l=20, r=10),
        height=280,  # Um pouco maior, para compensar as categorias inclinadas
        font=dict(size=12)
    )

    return fig_len

def get_pass_network_data(match_ids, data_path):
    pass_counts = {name: 0 for name in PLAYER_NAMES}
    pair_passes = {}

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f'{match_id}.json'), encoding='utf-8') as f:
                events = json.load(f)
            df = json_normalize(events, sep='_')
            passes = df[df['type_name'] == 'Pass']
            for _, row in passes.iterrows():
                passer = row.get('player_name')
                recipient = row.get('pass_recipient_name')
                if passer in PLAYER_NAMES and recipient in PLAYER_NAMES:
                    pair = tuple(sorted([passer, recipient]))
                    pair_passes[pair] = pair_passes.get(pair, 0) + 1
                    pass_counts[passer] += 1
        except:
            continue

    G = nx.Graph()
    for player in CUSTOM_POSITIONS:
        G.add_node(player)

    for (p1, p2), count in pair_passes.items():
        G.add_edge(p1, p2, weight=count)

    scaler = MinMaxScaler()
    vals = np.array([pass_counts[n] for n in G.nodes]).reshape(-1, 1)
    vals_scaled = scaler.fit_transform(vals).flatten()

    node_sizes = [100 + (6000 - 100) * val for val in vals_scaled]
    edge_widths = [G[u][v]['weight'] * 0.035 for u, v in G.edges]

    norm = colors.Normalize(vmin=min(pass_counts.values()), vmax=max(pass_counts.values()))
    cmap = cm.Reds
    node_colors = [f"rgba{tuple(int(c*255) for c in cmap(norm(pass_counts[n]))[:3]) + (1.0,)}" for n in G.nodes]

    return G, node_sizes, edge_widths, node_colors, pass_counts, pair_passes

def plot_pass_network(G, node_sizes, edge_widths, node_colors, pass_counts, pair_passes):
    fig = draw_pitch_plotly()
    positions = CUSTOM_POSITIONS

    # Linhas (arestas)
    for i, (u, v) in enumerate(G.edges):
        x0, y0 = positions[u]
        x1, y1 = positions[v]
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode='lines', line=dict(width=edge_widths[i], color='gray'),
            opacity=0.4, hoverinfo='skip', showlegend=False
        ))

        # Hover invisível
        fig.add_trace(go.Scatter(
            x=[(x0 + x1) / 2], y=[(y0 + y1) / 2],
            mode='markers', marker=dict(size=10, color='rgba(0,0,0,0)'),
            hoverinfo='text',
            hovertext=f"<b>{u}</b> ↔ <b>{v}</b><br>{G[u][v]['weight']} passes",
            showlegend=False
        ))

    # Nós (jogadores)
    for i, node in enumerate(G.nodes):
        x, y = positions[node]
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode='markers+text',
            marker=dict(size=node_sizes[i]**0.5, color=node_colors[i], line=dict(color='black', width=1)),
            text=[node], textposition='top center',
            textfont=dict(size=12, color='black'),
            hoverinfo='text',
            hovertext=f"<b>{node}</b><br>{pass_counts[node]} total passes",
            showlegend=False
        ))

    # Legenda
    _add_pass_network_legend(fig)

    fig.update_layout(
        height=800,
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(range=[-17, 85], showgrid=False, zeroline=False, visible=False)
    )

    return fig

def _add_pass_network_legend(fig):
    cmap = cm.Reds
    legend_y = -6
    x_start = 2
    x_gap = 6

    legend_sizes = [75, 150, 225, 300, 375, 450, 525]
    legend_vals = np.linspace(0, 1, len(legend_sizes))

    for i, (size, norm_val) in enumerate(zip(legend_sizes, legend_vals)):
        rgba = cmap(norm_val)
        color = f"rgba({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)}, 1)"
        fig.add_trace(go.Scatter(
            x=[x_start + i * x_gap], y=[legend_y],
            mode='markers',
            marker=dict(size=np.sqrt(size), color=color, line=dict(color='black', width=1)),
            hoverinfo="skip", showlegend=False
        ))

    # Linhas
    y_lines = legend_y - 7.6
    line_widths = [1, 1.5, 3, 4.5, 5, 6.5, 8]
    for i, w in enumerate(line_widths):
        fig.add_shape(
            type="line",
            x0=x_start + i * x_gap - 2, y0=y_lines,
            x1=x_start + i * x_gap + 2, y1=y_lines,
            line=dict(width=w, color='gray')
        )

    # 3. Textos explicativos
    fig.add_annotation(
        x=x_start + 49.5, y=legend_y - 3,
        text="Player made more Passes",
        showarrow=False, font=dict(size=12, color="black", family="Helvetica"), xanchor='center'
    )
    fig.add_annotation(
        x=x_start + 51, y=y_lines - 2,
        text="More Passes Between Players",
        showarrow=False, font=dict(size=12, color="black", family="Helvetica"), xanchor='center'
    )

    # 4. Setas horizontais
    fig.add_annotation(
        x=x_start + (len(legend_sizes) - 1) * x_gap + 2, y=legend_y - 3,
        ax=x_start - 2, ay=legend_y - 3,
        xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowsize=1.3, arrowwidth=1, arrowcolor='black'
    )
    fig.add_annotation(
        x=x_start + (len(line_widths) - 1) * x_gap + 2, y=y_lines - 2,
        ax=x_start - 2, ay=y_lines - 2,
        xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowsize=1.3, arrowwidth=1, arrowcolor='black'
    )

def shot_resume(match_ids, player_name, data_path):
    outcome_group = {
        "Goal": "Shots on Target",
        "Saved": "Shots on Target",
        "Saved to Post": "Shots on Target",
        "Post": "Shots off Target",
        "Off T": "Shots off Target"
    }

    outcome_labels = {
        "Goal": "Goal",
        "Saved": "Saved",
        "Saved to Post": "Saved to Post",
        "Post": "Post",
        "Off T": "Off Target"
    }

    data = []

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f'{match_id}.json'), encoding='utf-8') as f:
                events = json.load(f)
            df = json_normalize(events, sep='_')
            shots = df[(df['player_name'] == player_name) & (df['type_name'] == 'Shot')]
            for outcome_raw in shots['shot_outcome_name'].dropna():
                if outcome_raw in outcome_group:
                    group = outcome_group[outcome_raw]
                    label = outcome_labels[outcome_raw]
                    data.append((group, label))
        except Exception as e:
            print(f"Erro no jogo {match_id}: {e}")
            continue

    df_sunburst = pd.DataFrame(data, columns=['Group', 'Outcome'])
    df_counts = df_sunburst.value_counts().reset_index(name='Count')

    # sunburst
    fig = px.sunburst(
        df_counts,
        path=['Group', 'Outcome'],
        values='Count',
        color='Group',
        color_discrete_map={
            "Shots on Target": '#1F77B4',
            "Shots off Target": '#D62728'
        },
        hover_data={'Count': True},
    )

    fig.update_traces(textinfo='label+percent entry')
    fig.update_layout(
        margin=dict(t=10, b=10, l=0, r=0)
    )

    return fig

def dribbles_all(player_name, data_path, comp_id, season_id):
    # 1. Carregar partidas
    with open(os.path.join(data_path, 'matches', str(comp_id), f"{season_id}.json"), encoding='utf-8') as f:
        matches = json.load(f)

    match_ids = [m['match_id'] for m in matches]
    match_dict = {
        m['match_id']: f"{m['home_team']['home_team_name']} vs {m['away_team']['away_team_name']}"
        for m in matches
    }

    # 2. Coletar dribles
    complete = []
    incomplete = []
    nutmeg_complete = []
    nutmeg_incomplete = []

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f"{match_id}.json"), encoding='utf-8') as f:
                events = json.load(f)

            for e in events:
                if e.get("player", {}).get("name") != player_name:
                    continue
                if e.get("type", {}).get("name") != "Dribble":
                    continue

                loc = e.get("location")
                if not isinstance(loc, list) or len(loc) < 2:
                    continue

                outcome = e.get("dribble", {}).get("outcome", {}).get("name", "Complete")
                match_name = match_dict.get(match_id, f"Match {match_id}")
                nutmeg = e.get("dribble", {}).get("nutmeg", False)
                overrun = e.get("dribble", {}).get("overrun", False)
                no_touch = e.get("dribble", {}).get("no_touch", False)
                under_pressure = e.get("under_pressure", False)

                hover = (
                    f"Match: {match_name}<br>"
                    f"Outcome: {outcome}<br>"
                    f"Nutmeg: {'Yes' if nutmeg else 'No'}<br>"
                    f"Overrun: {'Yes' if overrun else 'No'}<br>"
                    f"No Touch: {'Yes' if no_touch else 'No'}<br>"
                    f"Under Pressure: {'Yes' if under_pressure else 'No'}"
                )

                point = {'x': loc[0], 'y': loc[1], 'hover': hover}

                if outcome == "Complete":
                    (nutmeg_complete if nutmeg else complete).append(point)
                else:
                    (nutmeg_incomplete if nutmeg else incomplete).append(point)

        except:
            continue

    # 3. Visualização
    fig = draw_pitch_plotly_dribble()

    def add_dribbles(dribble_list, color, symbol='circle', alpha=0.8, size=8):
        rgba = f"rgba{(*colors.to_rgba(color)[:3], alpha)}"
        fig.add_trace(go.Scatter(
            x=[p['x'] for p in dribble_list],
            y=[80 - p['y'] for p in dribble_list],  # inverter Y
            mode='markers',
            marker=dict(color=rgba, size=size, symbol=symbol, line=dict(width=0.4, color='black')),
            text=[p['hover'] for p in dribble_list],
            hoverinfo='text',
            showlegend=False
        ))

    # Adiciona todos os tipos
    add_dribbles(complete, '#1F77B4')  
    add_dribbles(incomplete, '#D62728')  
    add_dribbles(nutmeg_complete, '#1F77B4', symbol='star', size=12) 
    add_dribbles(nutmeg_incomplete, '#D62728', symbol='star', size=12)  

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(range=[-7, 85], showgrid=False, zeroline=False, visible=False),
        xaxis=dict(showgrid=False, zeroline=False, visible=False)
    )

    return fig

def dribbles_sucess(player_name, data_path, comp_id, season_id):
    # 1. Carregar partidas
    with open(os.path.join(data_path, 'matches', str(comp_id), f"{season_id}.json"), encoding='utf-8') as f:
        matches = json.load(f)

    match_ids = [m['match_id'] for m in matches]
    match_dict = {
        m['match_id']: f"{m['home_team']['home_team_name']} vs {m['away_team']['away_team_name']}"
        for m in matches
    }

    # 2. Coletar dribles
    complete = []
    incomplete = []
    nutmeg_complete = []
    nutmeg_incomplete = []

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f"{match_id}.json"), encoding='utf-8') as f:
                events = json.load(f)

            for e in events:
                if e.get("player", {}).get("name") != player_name:
                    continue
                if e.get("type", {}).get("name") != "Dribble":
                    continue

                loc = e.get("location")
                if not isinstance(loc, list) or len(loc) < 2:
                    continue

                outcome = e.get("dribble", {}).get("outcome", {}).get("name", "Complete")
                match_name = match_dict.get(match_id, f"Match {match_id}")
                nutmeg = e.get("dribble", {}).get("nutmeg", False)
                overrun = e.get("dribble", {}).get("overrun", False)
                no_touch = e.get("dribble", {}).get("no_touch", False)
                under_pressure = e.get("under_pressure", False)

                hover = (
                    f"Match: {match_name}<br>"
                    f"Outcome: {outcome}<br>"
                    f"Nutmeg: {'Yes' if nutmeg else 'No'}<br>"
                    f"Overrun: {'Yes' if overrun else 'No'}<br>"
                    f"No Touch: {'Yes' if no_touch else 'No'}<br>"
                    f"Under Pressure: {'Yes' if under_pressure else 'No'}"
                )

                point = {'x': loc[0], 'y': loc[1], 'hover': hover}

                if outcome == "Complete":
                    (nutmeg_complete if nutmeg else complete).append(point)
                else:
                    (nutmeg_incomplete if nutmeg else incomplete).append(point)

        except:
            continue

    # 3. Visualização
    fig = draw_pitch_plotly_dribble()

    def add_dribbles(dribble_list, color, symbol='circle', alpha=0.8, size=8):
        rgba = f"rgba{(*colors.to_rgba(color)[:3], alpha)}"
        fig.add_trace(go.Scatter(
            x=[p['x'] for p in dribble_list],
            y=[80 - p['y'] for p in dribble_list],  # inverter Y
            mode='markers',
            marker=dict(color=rgba, size=size, symbol=symbol, line=dict(width=0.4, color='black')),
            text=[p['hover'] for p in dribble_list],
            hoverinfo='text',
            showlegend=False
        ))

    # Adiciona todos os tipos
    add_dribbles(complete, '#1F77B4')   
    add_dribbles(nutmeg_complete, '#1F77B4', symbol='star', size=12)   

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(range=[-7, 85], showgrid=False, zeroline=False, visible=False),
        xaxis=dict(showgrid=False, zeroline=False, visible=False)
    )

    return fig

def dribbles_failed(player_name, data_path, comp_id, season_id):
    # 1. Carregar partidas
    with open(os.path.join(data_path, 'matches', str(comp_id), f"{season_id}.json"), encoding='utf-8') as f:
        matches = json.load(f)

    match_ids = [m['match_id'] for m in matches]
    match_dict = {
        m['match_id']: f"{m['home_team']['home_team_name']} vs {m['away_team']['away_team_name']}"
        for m in matches
    }

    complete = []
    incomplete = []
    nutmeg_complete = []
    nutmeg_incomplete = []

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f"{match_id}.json"), encoding='utf-8') as f:
                events = json.load(f)

            for e in events:
                if e.get("player", {}).get("name") != player_name:
                    continue
                if e.get("type", {}).get("name") != "Dribble":
                    continue

                loc = e.get("location")
                if not isinstance(loc, list) or len(loc) < 2:
                    continue

                outcome = e.get("dribble", {}).get("outcome", {}).get("name", "Complete")
                match_name = match_dict.get(match_id, f"Match {match_id}")
                nutmeg = e.get("dribble", {}).get("nutmeg", False)
                overrun = e.get("dribble", {}).get("overrun", False)
                no_touch = e.get("dribble", {}).get("no_touch", False)
                under_pressure = e.get("under_pressure", False)

                hover = (
                    f"Match: {match_name}<br>"
                    f"Outcome: {outcome}<br>"
                    f"Nutmeg: {'Yes' if nutmeg else 'No'}<br>"
                    f"Overrun: {'Yes' if overrun else 'No'}<br>"
                    f"No Touch: {'Yes' if no_touch else 'No'}<br>"
                    f"Under Pressure: {'Yes' if under_pressure else 'No'}"
                )

                point = {'x': loc[0], 'y': loc[1], 'hover': hover}

                if outcome == "Complete":
                    (nutmeg_complete if nutmeg else complete).append(point)
                else:
                    (nutmeg_incomplete if nutmeg else incomplete).append(point)

        except:
            continue

    # 3. Visualização
    fig = draw_pitch_plotly_dribble()

    def add_dribbles(dribble_list, color, symbol='circle', alpha=0.8, size=8):
        rgba = f"rgba{(*colors.to_rgba(color)[:3], alpha)}"
        fig.add_trace(go.Scatter(
            x=[p['x'] for p in dribble_list],
            y=[80 - p['y'] for p in dribble_list],  # inverter Y
            mode='markers',
            marker=dict(color=rgba, size=size, symbol=symbol, line=dict(width=0.4, color='black')),
            text=[p['hover'] for p in dribble_list],
            hoverinfo='text',
            showlegend=False
        ))

    # Adiciona todos os tipos
    add_dribbles(incomplete, '#D62728') 
    add_dribbles(nutmeg_incomplete, '#D62728', symbol='star', size=12)  

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(range=[-7, 85], showgrid=False, zeroline=False, visible=False),
        xaxis=dict(showgrid=False, zeroline=False, visible=False)
    )

    return fig

def dribbles_nutmeg_sucess(player_name, data_path, comp_id, season_id):
    # 1. Carregar partidas
    with open(os.path.join(data_path, 'matches', str(comp_id), f"{season_id}.json"), encoding='utf-8') as f:
        matches = json.load(f)

    match_ids = [m['match_id'] for m in matches]
    match_dict = {
        m['match_id']: f"{m['home_team']['home_team_name']} vs {m['away_team']['away_team_name']}"
        for m in matches
    }

    # 2. Coletar dribles
    complete = []
    incomplete = []
    nutmeg_complete = []
    nutmeg_incomplete = []

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f"{match_id}.json"), encoding='utf-8') as f:
                events = json.load(f)

            for e in events:
                if e.get("player", {}).get("name") != player_name:
                    continue
                if e.get("type", {}).get("name") != "Dribble":
                    continue

                loc = e.get("location")
                if not isinstance(loc, list) or len(loc) < 2:
                    continue

                outcome = e.get("dribble", {}).get("outcome", {}).get("name", "Complete")
                match_name = match_dict.get(match_id, f"Match {match_id}")
                nutmeg = e.get("dribble", {}).get("nutmeg", False)
                overrun = e.get("dribble", {}).get("overrun", False)
                no_touch = e.get("dribble", {}).get("no_touch", False)
                under_pressure = e.get("under_pressure", False)

                hover = (
                    f"Match: {match_name}<br>"
                    f"Outcome: {outcome}<br>"
                    f"Nutmeg: {'Yes' if nutmeg else 'No'}<br>"
                    f"Overrun: {'Yes' if overrun else 'No'}<br>"
                    f"No Touch: {'Yes' if no_touch else 'No'}<br>"
                    f"Under Pressure: {'Yes' if under_pressure else 'No'}"
                )

                point = {'x': loc[0], 'y': loc[1], 'hover': hover}

                if outcome == "Complete":
                    (nutmeg_complete if nutmeg else complete).append(point)
                else:
                    (nutmeg_incomplete if nutmeg else incomplete).append(point)

        except:
            continue

    # 3. Visualização
    fig = draw_pitch_plotly_dribble()

    def add_dribbles(dribble_list, color, symbol='circle', alpha=0.8, size=8):
        rgba = f"rgba{(*colors.to_rgba(color)[:3], alpha)}"
        fig.add_trace(go.Scatter(
            x=[p['x'] for p in dribble_list],
            y=[80 - p['y'] for p in dribble_list],  # inverter Y
            mode='markers',
            marker=dict(color=rgba, size=size, symbol=symbol, line=dict(width=0.4, color='black')),
            text=[p['hover'] for p in dribble_list],
            hoverinfo='text',
            showlegend=False
        ))

    add_dribbles(nutmeg_complete, '#1F77B4', symbol='star', size=12)  # azul

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(range=[-7, 85], showgrid=False, zeroline=False, visible=False),
        xaxis=dict(showgrid=False, zeroline=False, visible=False)
    )

    return fig

def dribbles_nutmeg_failed(player_name, data_path, comp_id, season_id):
    # 1. Carregar partidas
    with open(os.path.join(data_path, 'matches', str(comp_id), f"{season_id}.json"), encoding='utf-8') as f:
        matches = json.load(f)

    match_ids = [m['match_id'] for m in matches]
    match_dict = {
        m['match_id']: f"{m['home_team']['home_team_name']} vs {m['away_team']['away_team_name']}"
        for m in matches
    }

    # 2. Coletar dribles
    complete = []
    incomplete = []
    nutmeg_complete = []
    nutmeg_incomplete = []

    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f"{match_id}.json"), encoding='utf-8') as f:
                events = json.load(f)

            for e in events:
                if e.get("player", {}).get("name") != player_name:
                    continue
                if e.get("type", {}).get("name") != "Dribble":
                    continue

                loc = e.get("location")
                if not isinstance(loc, list) or len(loc) < 2:
                    continue

                outcome = e.get("dribble", {}).get("outcome", {}).get("name", "Complete")
                match_name = match_dict.get(match_id, f"Match {match_id}")
                nutmeg = e.get("dribble", {}).get("nutmeg", False)
                overrun = e.get("dribble", {}).get("overrun", False)
                no_touch = e.get("dribble", {}).get("no_touch", False)
                under_pressure = e.get("under_pressure", False)

                hover = (
                    f"Match: {match_name}<br>"
                    f"Outcome: {outcome}<br>"
                    f"Nutmeg: {'Yes' if nutmeg else 'No'}<br>"
                    f"Overrun: {'Yes' if overrun else 'No'}<br>"
                    f"No Touch: {'Yes' if no_touch else 'No'}<br>"
                    f"Under Pressure: {'Yes' if under_pressure else 'No'}"
                )

                point = {'x': loc[0], 'y': loc[1], 'hover': hover}

                if outcome == "Complete":
                    (nutmeg_complete if nutmeg else complete).append(point)
                else:
                    (nutmeg_incomplete if nutmeg else incomplete).append(point)

        except:
            continue

    # 3. Visualização
    fig = draw_pitch_plotly_dribble()

    def add_dribbles(dribble_list, color, symbol='circle', alpha=0.8, size=8):
        rgba = f"rgba{(*colors.to_rgba(color)[:3], alpha)}"
        fig.add_trace(go.Scatter(
            x=[p['x'] for p in dribble_list],
            y=[80 - p['y'] for p in dribble_list],  # inverter Y
            mode='markers',
            marker=dict(color=rgba, size=size, symbol=symbol, line=dict(width=0.4, color='black')),
            text=[p['hover'] for p in dribble_list],
            hoverinfo='text',
            showlegend=False
        ))

    add_dribbles(nutmeg_incomplete, '#D62728', symbol='star', size=12)  # laranja

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(range=[-7, 85], showgrid=False, zeroline=False, visible=False),
        xaxis=dict(showgrid=False, zeroline=False, visible=False)
    )

    return fig

def plot_dribble_success_donut(player_name, comp_id, season_id, data_path):
    # Contadores
    successful = 0
    failed = 0

    # 1. Carregar partidas
    with open(os.path.join(data_path, 'matches', str(comp_id), f"{season_id}.json"), encoding='utf-8') as f:
        matches = json.load(f)

    match_ids = [m['match_id'] for m in matches]

    # 2. Verificar todos os eventos de drible
    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f"{match_id}.json"), encoding='utf-8') as f:
                events = json.load(f)

            for e in events:
                if e.get("player", {}).get("name") != player_name:
                    continue
                if e.get("type", {}).get("name") != "Dribble":
                    continue

                outcome = e.get("dribble", {}).get("outcome", {}).get("name", "Complete")
                if outcome == "Complete":
                    successful += 1
                else:
                    failed += 1

        except:
            continue

    # Dados para o gráfico
    labels = ['Successful', 'Failed']
    values = [successful, failed]


    # Criar gráfico donut
    fig = px.pie(
        names=labels,
        values=values,
        color=labels,
        color_discrete_map={'Successful': '#1F77B4', 'Failed': '#D62728'},
        hole=0.35
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        textfont_size=11,
        hovertemplate='%{label}<br>%{value} dribbles<br>%{percent}'
    )

    fig.update_layout(
        title='Dribble Success Rate',  
        title_font_size=13,
        showlegend=False,
        template='plotly_white',
        margin=dict(t=30, b=10, l=10, r=10),
        height=180,
        font=dict(size=12)
    )
    return fig

def plot_nutmeg_success_donut(player_name, comp_id, season_id, data_path):
    # Contadores
    nutmeg_successful = 0
    nutmeg_failed = 0

    # 1. Carregar partidas
    with open(os.path.join(data_path, 'matches', str(comp_id), f"{season_id}.json"), encoding='utf-8') as f:
        matches = json.load(f)

    match_ids = [m['match_id'] for m in matches]

    # 2. Verificar todos os eventos de drible
    for match_id in match_ids:
        try:
            with open(os.path.join(data_path, 'events', f"{match_id}.json"), encoding='utf-8') as f:
                events = json.load(f)

            for e in events:
                if e.get("player", {}).get("name") != player_name:
                    continue
                if e.get("type", {}).get("name") != "Dribble":
                    continue
                if not e.get("dribble", {}).get("nutmeg", False):
                    continue  # só queremos nutmegs

                outcome = e.get("dribble", {}).get("outcome", {}).get("name", "Complete")
                if outcome == "Complete":
                    nutmeg_successful += 1
                else:
                    nutmeg_failed += 1

        except:
            continue

    # Evitar divisão por zero
    if nutmeg_successful + nutmeg_failed == 0:
        print("Nenhum drible tipo nutmeg encontrado.")
        return

    # Dados para o gráfico
    labels = ['Successful Nutmeg', 'Failed Nutmeg']
    values = [nutmeg_successful, nutmeg_failed]

    # Criar gráfico donut
    fig = px.pie(
        names=labels,
        values=values,
        color=labels,
        color_discrete_map={
            'Successful Nutmeg': '#1F77B4',
            'Failed Nutmeg': '#D62728'
        },
        hole=0.35
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        textfont_size=11,
        hovertemplate='%{label}<br>%{value} dribbles<br>%{percent}'
    )

    fig.update_layout(
        title='Nutmeg Dribble Success Rate', 
        title_font_size=13,
        showlegend=False,
        template='plotly_white',
        margin=dict(t=30, b=10, l=10, r=10),
        height=180,
        font=dict(size=12)
    )

    return fig



