# Dicionário de Dados e Metadados (FAIR Interoperable)

* **Projeto:** Dinâmica Histórica de Roubos de Veículos no Município do Rio de Janeiro (2003–2022)
* **Autor:** Caio Silva Lopes
* **Curso / Período:** Bacharelado em Sistemas de Informação — 6º Período (Semestre Letivo 2026.2)
* **Disciplina:** Linguagem de Programação (Análise e Visualização de Dados com Python)
* **Fonte Primária Perene:** Instituto de Segurança Pública do Estado do Rio de Janeiro (ISP-RJ) — `http://www.ispdados.rj.gov.br/` (data de referência da extração original: 24/05/2022)
* **Órgão Tabulador:** Instituto Pereira Passos (IPP) — Coordenadoria Técnica de Informações da Cidade (Portal DATA.RIO — Tabela 2306)
* **Artefatos de Dados Persistidos (`data/processed/`):**
  * `data/processed/roubo_veiculos_mrj_2003_2022.csv` (Formato tabular aberto CSV UTF-8)
  * `data/processed/roubo_veiculos_mrj_2003_2022.csv.gz` (Formato comprimido GZIP)
  * `data/processed/roubo_veiculos_mrj_2003_2022.json` (Formato estruturado JSON orientado a registros)
  * `data/processed/definicoes_metadados_isp.txt` (Notas metodológicas extraídas da aba `Definições`)
  * `data/processed/auditoria_etl.json` (Relatório determinístico de validação de integridade do pipeline)

---

## 1. Especificação das Variáveis do Conjunto de Dados Tratado

| Nome da Variável | Rótulo Original (`2306.xls`) | Tipo Primitivo | Formato / Unidade | Domínio / Intervalo Observado | Descrição de Negócio e Fórmula de Cálculo |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `ano` | `Ano (1º quadrimestre)` | `int64` | `AAAA` (Ano civil) | `2003` a `2022` ($N = 20$) | Ano civil de referência correspondente ao acumulado do 1º quadrimestre (janeiro, fevereiro, março e abril). |
| `total_jan_abr` | `Total - Jan-Abr` | `int64` | Contagem inteira (casos) | `3140` a `9679` | Total absoluto de Registros de Ocorrência (RO) de roubo de veículos lavrados pela Polícia Civil no Município do Rio de Janeiro entre janeiro e abril de cada ano. |
| `dif_absoluta` | `Diferença Absoluta` | `float64` | Variação inteira ($\Delta$ casos) | `-2684.0` a `2331.0` (`NaN` em 2003) | Diferença absoluta em relação ao 1º quadrimestre do ano anterior: $$\Delta_{\text{abs}, t} = \text{total\_jan\_abr}_t - \text{total\_jan\_abr}_{t-1}$$ No ano inicial (2003), o marcador textual `".."` foi convertido para `NaN`. |
| `dif_percentual` | `Diferença %` | `float64` | Percentual (`%`) | `-31.396111` a `37.747797` (`NaN` em 2003) | Variação percentual relativa ao 1º quadrimestre do ano anterior: $$\Delta_{\%, t} = \left(\frac{\text{total\_jan\_abr}_t - \text{total\_jan\_abr}_{t-1}}{\text{total\_jan\_abr}_{t-1}}\right) \times 100$$ |
| `populacao` | `População` | `float64` | Habitantes (projeção contínua) | `5865737.42` a `6802575.57` | Projeção demográfica oficial elaborada pelo ISP para o Município do Rio de Janeiro, referente ao último mês do quadrimestre (abril). |
| `taxa_100k` | `Taxa por 100 mil habitantes` | `float64` | Ocorrências / 100 mil hab. | `49.428096` a `145.898110` | Taxa de incidência criminal relativizada pela população municipal projetada: $$\text{Taxa}_{100k, t} = \left(\frac{\text{total\_jan\_abr}_t}{\text{populacao}_t}\right) \times 100.000$$ |
| `media_mensal` | `Média mensal` | `float64` | Ocorrências / mês | `785.00` a `2419.75` | Média aritmética mensal de roubos de veículos registrada no 1º quadrimestre: $$\text{Média}_{\text{mensal}, t} = \frac{\text{total\_jan\_abr}_t}{4}$$ |

---

## 2. Notas Metodológicas Oficiais (Extraídas da Aba `Definições`)

> "A classificação de um crime realizada pela Polícia Civil é provisória, ou seja, corresponde à primeira impressão acerca do fato durante o período do inquérito policial. Deste modo, o título do Registro de Ocorrência pode ser alterado pela autoridade policial no decorrer da investigação mediante a confecção de um Registro de Aditamento. Do mesmo modo, pode ocorrer alteração na classificação por parte do Ministério Público durante o oferecimento da denúncia e pelo Judiciário na confirmação da sentença."

* **Base Normativa:** Secretaria Nacional de Segurança Pública (SENASP) — *Manual de Preenchimento do Formulário de Coleta Mensal de Ocorrências Criminais e Atividades de Polícia* e Secretaria de Estado de Segurança (SESEG) — *Manual do Programa Delegacia Legal*.
* **Rastreabilidade de Higienização:** Na aba original `T 2306` (dimensão bruta $36 \times 7$), as linhas de índice `0` a `8` contêm cabeçalhos institucionais mesclados e as linhas `29` a `35` guardam notas de rodapé. O módulo `src/etl.py` isola o intervalo `iloc[9:29]`, valida a identidade algébrica das colunas derivadas com erro zero (`atol=1e-4`) e descarta a aba técnica vazia `ESRI_MAPINFO_SHEET` ($0 \times 0$).
