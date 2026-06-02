import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def gerar_dados_ecommerce():
    np.random.seed(42)
    n_vendas = 500
    
    # 1. Base de produtos com inconsistências textuais propositais (Moda Consciente/Minimalista)
    produtos_brutos = [
        "Camisa de Linho Orgânico - Bege", "camisa linho bege MINI", "CAMISA LINHO BEGE",
        "Calça Alfaiataria Minimalista", "calca alfaiataria preta", "CALÇA ALFAIATARIA PRETA",
        "Vestido Midi Algodão Sustentável", "vestido midi algodao", "VESTIDO SUSTENTAVEL MIDI",
        "Blazer Vintage Marrom Sépia", "blazer vintage marrom", "BLAZER SEPIA VINTAGE",
        "Tênis Vegano Casual Branco", "tenis vegano branco", "TENIS CASUAL VEGANO"
    ]
    
    precos_base = [189.90, 249.90, 299.90, 389.90, 279.90]
    
    data_vendas = []
    
    # Gerando dados aleatórios, mas com problemas estruturais
    for i in range(n_vendas):
        prod = np.random.choice(produtos_brutos)
        idx_preco = produtos_brutos.index(prod) // 3
        preco = precos_base[idx_preco] + np.random.uniform(-20, 20)
        
        # Inserindo Outliers Propositais (Erros de digitação do sistema antigo)
        if i in [15, 120, 345]:
            preco = 9999.00  # Preço bizarro
        # Inserindo Valores Ausentes (Missing Data)
        elif i in [50, 210, 415]:
            preco = np.nan
            
        # Datas em formatos inconsistentes
        data_base = datetime(2026, 1, 1) + timedelta(days=int(np.random.randint(0, 120)))
        if i % 10 == 0:
            data_str = data_base.strftime("%d/%m/%Y")
        elif i % 10 == 1:
            data_str = data_base.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data_str = data_base.strftime("%Y-%m-%d")
            
        # IDs de clientes com alguns nulos
        cliente_id = f"CLI-{np.random.randint(1000, 1050)}"
        if i in [88, 199, 444]:
            cliente_id = np.nan
            
        data_vendas.append({
            "id_transacao": f"TRX-{10000 + i}",
            "data_venda": data_str,
            "id_cliente": cliente_id,
            "produto_bruto": prod,
            "preco_venda": preco,
            "quantidade": int(np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1]))
        })
        
    df = pd.DataFrame(data_vendas)
    
    # Garante que a pasta 'data' existe
    os.makedirs("data", exist_ok=True)
    
    # Salva o arquivo bruto
    df.to_csv("data/ecommerce_raw_data.csv", index=False, encoding="utf-8")
    print("✨ Arquivo 'data/ecommerce_raw_data.csv' gerado com sucesso!")
    print(f"📊 Total de linhas geradas: {len(df)}")

if __name__ == "__main__":
    gerar_dados_ecommerce()