# Exercício 05 — Resolver variável de ambiente (${VAR:-default}) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`resolver`** — `${VAR:-default}` usa o default quando a variável está ausente OU vazia.

```bash
cd modulos/10-docker-avancado/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
Separe por ':-'; use ambiente.get(nome) e caia no default se vazio/ausente.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def resolver(expr, ambiente):
    if ':-' in expr:
        nome, default = expr.split(':-', 1)
    else:
        nome, default = expr, ''
    val = ambiente.get(nome)
    return val if val not in (None, '') else default
```
:::

---
**Revisado em:** 2026-08-29
