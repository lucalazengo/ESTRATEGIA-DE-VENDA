import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Prospecção - Irrigação",
    page_icon="🌿",
    layout="wide"
)

# Estilo visual
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #f5f5f5;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1.2em;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1em;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.header("Dashboard de Prospecção de Vendas - Irrigação")
st.markdown("Visão geral dos indicadores de performance e tendências.")

# Filtros
col1, col2 = st.columns(2)
with col1:
    categoria = st.selectbox("Selecione a Categoria", ["Todas", "Scoriflex", "Outros"])
with col2:
    periodo = st.date_input("Selecione o Período", [pd.to_datetime("2023-01-01"), pd.to_datetime("2023-10-01")])

# Dados simulados
volume_total = 1365
valor_total = 5000
diferenca_meta = 211
meta = 4800

# Métricas principais
st.markdown("### Métricas Principais")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <strong>Total de Litros Vendidos</strong><br>
        <span style="font-size:2em; color:#2e7d32;">{volume_total:,.0f}</span><br>
        <span style="color:green;">↑ 12,5% vs mês anterior</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <strong>Valor Total de Venda</strong><br>
        <span style="font-size:2em; color:#2e7d32;">R$ {valor_total:,.0f}</span><br>
        <span style="color:red;">↓ 1,2% vs mês anterior</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <strong>Diferença para a Meta</strong><br>
        <span style="font-size:2em; color:#2e7d32;">R$ {diferenca_meta:,.0f}</span><br>
        <span style="color:green;">↑ 50 novos</span>
    </div>
    """, unsafe_allow_html=True)

# Gráfico de barras
st.markdown("### Visualizações Detalhadas")

categorias = ["Scoriflex", "Outro Produto A", "Outro Produto B"]
valores = [2000, 1800, 1200]

fig = go.Figure(go.Bar(
    x=categorias,
    y=valores,
    text=[f"R$ {v:,.0f}" for v in valores],
    textposition='auto',
    marker_color=['#66bb6a', '#42a5f5', '#ffa726']
))

fig.update_layout(
    title="Valor por Categoria",
    xaxis_title="Categoria",
    yaxis_title="Valor (R$)",
    height=400,
    margin=dict(l=0, r=0, t=40, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig, use_container_width=True)