"""Exercício 02 (M2) — Pre-commit: achar segredos antes do commit.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""

import re

PADROES = [
    ("chave_aws", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("chave_privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("senha", re.compile(r"(?i)\b(password|senha|secret|token)\s*[:=]\s*(.+)")),
]
PLACEHOLDER = re.compile(r"^(\$\{.*\}|<.*>|\{\{.*\}\}|\*+|x+|changeme|none|null|os\.(environ|getenv).*)$", re.I)


def achar_segredos(arquivos: dict) -> list:
    """arquivos = {caminho: conteudo}. Retorne a lista ORDENADA de (caminho, numero_da_linha, tipo):
      - arquivo chamado ".env" (em qualquer pasta) com conteúdo não vazio -> (caminho, 0, "arquivo_env")
      - linha com chave AWS (AKIA + 16 maiúsculas/dígitos) -> "chave_aws"
      - linha com cabeçalho "-----BEGIN ... PRIVATE KEY-----" -> "chave_privada"
      - linha "password|senha|secret|token" seguido de = ou : e um valor -> "senha", EXCETO se o valor
        (o resto da linha, sem espaços, aspas e ")" / "," nas pontas) for placeholder: ${...}, <...>,
        {{...}}, só asteriscos, só x, changeme, None, null, ou leitura de ambiente (os.environ/os.getenv)
    Linhas numeradas a partir de 1; no máximo um achado por (linha, tipo)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
