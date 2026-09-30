import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import resolver  # noqa: E402

SERVICOS = {("db", "dev"): "10.0.1.5", ("db", "prod"): "10.0.9.5", ("api", "prod"): "10.0.9.7",
            ("kafka", "dados"): "10.0.4.2"}


def test_nome_curto_depende_do_namespace():
    assert resolver("db", "dev", SERVICOS) == "10.0.1.5"
    assert resolver("db", "prod", SERVICOS) == "10.0.9.5"


def test_nome_com_namespace_e_completo():
    assert resolver("kafka.dados", "prod", SERVICOS) == "10.0.4.2"
    assert resolver("api.prod.svc.cluster.local", "dev", SERVICOS) == "10.0.9.7"


def test_nome_curto_nao_cruza_namespace():
    with pytest.raises(KeyError):
        resolver("kafka", "prod", SERVICOS)          # existe, mas em "dados"
    with pytest.raises(KeyError):
        resolver("api", "dev", SERVICOS)


@pytest.mark.parametrize("nome", ["", "a.b.c", "api.prod.svc"])
def test_formatos_invalidos(nome):
    with pytest.raises(ValueError):
        resolver(nome, "prod", SERVICOS)
