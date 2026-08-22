"""Etapa 1 — Ingestão: ler o CSV de pedidos."""
from pathlib import Path

import pandas as pd

CSV = Path(__file__).resolve().parents[1] / "data" / "pedidos.csv"


def ler_pedidos(caminho: Path = CSV) -> pd.DataFrame:
    """Lê o CSV de pedidos como DataFrame (valores brutos, sem limpeza)."""
    return pd.read_csv(caminho)
