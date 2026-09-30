"""Exercício 03 (M2) — Conventional Commits: validar e calcular a próxima versão.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""

import re

TIPOS = {"feat", "fix", "docs", "chore", "refactor", "test", "perf", "ci", "build", "style"}
CABECALHO = re.compile(r"^(?P<tipo>[a-z]+)(\((?P<escopo>[a-z0-9_\-/]+)\))?(?P<quebra>!)?: (?P<desc>\S.*)$")


def analisar_commit(mensagem: str) -> dict:
    """Primeira linha no formato "tipo(escopo opcional)!(opcional): descrição".
    Regras: tipo em TIPOS; descrição não vazia; primeira linha com no máximo 72 caracteres.
    breaking = há "!" OU alguma linha do corpo começa com "BREAKING CHANGE:".
    Retorne {"tipo", "escopo" (ou None), "breaking", "descricao"}. Inválido -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def proxima_versao(versao: str, mensagens: list) -> str:
    """Semver a partir dos commits desde a última versão: algum breaking -> MAJOR; senão algum feat ->
    MINOR; senão algum fix ou perf -> PATCH; senão a versão não muda. Commit inválido -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
