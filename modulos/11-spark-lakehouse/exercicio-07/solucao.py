"""Exercício 07 (M11) — Delta log: reconstruir versões, time travel e VACUUM.

Rode `pytest -q`. Detalhes no enunciado (exercicio-07.md).
"""


def arquivos_da_versao(log: list, versao: int) -> list:
    """log[i] = commit da versão i: {"ts": int, "add": [arquivos], "remove": [arquivos]}.
    Reproduza os commits 0..versao (em cada um, aplique os remove e depois os add) e retorne os arquivos
    ativos, ordenados. Versão fora do log -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def versao_no_instante(log: list, ts: int) -> int:
    """Maior versão com commit feito até `ts` (inclusive). Antes do primeiro commit -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def removiveis_no_vacuum(log: list, agora: int, retencao: int) -> list:
    """Arquivos que NÃO estão na versão mais recente e cuja remoção (o commit que os removeu) aconteceu
    há MAIS de `retencao` unidades de tempo (agora - ts do commit > retencao). Ordenados."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
