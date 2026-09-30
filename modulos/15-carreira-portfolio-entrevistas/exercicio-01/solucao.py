"""Exercício 01 (M15) — Um linter de README de portfólio.

Rode `pytest -q`. Detalhes no enunciado (exercicio-01.md).
"""

import re
import unicodedata

SECOES = {
    "o_que": ["sobre", "o que e", "visao geral", "resumo", "descricao"],
    "por_que": ["por que", "motivacao", "problema", "contexto"],
    "arquitetura": ["arquitetura", "stack", "desenho", "fluxo"],
    "como_rodar": ["como rodar", "como executar", "execucao", "setup", "instalacao", "quickstart"],
    "aprendizados": ["aprendi", "aprendizados", "licoes", "proximos passos"],
}


def avaliar_readme(texto: str) -> dict:
    """Leia os títulos de seção (linhas que começam com "#", qualquer nível), normalize (sem acento,
    minúsculas) e marque uma seção de SECOES como presente se algum título CONTÉM algum dos sinônimos.
    Além disso:
      "diagrama": há uma imagem Markdown ![...](...) no texto
      "comandos": há um bloco de código cercado por ``` com ao menos uma linha não vazia
    Retorne {"faltando": [seções de SECOES ausentes, na ordem de SECOES],
             "diagrama": bool, "comandos": bool,
             "nota": % de itens atendidos entre as 5 seções + diagrama + comandos (7 itens), inteiro}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
