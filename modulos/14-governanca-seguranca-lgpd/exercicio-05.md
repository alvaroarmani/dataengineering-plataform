# Exercício 05 — Classificação LGPD por nome e por conteúdo

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Classificar colunas só pelo **nome** (teoria 03: dado pessoal × dado sensível) falha dos dois lados.
`Raça_Declarada` não bate com `raca` sem normalizar acento e caixa; e a coluna `observacoes` parece
inofensiva até você olhar o conteúdo e achar e-mails e CPFs digitados pelo atendimento. Por isso
ferramentas de descoberta de dados pessoais olham o nome **e** uma amostra dos valores.

A regra de precedência é da lei: se há indício de dado **sensível** (saúde, religião, biometria…),
a coluna é sensível, ainda que também contenha dado pessoal comum.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `classificar_coluna(nome, amostra)` e `mapear_tabela(colunas)`.

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — tokens normalizados
Tire os acentos com `unicodedata.normalize("NFKD", ...).encode("ascii", "ignore")`, passe para minúsculas e quebre com `re.split(r"[^a-z0-9]+", ...)`. Compare **tokens inteiros** — `nomenclatura` não é `nome`.
:::
:::{dropdown} Dica 2 — a ordem
Teste sensível antes de pessoal: a interseção com `SENSIVEIS` decide primeiro.
:::
:::{dropdown} Dica 3 — olhar o conteúdo
Duas regex bastam: e-mail (`[\w.+-]+@[\w-]+\.[\w.]+`) e CPF com pontuação opcional (`\d{3}\.?\d{3}\.?\d{3}-?\d{2}`). Ignore valores que não são string.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import re
import unicodedata

SENSIVEIS = {"raca", "etnia", "saude", "religiao", "biometria", "genetico", "sindicato", "orientacao", "sexual"}
PESSOAIS = {"cpf", "email", "nome", "telefone", "celular", "endereco", "rg", "nascimento"}
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
RE_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")


def _tokens(nome: str) -> set:
    ascii_ = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
    return set(re.split(r"[^a-z0-9]+", ascii_)) - {""}


def classificar_coluna(nome: str, amostra: list) -> str:
    tokens = _tokens(nome)
    if tokens & SENSIVEIS:
        return "sensivel"
    if tokens & PESSOAIS:
        return "pessoal"
    for v in amostra:
        if isinstance(v, str) and (RE_EMAIL.search(v) or RE_CPF.search(v)):
            return "pessoal"
    return "comum"


def mapear_tabela(colunas: dict) -> dict:
    out = {"sensivel": [], "pessoal": [], "comum": []}
    for nome in sorted(colunas):
        out[classificar_coluna(nome, colunas[nome])].append(nome)
    return out
```
A coluna `observacao` é o achado típico de uma varredura real: ninguém a declarou como pessoal,
mas o time de atendimento digita e-mails nela. Só olhando o conteúdo ela aparece — e, a partir daí,
entra no inventário de dados pessoais, no mascaramento e nos pedidos de exclusão.

Regex é uma heurística: gera falso positivo (um número de pedido com 11 dígitos parece CPF) e falso
negativo (CPF escrito por extenso). Ferramentas como o Cloud DLP do Google ou o Microsoft Presidio
combinam padrões, dígitos verificadores e contexto — mas a arquitetura é a mesma: nome + amostra +
precedência do sensível.
:::

---
**Revisado em:** 2026-09-30
