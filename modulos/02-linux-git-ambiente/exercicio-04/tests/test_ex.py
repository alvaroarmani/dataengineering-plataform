import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import resumo_status  # noqa: E402

SAIDA = """M  dags/vendas.py
 M README.md
MM models/fct_vendas.sql
A  models/dim_loja.sql
 D notebooks/rascunho.ipynb
R  sql/old.sql -> sql/novo.sql
?? dados/tmp.csv
?? .env
"""


def test_resumo_completo():
    assert resumo_status(SAIDA) == {
        "staged": ["dags/vendas.py", "models/dim_loja.sql", "models/fct_vendas.sql", "sql/novo.sql"],
        "nao_staged": ["README.md", "models/fct_vendas.sql", "notebooks/rascunho.ipynb"],
        "untracked": [".env", "dados/tmp.csv"],
        "renomeados": [("sql/old.sql", "sql/novo.sql")],
    }


def test_arquivo_nas_duas_areas():
    r = resumo_status("MM a.py\n")
    assert r["staged"] == ["a.py"] and r["nao_staged"] == ["a.py"]


def test_saida_vazia_e_linhas_em_branco():
    assert resumo_status("") == {"staged": [], "nao_staged": [], "untracked": [], "renomeados": []}
    assert resumo_status("\n\n?? x\n")["untracked"] == ["x"]


def test_linha_malformada():
    with pytest.raises(ValueError):
        resumo_status("Mx arquivo.py")
