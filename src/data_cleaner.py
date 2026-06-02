import pandas as pd
import numpy as np
import os

def limpar_dados_ecommerce():
    print(" Iniciando o pipeline de tratamento e correção de dados...")
    
    # 1. Carregar os dados brutos
    df = pd.read_csv("data/ecommerce_raw_data.csv")
    print(f" Dados originais carregados: {len(df)} registros.")
    
    # ----------------------------------------------------
    # Tratamento de Valores Ausentes (Missing Data)
    # ----------------------------------------------------
    # IDs de clientes nulos não servem para análise de comportamento. removê-los.
    df = df.dropna(subset=['id_cliente'])
    
    # Preços ausentes (NaN): imputar (preencher) usando a Mediana do preço
    mediana_preco = df['preco_venda'].median()
    df['preco_venda'] = df['preco_venda'].fillna(mediana_preco)
    
    # ----------------------------------------------------
    # Padronização Textual (Inconsistências de String)
    # ----------------------------------------------------
    # normalizar os nomes dos produtos para caixa alta e remover espaços extras
    df['produto_limpo'] = df['produto_bruto'].str.upper().str.strip()
    
    # Correção semântica de sinônimos via mapeamento (Agrupando o que é igual)
    mapeamento_produtos = {
        "CAMISA DE LINHO ORGÂNICO - BEGE": "CAMISA LINHO BEGE",
        "CAMISA LINHO BEGE MINI": "CAMISA LINHO BEGE",
        "CALÇA ALFAIATARIA MINIMALISTA": "CALÇA ALFAIATARIA PRETA",
        "CALCA ALFAIATARIA PRETA": "CALÇA ALFAIATARIA PRETA",
        "VESTIDOMIDI ALGODÃO SUSTENTÁVEL": "VESTIDO MIDI ALGODÃO",
        "VESTIDO MIDI ALGODÃO SUSTENTÁVEL": "VESTIDO MIDI ALGODÃO",
        "VESTIDO MIDI ALGODOAO": "VESTIDO MIDI ALGODÃO",
        "VESTIDO SUSTENTAVEL MIDI": "VESTIDO MIDI ALGODÃO",
        "BLAZER VINTAGE MARROM SÉPIA": "BLAZER VINTAGE MARROM",
        "BLAZER SEPIA VINTAGE": "BLAZER VINTAGE MARROM",
        "TÊNIS VEGANO CASUAL BRANCO": "TÊNIS VEGANO BRANCO",
        "TENIS VEGANO BRANCO": "TÊNIS VEGANO BRANCO",
        "TENIS CASUAL VEGANO": "TÊNIS VEGANO BRANCO"
    }
    # Se o produto estiver no mapeamento, substitui. Se não, mantém o nome atual.
    df['produto_limpo'] = df['produto_limpo'].map(mapeamento_produtos).fillna(df['produto_limpo'])
    
    # ----------------------------------------------------
    #  Tratamento de Datas Heterogêneas
    # ----------------------------------------------------
    # Forçar o Pandas a converter os formatos misturados de data para o padrão datetime
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce', yearfirst=True)
    
    # ----------------------------------------------------
    # Tratamento Estatístico de Outliers (Filtro IQR)
    # ----------------------------------------------------
    # Aplicar a técnica da Amplitude Interquartílica (IQR)
    # para remover os preços absurdos (como o cinto de R$ 9999) de forma estritamente estatística.
    Q1 = df['preco_venda'].quantile(0.25) # Primeiro quartil (25%)
    Q3 = df['preco_venda'].quantile(0.75) # Terceiro quartil (75%)
    IQR = Q3 - Q1                         # Amplitude Interquartílica
    
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    # Filtrando o DataFrame para manter apenas preços dentro dos limites aceitáveis
    df_filtrado = df[(df['preco_venda'] >= limite_inferior) & (df['preco_venda'] <= limite_superior)].copy()
    
    # Criar uma coluna de faturamento bruto
    df_filtrado['faturamento'] = df_filtrado['preco_venda'] * df_filtrado['quantidade']
    
    # ----------------------------------------------------
    #  Exportação dos Dados Consolidados
    # ----------------------------------------------------
    df_filtrado.to_csv("data/ecommerce_cleaned_data.csv", index=False, encoding="utf-8")
    
    print(f" Pipeline concluído com sucesso!")
    print(f"Registros removidos (Outliers/Nulos): {len(df) - len(df_filtrado)}")
    print(f" Dados limpos salvos em 'data/ecommerce_cleaned_data.csv' com {len(df_filtrado)} linhas.")

if __name__ == "__main__":
    limpar_dados_ecommerce()