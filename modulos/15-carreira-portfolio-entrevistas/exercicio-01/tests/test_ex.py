import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import avaliar_readme  # noqa: E402

BOM = """# Pipeline de vendas do Olist

## Sobre
Ingestão diária, dbt e dashboard.

## Motivação
O time comercial montava planilhas à mão.

## Arquitetura
![arquitetura](docs/arquitetura.png)

## Como executar
```bash
docker compose up -d
make run
```

## O que aprendi
Idempotência de verdade.
"""

FRACO = """# meu-projeto
Um projeto de dados.

### Setup
```
```
"""


def test_readme_completo():
    assert avaliar_readme(BOM) == {"faltando": [], "diagrama": True, "comandos": True, "nota": 100}


def test_readme_fraco():
    r = avaliar_readme(FRACO)
    assert r["faltando"] == ["o_que", "por_que", "arquitetura", "aprendizados"]
    assert r == {**r, "diagrama": False, "comandos": False, "nota": 14}


def test_sinonimos_e_acentos():
    txt = "## Visão geral\n## O PROBLEMA\n## Stack\n## Instalação\n## Lições\n"
    assert avaliar_readme(txt)["faltando"] == []


def test_titulo_em_texto_corrido_nao_conta():
    assert avaliar_readme("A arquitetura é simples e o setup também.")["faltando"] == [
        "o_que", "por_que", "arquitetura", "como_rodar", "aprendizados"]
