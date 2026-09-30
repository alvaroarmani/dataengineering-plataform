# Exercício 04 — Recomendação: pessoas que você talvez conheça

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
A consulta de recomendação da teoria 02 é o caso de uso que popularizou os bancos de grafos:
"amigos dos meus amigos que ainda não são meus amigos, ordenados por quantos amigos temos em
comum". Em SQL, isso é um self-join duplo sobre a tabela de amizades; em Cypher, um padrão de
dois saltos. Você vai implementá-la sobre a lista de adjacência.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `amigos_em_comum(grafo, a, b)` e `recomendar(grafo, pessoa, top_n)`.

```bash
cd modulos/22-grafos-conhecimento/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — interseção
Amigos em comum é interseção de conjuntos: `set(grafo[a]) & set(grafo[b])`.
:::
:::{dropdown} Dica 2 — dois saltos
Para cada amigo da pessoa, percorra os amigos **dele**; cada vez que um candidato aparece, é um amigo em comum a mais. Um dict de contagem resolve.
:::
:::{dropdown} Dica 3 — filtros e ordem
Descarte a própria pessoa e quem já está em `amigos`. Ordene com `key=lambda x: (-x[1], x[0])` e corte com `[:top_n]`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def amigos_em_comum(grafo: dict, a, b) -> list:
    return sorted(set(grafo[a]) & set(grafo[b]))


def recomendar(grafo: dict, pessoa, top_n: int = 3) -> list:
    amigos = set(grafo[pessoa])
    cont = {}
    for amigo in amigos:
        for cand in grafo[amigo]:
            if cand != pessoa and cand not in amigos:
                cont[cand] = cont.get(cand, 0) + 1
    return sorted(cont.items(), key=lambda x: (-x[1], x[0]))[:top_n]
```
A contagem funciona porque cada caminho `pessoa → amigo → candidato` corresponde a **um** amigo
em comum: a `dara` chega ao `bruno` por dois caminhos (via `caio` e via `eva`), por isso ele lidera.

O equivalente em Cypher:
```
MATCH (p:Pessoa {nome: "dara"})-[:AMIGO]-(a)-[:AMIGO]-(c)
WHERE c <> p AND NOT (p)-[:AMIGO]-(c)
RETURN c.nome, count(a) AS em_comum ORDER BY em_comum DESC, c.nome LIMIT 3
```
Em SQL, a mesma consulta pede dois self-joins e um `NOT EXISTS` — e o custo cresce rápido com a
profundidade, que é o argumento da teoria 01 para o modelo de grafo.
:::

---
**Revisado em:** 2026-09-30
