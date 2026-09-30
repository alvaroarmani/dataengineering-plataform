"""Exercício 05 (M20) — Scheduler: onde cada pod vai rodar.

Rode `pytest -q`. Detalhes no enunciado (exercicio-05.md).
"""


def agendar(pods: list, nos: dict) -> dict:
    """pods = [(nome, cpu, mem)] na ordem de chegada; nos = {nome: (cpu_total, mem_total)}.
    Para cada pod: nós viáveis = onde cpu E mem livres comportam o pod. Entre eles, escolha o que
    fica com a MAIOR fração livre de CPU após receber o pod (cpu_livre_depois / cpu_total);
    empate: nome do nó. Sem nó viável -> "Pending".
    Retorne {"alocacao": {pod: no ou "Pending"}, "livre": {no: (cpu_livre, mem_livre)}}.
    Pod com cpu ou mem <= 0 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
