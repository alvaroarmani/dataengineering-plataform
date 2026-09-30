# Exercício 05 — Interpolação de variáveis do Compose

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O `docker-compose.yml` lê configuração do ambiente (teoria 03) com uma sintaxe que tem mais nuances do
que parece: `${VAR:-padrao}` usa o padrão se a variável **não existe ou está vazia**; `${VAR-padrao}`
só se ela **não existe** (vazia é um valor válido); `${VAR:?mensagem}` **aborta** se estiver ausente ou
vazia — o jeito certo de exigir uma senha em vez de subir com senha vazia; e `$$` é um `$` literal (para
passar `$HOME` para dentro do container).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `interpolar(texto, ambiente)`.

```bash
cd modulos/10-docker-avancado/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — uma regex com alternativas
Três formas: `$$`, `${NOME...}` (com um operador opcional `:-`, `-`, `:?`, `?` e um argumento) e `$NOME`. Grupos nomeados deixam a função de troca legível.
:::
:::{dropdown} Dica 2 — ausente x vazia
Guarde `existe = nome in ambiente` e `valor = ambiente.get(nome, "")`. As formas com `:` olham `valor` (vazio conta como faltando); as sem `:` olham `existe`.
:::
:::{dropdown} Dica 3 — re.sub com função
`PADRAO.sub(troca, texto)` chama `troca(match)` para cada ocorrência — levante o `ValueError` de dentro dela.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import re

PADRAO = re.compile(r"\$\$|\$\{(?P<nome>[A-Za-z_][A-Za-z0-9_]*)(?:(?P<op>:-|-|:\?|\?)(?P<arg>[^}]*))?\}|\$(?P<simples>[A-Za-z_][A-Za-z0-9_]*)")


def interpolar(texto: str, ambiente: dict) -> str:
    def troca(m):
        if m.group(0) == "$$":
            return "$"
        nome = m.group("nome") or m.group("simples")
        op, arg = m.group("op"), m.group("arg")
        existe = nome in ambiente
        valor = ambiente.get(nome, "")
        if op == ":-":
            return valor if valor else arg
        if op == "-":
            return valor if existe else arg
        if op == ":?" and not valor:
            raise ValueError(arg or f"{nome} obrigatória")
        if op == "?" and not existe:
            raise ValueError(arg or f"{nome} obrigatória")
        return valor

    return PADRAO.sub(troca, texto)
```
O `${PG_PASSWORD:?defina PG_PASSWORD}` é o uso mais valioso da sintaxe: sem ele, esquecer o `.env` faz o
Postgres subir **sem senha** (ou com uma senha vazia), e ninguém percebe até ser tarde. Com ele, o
`docker compose up` para imediatamente com uma mensagem clara.

A diferença `:-` x `-` importa quando "vazio" é intencional: `LOG_PREFIX=` (vazio de propósito)
continua vazio com `${LOG_PREFIX-[etl]}`, mas vira `[etl]` com `${LOG_PREFIX:-[etl]}`. É a mesma sintaxe
do shell POSIX (`bash`), então vale para scripts de entrypoint também.
:::

---
**Revisado em:** 2026-09-30
