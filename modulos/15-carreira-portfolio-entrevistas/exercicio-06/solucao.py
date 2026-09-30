"""Exercício 06 (M15) — Revisar um documento de design: as correntes de fundo.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""

import re
import unicodedata

SINAIS = {
    "qualidade": ["teste", "validacao", "contrato", "great expectations", "dbt test", "qualidade"],
    "seguranca": ["iam", "criptografia", "acesso", "lgpd", "mascaramento", "segredo", "seguranca"],
    "observabilidade": ["alerta", "monitoramento", "log", "metrica", "freshness", "observabilidade"],
    "custo": ["custo", "finops", "orcamento", "particionamento", "bytes"],
    "idempotencia": ["idempot", "reprocess", "backfill", "upsert", "merge", "exactly-once"],
}
PERGUNTAS = {
    "qualidade": "Como você garante que o dado que chega está correto?",
    "seguranca": "Quem pode acessar esses dados e como os dados pessoais são protegidos?",
    "observabilidade": "Como você fica sabendo que o pipeline quebrou ou atrasou?",
    "custo": "Quanto isso custa por mês e como você controla o custo?",
    "idempotencia": "O que acontece se o job rodar duas vezes ou precisar reprocessar um dia?",
}


def revisar_design(texto: str) -> dict:
    """Normalize o texto (sem acento, minúsculas) e procure os SINAIS como PALAVRAS (ou início de palavra:
    "idempot" casa "idempotente"; "log" não casa "catalogo"). Retorne
    {"cobertas": [correntes com algum sinal, na ordem de SINAIS],
     "faltando": [as outras, na mesma ordem],
     "perguntas": [PERGUNTAS de cada faltante, na mesma ordem]}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
