#!/usr/bin/env python3
"""Baixa os datasets do curso conforme datasets/manifest.yaml (reproduzível).

Uso:
    python datasets/baixar.py            # baixa todos os que têm URL direta
    python datasets/baixar.py nyc_taxi   # baixa só um dataset

Datasets sem URL direta (ex.: Olist no Kaggle) exigem autenticação — o script
explica como obter e onde colocar os arquivos (datasets/data/<nome>/).
"""
import os
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DATA = RAIZ / "datasets" / "data"


def carregar_manifesto():
    import yaml  # pyyaml já é dep do projeto (jupyter-book)

    texto = (RAIZ / "datasets" / "manifest.yaml").read_text(encoding="utf-8")
    # expande ${VAR:-default} simples a partir do ambiente
    def _expand(m):
        import re
        def sub(x):
            nome, _, default = x.group(1).partition(":-")
            return os.environ.get(nome, default)
        return re.sub(r"\$\{([^}]+)\}", sub, m)
    return yaml.safe_load(_expand(texto))["datasets"]


def baixar_um(nome, spec):
    url = (spec.get("url") or "").strip()
    alvo = DATA / spec["arquivos"][0]
    alvo.parent.mkdir(parents=True, exist_ok=True)
    if alvo.exists():
        print(f"[{nome}] já existe: {alvo.relative_to(RAIZ)} (pulando)")
        return
    if not url:
        print(f"[{nome}] SEM URL direta ({spec['origem']}).")
        print(f"        Baixe manualmente e coloque em: {alvo.parent.relative_to(RAIZ)}/")
        print("        (ou defina uma URL de mirror via variável de ambiente — ver manifest.yaml)")
        return
    print(f"[{nome}] baixando {url} -> {alvo.relative_to(RAIZ)} ...")
    urllib.request.urlretrieve(url, alvo)
    print(f"[{nome}] ok ({alvo.stat().st_size // 1024} KB)")


def main(argv):
    datasets = carregar_manifesto()
    alvos = argv or list(datasets)
    for nome in alvos:
        if nome not in datasets:
            print(f"desconhecido: {nome} (disponíveis: {', '.join(datasets)})")
            continue
        baixar_um(nome, datasets[nome])


if __name__ == "__main__":
    main(sys.argv[1:])
