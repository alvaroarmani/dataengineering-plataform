"""Testes do Exercício 11 (M08) — PTAX real do Banco Central. Faça todos passarem: pytest -q"""
import copy
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import dias_sem_cotacao, maior_variacao_diaria, normalizar_ptax, upsert_por_data  # noqa: E402

PTAX = RAIZ / "datasets" / "amostras" / "ptax_2024_01.json"


@pytest.fixture(scope="module")
def payload():
    return json.loads(PTAX.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def registros(payload):
    return normalizar_ptax(payload)


# ---------- normalizar_ptax ----------
def test_normaliza_a_resposta_real(registros):
    assert len(registros) == 22
    assert registros[0] == {"data": "2024-01-02", "compra": 4.891, "venda": 4.8916}
    assert registros[-1] == {"data": "2024-01-31", "compra": 4.9529, "venda": 4.9535}


def test_normaliza_ordena_mesmo_com_payload_embaralhado(payload):
    embaralhado = copy.deepcopy(payload)
    embaralhado["value"].reverse()
    datas = [r["data"] for r in normalizar_ptax(embaralhado)]
    assert datas == sorted(datas) and len(datas) == 22


def test_contrato_quebrado_levanta_erro():
    with pytest.raises(ValueError):
        normalizar_ptax({"erro": "servico indisponivel"})


# ---------- upsert_por_data ----------
def test_upsert_e_idempotente(registros):
    uma_vez = upsert_por_data([], registros)
    duas_vezes = upsert_por_data(uma_vez, registros)
    assert duas_vezes == uma_vez and len(duas_vezes) == 22


def test_upsert_substitui_e_insere(registros):
    destino = registros[:5]
    correcao = {"data": registros[4]["data"], "compra": 9.0, "venda": 9.1}   # reprocesso de um dia
    novo_dia = {"data": "2024-02-01", "compra": 4.95, "venda": 4.96}
    out = upsert_por_data(destino, [novo_dia, correcao])
    assert len(out) == 6
    assert out[4] == correcao and out[-1] == novo_dia
    assert [r["data"] for r in out] == sorted(r["data"] for r in out)


# ---------- dias_sem_cotacao ----------
def test_completude_precisa_do_calendario_de_feriados(registros):
    # 1º de janeiro é feriado: sem o calendário, a checagem acusa um falso "buraco"
    assert dias_sem_cotacao(registros, "2024-01-01", "2024-01-31", []) == ["2024-01-01"]
    assert dias_sem_cotacao(registros, "2024-01-01", "2024-01-31", ["2024-01-01"]) == []


def test_completude_acha_buracos_reais(registros):
    faltando = [r for r in registros if r["data"] not in ("2024-01-10", "2024-01-11", "2024-01-29")]
    assert dias_sem_cotacao(faltando, "2024-01-01", "2024-01-31", ["2024-01-01"]) == [
        "2024-01-10", "2024-01-11", "2024-01-29"]


def test_completude_ignora_fim_de_semana():
    # 06/01/2024 e 07/01/2024 são sábado e domingo
    assert dias_sem_cotacao([], "2024-01-06", "2024-01-07", []) == []


# ---------- maior_variacao_diaria ----------
def test_maior_variacao_no_mes(registros):
    assert maior_variacao_diaria(registros) == ("2024-01-24", -1.052)


def test_maior_variacao_na_primeira_quinzena(registros):
    assert maior_variacao_diaria([r for r in registros if r["data"] <= "2024-01-12"]) == ("2024-01-03", 0.6051)


def test_maior_variacao_com_poucos_registros(registros):
    assert maior_variacao_diaria(registros[:1]) is None
    assert maior_variacao_diaria([]) is None
