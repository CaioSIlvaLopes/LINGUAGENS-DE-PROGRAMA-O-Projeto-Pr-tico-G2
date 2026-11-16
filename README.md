# Dinâmica Histórica de Roubos de Veículos no Município do Rio de Janeiro (2003–2022)

![Python](https://img.shields.io/badge/Python-3.11-38bdf8?style=flat-square&logo=python)
![FAIR](https://img.shields.io/badge/Princ%C3%ADpios-FAIR%20Compliant-f97316?style=flat-square)
![License](https://img.shields.io/badge/Licen%C3%A7a-MIT%20%2F%20CC--BY%204.0-38bdf8?style=flat-square)
![Status](https://img.shields.io/badge/Projeto%20Final-LP6%20%28G2%29-f97316?style=flat-square)

**Autor:** Caio Silva Lopes  
**Curso:** Bacharelado em Sistemas de Informação — 6º Período  
**Disciplina:** Linguagem de Programação (Análise e Visualização de Dados com Python)  
**Repositório Oficial:** [https://github.com/CaioSIlvaLopes/LINGUAGENS-DE-PROGRAMA-O-Projeto-Pr-tico-G2.git](https://github.com/CaioSIlvaLopes/LINGUAGENS-DE-PROGRAMA-O-Projeto-Pr-tico-G2.git)  
**Artigo Científico (GitHub Pages):** [https://caiosilvalopes.github.io/LINGUAGENS-DE-PROGRAMA-O-Projeto-Pr-tico-G2/](https://caiosilvalopes.github.io/LINGUAGENS-DE-PROGRAMA-O-Projeto-Pr-tico-G2/)

---

## 1. Resumo Executivo

Este repositório reúne o pipeline determinístico de Engenharia de Dados, a Análise Exploratória de Dados (EDA) e o artigo acadêmico interativo sobre a série histórica de **incidências de roubo de veículos no Município do Rio de Janeiro (MRJ)** durante o **1º quadrimestre (janeiro a abril)** entre **2003 e 2022**.

Os dados brutos provêm da **Tabela 2306** do portal **DATA.RIO** (Instituto Pereira Passos — IPP), consolidados a partir dos Registros de Ocorrência (RO) do **Instituto de Segurança Pública do Estado do Rio de Janeiro (ISP-RJ)**.

* **Fonte Primária Perene:** [Portal ISP Dados Abertos](http://www.ispdados.rj.gov.br/) / [DATA.RIO](https://www.data.rio/)
* **Palavras-chave Indexadoras:** Segurança Pública; Roubo de Veículos; Rio de Janeiro; Ciência Aberta; Princípios FAIR; Análise de Séries Temporais; Python.

---

## 2. Principais Indicadores Estatísticos (2003–2022)

| Variável | Contagem (N) | Média | Mediana | Mínimo | Máximo | Desvio Padrão |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Total no 1º Quadrimestre (`total_jan_abr`)** | 20 | 6.216,30 | 5.976,00 | 3.140,00 (2011) | 9.679,00 (2018) | 1.982,21 |
| **Diferença Absoluta Anual (`dif_absoluta`)** | 19 | -223,53 | -160,00 | -2.684,00 (2019) | 2.331,00 (2017) | 1.283,63 |
| **Diferença Percentual Anual (`dif_percentual`)** | 19 | -1,50% | -2,67% | -31,40% (2011) | 37,75% (2014) | 20,77% |
| **População Projetada (`populacao`)** | 20 | 6.391.547,44 | 6.400.913,35 | 5.865.737,42 | 6.802.575,57 | 267.889,48 |
| **Taxa por 100 mil hab. (`taxa_100k`)** | 20 | 97,90 | 95,63 | 49,43 (2011) | 145,90 (2003) | 33,00 |
| **Média Mensal (`media_mensal`)** | 20 | 1.554,08 | 1.494,00 | 785,00 (2011) | 2.419,75 (2018) | 495,55 |

---

## 3. Arquitetura do Repositório (Padrão FAIR)

```text
LINGUAGENS-DE-PROGRAMA-O-Projeto-Pr-tico-G2/
├── README.md                  # Apresentação do projeto, resumo, badges e tutorial de execução
├── LICENSE                    # Licença aberta dupla (MIT para código e CC-BY 4.0 para dados/texto)
├── requirements.txt           # Dependências com versões estritas congeladas (pip freeze)
├── .gitignore                 # Arquivos ignorados (.venv, __pycache__, etc.)
│
├── data/
│   ├── raw/                   # Conjunto de dados bruto original (2306.xls)
│   ├── processed/             # Conjunto de dados tratado (.csv, .csv.gz e .parquet)
│   └── data_dictionary.md     # Metadados e dicionário de variáveis (FAIR Interoperable)
│
├── notebooks/
│   └── analise_exploratoria.ipynb  # Notebook de exploração estatística, ciclos e correlações
│
├── src/
│   ├── __init__.py            # Inicializador do pacote Python
│   └── etl.py                 # Pipeline determinístico de extração, limpeza, validação e carga
│
└── docs/                      # Artigo acadêmico estático publicado via GitHub Pages
    ├── index.html             # Artigo científico completo em HTML5 + Plotly.js
    └── assets/                # Figuras estáticas de alta resolução exportadas
        └── analise_roubo_veiculos_rj.png
```

---

## 4. Tutorial de Reprodução do Ambiente e Pipeline

```bash
# 1. Clonar o repositório
git clone https://github.com/CaioSIlvaLopes/LINGUAGENS-DE-PROGRAMA-O-Projeto-Pr-tico-G2.git
cd LINGUAGENS-DE-PROGRAMA-O-Projeto-Pr-tico-G2

# 2. Criar e ativar o ambiente virtual Python
python -m venv .venv
# No Windows (PowerShell):
.venv\Scripts\Activate.ps1
# No Linux/macOS:
source .venv/bin/activate

# 3. Instalar as dependências congeladas
pip install -r requirements.txt

# 4. Executar o pipeline determinístico de ETL
python src/etl.py
```

---

## 5. Licença e Reuso (FAIR Reusable)

* **Software e Scripts (`src/`, `notebooks/`):** Licenciados sob a **MIT License** — Copyright (c) 2026 **Caio Silva Lopes**.
* **Dados Tratados, Documentação e Artigo (`data/`, `docs/`):** Licenciados sob **Creative Commons Attribution 4.0 International (CC-BY 4.0)**.
