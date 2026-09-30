"""Exercício 02 (M15) — Quais projetos vão para o currículo.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""

from datetime import date

PESOS = {"dados_reais": 3, "testes": 2, "ci": 2, "demo": 2, "readme_nota": 0.03}


def escolher_projetos(projetos: list, hoje: str, n: int = 3) -> list:
    """projetos = [{"nome", "readme_nota" (0-100), "commits", "ultimo_commit" ('AAAA-MM-DD'), "dados_reais",
    "testes", "ci", "demo" (bools), "foco": parte do ciclo ("ingestao", "modelagem", "orquestracao"...)}].
    Eliminados: readme_nota < 50, commits < 5 ou último commit há mais de 365 dias.
    Pontuação = soma dos PESOS (bools valem 1/0; readme_nota entra como nota * 0.03), 2 casas.
    Escolha gulosa: em ordem de pontuação (empate: nome), pegue um projeto se o "foco" dele ainda não
    foi escolhido; se sobrarem vagas, complete com os melhores restantes (mesmo repetindo foco).
    Retorne [(nome, pontuacao)] na ordem de escolha."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
