import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import classificar_coluna, mapear_tabela  # noqa: E402


@pytest.mark.parametrize("nome, esperado", [
    ("Raça_Declarada", "sensivel"),
    ("plano_de_saude", "sensivel"),
    ("CPF", "pessoal"),
    ("email_contato", "pessoal"),
    ("valor_total", "comum"),
    ("nomenclatura_produto", "comum"),      # "nome" só como token inteiro
])
def test_pelo_nome(nome, esperado):
    assert classificar_coluna(nome, []) == esperado


def test_pelo_conteudo():
    assert classificar_coluna("observacoes", ["cliente pediu 2a via", "contato: ana@x.com"]) == "pessoal"
    assert classificar_coluna("obs", ["doc 123.456.789-09 conferido"]) == "pessoal"
    assert classificar_coluna("obs", ["12345678909"]) == "pessoal"
    assert classificar_coluna("obs", ["pedido 1234567", None, 42]) == "comum"


def test_sensivel_vence_pessoal():
    assert classificar_coluna("religiao_email", []) == "sensivel"
    assert classificar_coluna("saude_obs", ["ana@x.com"]) == "sensivel"


def test_mapear_tabela():
    colunas = {"id": [1, 2], "nome_cliente": ["Ana"], "observacao": ["ligar p/ bruno@y.com"],
               "CID_saude": ["J11"], "valor": [10.5]}
    assert mapear_tabela(colunas) == {"sensivel": ["CID_saude"], "pessoal": ["nome_cliente", "observacao"],
                                      "comum": ["id", "valor"]}
