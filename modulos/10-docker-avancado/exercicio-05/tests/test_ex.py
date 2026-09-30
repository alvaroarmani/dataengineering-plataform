import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import interpolar  # noqa: E402

AMB = {"PG_USER": "airflow", "PG_HOST": "", "PG_PORT": "5432"}


def test_variaveis_simples():
    assert interpolar("postgresql://${PG_USER}@db:$PG_PORT/dw", AMB) == "postgresql://airflow@db:5432/dw"


def test_padrao_com_e_sem_dois_pontos():
    assert interpolar("${PG_HOST:-localhost}", AMB) == "localhost"      # vazia -> padrão
    assert interpolar("${PG_HOST-localhost}", AMB) == ""                # vazia é valor
    assert interpolar("${PG_DB-dw}", AMB) == "dw"                       # ausente -> padrão


def test_obrigatoria():
    with pytest.raises(ValueError, match="defina PG_PASSWORD"):
        interpolar("${PG_PASSWORD:?defina PG_PASSWORD}", AMB)
    with pytest.raises(ValueError):
        interpolar("${PG_HOST:?host vazio}", AMB)
    assert interpolar("${PG_HOST?nao usado}", AMB) == ""


def test_cifrao_literal_e_ausente():
    assert interpolar("echo $$HOME e ${NADA}", AMB) == "echo $HOME e "
