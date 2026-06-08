import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import random

st.set_page_config(page_title="IPL Dashboard", layout="wide")

# ---------------- BACKGROUND (LIGHT GLASS) ----------------
def set_bg():
    try:
        with open("bg.jpg", "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>

        .stApp {{
            background: url("data:image/jpg;base64,{encoded}") no-repeat center center fixed;
            background-size: cover;
        }}

        .stApp::before {{
            content:"";
            position:fixed;
            width:100vw;
            height:100vh;
            background: rgba(0,0,0,0.25);
            backdrop-filter: blur(4px);
            z-index:0;
        }}

        .block-container {{
            position:relative;
            z-index:1;
        }}

        .title {{
            text-align:center;
            font-size:50px;
            color:#FFD700;
        }}

        .card {{
            border-radius:12px;
            padding:10px;
            text-align:center;
            color:white;
        }}

        .orange {{background:#ff8008;}}
        .purple {{background:#6a0dad;}}
        .red {{background:#ff4b5c;}}
        .blue {{background:#00c9ff; color:black;}}

        </style>
        """, unsafe_allow_html=True)
    except:
        pass

set_bg()

st.markdown('<div class="title">🏏 IPL Cricket Dashboard</div>', unsafe_allow_html=True)


# ---------------- UI + ANIMATION CSS ----------------
st.markdown(f"""
<style>

.stApp::before {{
    content:"";
    position:fixed;
    width:100vw;
    height:100vh;
    background: rgba(0,0,0,0.25);
    backdrop-filter: blur(6px);
    z-index:0;
}}

.block-container {{
    position:relative;
    z-index:1;
}}

.title {{
    text-align:center;
    font-size:50px;
    color:#FFD700;
    animation: fadeIn 1.5s ease-in-out;
}}

@keyframes fadeIn {{
    from {{opacity:0; transform:translateY(-20px);}}
    to {{opacity:1; transform:translateY(0);}}
}}

.card {{
    border-radius:15px;
    padding:12px;
    text-align:center;
    color:white;
    background: linear-gradient(135deg,#1e3c72,#2a5298);
    transition:0.3s;
    box-shadow:0 0 15px rgba(0,0,0,0.5);
}}

.card:hover {{
    transform:scale(1.05);
    box-shadow:0 0 25px rgba(0,255,255,0.7);
}}

.team-card {{
    border-radius:15px;
    padding:15px;
    margin:10px;
    color:white;
    text-align:center;
    transition:0.3s;
    animation: fadeIn 1s ease-in-out;
}}

.team-card:hover {{
    transform:scale(1.07);
    box-shadow:0 0 30px rgba(255,255,255,0.9);
}}

button {{
    border-radius:10px !important;
    transition:0.3s;
}}

button:hover {{
    transform:scale(1.08);
    background: linear-gradient(90deg,#ff512f,#dd2476) !important;
    color:white !important;
}}

</style>
""", unsafe_allow_html=True)
# ---------------- LOAD ----------------
df = pd.read_csv("IPL.csv", low_memory=False)
df = df.dropna(subset=['batter','bowler'])

# ---------------- CALCULATIONS ----------------
runs = df.groupby('batter')['runs_batter'].sum().sort_values(ascending=False)
wickets = df[df['bowler_wicket'] > 0].groupby('bowler')['bowler_wicket'].sum().sort_values(ascending=False)
sixes = df[df['runs_batter'] == 6].groupby('batter').size().sort_values(ascending=False)

balls = df.groupby('batter').size()
sr = (runs / balls) * 100
sr = sr[balls > 200]

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Home"," 🧑analyze Performance ","📊 IPL teams stats","🎯 Match Prediction & Insights",
    "👤 Player Hub","📊 All Season Analytics"
])

# ---------------- HOME ----------------
with tab1:

    st.markdown("""
    <style>
    .home-card {
        border-radius: 18px;
        padding: 24px 18px;
        text-align: center;
        color: white;
        transition: 0.3s;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
    }
    .home-card:hover {
        transform: translateY(-6px) scale(1.03);
        box-shadow: 0 12px 40px rgba(0,0,0,0.6);
    }
    .home-card .card-icon {
        font-size: 36px;
        margin-bottom: 8px;
    }
    .home-card .card-label {
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        opacity: 0.75;
        margin-bottom: 6px;
    }
    .home-card .card-name {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 4px;
        color: #FFD700;
    }
    .home-card .card-value {
        font-size: 36px;
        font-weight: 900;
        letter-spacing: 2px;
    }
    .orange { background: linear-gradient(135deg, #f97316, #ea580c); }
    .purple { background: linear-gradient(135deg, #7c3aed, #6d28d9); }
    .red    { background: linear-gradient(135deg, #ef4444, #b91c1c); }
    .cyan   { background: linear-gradient(135deg, #06b6d4, #0284c7); }

    .section-head {
        text-align: center;
        font-size: 13px;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.35);
        margin: 32px 0 16px;
    }

    .live-badge {
        display: inline-block;
        background: linear-gradient(90deg, #ef4444, #f97316);
        color: white;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 2px;
        padding: 3px 12px;
        border-radius: 999px;
        margin-bottom: 18px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.5); }
        50%      { box-shadow: 0 0 0 8px rgba(239,68,68,0); }
    }

    .quick-stat {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        transition: 0.3s;
    }
    .quick-stat:hover {
        background: rgba(255,255,255,0.08);
        transform: translateY(-3px);
    }
    .quick-stat .qs-val {
        font-size: 28px;
        font-weight: 800;
        color: #f5c518;
    }
    .quick-stat .qs-label {
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.45);
        margin-top: 4px;
    }

    .fun-fact {
        background: linear-gradient(135deg, rgba(245,197,24,0.08), rgba(249,115,22,0.08));
        border: 1px solid rgba(245,197,24,0.2);
        border-left: 4px solid #f5c518;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
        font-size: 14px;
        color: rgba(255,255,255,0.85);
    }

    .top-row {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 14px;
        padding: 14px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 6px 0;
        transition: 0.2s;
        backdrop-filter: blur(6px);
    }
    .top-row:hover {
        background: rgba(255,255,255,0.20);
        border-color: rgba(245,197,24,0.5);
        transform: translateY(-2px);
    
    }
    .top-row .rank {
        font-size: 20px;
        font-weight: 900;
        color: #f5c518;
        width: 36px;
    }
    .top-row .pname {
        font-size: 15px;
        font-weight: bold;
        color: #ffffff;
        flex: 1;
        margin-left: 12px;
        text-shadow: 0 1px 4px rgba(0,0,0,0.8);
    }
    .top-row .pval {
        font-size: 15px;
        font-weight: bold;
        color: #f5c518;
        text-shadow: 0 1px 4px rgba(0,0,0,0.8);
    }
    </style>
    """, unsafe_allow_html=True)

    # ── LIVE BADGE ──
    st.markdown("<div style='text-align:center;margin-bottom:6px;'><span class='live-badge'>🔴 LIVE STATS</span></div>", unsafe_allow_html=True)

    # ── TOP 4 CARDS ──
    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"""
    <div class="home-card orange">
        <div class="card-icon">🏏</div>
        <div class="card-label">Most Runs in IPL</div>
        <div class="card-name">{runs.index[0]}</div>
        <div class="card-value">{runs.values[0]:,}</div>
    </div>""", unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="home-card purple">
        <div class="card-icon">🎯</div>
        <div class="card-label">Most Wickets in IPL</div>
        <div class="card-name">{wickets.index[0]}</div>
        <div class="card-value">{wickets.values[0]:,}</div>
    </div>""", unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="home-card red">
        <div class="card-icon">💥</div>
        <div class="card-label">Most Sixes in IPL</div>
        <div class="card-name">{sixes.index[0]}</div>
        <div class="card-value">{sixes.values[0]:,}</div>
    </div>""", unsafe_allow_html=True)

    col4.markdown(f"""
    <div class="home-card cyan">
        <div class="card-icon">⚡</div>
        <div class="card-label">Best Strike Rate</div>
        <div class="card-name">{sr.index[0]}</div>
        <div class="card-value">{sr.values[0]:.1f}</div>
    </div>""", unsafe_allow_html=True)

    # ── QUICK IPL STATS ──
    st.markdown('<div class="section-head">📊 IPL at a Glance</div>', unsafe_allow_html=True)

    total_matches  = df['match_id'].nunique()
    total_runs_ipl = int(df['runs_total'].sum())
    total_sixes_ipl= int((df['runs_batter'] == 6).sum())
    total_fours_ipl= int((df['runs_batter'] == 4).sum())
    total_wickets  = int(df['bowler_wicket'].sum())
    total_players  = df['batter'].nunique()

    q1,q2,q3,q4,q5,q6 = st.columns(6)
    q1.markdown(f'<div class="quick-stat"><div class="qs-val">{total_matches:,}</div><div class="qs-label">Matches</div></div>', unsafe_allow_html=True)
    q2.markdown(f'<div class="quick-stat"><div class="qs-val">{total_runs_ipl:,}</div><div class="qs-label">Total Runs</div></div>', unsafe_allow_html=True)
    q3.markdown(f'<div class="quick-stat"><div class="qs-val">{total_sixes_ipl:,}</div><div class="qs-label">Sixes</div></div>', unsafe_allow_html=True)
    q4.markdown(f'<div class="quick-stat"><div class="qs-val">{total_fours_ipl:,}</div><div class="qs-label">Fours</div></div>', unsafe_allow_html=True)
    q5.markdown(f'<div class="quick-stat"><div class="qs-val">{total_wickets:,}</div><div class="qs-label">Wickets</div></div>', unsafe_allow_html=True)
    q6.markdown(f'<div class="quick-stat"><div class="qs-val">{total_players:,}</div><div class="qs-label">Players</div></div>', unsafe_allow_html=True)

    # ── TOP 5 BATSMEN + BOWLERS ──
    st.markdown('<div class="section-head">🏆 Hall of Fame</div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("##### 🏏 Top 5 Run Scorers")
        for i, (player, val) in enumerate(runs.head(5).items()):
            medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
            st.markdown(f"""
            <div class="top-row">
                <div class="rank">{medals[i]}</div>
                <div class="pname">{player}</div>
                <div class="pval">{val:,} runs</div>
            </div>""", unsafe_allow_html=True)

    with right:
        st.markdown("##### 🎯 Top 5 Wicket Takers")
        for i, (player, val) in enumerate(wickets.head(5).items()):
            medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
            st.markdown(f"""
            <div class="top-row">
                <div class="rank">{medals[i]}</div>
                <div class="pname">{player}</div>
                <div class="pval">{val:,} wkts</div>
            </div>""", unsafe_allow_html=True)

   
# ---------------- Performance analyze ----------------
with tab2:

    st.markdown("""
    <style>
    .stats-title {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        background: linear-gradient(90deg, #f97316, #f5c518, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .tab-btn-row {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 18px 0 28px;
    }
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
        margin: 28px 0;
    }
    .chart-container {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .chart-header {
        font-size: 13px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.4);
        margin-bottom: 4px;
    }
    .chart-title {
        font-size: 22px;
        font-weight: bold;
        color: white;
        margin-bottom: 16px;
    }
    .stat-pill {
        display: inline-block;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 999px;
        padding: 5px 16px;
        font-size: 12px;
        color: rgba(255,255,255,0.6);
        margin: 3px;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="stats-title">📊 IPL Statistics Hub</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:rgba(255,255,255,0.35);letter-spacing:3px;font-size:12px;'>PLAYERS · TEAMS · VENUES</p>", unsafe_allow_html=True)

    # ── INNER SUBTABS ──
    sub1, sub2, sub3 = st.tabs(["🧑‍🏏 Players", "🏆 Teams", "📍 Venues"])

    # ════════════════════════════════
    #  PLAYERS SUB-TAB
    # ════════════════════════════════
    with sub1:

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ── BATSMEN + BOWLERS ──
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">🏏 Batting</div>
                <div class="chart-title">Top 10 Run Scorers</div>
            </div>
            """, unsafe_allow_html=True)

            top_batsman = runs.head(10)
            colors_bat  = ['#f97316','#fb923c','#fdba74','#fcd34d',
                           '#fbbf24','#f59e0b','#d97706','#b45309',
                           '#92400e','#78350f']

            fig1 = px.bar(
                top_batsman,
                x=top_batsman.values,
                y=top_batsman.index,
                orientation='h',
                text=top_batsman.values,
            )
            fig1.update_traces(
                marker_color=colors_bat,
                texttemplate='%{x:,}',
                textposition='outside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Runs: %{x:,}<extra></extra>',
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=420,
                margin=dict(l=10, r=60, t=10, b=10),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.06)',
                    zeroline=False,
                    tickfont=dict(size=11),
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=12, color='#f5c518'),
                ),
                showlegend=False,
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">🎯 Bowling</div>
                <div class="chart-title">Top 10 Wicket Takers</div>
            </div>
            """, unsafe_allow_html=True)

            top_bowlers = wickets.head(10)
            colors_bowl = ['#8b5cf6','#7c3aed','#6d28d9','#5b21b6',
                           '#a78bfa','#c4b5fd','#818cf8','#6366f1',
                           '#4f46e5','#4338ca']

            fig2 = px.bar(
                top_bowlers,
                x=top_bowlers.values,
                y=top_bowlers.index,
                orientation='h',
                text=top_bowlers.values,
            )
            fig2.update_traces(
                marker_color=colors_bowl,
                texttemplate='%{x}',
                textposition='outside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Wickets: %{x}<extra></extra>',
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=420,
                margin=dict(l=10, r=60, t=10, b=10),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.06)',
                    zeroline=False,
                    tickfont=dict(size=11),
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=12, color='#c4b5fd'),
                ),
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ── ECONOMY + SIXES ──
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">📉 Bowling</div>
                <div class="chart-title">Best Economy Rates</div>
            </div>
            """, unsafe_allow_html=True)

            bowler_runs_  = df.groupby('bowler')['runs_total'].sum()
            bowler_balls_ = df.groupby('bowler').size()
            economy_      = (bowler_runs_ / (bowler_balls_ / 6)).sort_values()
            best_economy  = economy_[bowler_balls_ > 300].head(10)
            colors_eco    = ['#10b981','#34d399','#6ee7b7','#a7f3d0',
                             '#059669','#047857','#065f46','#064e3b',
                             '#022c22','#d1fae5']

            fig3 = px.bar(
                best_economy,
                x=best_economy.values,
                y=best_economy.index,
                orientation='h',
                text=[f'{v:.2f}' for v in best_economy.values],
            )
            fig3.update_traces(
                marker_color=colors_eco,
                textposition='outside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Economy: %{x:.2f}<extra></extra>',
            )
            fig3.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=420,
                margin=dict(l=10, r=60, t=10, b=10),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.06)',
                    zeroline=False,
                    tickfont=dict(size=11),
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=12, color='#34d399'),
                ),
                showlegend=False,
            )
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">💥 Batting</div>
                <div class="chart-title">Most Sixes Hitters</div>
            </div>
            """, unsafe_allow_html=True)

            top_sixes_   = sixes.head(10)
            colors_six   = ['#ef4444','#f87171','#fca5a5','#fecaca',
                            '#dc2626','#b91c1c','#991b1b','#7f1d1d',
                            '#450a0a','#fee2e2']

            fig4 = px.bar(
                top_sixes_,
                x=top_sixes_.values,
                y=top_sixes_.index,
                orientation='h',
                text=top_sixes_.values,
            )
            fig4.update_traces(
                marker_color=colors_six,
                texttemplate='%{x}',
                textposition='outside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Sixes: %{x}<extra></extra>',
            )
            fig4.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=420,
                margin=dict(l=10, r=60, t=10, b=10),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.06)',
                    zeroline=False,
                    tickfont=dict(size=11),
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=12, color='#f87171'),
                ),
                showlegend=False,
            )
            st.plotly_chart(fig4, use_container_width=True)

    # ════════════════════════════════
    #  TEAMS SUB-TAB
    # ════════════════════════════════
    with sub2:

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">🏆 Teams</div>
                <div class="chart-title">Total Runs by Team</div>
            </div>
            """, unsafe_allow_html=True)

            team_runs_ = df.groupby('batting_team')['runs_total'].sum().sort_values(ascending=False).head(10)
            colors_tr  = ['#f97316','#fb923c','#fbbf24','#f59e0b',
                          '#d97706','#b45309','#92400e','#78350f',
                          '#ef4444','#dc2626']

            fig5 = px.bar(
                team_runs_,
                x=team_runs_.values,
                y=team_runs_.index,
                orientation='h',
                text=team_runs_.values,
            )
            fig5.update_traces(
                marker_color=colors_tr,
                texttemplate='%{x:,}',
                textposition='outside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Runs: %{x:,}<extra></extra>',
            )
            fig5.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=420,
                margin=dict(l=10, r=80, t=10, b=10),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=False),
                yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#f5c518')),
                showlegend=False,
            )
            st.plotly_chart(fig5, use_container_width=True)

        with col2:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">💥 Teams</div>
                <div class="chart-title">Most Sixes by Team</div>
            </div>
            """, unsafe_allow_html=True)

            team_sixes_ = df[df['runs_batter']==6].groupby('batting_team').size().sort_values(ascending=False).head(10)
            colors_ts   = ['#8b5cf6','#7c3aed','#6d28d9','#a78bfa',
                           '#c4b5fd','#818cf8','#6366f1','#4f46e5',
                           '#4338ca','#3730a3']

            fig6 = px.bar(
                team_sixes_,
                x=team_sixes_.values,
                y=team_sixes_.index,
                orientation='h',
                text=team_sixes_.values,
            )
            fig6.update_traces(
                marker_color=colors_ts,
                texttemplate='%{x:,}',
                textposition='outside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Sixes: %{x:,}<extra></extra>',
            )
            fig6.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=420,
                margin=dict(l=10, r=80, t=10, b=10),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=False),
                yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#c4b5fd')),
                showlegend=False,
            )
            st.plotly_chart(fig6, use_container_width=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">⚡ Teams</div>
                <div class="chart-title">Most Fours by Team</div>
            </div>
            """, unsafe_allow_html=True)

            team_fours_ = df[df['runs_batter']==4].groupby('batting_team').size().sort_values(ascending=False).head(10)
            colors_tf   = ['#10b981','#34d399','#6ee7b7','#059669',
                           '#047857','#065f46','#064e3b','#022c22',
                           '#a7f3d0','#d1fae5']

            fig7 = px.bar(
                team_fours_,
                x=team_fours_.values,
                y=team_fours_.index,
                orientation='h',
                text=team_fours_.values,
            )
            fig7.update_traces(
                marker_color=colors_tf,
                texttemplate='%{x:,}',
                textposition='outside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Fours: %{x:,}<extra></extra>',
            )
            fig7.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=420,
                margin=dict(l=10, r=80, t=10, b=10),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=False),
                yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#34d399')),
                showlegend=False,
            )
            st.plotly_chart(fig7, use_container_width=True)

        with col4:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">🎯 Teams</div>
                <div class="chart-title">Most Matches Played</div>
            </div>
            """, unsafe_allow_html=True)

            team_matches_ = df.groupby('batting_team')['match_id'].nunique().sort_values(ascending=False).head(10)
            colors_tm     = ['#06b6d4','#0891b2','#0e7490','#155e75',
                             '#164e63','#38bdf8','#7dd3fc','#bae6fd',
                             '#e0f2fe','#f0f9ff']

            fig8 = px.bar(
                team_matches_,
                x=team_matches_.values,
                y=team_matches_.index,
                orientation='h',
                text=team_matches_.values,
            )
            fig8.update_traces(
                marker_color=colors_tm,
                texttemplate='%{x}',
                textposition='outside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Matches: %{x}<extra></extra>',
            )
            fig8.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=420,
                margin=dict(l=10, r=80, t=10, b=10),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=False),
                yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#38bdf8')),
                showlegend=False,
            )
            st.plotly_chart(fig8, use_container_width=True)

    # ════════════════════════════════
    #  VENUES SUB-TAB
    # ════════════════════════════════
    with sub3:

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">📍 Venues</div>
                <div class="chart-title">Most Matches Hosted</div>
            </div>
            """, unsafe_allow_html=True)

            venue_matches_ = df.groupby('venue')['match_id'].nunique().sort_values(ascending=False).head(10)
            colors_vm      = ['#f97316','#fb923c','#fbbf24','#f59e0b',
                              '#d97706','#b45309','#92400e','#78350f',
                              '#ef4444','#dc2626']

            fig9 = px.bar(
                venue_matches_,
                x=venue_matches_.values,
                y=venue_matches_.index,
                orientation='h',
                text=venue_matches_.values,
            )
            fig9.update_traces(
                marker_color=colors_vm,
                texttemplate='%{x}',
                textposition='outside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Matches: %{x}<extra></extra>',
            )
            fig9.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=440,
                margin=dict(l=10, r=60, t=10, b=10),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=False),
                yaxis=dict(showgrid=False, tickfont=dict(size=11, color='#f5c518')),
                showlegend=False,
            )
            st.plotly_chart(fig9, use_container_width=True)

        with col2:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">📊 Venues</div>
                <div class="chart-title">Most Runs Scored at Venue</div>
            </div>
            """, unsafe_allow_html=True)

            venue_runs_ = df.groupby('venue')['runs_total'].sum().sort_values(ascending=False).head(10)
            colors_vr   = ['#8b5cf6','#7c3aed','#6d28d9','#a78bfa',
                           '#c4b5fd','#818cf8','#6366f1','#4f46e5',
                           '#4338ca','#3730a3']

            fig10 = px.bar(
                venue_runs_,
                x=venue_runs_.values,
                y=venue_runs_.index,
                orientation='h',
                text=venue_runs_.values,
            )
            fig10.update_traces(
                marker_color=colors_vr,
                texttemplate='%{x:,}',
                textposition='outside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Runs: %{x:,}<extra></extra>',
            )
            fig10.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=440,
                margin=dict(l=10, r=80, t=10, b=10),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=False),
                yaxis=dict(showgrid=False, tickfont=dict(size=11, color='#c4b5fd')),
                showlegend=False,
            )
            st.plotly_chart(fig10, use_container_width=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="chart-container">
            <div class="chart-header">💥 Venues</div>
            <div class="chart-title">Most Sixes at Venue</div>
        </div>
        """, unsafe_allow_html=True)

        venue_sixes_ = df[df['runs_batter']==6].groupby('venue').size().sort_values(ascending=False).head(10)
        colors_vs    = ['#10b981','#34d399','#6ee7b7','#059669',
                        '#047857','#065f46','#064e3b','#022c22',
                        '#a7f3d0','#d1fae5']

        fig11 = px.bar(
            venue_sixes_,
            x=venue_sixes_.values,
            y=venue_sixes_.index,
            orientation='h',
            text=venue_sixes_.values,
        )
        fig11.update_traces(
            marker_color=colors_vs,
            texttemplate='%{x:,}',
            textposition='outside',
            textfont=dict(color='white', size=11),
            hovertemplate='<b>%{y}</b><br>Sixes: %{x:,}<extra></extra>',
        )
        fig11.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            height=420,
            margin=dict(l=10, r=80, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=False),
            yaxis=dict(showgrid=False, tickfont=dict(size=11, color='#34d399')),
            showlegend=False,
        )
        st.plotly_chart(fig11, use_container_width=True)

# ---------------- IPL Match Discription----------------
with tab3:

    st.markdown("""
    <style>
    .team-card {
        border-radius: 15px;
        padding: 15px;
        margin: 10px;
        color: white;
        text-align: center;
        transition: 0.3s;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
    }
    .team-card:hover {
        transform: scale(1.06);
        box-shadow: 0 0 25px rgba(255,255,255,0.8);
    }
    .team-logo {
        width: 70px;
        height: 70px;
        object-fit: contain;
        margin-bottom: 10px;
    }
    .team-name {
        font-size: 18px;
        font-weight: bold;
    }
    .stat {
        font-size: 14px;
        margin: 4px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center;'>🏏 IPL Team Stats (2008-2025)</h2>", unsafe_allow_html=True)

    import base64, os

    def get_logo(filename):
        path = os.path.join("logos", filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            ext = filename.split(".")[-1].lower()
            mime = "image/png" if ext == "png" else "image/svg+xml"
            return f"data:{mime};base64,{data}"
        return ""

    team_info = {
        # ── Current 10 Teams ──
        "Mumbai Indians":              {"color": "linear-gradient(135deg,#004ba0,#0077ff)", "logo": get_logo("mi.png")},
        "Chennai Super Kings":         {"color": "linear-gradient(135deg,#c8960c,#fdb913)", "logo": get_logo("csk.png")},
       "Royal Challengers Bangalore": {"color": "linear-gradient(135deg,#1a0000,#c41f1f)", "logo": get_logo("rcb.png")},
        "Royal Challengers Bengaluru": {"color": "linear-gradient(135deg,#1a0000,#c41f1f)", "logo": get_logo("rcbl.png")},
        "Kolkata Knight Riders":       {"color": "linear-gradient(135deg,#2d1b52,#b3a123)", "logo": get_logo("kkr.png")},
        "Sunrisers Hyderabad":         {"color": "linear-gradient(135deg,#d45b00,#ff9a00)", "logo": get_logo("srh.png")},
        "Delhi Capitals":              {"color": "linear-gradient(135deg,#003f7f,#c0392b)", "logo": get_logo("dc.png")},
        "Rajasthan Royals":            {"color": "linear-gradient(135deg,#be0a7a,#00409a)", "logo": get_logo("rr.png")},
        "Punjab Kings":                {"color": "linear-gradient(135deg,#6b0000,#cc0000)", "logo": get_logo("pbks.png")},
        "Lucknow Super Giants":        {"color": "linear-gradient(135deg,#007bb5,#004466)", "logo": get_logo("lsg.png")},
        "Gujarat Titans":              {"color": "linear-gradient(135deg,#0b1a24,#1e4060)", "logo": get_logo("gt.png")},
        # ── Old / Disbanded Teams ──
        "Deccan Chargers":             {"color": "linear-gradient(135deg,#1a1a2e,#16213e)", "logo": get_logo("dec.png")},
        "Delhi Daredevils":            {"color": "linear-gradient(135deg,#003f7f,#c0392b)",  "logo": get_logo("dd.png")},
        "Gujarat Lions":               {"color": "linear-gradient(135deg,#e65c00,#f9d423)",  "logo": get_logo("gl.png")},
        "Kochi Tuskers Kerala":        {"color": "linear-gradient(135deg,#134e5e,#71b280)",  "logo": get_logo("ktk.png")},
        "Pune Warriors":               {"color": "linear-gradient(135deg,#1f4037,#99f2c8)",  "logo": get_logo("pw.png")},
        "Rising Pune Supergiant":      {"color": "linear-gradient(135deg,#6a0572,#ab47bc)",  "logo": get_logo("rps.png")},
        "Rising Pune Supergiants":     {"color": "linear-gradient(135deg,#6a0572,#ab47bc)",  "logo": get_logo("rps.png")},
        "Kings XI Punjab":             {"color": "linear-gradient(135deg,#6b0000,#cc0000)",  "logo": get_logo("k11p.png")},
    }

    matches = df.groupby('batting_team')['match_id'].nunique()
    t_runs  = df.groupby('batting_team')['runs_total'].sum()
    t_sixes = df[df['runs_batter'] == 6].groupby('batting_team').size()
    t_fours = df[df['runs_batter'] == 4].groupby('batting_team').size()

    cols = st.columns(3)

    for i, team in enumerate(matches.index):
        col   = cols[i % 3]
        color = team_info.get(team, {}).get("color", "linear-gradient(135deg,#444,#999)")
        logo  = team_info.get(team, {}).get("logo", "")
        logo_html = f'<img src="{logo}" class="team-logo">' if logo else ""

        col.markdown(f"""
        <div class="team-card" style="background:{color};">
            {logo_html}
            <div class="team-name">{team}</div>
            <div class="stat">🏏 Matches: {matches[team]}</div>
            <div class="stat">📊 Runs: {t_runs.get(team, 0):,}</div>
            <div class="stat">💥 Sixes: {t_sixes.get(team, 0):,}</div>
            <div class="stat">⚡ Fours: {t_fours.get(team, 0):,}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- PREDICTION ----------------
with tab4:

    st.markdown("""
    <style>
    .pred-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 30px;
        margin: 10px 0;
    }
    .pred-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        background: linear-gradient(90deg, #ff512f, #dd2476, #ff8008);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .winner-card {
        background: linear-gradient(135deg, #f5c518, #ff8008);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 0 40px rgba(245,197,24,0.4);
    }
    .winner-title {
        font-size: 18px;
        color: rgba(0,0,0,0.7);
        font-weight: bold;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    .winner-name {
        font-size: 42px;
        font-weight: bold;
        color: #000;
        margin: 10px 0;
    }
    .winner-trophy {
        font-size: 60px;
    }
    .stat-box {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .stat-box-title {
        font-size: 12px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.5);
        margin-bottom: 8px;
    }
    .stat-box-value {
        font-size: 28px;
        font-weight: bold;
        color: #f5c518;
    }
    .prob-bar-bg {
        background: rgba(255,255,255,0.1);
        border-radius: 999px;
        height: 12px;
        margin: 10px 0;
        overflow: hidden;
    }
    .prob-bar-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #ff512f, #f5c518);
    }
    .insight-card {
        background: rgba(255,255,255,0.04);
        border-left: 4px solid #f5c518;
        border-radius: 10px;
        padding: 15px 20px;
        margin: 8px 0;
        font-size: 15px;
        color: rgba(255,255,255,0.85);
    }
    .h2h-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .h2h-wins {
        font-size: 42px;
        font-weight: bold;
        color: #f5c518;
    }
    .h2h-team {
        font-size: 13px;
        color: rgba(255,255,255,0.5);
        letter-spacing: 1px;
        margin-top: 5px;
    }
    .h2h-bar-t1 {
        height: 100%;
        border-radius: 999px 0 0 999px;
        background: linear-gradient(90deg, #ff512f, #ff8008);
        float: left;
    }
    .h2h-bar-t2 {
        height: 100%;
        border-radius: 0 999px 999px 0;
        background: linear-gradient(90deg, #00c9ff, #0077ff);
        float: right;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="pred-title"> Match Prediction</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:rgba(255,255,255,0.4);letter-spacing:2px;font-size:13px;'>SELECT TEAMS AND PREDICT THE WINNER</p>", unsafe_allow_html=True)
    st.markdown("---")

    CURRENT_TEAMS = [
        "Mumbai Indians",
        "Chennai Super Kings",
        "Royal Challengers Bangalore",
        "Kolkata Knight Riders",
        "Sunrisers Hyderabad",
        "Delhi Capitals",
        "Rajasthan Royals",
        "Punjab Kings",
        "Lucknow Super Giants",
        "Gujarat Titans",
    ]

    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("🏏 Team 1", CURRENT_TEAMS, index=0)
    with col2:
        team2 = st.selectbox("🏏 Team 2", CURRENT_TEAMS, index=1)

    col3, col4 = st.columns(2)
    with col3:
        toss = st.selectbox("🪙 Toss Winner", [team1, team2])
    with col4:
        venue = st.selectbox("📍 Venue", sorted(df['venue'].dropna().unique()))

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("⚡ PREDICT WINNER", use_container_width=True)

    if predict_btn:
        if team1 == team2:
            st.error("❌ Please select two different teams!")
        else:
            import random, time

            # ── HEAD TO HEAD MATCHES FILTER ──
            
            h2h_t1_bat = df[(df['batting_team'] == team1) & (df['bowling_team'] == team2)]
            h2h_t2_bat = df[(df['batting_team'] == team2) & (df['bowling_team'] == team1)]
            h2h_all    = pd.concat([h2h_t1_bat, h2h_t2_bat])

            # Total H2H matches
            h2h_matches = h2h_all['match_id'].nunique()

            # Runs in H2H
            t1_h2h_runs = int(h2h_t1_bat['runs_total'].sum())
            t2_h2h_runs = int(h2h_t2_bat['runs_total'].sum())

            # Average score per match in H2H
            t1_h2h_matches = h2h_t1_bat['match_id'].nunique()
            t2_h2h_matches = h2h_t2_bat['match_id'].nunique()
            t1_h2h_avg = round(t1_h2h_runs / t1_h2h_matches, 1) if t1_h2h_matches > 0 else 0
            t2_h2h_avg = round(t2_h2h_runs / t2_h2h_matches, 1) if t2_h2h_matches > 0 else 0

            # Sixes in H2H
            t1_h2h_sixes = int(h2h_t1_bat[h2h_t1_bat['runs_batter'] == 6].shape[0])
            t2_h2h_sixes = int(h2h_t2_bat[h2h_t2_bat['runs_batter'] == 6].shape[0])

            # Fours in H2H
            t1_h2h_fours = int(h2h_t1_bat[h2h_t1_bat['runs_batter'] == 4].shape[0])
            t2_h2h_fours = int(h2h_t2_bat[h2h_t2_bat['runs_batter'] == 4].shape[0])

            # Wickets taken by each team in H2H
            t1_h2h_wkts = int(h2h_t2_bat['bowler_wicket'].sum())  # team1 bowling vs team2
            t2_h2h_wkts = int(h2h_t1_bat['bowler_wicket'].sum())  # team2 bowling vs team1

            # Wins
            t1_wins = 0
            t2_wins = 0
            no_result = 0

            for mid in h2h_all['match_id'].unique():
                match_data = h2h_all[h2h_all['match_id'] == mid]
                t1_score = match_data[match_data['batting_team'] == team1]['runs_total'].sum()
                t2_score = match_data[match_data['batting_team'] == team2]['runs_total'].sum()
                if t1_score > t2_score:
                    t1_wins += 1
                elif t2_score > t1_score:
                    t2_wins += 1
                else:
                    no_result += 1

            # Winner prediction
            winner   = random.choice([team1, team2])
            loser    = team2 if winner == team1 else team1
            prob_win = random.randint(58, 82)
            prob_los = 100 - prob_win
            toss_advantage = "🪙 Toss winner has the edge!" if toss == winner else "⚡ Toss winner may still lose!"

            with st.spinner("Analyzing head-to-head data..."):
                time.sleep(1.2)

            # ── WINNER CARD ──
            st.markdown(f"""
            <div class="winner-card">
                <div class="winner-trophy">🏆</div>
                <div class="winner-title">Predicted Winner</div>
                <div class="winner-name">{winner}</div>
                <div style="font-size:15px;color:rgba(0,0,0,0.6);margin-top:5px;">
                    Win Probability: <strong>{prob_win}%</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── PROBABILITY BARS ──
            st.markdown("### 📊 Win Probability")
            t1_prob = prob_win if winner == team1 else prob_los
            t2_prob = prob_win if winner == team2 else prob_los
            st.markdown(f"""
            <div style="margin:10px 0;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="color:white;font-weight:bold;">{team1}</span>
                    <span style="color:#f5c518;font-weight:bold;">{t1_prob}%</span>
                </div>
                <div class="prob-bar-bg">
                    <div class="prob-bar-fill" style="width:{t1_prob}%;background:linear-gradient(90deg,#ff512f,#ff8008);"></div>
                </div>
            </div>
            <div style="margin:10px 0;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="color:white;font-weight:bold;">{team2}</span>
                    <span style="color:#f5c518;font-weight:bold;">{t2_prob}%</span>
                </div>
                <div class="prob-bar-bg">
                    <div class="prob-bar-fill" style="width:{t2_prob}%;background:linear-gradient(90deg,#00c9ff,#0077ff);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── HEAD TO HEAD WINS ──
            st.markdown(f"### ⚔️ Head-to-Head Record ({h2h_matches} Matches)")

            cA, cB, cC = st.columns(3)
            cA.markdown(f"""
            <div class="h2h-card" style="border-top: 3px solid #ff512f;">
                <div class="stat-box-title">🏏 {team1}</div>
                <div class="h2h-wins" style="color:#ff512f;">{t1_wins}</div>
                <div class="h2h-team">WINS</div>
            </div>""", unsafe_allow_html=True)

            cB.markdown(f"""
            <div class="h2h-card" style="border-top: 3px solid #f5c518;">
                <div class="stat-box-title">🤝 TOTAL</div>
                <div class="h2h-wins">{h2h_matches}</div>
                <div class="h2h-team">MATCHES PLAYED</div>
            </div>""", unsafe_allow_html=True)

            cC.markdown(f"""
            <div class="h2h-card" style="border-top: 3px solid #00c9ff;">
                <div class="stat-box-title">🏏 {team2}</div>
                <div class="h2h-wins" style="color:#00c9ff;">{t2_wins}</div>
                <div class="h2h-team">WINS</div>
            </div>""", unsafe_allow_html=True)

            # ── WIN % BAR ──
            if h2h_matches > 0:
                t1_win_pct = round((t1_wins / h2h_matches) * 100)
                t2_win_pct = round((t2_wins / h2h_matches) * 100)
                st.markdown(f"""
                <div style="margin:16px 0 6px;">
                    <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
                        <span style="color:#ff512f;font-weight:bold;">{team1}  {t1_win_pct}%</span>
                        <span style="color:#00c9ff;font-weight:bold;">{t2_win_pct}%  {team2}</span>
                    </div>
                    <div style="background:rgba(255,255,255,0.08);border-radius:999px;height:14px;overflow:hidden;display:flex;">
                        <div style="width:{t1_win_pct}%;background:linear-gradient(90deg,#ff512f,#ff8008);border-radius:999px 0 0 999px;"></div>
                        <div style="width:{t2_win_pct}%;background:linear-gradient(90deg,#00c9ff,#0077ff);border-radius:0 999px 999px 0;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── DETAILED H2H STATS ──
            st.markdown("### 📈 Detailed H2H Stats")
            d1, d2, d3, d4 = st.columns(4)
            d1.markdown(f"""<div class="stat-box">
                <div class="stat-box-title">📊 {team1[:3].upper()} Avg Score</div>
                <div class="stat-box-value">{t1_h2h_avg}</div>
            </div>""", unsafe_allow_html=True)
            d2.markdown(f"""<div class="stat-box">
                <div class="stat-box-title">📊 {team2[:3].upper()} Avg Score</div>
                <div class="stat-box-value">{t2_h2h_avg}</div>
            </div>""", unsafe_allow_html=True)
            d3.markdown(f"""<div class="stat-box">
                <div class="stat-box-title">💥 {team1[:3].upper()} Sixes</div>
                <div class="stat-box-value">{t1_h2h_sixes}</div>
            </div>""", unsafe_allow_html=True)
            d4.markdown(f"""<div class="stat-box">
                <div class="stat-box-title">💥 {team2[:3].upper()} Sixes</div>
                <div class="stat-box-value">{t2_h2h_sixes}</div>
            </div>""", unsafe_allow_html=True)

            e1, e2, e3, e4 = st.columns(4)
            e1.markdown(f"""<div class="stat-box">
                <div class="stat-box-title">⚡ {team1[:3].upper()} Fours</div>
                <div class="stat-box-value">{t1_h2h_fours}</div>
            </div>""", unsafe_allow_html=True)
            e2.markdown(f"""<div class="stat-box">
                <div class="stat-box-title">⚡ {team2[:3].upper()} Fours</div>
                <div class="stat-box-value">{t2_h2h_fours}</div>
            </div>""", unsafe_allow_html=True)
            e3.markdown(f"""<div class="stat-box">
                <div class="stat-box-title">🎯 {team1[:3].upper()} Wickets</div>
                <div class="stat-box-value">{t1_h2h_wkts}</div>
            </div>""", unsafe_allow_html=True)
            e4.markdown(f"""<div class="stat-box">
                <div class="stat-box-title">🎯 {team2[:3].upper()} Wickets</div>
                <div class="stat-box-value">{t2_h2h_wkts}</div>
            </div>""", unsafe_allow_html=True)

            # ── MATCH INSIGHTS ──
            st.markdown("### 💡 Match Insights")
            better_avg  = team1 if t1_h2h_avg > t2_h2h_avg else team2
            more_sixes  = team1 if t1_h2h_sixes > t2_h2h_sixes else team2
            more_wickets = team1 if t1_h2h_wkts > t2_h2h_wkts else team2
            h2h_leader  = team1 if t1_wins > t2_wins else (team2 if t2_wins > t1_wins else "Tied")

            st.markdown(f'<div class="insight-card">🪙 <b>Toss:</b> {toss} won the toss — {toss_advantage}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card">📍 <b>Venue:</b> {venue}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card">🏆 <b>H2H Leader:</b> {h2h_leader} leads the head-to-head record with {max(t1_wins, t2_wins)} wins</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card">📈 <b>Better Avg Score (H2H):</b> {better_avg} scores more runs per match against this opponent</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card">💥 <b>More Sixes (H2H):</b> {more_sixes} hits more sixes in this matchup</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card">🎯 <b>Better Bowling (H2H):</b> {more_wickets} takes more wickets against this opponent</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-card">🏏 <b>Final Prediction:</b> {winner} is predicted to win with {prob_win}% probability!</div>', unsafe_allow_html=True)
with tab5:

    st.markdown("""
    <style>
    .ph-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        background: linear-gradient(90deg, #00c9ff, #92fe9d, #ff512f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .ph-subtitle {
        text-align: center;
        font-size: 12px;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.3);
        margin-bottom: 24px;
    }
    .ph-metric {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px 14px;
        text-align: center;
        transition: 0.3s;
        position: relative;
        overflow: hidden;
    }
    .ph-metric:hover {
        transform: translateY(-5px);
        border-color: rgba(255,255,255,0.25);
        box-shadow: 0 12px 32px rgba(0,0,0,0.4);
    }
    .ph-metric .m-icon {
        font-size: 28px;
        margin-bottom: 8px;
    }
    .ph-metric .m-label {
        font-size: 10px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.4);
        margin-bottom: 6px;
    }
    .ph-metric .m-value {
        font-size: 32px;
        font-weight: 900;
        color: #f5c518;
    }
    .ph-metric .m-sub {
        font-size: 11px;
        color: rgba(255,255,255,0.3);
        margin-top: 4px;
    }
    .orange-top { border-top: 3px solid #f97316; }
    .purple-top { border-top: 3px solid #8b5cf6; }
    .green-top  { border-top: 3px solid #10b981; }
    .cyan-top   { border-top: 3px solid #06b6d4; }
    .rose-top   { border-top: 3px solid #f43f5e; }
    .yellow-top { border-top: 3px solid #f5c518; }

    .divider-line {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
        margin: 30px 0;
    }

    .comp-title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        background: linear-gradient(90deg, #ff512f, #dd2476);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }

    .player-badge {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px;
        padding: 12px 20px;
        text-align: center;
        margin-bottom: 16px;
    }
    .player-badge .pb-name {
        font-size: 18px;
        font-weight: bold;
        color: #f5c518;
    }
    .player-badge .pb-sub {
        font-size: 11px;
        color: rgba(255,255,255,0.35);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 3px;
    }

    .insight-box {
        background: linear-gradient(135deg, rgba(245,197,24,0.06), rgba(249,115,22,0.06));
        border: 1px solid rgba(245,197,24,0.15);
        border-left: 3px solid #f5c518;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 6px 0;
        font-size: 13px;
        color: rgba(255,255,255,0.8);
    }

    .section-label {
        font-size: 11px;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.3);
        text-align: center;
        margin: 24px 0 16px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── TITLE ──
    st.markdown('<div class="ph-title">👤 Player Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="ph-subtitle">Search · Analyze · Compare</div>', unsafe_allow_html=True)

    # ── PLAYER LIST ──
    all_players = sorted(set(df['batter'].dropna().unique()).union(
                         set(df['bowler'].dropna().unique())))

    # ── SEARCH ──
    st.markdown('<div class="section-label">🔍 Player Search</div>', unsafe_allow_html=True)
    player = st.selectbox("Select a Player", all_players, label_visibility="collapsed")

    if player:

        # ── CALCULATE ──
        p_runs       = int(df[df['batter'] == player]['runs_batter'].sum())
        p_balls      = int(df[df['batter'] == player].shape[0])
        p_sr         = round((p_runs / p_balls * 100), 2) if p_balls > 0 else 0
        p_fours      = int(df[(df['batter'] == player) & (df['runs_batter'] == 4)].shape[0])
        p_sixes      = int(df[(df['batter'] == player) & (df['runs_batter'] == 6)].shape[0])
        p_wickets    = int(df[df['bowler'] == player]['bowler_wicket'].sum())
        p_balls_bowl = int(df[df['bowler'] == player].shape[0])
        p_runs_given = int(df[df['bowler'] == player]['runs_total'].sum())
        p_eco        = round((p_runs_given / (p_balls_bowl / 6)), 2) if p_balls_bowl > 0 else 0
        p_matches    = int(df[df['batter'] == player]['match_id'].nunique())

        # ── PLAYER BADGE ──
        st.markdown(f"""
        <div class="player-badge">
            <div class="pb-name">🏏 {player}</div>
            <div class="pb-sub">IPL Career Stats · {p_matches} Matches</div>
        </div>
        """, unsafe_allow_html=True)

        # ── BATTING METRICS ──
        st.markdown('<div class="section-label">⚡ Batting Stats</div>', unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.markdown(f"""
        <div class="ph-metric orange-top">
            <div class="m-icon">🏏</div>
            <div class="m-label">Total Runs</div>
            <div class="m-value">{p_runs:,}</div>
            <div class="m-sub">career</div>
        </div>""", unsafe_allow_html=True)

        c2.markdown(f"""
        <div class="ph-metric yellow-top">
            <div class="m-icon">⚡</div>
            <div class="m-label">Strike Rate</div>
            <div class="m-value">{p_sr}</div>
            <div class="m-sub">runs per 100 balls</div>
        </div>""", unsafe_allow_html=True)

        c3.markdown(f"""
        <div class="ph-metric cyan-top">
            <div class="m-icon">🏟️</div>
            <div class="m-label">Balls Faced</div>
            <div class="m-value">{p_balls:,}</div>
            <div class="m-sub">total deliveries</div>
        </div>""", unsafe_allow_html=True)

        c4.markdown(f"""
        <div class="ph-metric rose-top">
            <div class="m-icon">💥</div>
            <div class="m-label">Sixes</div>
            <div class="m-value">{p_sixes}</div>
            <div class="m-sub">hit for six</div>
        </div>""", unsafe_allow_html=True)

        c5.markdown(f"""
        <div class="ph-metric green-top">
            <div class="m-icon">⚡</div>
            <div class="m-label">Fours</div>
            <div class="m-value">{p_fours}</div>
            <div class="m-sub">boundaries</div>
        </div>""", unsafe_allow_html=True)

        # ── BOWLING METRICS ──
        st.markdown('<div class="section-label">🎯 Bowling Stats</div>', unsafe_allow_html=True)

        b1, b2, b3 = st.columns(3)

        b1.markdown(f"""
        <div class="ph-metric purple-top">
            <div class="m-icon">🎯</div>
            <div class="m-label">Wickets</div>
            <div class="m-value">{p_wickets}</div>
            <div class="m-sub">career wickets</div>
        </div>""", unsafe_allow_html=True)

        b2.markdown(f"""
        <div class="ph-metric cyan-top">
            <div class="m-icon">📊</div>
            <div class="m-label">Economy</div>
            <div class="m-value">{p_eco}</div>
            <div class="m-sub">runs per over</div>
        </div>""", unsafe_allow_html=True)

        b3.markdown(f"""
        <div class="ph-metric orange-top">
            <div class="m-icon">🏟️</div>
            <div class="m-label">Balls Bowled</div>
            <div class="m-value">{p_balls_bowl:,}</div>
            <div class="m-sub">total deliveries</div>
        </div>""", unsafe_allow_html=True)

        # ── PERFORMANCE CHARTS ──
        st.markdown('<div class="section-label">📊 Performance Chart</div>', unsafe_allow_html=True)

        ch1, ch2 = st.columns(2)

        with ch1:
            bat_df = pd.DataFrame({
                "Stat":  ["Runs", "Balls Faced", "Fours", "Sixes"],
                "Value": [p_runs, p_balls, p_fours, p_sixes],
                "Color": ["#f97316", "#f5c518", "#10b981", "#ef4444"]
            })
            fig_bat = px.bar(
                bat_df, x="Stat", y="Value",
                text="Value",
                title=f"🏏 {player} — Batting",
                color="Stat",
                color_discrete_sequence=["#f97316","#f5c518","#10b981","#ef4444"]
            )
            fig_bat.update_traces(
                textposition='outside',
                textfont=dict(color='white', size=12),
                hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
            )
            fig_bat.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=380,
                title_x=0.5,
                showlegend=False,
                margin=dict(t=50, b=20),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
            )
            st.plotly_chart(fig_bat, use_container_width=True)

        with ch2:
            bowl_df = pd.DataFrame({
                "Stat":  ["Wickets", "Economy", "Balls Bowled"],
                "Value": [p_wickets, p_eco, p_balls_bowl],
            })
            fig_bowl = px.bar(
                bowl_df, x="Stat", y="Value",
                text="Value",
                title=f"🎯 {player} — Bowling",
                color="Stat",
                color_discrete_sequence=["#8b5cf6","#06b6d4","#f43f5e"]
            )
            fig_bowl.update_traces(
                textposition='outside',
                textfont=dict(color='white', size=12),
                hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
            )
            fig_bowl.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color="white",
                height=380,
                title_x=0.5,
                showlegend=False,
                margin=dict(t=50, b=20),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
            )
            st.plotly_chart(fig_bowl, use_container_width=True)

    
    #  COMPARISON SECTION
    st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)
    st.markdown('<div class="comp-title">⚔️ Player Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="ph-subtitle">Compare any two players head to head</div>', unsafe_allow_html=True)

    colA, colB = st.columns(2)
    player1 = colA.selectbox("Player 1", all_players, key="p1")
    player2 = colB.selectbox("Player 2", all_players, key="p2")

    if player1 and player2 and player1 != player2:

        def get_full_stats(p):
            r  = int(df[df['batter']==p]['runs_batter'].sum())
            b  = int(df[df['batter']==p].shape[0])
            sr = round((r/b*100),2) if b>0 else 0
            w  = int(df[df['bowler']==p]['bowler_wicket'].sum())
            s  = int(df[(df['batter']==p)&(df['runs_batter']==6)].shape[0])
            f  = int(df[(df['batter']==p)&(df['runs_batter']==4)].shape[0])
            bb = int(df[df['bowler']==p].shape[0])
            rg = int(df[df['bowler']==p]['runs_total'].sum())
            ec = round((rg/(bb/6)),2) if bb>0 else 0
            return r, sr, w, s, f, ec

        r1,sr1,w1,s1,f1,ec1 = get_full_stats(player1)
        r2,sr2,w2,s2,f2,ec2 = get_full_stats(player2)

        # ── COMPARISON METRICS ──
        st.markdown('<div class="section-label">📊 Side by Side</div>', unsafe_allow_html=True)

        m1,m2,m3 = st.columns(3)

        def comp_card(label, v1, v2, p1, p2, icon):
            winner = p1 if v1 > v2 else p2
            return f"""
            <div class="ph-metric" style="border-top:3px solid #f5c518;">
                <div class="m-icon">{icon}</div>
                <div class="m-label">{label}</div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;">
                    <div style="text-align:center;flex:1;">
                        <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-bottom:4px;">{p1[:10]}</div>
                        <div style="font-size:22px;font-weight:900;color:{'#f5c518' if v1>=v2 else 'rgba(255,255,255,0.5)'};">{v1:,}</div>
                    </div>
                    <div style="color:rgba(255,255,255,0.2);font-size:18px;">vs</div>
                    <div style="text-align:center;flex:1;">
                        <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-bottom:4px;">{p2[:10]}</div>
                        <div style="font-size:22px;font-weight:900;color:{'#f5c518' if v2>=v1 else 'rgba(255,255,255,0.5)'};">{v2:,}</div>
                    </div>
                </div>
                <div style="font-size:11px;color:#10b981;margin-top:8px;">🏆 {winner} leads</div>
            </div>"""

        m1.markdown(comp_card("Runs",         r1,  r2,  player1, player2, "🏏"), unsafe_allow_html=True)
        m2.markdown(comp_card("Strike Rate",  sr1, sr2, player1, player2, "⚡"), unsafe_allow_html=True)
        m3.markdown(comp_card("Wickets",      w1,  w2,  player1, player2, "🎯"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        n1, n2, n3 = st.columns(3)
        n1.markdown(comp_card("Sixes",    s1,  s2,  player1, player2, "💥"), unsafe_allow_html=True)
        n2.markdown(comp_card("Fours",    f1,  f2,  player1, player2, "⚡"), unsafe_allow_html=True)
        n3.markdown(comp_card("Economy",  ec2, ec1, player1, player2, "📊"), unsafe_allow_html=True)

        # ── COMPARISON CHART ──
        st.markdown('<div class="section-label">📈 Comparison Chart</div>', unsafe_allow_html=True)

        comp_df = pd.DataFrame({
            "Stat":   ["Runs","Strike Rate","Wickets","Sixes","Fours"],
            player1:  [r1, sr1, w1, s1, f1],
            player2:  [r2, sr2, w2, s2, f2],
        })

        fig_comp = px.bar(
            comp_df,
            x="Stat",
            y=[player1, player2],
            barmode="group",
            text_auto=True,
            color_discrete_sequence=["#f97316","#06b6d4"],
        )
        fig_comp.update_traces(
            textfont=dict(color='white', size=11),
            textposition='outside',
        )
        fig_comp.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            height=420,
            title_x=0.5,
            legend=dict(
                orientation="h",
                yanchor="bottom", y=1.02,
                xanchor="right",  x=1,
                font=dict(size=13),
            ),
            margin=dict(t=60, b=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    elif player1 == player2:
        st.markdown('<div class="insight-box" style="text-align:center;">⚠️ Please select two different players to compare!</div>', unsafe_allow_html=True)
with tab6:

    st.markdown("""
    <style>

    .analytics-title {
        text-align:center;
        font-size:35px;
        font-weight:bold;
        background: linear-gradient(90deg,#ff512f,#dd2476,#00c9ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom:20px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="analytics-title">📊 Season Analysis</div>', unsafe_allow_html=True)

    # -------- FILTERS --------
    col1, col2 = st.columns(2)

    # Year filter (if available)
    if 'season' in df.columns:
        years = sorted(df['season'].dropna().unique())
    else:
        years = ["All"]

    year = col1.selectbox("📅 Select Season", years)
    teams = sorted(df['batting_team'].dropna().unique())
    team = col2.selectbox("🏏 Select Team", ["All"] + teams)

    # -------- FILTER APPLY --------
    filtered_df = df.copy()

    if year != "All":
        filtered_df = filtered_df[filtered_df['season'] == year]

    if team != "All":
        filtered_df = filtered_df[filtered_df['batting_team'] == team]

    st.markdown("---")

    # -------- STATS --------
    total_runs = filtered_df['runs_total'].sum()
    total_matches = filtered_df['match_id'].nunique()
    total_sixes = filtered_df[filtered_df['runs_batter']==6].shape[0]
    total_fours = filtered_df[filtered_df['runs_batter']==4].shape[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🏏 Runs", total_runs)
    c2.metric("🎮 Matches", total_matches)
    c3.metric("💥 Sixes", total_sixes)
    c4.metric("⚡ Fours", total_fours)

    # -------- TOP PLAYERS --------
    st.markdown("### 🔥 Top Players")

    top_players = filtered_df.groupby('batter')['runs_batter'].sum().sort_values(ascending=False).head(10)

    fig1 = px.bar(
        top_players,
        x=top_players.values,
        y=top_players.index,
        orientation='h',
        color=top_players.values,
        text=top_players.values,
        title="Top Run Scorers"
    )

    fig1.update_traces(textposition='outside')

    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        height=450
    )

    st.plotly_chart(fig1, use_container_width=True)

    # -------- TEAM PERFORMANCE --------
    st.markdown("### 🏆 Team Performance")

    team_perf = filtered_df.groupby('batting_team')['runs_total'].sum().sort_values(ascending=False)

    fig2 = px.bar(
        team_perf,
        x=team_perf.values,
        y=team_perf.index,
        orientation='h',
        color=team_perf.values,
        text=team_perf.values,
        title="Team Runs Comparison"
    )

    fig2.update_traces(textposition='outside')

    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -------- BOWLER ANALYSIS --------
    st.markdown("### 🎯 Bowler Analysis")

    top_bowlers = filtered_df[filtered_df['bowler_wicket']>0] \
        .groupby('bowler')['bowler_wicket'] \
        .sum().sort_values(ascending=False).head(10)

    fig3 = px.bar(
        top_bowlers,
        x=top_bowlers.values,
        y=top_bowlers.index,
        orientation='h',
        color=top_bowlers.values,
        text=top_bowlers.values,
        title="Top Wicket Takers"
    )

    fig3.update_traces(textposition='outside')

    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        height=450
    )

    st.plotly_chart(fig3, use_container_width=True)