"""Exercício 01 (M20) — Serverless ou container? A decisão pelo custo (e o ponto de equilíbrio).

Rode `pytest -q`.

Preços ILUSTRATIVOS (ordem de grandeza das tabelas públicas; os reais variam por provedor, região
e data — confira sempre a página de preços antes de decidir):
"""

# Serverless (função): cobra por requisição e por GB-segundo de execução, com cota gratuita mensal.
PRECO_POR_MILHAO_REQ = 0.20
PRECO_GB_SEGUNDO = 0.0000166667
GRATIS_REQ = 1_000_000
GRATIS_GB_SEGUNDO = 400_000

# Container sempre ligado: cobra por hora de vCPU e de GB de memória, esteja ocioso ou não.
PRECO_VCPU_HORA = 0.04048
PRECO_GB_HORA = 0.004445
HORAS_MES = 730


def custo_serverless(req_mes: int, duracao_ms: float, memoria_gb: float) -> float:
    """Custo mensal (US$, 2 casas):
        gb_s = req_mes * (duracao_ms / 1000) * memoria_gb
        req_cobradas = max(0, req_mes - GRATIS_REQ);  gb_s_cobrados = max(0, gb_s - GRATIS_GB_SEGUNDO)
        custo = req_cobradas / 1e6 * PRECO_POR_MILHAO_REQ + gb_s_cobrados * PRECO_GB_SEGUNDO
    Qualquer argumento negativo -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def custo_container(vcpu: float, memoria_gb: float, replicas: int = 1) -> float:
    """Custo mensal (US$, 2 casas) de `replicas` containers ligados o mês todo:
        replicas * HORAS_MES * (vcpu * PRECO_VCPU_HORA + memoria_gb * PRECO_GB_HORA)
    vcpu/memória <= 0 ou replicas < 1 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def recomendar(req_mes, duracao_ms, memoria_fn_gb, vcpu, memoria_ct_gb, replicas=1) -> dict:
    """Compare as duas opções e retorne:
        {"escolha": "serverless" | "container",     # a mais barata; EMPATE -> "serverless"
         "serverless": custo, "container": custo,
         "economia_pct": economia da escolha sobre a outra, em % da mais cara, 1 casa (0.0 se empate)}"""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def ponto_de_equilibrio(duracao_ms, memoria_fn_gb, vcpu, memoria_ct_gb, replicas=1) -> int:
    """Menor número INTEIRO de requisições/mês a partir do qual o serverless fica MAIS CARO que o
    container (use custo_serverless e custo_container, já arredondados).
    Dica: o custo serverless só cresce com req_mes — busca binária resolve."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
