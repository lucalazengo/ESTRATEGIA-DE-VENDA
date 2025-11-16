import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(
    page_title="Estratégia de Vendas",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Título Principal ---
st.title("🌱 Estratégia de Vendas Clientes EIB")
st.markdown("Calcule o volume e o valor estimado de venda de produtos como o **Scoriflex** de forma interativa e visual.")

# Inicializar histórico na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# --- Cores do Tema (para os gráficos) ---
# Vamos definir as cores do nosso tema para usar nos gráficos
# Cor de fundo dos containers e gráficos
cor_fundo_grafico = "#262730"
# Cor principal do tema (verde/teal)
cor_primaria = "#26A69A"
# Cor de texto
cor_texto = "#FAFAFA"


# --- Sidebar com entrada de dados ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento
    st.header("📥 Entrada de Dados")
    produto = st.text_input("Nome do Produto", value="Scoriflex")
    dose = st.number_input("Dose (L/ha)", min_value=0.0, step=0.1, value=2.0)
    area = st.number_input("Área (hectares)", min_value=0.0, step=0.1, value=50.0)
    preco = st.number_input("Preço por litro (R$)", min_value=0.0, step=0.01, value=25.0)
    meta_venda = st.number_input("Meta de Venda (R$)", min_value=0.0, step=100.0, value=5000.0)
    
    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento
    calcular = st.button("🔍 Calcular Prospecção", use_container_width=True)

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
    
    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento

    # --- Métricas em Contêineres (Estilo da Imagem) ---
    col1, col2, col3 = st.columns(3, gap="medium") # <--- MUDANÇA: Adicionado gap

    with col1:
        with st.container(border=True): # <--- MUDANÇA: Adicionado container
            st.metric("📦 Volume Total (L)", f"{volume_total:,.2f} L")

    with col2:
        with st.container(border=True): # <--- MUDANÇA: Adicionado container
            st.metric("💰 Valor da Venda (R$)", f"R$ {valor_venda:,.2f}")

    with col3:
        with st.container(border=True): # <--- MUDANÇA: Adicionado container
            diferenca = valor_venda - meta_venda
            # <--- MUDANÇA: Lógica do delta_color corrigida
            cor_delta = "normal" if diferenca >= 0 else "inverse" 
            st.metric(
                "🎯 Diferença para a Meta", 
                f"R$ {diferenca:,.2f}", 
                delta=f"{diferenca:,.2f}", 
                delta_color=cor_delta
            )
            
    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento
    st.markdown("---") # Linha divisória
    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento

    # --- Gráficos (Estilizados para Tema Escuro) ---
    st.subheader("📊 Visualizações")

    # Gráfico 1: Pizza com volume
    fig1 = go.Figure(go.Pie(
        labels=['Área (ha)', 'Dose (L/ha)'],
        values=[area, dose],
        hole=0.4,
        marker_colors=[cor_primaria, '#507DBC'], # Usando a cor primária do tema
        textfont_color=cor_texto
    ))
    fig1.update_layout(
        title="Relação Área × Dose",
        height=300,
        # <--- MUDANÇAS PARA O TEMA ESCURO ---
        paper_bgcolor=cor_fundo_grafico,
        plot_bgcolor=cor_fundo_grafico,
        font_color=cor_texto,
        showlegend=True
    )
    
    # Gráfico 2: Barra com valor vs meta
    fig2 = go.Figure(go.Bar(
        x=['Valor da Venda', 'Meta de Venda'],
        y=[valor_venda, meta_venda],
        marker_color=[cor_primaria, '#E74C3C'], # Usando a cor primária
        text=[f"R$ {valor_venda:,.2f}", f"R$ {meta_venda:,.2f}"],
        textposition='auto',
        textfont_color=cor_texto
    ))
    fig2.update_layout(
        title="Comparação entre Valor de Venda e Meta",
        xaxis_title="Categoria",
        yaxis_title="Valor (R$)",
        height=400,
        # <--- MUDANÇAS PARA O TEMA ESCURO ---
        paper_bgcolor=cor_fundo_grafico,
        plot_bgcolor=cor_fundo_grafico,
        font_color=cor_texto,
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'), # Linhas de grade sutis
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
    )
    
    # Exibindo gráficos em colunas
    col_g1, col_g2 = st.columns(2, gap="medium")
    with col_g1:
        st.plotly_chart(fig1, use_container_width=True)
    with col_g2:
        st.plotly_chart(fig2, use_container_width=True)

    # Download
    st.download_button(
        label="📥 Baixar Resultado",
        data=f"Produto: {produto}\nVolume Total: {volume_total:.2f} L\nValor da Venda: R$ {valor_venda:.2f}",
        file_name=f"prospeccao_{produto.lower().replace(' ', '_')}.txt",
        mime="text/plain"
    )