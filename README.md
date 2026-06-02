# EcoStyle Intelligent Analytics & Insight Engine

Um pipeline completo de Engenharia e Análise de Dados desenvolvido para processar, limpar e extrair insights estratégicos de um e-commerce focado em moda consciente e minimalista.

Este projeto demonstra a aplicação prática de extração de dados, tratamento estatístico, modelagem relacional em SQL e a construção de um dashboard interativo integrado com Inteligência Artificial Generativa.

## Arquitetura e Funcionalidades

O sistema foi construído em etapas modulares, simulando um ambiente corporativo real:

1. **Geração e Ingestão de Dados (`gerador_dados_brutos.py`):** Criação de uma base de dados bruta simulando transações de e-commerce com ruídos e inconsistências intencionais.
2. **Data Cleaning e Engenharia de Features (`data_cleaner.py`):** - Tratamento de valores nulos (imputação pela mediana).
   - Padronização textual e semântica de strings.
   - Tratamento estatístico de _outliers_ utilizando o método de Amplitude Interquartílica (IQR).
3. **Modelagem Relacional (`banco_manager.py`):** Criação e provisionamento de um banco de dados SQLite (`.db`), garantindo integridade e estruturação via tabelas SQL.
4. **Visualização Analítica (`app/dashboard.py`):** Um dashboard interativo com design minimalista construído em Streamlit, exibindo KPIs de faturamento e performance de produtos.
5. **Insight Engine Integrado (IA):** Conexão via API com o modelo **Gemini 2.5 Flash** do Google, atuando como um consultor de negócios autônomo para gerar relatórios estratégicos com base nos dados do banco SQL.

## Tecnologias Utilizadas

- **Linguagem:** Python
- **Manipulação de Dados:** Pandas, NumPy
- **Banco de Dados:** SQLite3 (Linguagem SQL)
- **Interface Visual:** Streamlit
- **Inteligência Artificial:** Google GenAI SDK (Gemini API)
- **Ambiente e Segurança:** `venv`, `python-dotenv`

## Como Executar o Projeto Localmente

**1. Clone o repositório e acesse a pasta:**

```bash
git clone [https://github.com/Camilalarissa/ecostyle-insight-engine.git](https://https://github.com/Camilalarissa/ecostyle-insight-engine.git)
cd ecostyle-insight-engine
```
