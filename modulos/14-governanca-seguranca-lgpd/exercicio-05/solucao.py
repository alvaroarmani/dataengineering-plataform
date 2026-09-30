"""Exercício 05 (M14) — Classificação LGPD por nome e por conteúdo.

Rode `pytest -q`. Detalhes no enunciado (exercicio-05.md).
"""

import re
import unicodedata

SENSIVEIS = {"raca", "etnia", "saude", "religiao", "biometria", "genetico", "sindicato", "orientacao", "sexual"}
PESSOAIS = {"cpf", "email", "nome", "telefone", "celular", "endereco", "rg", "nascimento"}
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
RE_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")


def classificar_coluna(nome: str, amostra: list) -> str:
    """Retorne "sensivel", "pessoal" ou "comum".
      1. Normalize o nome (sem acento, minúsculo) e quebre em tokens por qualquer caractere que não seja
         letra/dígito ("Raça_Declarada" -> {"raca", "declarada"}).
      2. Algum token em SENSIVEIS -> "sensivel".
      3. Algum token em PESSOAIS, OU algum valor (str) da amostra contendo um e-mail ou um CPF
         (com ou sem pontuação) -> "pessoal".
      4. Senão -> "comum"."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def mapear_tabela(colunas: dict) -> dict:
    """colunas = {nome: amostra}. Retorne {"sensivel": [...], "pessoal": [...], "comum": [...]} ordenados."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
