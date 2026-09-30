import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import executar_saga  # noqa: E402

PASSOS = [("reservar", "liberar"), ("cobrar", "estornar"), ("emitir_nf", None), ("enviar", None)]


def test_caminho_feliz():
    assert executar_saga(PASSOS, "emitir_nf", {}) == {
        "status": "concluida", "log": ["ok:reservar", "ok:cobrar", "ok:emitir_nf", "ok:enviar"]}


def test_falha_antes_do_pivo_compensa_em_ordem_inversa():
    r = executar_saga(PASSOS, "emitir_nf", {"cobrar": [False]})
    assert r == {"status": "compensada", "log": ["ok:reservar", "falha:cobrar", "compensa:liberar"]}


def test_falha_no_ultimo_passo_reversivel():
    r = executar_saga(PASSOS + [], "emitir_nf", {"emitir_nf": [True], "cobrar": [True]})
    assert r["status"] == "concluida"
    passos = [("reservar", "liberar"), ("cobrar", "estornar"), ("antifraude", "desfazer_analise"), ("emitir_nf", None)]
    r2 = executar_saga(passos, "emitir_nf", {"antifraude": [False]})
    assert r2["log"] == ["ok:reservar", "ok:cobrar", "falha:antifraude", "compensa:estornar", "compensa:liberar"]


def test_depois_do_pivo_insiste_em_vez_de_compensar():
    r = executar_saga(PASSOS, "emitir_nf", {"enviar": [False, False, True]})
    assert r == {"status": "concluida",
                 "log": ["ok:reservar", "ok:cobrar", "ok:emitir_nf", "falha:enviar", "falha:enviar", "ok:enviar"]}


def test_pendente_sem_compensar():
    r = executar_saga(PASSOS, "emitir_nf", {"emitir_nf": [False, False]})
    assert r == {"status": "pendente", "log": ["ok:reservar", "ok:cobrar", "falha:emitir_nf", "falha:emitir_nf"]}


def test_pivo_invalido():
    with pytest.raises(ValueError):
        executar_saga(PASSOS, "voar", {})
