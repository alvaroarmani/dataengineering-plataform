# Exercício 13 — Qual índice o banco consegue usar? (a regra do prefixo)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro — e depois confira com `EXPLAIN`).

## Contexto
"Criei o índice e a query continua lenta" é uma das frases mais comuns em code review. Quase sempre
o motivo é a **ordem das colunas** num índice composto (teoria 07). Um B-Tree em
`(estado, cidade, data)` é como uma lista telefônica ordenada por estado, depois cidade, depois data:

- achar "SP, Campinas, a partir de março" é rápido — você desce pela ordem;
- achar "Campinas" **sem saber o estado** exige ler a lista inteira;
- depois de uma **faixa** (`estado > 'M'`), as cidades já não estão em ordem única — a descida para.

Você vai codificar essa regra e usá-la para duas decisões reais: **qual índice o planner escolhe** e
**se o índice já entrega o `ORDER BY` pronto** (sem um `SORT` caro).

## Tarefa
Em [`exercicio-13/solucao.py`](exercicio-13/solucao.py), implemente:

1. **`colunas_usadas(indice, filtros)`** — quantas colunas do prefixo o filtro aproveita.
2. **`melhor_indice(indices, filtros)`** — o índice que aproveita mais colunas (ou `None`: full scan).
3. **`evita_ordenacao(indice, filtros, order_by)`** — o índice entrega a ordem pedida?

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-13
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — percorra o índice, não o filtro
Um `for col in indice:` com `op = filtros.get(col)`: `"="` soma e segue; faixa soma e **retorna**;
qualquer outra coisa (inclusive `None`) retorna sem somar. Valide os operadores antes do laço.
:::
:::{dropdown} Dica 2 — desempate com tuplas
`min()` sobre tuplas `(-usadas, len(colunas), nome)` resolve os três critérios de uma vez. Se o
melhor tiver `usadas == 0`, devolva `None`.
:::
:::{dropdown} Dica 3 — ORDER BY
Para cada `j`, teste `indice[j:j+len(order_by)] == order_by`. Se não bateu e a coluna `indice[j]`
**não** está fixada por `"="`, pare: não dá para "pular" uma coluna livre.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def colunas_usadas(indice, filtros):
    for op in filtros.values():
        if op != "=" and op not in FAIXA and op not in NAO_INDEXAVEL:
            raise ValueError(f"operador desconhecido: {op}")
    n = 0
    for col in indice:
        op = filtros.get(col)
        if op == "=":
            n += 1                 # igualdade fixa a coluna: a próxima continua ordenada
        elif op in FAIXA:
            return n + 1           # a faixa usa esta coluna, mas embaralha as seguintes
        else:
            return n               # ausente ou não indexável: a descida para aqui
    return n

def melhor_indice(indices, filtros):
    candidatos = [(-colunas_usadas(cols, filtros), len(cols), nome) for nome, cols in indices.items()]
    melhor = min(candidatos)
    return melhor[2] if melhor[0] < 0 else None

def evita_ordenacao(indice, filtros, order_by):
    if not order_by:
        return True
    for j in range(len(indice)):
        if indice[j:j + len(order_by)] == list(order_by):
            return True
        if filtros.get(indice[j]) != "=":
            return False           # coluna livre antes da ordem pedida: precisa de SORT
    return False
```
**Confira no banco real** (DuckDB ou o Postgres da bancada):

```sql
CREATE INDEX ix ON vendas (estado, cidade, data);
EXPLAIN SELECT * FROM vendas WHERE cidade = 'Campinas';               -- Seq Scan
EXPLAIN SELECT * FROM vendas WHERE estado = 'SP' AND cidade = 'Campinas';  -- Index Scan
```
O planner real ainda pesa **seletividade** e **estatísticas** — com uma tabela minúscula, ele pode
preferir o full scan mesmo com o índice perfeito. A regra do prefixo diz o que é *possível*; o
custo estimado diz o que é *escolhido*.
:::

---
**Revisado em:** 2026-09-29
