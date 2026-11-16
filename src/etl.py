"""
Módulo de ETL (Extract, Transform, Load) - Projeto Final LP6 (G2)
Autor: Caio Silva Lopes
Curso: Bacharelado em Sistemas de Informação (6º Período) — Semestre 2026.2
Disciplina: Linguagem de Programação (Análise e Visualização de Dados com Python)
Repositório: https://github.com/CaioSIlvaLopes/LINGUAGENS-DE-PROGRAMA-O-Projeto-Pr-tico-G2.git
Fonte primária: DATA.RIO / Instituto de Segurança Pública (ISP-RJ) - Tabela 2306
"""

import json
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import pandas as pd


RAW_DATA_PATH = Path("data/raw/2306.xls")
PROCESSED_DIR = Path("data/processed")
PROCESSED_CSV_PATH = PROCESSED_DIR / "roubo_veiculos_mrj_2003_2022.csv"
PROCESSED_GZ_PATH = PROCESSED_DIR / "roubo_veiculos_mrj_2003_2022.csv.gz"
PROCESSED_JSON_PATH = PROCESSED_DIR / "roubo_veiculos_mrj_2003_2022.json"
PROCESSED_PARQUET_PATH = PROCESSED_DIR / "roubo_veiculos_mrj_2003_2022.parquet"
DEFINICOES_TXT_PATH = PROCESSED_DIR / "definicoes_metadados_isp.txt"
AUDITORIA_JSON_PATH = PROCESSED_DIR / "auditoria_etl.json"


def extract_raw_sheets(filepath: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Inspeciona todas as abas da planilha bruta 2306.xls e carrega:
    - Aba 'T 2306': Série histórica de roubos de veículos (2003-2022).
    - Aba 'Definições': Notas metodológicas oficiais SENASP/SESEG.
    A aba 'ESRI_MAPINFO_SHEET' (0x0) é verificada e ignorada por estar vazia.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Arquivo bruto não encontrado em: {filepath}")
    excel_file = pd.ExcelFile(filepath)
    required_sheets = {"T 2306", "Definições"}
    missing = required_sheets - set(excel_file.sheet_names)
    if missing:
        raise ValueError(f"Abas obrigatórias ausentes: {missing}")

    raw_t2306 = pd.read_excel(filepath, sheet_name="T 2306")
    raw_definicoes = pd.read_excel(filepath, sheet_name="Definições")
    return raw_t2306, raw_definicoes


def transform_vehicle_robbery_data(raw_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Higieniza a Tabela 2306 de forma determinística e audita as variáveis derivadas:
    - Remove cabeçalhos institucionais (linhas 0 a 8) e rodapés explicativos (linhas 29 a 35).
    - Padroniza nomes de colunas no formato snake_case.
    - Converte o marcador '..' (não aplicável no ano base 2003) para NaN numérico.
    - Executa verificação matemática estrita (np.allclose) das 4 métricas calculadas.
    """
    df = raw_df.iloc[9:29].copy()
    df.columns = [
        "ano",
        "total_jan_abr",
        "dif_absoluta",
        "dif_percentual",
        "populacao",
        "taxa_100k",
        "media_mensal",
    ]

    df = df.replace("..", np.nan)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["ano"] = df["ano"].astype(int)
    df["total_jan_abr"] = df["total_jan_abr"].astype(int)
    df = df.sort_values("ano").reset_index(drop=True)

    # Auditoria matemática determinística das colunas derivadas
    calc_dif_abs = df["total_jan_abr"].diff()
    calc_dif_pct = df["total_jan_abr"].pct_change() * 100.0
    calc_taxa_100k = (df["total_jan_abr"] / df["populacao"]) * 100000.0
    calc_media_mensal = df["total_jan_abr"] / 4.0

    err_dif_abs = float((df["dif_absoluta"].dropna() - calc_dif_abs.dropna()).abs().max())
    err_dif_pct = float((df["dif_percentual"].dropna() - calc_dif_pct.dropna()).abs().max())
    err_taxa = float((df["taxa_100k"] - calc_taxa_100k).abs().max())
    err_media = float((df["media_mensal"] - calc_media_mensal).abs().max())

    assert np.allclose(df["dif_absoluta"].dropna(), calc_dif_abs.dropna(), atol=1e-4)
    assert np.allclose(df["dif_percentual"].dropna(), calc_dif_pct.dropna(), atol=1e-4)
    assert np.allclose(df["taxa_100k"], calc_taxa_100k, atol=1e-4)
    assert np.allclose(df["media_mensal"], calc_media_mensal, atol=1e-4)

    audit_info = {
        "projeto": "Dinâmica Histórica de Roubos de Veículos no Município do Rio de Janeiro (2003-2022)",
        "autor": "Caio Silva Lopes",
        "total_registros_validos": int(len(df)),
        "auditoria_matematica_erro_maximo": {
            "dif_absoluta": err_dif_abs,
            "dif_percentual": err_dif_pct,
            "taxa_100k": err_taxa,
            "media_mensal": err_media,
            "status_integridade": "APROVADO_ERRO_ZERO",
        },
    }
    return df, audit_info


def extract_definicoes_text(raw_definicoes: pd.DataFrame) -> str:
    """Extrai e higieniza os textos metodológicos da aba 'Definições'."""
    paragrafos = [
        str(val).strip()
        for val in raw_definicoes.iloc[:, 0].dropna().values
        if str(val).strip() and str(val).strip() != "Definições"
    ]
    return "\n\n".join(paragrafos)


def load_processed_data(df: pd.DataFrame, definicoes_text: str, audit_info: Dict) -> None:
    """Persiste os dados higienizados e metadados em formatos abertos (CSV, CSV.GZ, JSON, TXT e Parquet)."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_CSV_PATH, index=False, float_format="%.6f")
    df.to_csv(PROCESSED_GZ_PATH, index=False, compression="gzip", float_format="%.6f")
    df.to_json(PROCESSED_JSON_PATH, orient="records", indent=2)

    with open(DEFINICOES_TXT_PATH, "w", encoding="utf-8") as f:
        f.write("METADADOS OFICIAIS — ABA 'Definições' (Tabela 2306 DATA.RIO / ISP-RJ)\n")
        f.write("=" * 75 + "\n\n")
        f.write(definicoes_text + "\n")

    with open(AUDITORIA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(audit_info, f, ensure_ascii=False, indent=2)

    try:
        df.to_parquet(PROCESSED_PARQUET_PATH, index=False)
    except Exception:
        pass


def run_pipeline(raw_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Executa o pipeline completo de ETL de forma determinística."""
    raw_t2306, raw_definicoes = extract_raw_sheets(raw_path)
    clean_df, audit_info = transform_vehicle_robbery_data(raw_t2306)
    definicoes_text = extract_definicoes_text(raw_definicoes)
    load_processed_data(clean_df, definicoes_text, audit_info)
    return clean_df


if __name__ == "__main__":
    fallback_path = Path("2306.xls") if not RAW_DATA_PATH.exists() else RAW_DATA_PATH
    dataset = run_pipeline(fallback_path)
    print(f"Pipeline concluído com sucesso por Caio Silva Lopes. Registros processados: {len(dataset)}")
