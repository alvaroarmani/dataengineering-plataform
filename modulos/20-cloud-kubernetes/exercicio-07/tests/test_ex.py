"""Grader do Exercício 07 (M20) — valida a ESTRUTURA do manifesto do Deployment.

Grader de artefato (como o CI faria antes de aplicar): confere kind, réplicas, casamento
selector↔labels e a imagem. Para RODAR num cluster de verdade, use o lab-01 (kind).
"""
import sys
from pathlib import Path

import pytest
import yaml

MANIFESTO = Path(__file__).resolve().parents[1] / "deployment.yaml"


def _doc():
    return yaml.safe_load(MANIFESTO.read_text(encoding="utf-8"))


def test_e_um_deployment():
    d = _doc()
    assert d.get("apiVersion") == "apps/v1" and d.get("kind") == "Deployment"


def test_tres_replicas():
    d = _doc()
    assert d["spec"].get("replicas") == 3, "use replicas: 3"


def test_selector_bate_com_labels_do_template():
    d = _doc()
    try:
        sel = d["spec"]["selector"]["matchLabels"]
        lbl = d["spec"]["template"]["metadata"]["labels"]
    except (KeyError, TypeError):
        pytest.fail("faltam selector.matchLabels e/ou template.metadata.labels")
    assert sel and sel == lbl, "selector.matchLabels deve bater EXATAMENTE com os labels do template"


def test_container_nginx():
    d = _doc()
    conts = d["spec"]["template"]["spec"]["containers"]
    assert conts and conts[0].get("image") == "nginx:1.27", "o container deve usar image nginx:1.27"
