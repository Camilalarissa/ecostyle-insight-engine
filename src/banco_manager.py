import sqlite3
import pandas as pd
import os

def criar_e_povoar_banco():
    print("Iniciando o provisionamento do Banco de Dados SQL...")
    
    # 1. Conectar ao arquivo de banco de dados 
    conexao = sqlite3.connect("database/ecostyle_vendas.db")
    cursor = conexao.cursor()
    
    # 2. Criar a tabela de vendas estruturada (DDL)
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas_df (
            id_transacao TEXT PRIMARY KEY,
            data_venda TEXT NOT NULL,
            id_cliente TEXT NOT NULL,
            produto_bruto TEXT,
            preco_venda REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            produto_limpo TEXT NOT NULL,
            faturamento REAL NOT NULL
        )
    ''')
    conexao.commit()
    print("✅ Tabela 'vendas_df' criada com sucesso no esquema relacional.")
    
    # 3. Carregar os dados limpos do CSV usando Pandas para jogar no SQL
    df_limpo = pd.read_csv("data/ecommerce_cleaned_data.csv")
    
    # Inserir os registros no banco de dados
    # 'if_exists=replace' reconstrói a carga caso você rode o script mais de uma vez
    df_limpo.to_sql("vendas_df", conexao, if_exists="replace", index=False)
    conexao.commit()
    
    # 4. Teste de Validação Teórica (Verificando a consistência por query SQL)
    cursor.execute("SELECT COUNT(*), SUM(faturamento) FROM vendas_df")
    total_linhas, faturamento_total = cursor.fetchone()
    
    print("Carga de dados concluída!")
    print(f"Registros migrados para o SQL: {total_linhas}")
    print(f"Faturamento total consolidado no banco: R$ {faturamento_total:,.2f}")
    
    conexao.close()

if __name__ == "__main__":
    criar_e_povoar_banco()