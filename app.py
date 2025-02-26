import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Configuração da página
st.set_page_config(page_title="Análise de Questões", layout="wide")
st.title("Gráfico de Donut - Distribuição de Respostas por Questão")

# Criação do DataFrame com os dados fornecidos
data = {
    'Questão': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 
                6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10,
                11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14,
                15, 15, 15, 15, 15],
    'Alternativa': ['A', 'B', 'C', 'D', 'E', 'A', 'B', 'C', 'D', 'E', 'A', 'B', 'C', 'D', 'E',
                    'A', 'B', 'C', 'D', 'E', 'A', 'B', 'C', 'D', 'E', 'A', 'B', 'C', 'D', 'E',
                    'A', 'B', 'C', 'D', 'E', 'A', 'B', 'C', 'D', 'E', 'A', 'B', 'C', 'D', 'E',
                    'A', 'B', 'C', 'D', 'E', 'A', 'B', 'C', 'D', 'E', 'A', 'B', 'C', 'D', 'E',
                    'A', 'B', 'C', 'D', 'E', 'A', 'B', 'C', 'D', 'E', 'A', 'B', 'C', 'D', 'E'],
    'Valor': [68, 1, 24, 3, 4, 4, 28, 3, 59, 6, 72, 3, 24, 0, 1, 10, 41, 7, 24, 16, 7, 1, 3, 1, 85,
             10, 18, 68, 4, 0, 49, 6, 1, 22, 22, 21, 74, 3, 0, 3, 6, 79, 7, 3, 4, 9, 16, 16, 51, 7,
             21, 69, 0, 9, 1, 4, 68, 4, 12, 12, 84, 10, 1, 1, 3, 1, 19, 3, 0, 76, 1, 0, 93, 0, 6]
}

df = pd.DataFrame(data)

# Criar um seletor para escolher a questão
questoes_disponiveis = sorted(df['Questão'].unique())
questao_selecionada = st.selectbox("Selecione a Questão:", questoes_disponiveis)

# Filtrar dados para a questão selecionada
filtered_df = df[df['Questão'] == questao_selecionada]

# Criar o gráfico de donut
col1, col2 = st.columns([2, 1])

with col1:
    # Calcular o total para a questão selecionada
    total_respostas = filtered_df['Valor'].sum()
    
    fig = go.Figure(data=[go.Pie(
        labels=filtered_df['Alternativa'],
        values=filtered_df['Valor'],
        hole=0.4,
        marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    )])
    
    fig.update_layout(
        title_text=f"Distribuição de Respostas - Questão {questao_selecionada}",
        annotations=[dict(text=f'Total: {total_respostas}', x=0.5, y=0.5, font_size=20, showarrow=False)],
        legend_title="Alternativas",
        height=500,
        width=600
    )
    
    st.plotly_chart(fig)

with col2:
    # Tabela com os valores e percentuais
    filtered_df['Percentual (%)'] = (filtered_df['Valor'] / total_respostas * 100).round(1)
    st.subheader("Resumo dos Dados")
    st.dataframe(filtered_df[['Alternativa',  'Percentual (%)']], width=400)
    
    # Adicionar informações estatísticas
    alternativa_maior_valor = filtered_df.loc[filtered_df['Valor'].idxmax(), 'Alternativa']
    maior_valor = filtered_df['Valor'].max()
    maior_percentual = (maior_valor / total_respostas * 100).round(1)
    
    st.subheader("Informações Adicionais")
    st.write(f"Alternativa mais escolhida: **{alternativa_maior_valor}** ({maior_percentual}%)")
    st.write(f"Total de respostas: **{total_respostas}**")

# Adicionar gráfico de barras comparativo
st.subheader("Comparação entre Alternativas")
fig_bar = go.Figure(data=[
    go.Bar(
        x=filtered_df['Alternativa'],
        y=filtered_df['Valor'],
        marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
        text=filtered_df['Valor'],
        textposition='auto'
    )
])

fig_bar.update_layout(
    xaxis_title="Alternativa",
    yaxis_title="Quantidade de Respostas",
    height=400
)

st.plotly_chart(fig_bar)

