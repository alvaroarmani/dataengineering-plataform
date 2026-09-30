"""Exercício 06 (M10) — Referência de imagem: registry, tag, digest e reprodutibilidade.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""

import re


def parse_imagem(ref: str) -> dict:
    """Retorne {"registry", "repositorio", "tag", "digest"}:
      - registry: o 1º segmento, se houver "/" e ele contiver "." ou ":" ou for "localhost"; senão "docker.io"
      - repositorio: o resto; no docker.io, sem "/" -> prefixo "library/"
      - digest: o que vier depois de "@" (ou None); tag: depois do último ":" do repositório (ou "latest"
        se não houver tag nem digest; None se só houver digest)
    Referência vazia ou com espaços/maiúsculas no repositório -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def reprodutivel(ref: str) -> str:
    """"digest" se tiver digest; "versao" se a tag tiver ao menos dois números (ex.: 16.4, 1.8.2);
    senão "flutuante" (ex.: latest, 16, slim). Uma tag como 3.12-slim conta como versão."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
