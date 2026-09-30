# Exercício 03 — Unicidade com chave composta

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O teste `unique` do dbt (teoria 02) parece trivial até a chave ser **composta** — pedido + item,
cliente + dia — e aparecer `NULL` num dos componentes. Nesse caso, dizer "é duplicado" ou "não é"
é uma decisão: em SQL, `NULL = NULL` não é verdadeiro, então duas linhas com chave nula **não**
colidem numa constraint `UNIQUE`… mas também não identificam nada.

A prática profissional é separar os dois problemas: **duplicidade** e **chave incompleta**.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `checar_unicidade(linhas, chave)`.

```bash
cd modulos/12-qualidade-observabilidade/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — a chave como tupla
`k = tuple(r.get(c) for c in chave)` — tuplas podem ser chave de dict. `r.get` devolve `None` para campo ausente, então ausente e nulo caem no mesmo caso.
:::
:::{dropdown} Dica 2 — separe antes de contar
Se `any(v is None for v in k)`, some em `chave_incompleta` e `continue`. Só depois conte as ocorrências.
:::
:::{dropdown} Dica 3 — ordenação
`sorted(pares, key=lambda x: (-x[1], x[0]))`: ocorrências decrescentes, empate pela própria chave.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def checar_unicidade(linhas: list, chave: list) -> dict:
    if not chave:
        raise ValueError("chave vazia")
    cont, incompletas = {}, 0
    for r in linhas:
        k = tuple(r.get(c) for c in chave)
        if any(v is None for v in k):
            incompletas += 1
            continue
        cont[k] = cont.get(k, 0) + 1
    dup = sorted(((k, n) for k, n in cont.items() if n > 1), key=lambda x: (-x[1], x[0]))
    return {"duplicadas": dup, "chave_incompleta": incompletas}
```
Com `["pedido"]` como chave, o pedido 10 "tem duplicata" — mas é só um pedido com dois itens. A
**granularidade** da chave é a pergunta de modelagem (grão, M05) aparecendo no teste de
qualidade: escolher a chave errada gera alerta falso toda noite.

Separar `chave_incompleta` evita dois erros opostos: contar as linhas nulas como duplicadas
(falso alarme) ou ignorá-las (linhas que nenhum join vai encontrar). No dbt, isso vira dois
testes: `unique_combination_of_columns` e `not_null` em cada componente.
:::

---
**Revisado em:** 2026-09-30
