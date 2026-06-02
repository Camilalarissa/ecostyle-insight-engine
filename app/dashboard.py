import subprocess
import sys


try:
    import google.genai
    import streamlit
except ImportError:
    
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "google-genai", "python-dotenv", "pandas", "numpy"])

import streamlit as st
import pandas as pd
import sqlite3
import os
from google import genai
from dotenv import load_dotenv

#  chave do arquivo .env
load_dotenv()

#  estética da página
st.set_page_config(page_title="EcoStyle Analytics", page_icon="📊", layout="wide")

# paleta minimalista 
st.markdown("""
    <style>
    .reportview-container { background: #F5F1E6; }
    h1, h2, h3 { color: #704214; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #704214; color: white; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

st.title(" EcoStyle Intelligent Analytics & Insight Engine")
st.markdown("---")

# 1. Banco SQL 
def carregar_dados_sql():
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(caminho_atual, "..", "database", "ecostyle_vendas.db")
    
    conexao = sqlite3.connect(caminho_banco)
    
    # Query agregando faturamento por produto limpo
    query_produtos = """
        SELECT produto_limpo, SUM(quantidade) as total_vendas, SUM(faturamento) as faturamento_total 
        FROM vendas_df 
        GROUP BY produto_limpo 
        ORDER BY faturamento_total DESC
    """
    df_produtos = pd.read_sql_query(query_produtos, conexao)
    
    # Query geral para métricas globais
    df_geral = pd.read_sql_query("SELECT * FROM vendas_df", conexao)
    conexao.close()
    return df_produtos, df_geral

# Chamada da função totalmente encostada na margem esquerda (fora do escopo da função)
df_produtos, df_geral = carregar_dados_sql()

# KPIs Principais (Indicadores de Performance)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(" Faturamento Bruto", f"R$ {df_geral['faturamento'].sum():,.2f}")
with col2:
    st.metric("Peças Comercializadas", f"{df_geral['quantidade'].sum()} un")
with col3:
    st.metric("Ticket Médio por Venda", f"R$ {df_geral['preco_venda'].mean():,.2f}")

st.markdown("### Performance de Linhas de Produto (Moda Consciente)")

# Exibição de gráficos nativos do Streamlit
st.bar_chart(data=df_produtos.set_index('produto_limpo')['faturamento_total'])

st.markdown("---")
st.markdown("###  Insight Engine: Diagnóstico Estratégico via IA Generativa")

# 3. Integração com a API do Gemini para atuar como Analista de Negócios
if st.button("Gerar Relatório de Insights com Gemini 2.5 Flash"):
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.warning("⚠️ Chave de API não encontrada no arquivo .env. Configure para habilitar a IA.")
    else:
        with st.spinner("Analisando métricas de estoque e vendas em tempo real..."):
            try:
                # Prepara um resumo textual do banco de dados para enviar para a IA contextualizar
                resumo_metricas = df_produtos.to_string(index=False)
                
                # Inicializa o cliente usando a nova biblioteca oficial do Google GenAI
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                Atue como um Consultor de Negócios Sênior especialista em E-commerce de Moda Consciente e Minimalista.
                Analise os dados de faturamento reais gerados pelo nosso banco SQL abaixo:
                
                {resumo_metricas}
                
                Gere um relatório executivo curto, dividido em 3 tópicos:
                1. Desempenho Crítico (O que está vendendo mais e o que está estagnado).
                2. Sugestão de precificação ou marketing com base no nicho sustentável.
                3. Uma ação estratégica recomendada para alavancar o faturamento.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                # Exibe o feedback da IA na tela formatado em Markdown limpo
                st.markdown("#### Relatório Estratégico Gerado:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Erro ao se comunicar com o Gemini: {e}")