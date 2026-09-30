import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import auditar_catalogo  # noqa: E402

CATALOGO = {
    "fct_vendas": {"dono": "ana", "descricao": "Vendas por item", "ultimo_acesso": "2026-09-29", "pii": False},
    "dim_cliente": {"dono": "  ", "descricao": "Clientes com CPF e e-mail", "ultimo_acesso": "2026-09-28", "pii": True},
    "tmp_export_2025": {"dono": None, "descricao": None, "ultimo_acesso": "2025-11-02", "pii": False},
    "stg_leads": {"dono": None, "descricao": "Leads do site", "ultimo_acesso": None, "pii": True},
    "mart_frete": {"dono": "bruno", "descricao": "", "ultimo_acesso": "2026-07-02", "pii": False},
}


def test_problemas_por_ativo():
    assert auditar_catalogo(CATALOGO, "2026-09-30")["problemas"] == {
        "dim_cliente": ["sem_dono"],
        "mart_frete": ["sem_descricao"],
        "stg_leads": ["abandonado", "sem_dono"],
        "tmp_export_2025": ["abandonado", "sem_descricao", "sem_dono"],
    }


def test_criticos_sao_pii_sem_dono():
    assert auditar_catalogo(CATALOGO, "2026-09-30")["criticos"] == ["dim_cliente", "stg_leads"]


def test_fronteira_do_abandono():
    # mart_frete: 90 dias exatos não é abandono; 91 é
    assert "abandonado" not in auditar_catalogo(CATALOGO, "2026-09-30")["problemas"]["mart_frete"]
    assert "abandonado" in auditar_catalogo(CATALOGO, "2026-10-01")["problemas"]["mart_frete"]


def test_limite_configuravel_e_catalogo_limpo():
    r = auditar_catalogo({"a": CATALOGO["fct_vendas"]}, "2026-09-30", dias_abandono=0)
    assert r == {"problemas": {"a": ["abandonado"]}, "criticos": []}
    assert auditar_catalogo({"a": CATALOGO["fct_vendas"]}, "2026-09-30") == {"problemas": {}, "criticos": []}
