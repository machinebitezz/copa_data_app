# basic libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

pd.set_option("display.max_columns", 100)
pd.set_option("display.max_rows", 200)

# custom palette
colors = ["#66C8D5", "#00478E", "#E1EAA7", "#84A266", "#F25C5C", ]
sns.set_palette(sns.color_palette(colors))

# Times mais fortes
# ====================================================================================== #
df = pd.read_csv('./international_matches.csv', parse_dates=['date'])
fifa_rank = df[['date', 'home_team', 'away_team', 'home_team_fifa_rank', 'away_team_fifa_rank']]
home = fifa_rank[['date', 'home_team', 'home_team_fifa_rank']].rename(
    columns={'home_team': 'team', 'home_team_fifa_rank': 'rank'})
away = fifa_rank[['date', 'away_team', 'away_team_fifa_rank']].rename(
    columns={'away_team': 'team', 'away_team_fifa_rank': 'rank'})
fifa_rank = home.append(away)
fifa_rank = fifa_rank.sort_values(['team', 'date'], ascending=[True, False])
fifa_rank['row_number'] = fifa_rank.groupby('team').cumcount() + 1
fifa_rank_top = fifa_rank[fifa_rank['row_number'] == 1].drop('row_number', axis=1).nsmallest(5, 'rank')

# Times mais ofensivos
# ====================================================================================== #
offense = df[['date', 'home_team', 'away_team', 'home_team_mean_offense_score', 'away_team_mean_offense_score']]
home = offense[['date', 'home_team', 'home_team_mean_offense_score']].rename(
    columns={'home_team': 'team', 'home_team_mean_offense_score': 'offense_score'})
away = offense[['date', 'away_team', 'away_team_mean_offense_score']].rename(
    columns={'away_team': 'team', 'away_team_mean_offense_score': 'offense_score'})
offense = home.append(away)
offense = offense.sort_values(['team', 'date'], ascending=[True, False])
offense['row_number'] = offense.groupby('team').cumcount() + 1
offense_top = offense[offense['row_number'] == 1].drop('row_number', axis=1).nlargest(20, 'offense_score')
fig_offense, axes = plt.subplots(1, 1, figsize=(10, 6))
ax = sns.barplot(data=offense_top, y='team', x='offense_score', orientation='horizontal', color="#66C8D5")
ax.set_title('Teams with the strongest offense', fontsize=15)
ax.set(xlabel='', ylabel='')

# Time da casa
# ====================================================================================== #
home_team_advantage = df[df['neutral_location'] == False]['home_team_result'].value_counts(normalize=True)
fig_home_advantage, axes = plt.subplots(1, 1, figsize=(8, 8))
ax = plt.pie(home_team_advantage, labels=['Win', 'Lose', 'Draw'], autopct='%.0f%%')
plt.title('Home team match result', fontsize=15)
# ====================================================================================== #

st.title('Dados da Copa do Mundo 2022')

# Times mais fortes
descricaoPontuacaoFifa = """
A FIFA atualiza o ranking das equipes várias vezes ao ano com base no desempenho da equipe nas partidas. 
Cada equipe recebe um certo número de pontos com base na vitória ou empate, na importância da partida e na força da equipe adversária. 
O número total de pontos determina a classificação da equipe na FIFA.
"""
st.header("Qual será o time mais forte?")
st.markdown(descricaoPontuacaoFifa)
with st.expander("Ver resultado..."):
    st.dataframe(fifa_rank_top)

# Times mais ofensivos
descricaoTimeMaisOfensivo = """
Costuma-se dizer que a posição mais importante no futebol é a de atacante. 
Sem o atacante, o time faria menos gols o que reduz as chances do time vencer a partida. 
Qual time tem o ataque mais forte?
"""
st.header("Qual o time mais ofensivo?")
st.markdown(descricaoTimeMaisOfensivo)
with st.expander("Ver resultado..."):
    st.pyplot(fig_offense)

# Jogador de casa tem mais chances de ganhar?
descricaoTimeDaCasa = """
Outra sabedoria do povo em relação ao futebol é que o time da casa tem mais chances de ganhar.
Vamos verificar essa afirmativa com base em dados
"""
st.header("O time da casa tem mais chances de ganhar?")
st.markdown(descricaoTimeDaCasa)
with st.expander("Ver resultado..."):
    st.pyplot(fig_home_advantage)
