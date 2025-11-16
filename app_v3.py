import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Prospecção de Vendas - Irrigação",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🌱 Prospecção de Vendas de Produtos de Irrigação")
st.markdown("Calcule o volume e o valor estimado de venda de produtos como o **Scoriflex** de forma interativa e visual.")

# Inicializar histórico na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# Sidebar com entrada de dados
with st.sidebar:
    st.header("📥 Entrada de Dados")
    produto = st.text_input("Nome do Produto", value="Scoriflex")
    dose = st.number_input("Dose (L/ha)", min_value=0.0, step=0.1, value=2.0)
    area = st.number_input("Área (hectares)", min_value=0.0, step=0.1, value=50.0)
    preco = st.number_input("Preço por litro (R$)", min_value=0.0, step=0.01, value=25.0)
    meta_venda = st.number_input("Meta de Venda (R$)", min_value=0.0, step=100.0, value=5000.0)

    calcular = st.button("🔍 Calcular Prospecção")

# Cálculo
if calcular:
    volume_total = dose * area
    valor_venda = volume_total * preco
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Armazenar no histórico
    st.session_state.historico.append({
        "Produto": produto,
        "Volume (L)": f"{volume_total:.2f}",
        "Valor (R$)": f"R$ {valor_venda:.2f}",
        "Data/Hora": data_hora
    })

    # Colunas de resultado
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📦 Volume Total (L)", f"{volume_total:,.2f} L")

    with col2:
        st.metric("💰 Valor da Venda (R$)", f"R$ {valor_venda:,.2f}")

    with col3:
        diferenca = valor_venda - meta_venda
        cor = "green" if diferenca >= 0 else "red"
        st.metric("🎯 Diferença para a Meta", f"R$ {diferenca:,.2f}", delta=f"{diferenca:,.2f}", delta_color="normal")

    # Gráficos
    st.subheader("📊 Visualizações")

    # Gráfico 1: Pizza com volume
    fig1 = go.Figure(go.Pie(
        labels=['Área (ha)', 'Dose (L/ha)'],
        values=[area, dose],
        hole=0.4,
        marker_colors=['#27ae60', '#3498db'],
        title="Relação Área × Dose"
    ))
    fig1.update_layout(height=300)
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Barra com valor vs meta
    fig2 = go.Figure(go.Bar(
        x=['Valor da Venda', 'Meta de Venda'],
        y=[valor_venda, meta_venda],
        marker_color=['#2ecc71', '#e74c3c'],
        text=[f"R$ {valor_venda:,.2f}", f"R$ {meta_venda:,.2f}"],
        textposition='auto'
    ))
    fig2.update_layout(
        title="Comparação entre Valor de Venda e Meta",
        xaxis_title="Categoria",
        yaxis_title="Valor (R$)",
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Download
    st.download_button(
        label="📥 Baixar Resultado",
        data=f"Produto: {produto}\nVolume Total: {volume_total:.2f} L\nValor da Venda: R$ {valor_venda:.2f}",
        file_name=f"prospeccao_{produto.lower().replace(' ', '_')}.txt",
        mime="text/plain"
    )

# Histórico de simulações
if st.session_state.historico:
    st.subheader("📜 Histórico de Simulações")
    df_hist = pd.DataFrame(st.session_state.historico)
    st.dataframe(df_hist, use_container_width=True)