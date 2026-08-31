"""Testes do Exercício 06 (M20). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import dns_servico  # noqa: E402


def test_dns_servico():
    assert dns_servico(*('api', 'prod')) == 'api.prod.svc.cluster.local'
    assert dns_servico(*('db', 'default')) == 'db.default.svc.cluster.local'
