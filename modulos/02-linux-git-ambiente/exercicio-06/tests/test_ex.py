import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import conflitos, parse_porta  # noqa: E402


@pytest.mark.parametrize("spec, esperado", [
    ("8080:80", {"ip": "0.0.0.0", "host": 8080, "container": 80, "protocolo": "tcp"}),
    ("127.0.0.1:5432:5432", {"ip": "127.0.0.1", "host": 5432, "container": 5432, "protocolo": "tcp"}),
    ("5353:53/udp", {"ip": "0.0.0.0", "host": 5353, "container": 53, "protocolo": "udp"}),
    ("3000", {"ip": "0.0.0.0", "host": None, "container": 3000, "protocolo": "tcp"}),
])
def test_parse(spec, esperado):
    assert parse_porta(spec) == esperado


@pytest.mark.parametrize("spec", ["70000:80", "abc:80", "80/sctp", "1:2:3:4", "0:80"])
def test_parse_invalido(spec):
    with pytest.raises(ValueError):
        parse_porta(spec)


def test_conflitos_na_bancada():
    servicos = {
        "postgres": ["127.0.0.1:5432:5432"],
        "postgres_testes": ["5432:5432"],           # 0.0.0.0 colide com 127.0.0.1
        "airflow": ["8080:8080"],
        "spark_ui": ["8080:4040"],
        "dns": ["5353:53/udp"],
        "mdns_tcp": ["5353:5353"],                  # mesma porta, protocolo diferente: ok
        "jupyter": ["8888"],
    }
    assert conflitos(servicos) == [(5432, "tcp", ["postgres", "postgres_testes"]),
                                   (8080, "tcp", ["airflow", "spark_ui"])]


def test_ips_diferentes_nao_conflitam():
    assert conflitos({"a": ["127.0.0.1:80:80"], "b": ["192.168.0.10:80:80"]}) == []
