import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import alcanca  # noqa: E402

SERVICOS = {
    "postgres": {"redes": ["backend"], "porta": 5432, "publica": [5433]},
    "airflow": {"redes": ["backend", "frontend"], "porta": 8080, "publica": [8080]},
    "metabase": {"redes": ["frontend"], "porta": 3000, "publica": [3000]},
}


@pytest.mark.parametrize("origem, endereco, esperado", [
    ("airflow", "postgres:5432", (True, "postgres")),
    ("airflow", "postgres:5433", (False, "porta_errada")),           # porta do host, não da rede
    ("airflow", "localhost:5432", (False, "localhost_no_container")),
    ("airflow", "localhost:8080", (True, "airflow")),                 # ele mesmo
    ("metabase", "postgres:5432", (False, "sem_rede_em_comum")),
    ("metabase", "airflow:8080", (True, "airflow")),
    ("host", "localhost:5433", (True, "postgres")),
    ("host", "localhost:5432", (False, "porta_errada")),
    ("host", "postgres:5432", (False, "host_nao_resolve_nome")),
    ("airflow", "redis:6379", (False, "servico_inexistente")),
])
def test_alcance(origem, endereco, esperado):
    assert alcanca(SERVICOS, origem, endereco) == esperado


def test_endereco_malformado():
    with pytest.raises(ValueError):
        alcanca(SERVICOS, "airflow", "postgres:abc")
