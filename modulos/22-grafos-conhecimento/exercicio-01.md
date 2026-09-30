# Exercício 01 — Da tabela de arestas à lista de adjacência

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Grafos quase nunca nascem prontos: na empresa, eles chegam como uma **tabela de relacionamentos**
— `seguidores(origem, destino)`, `transferencias(de, para)`, `dependencias(tabela, depende_de)`
— exportada de um banco relacional. O primeiro passo de qualquer análise de grafo (e do import
para o Neo4j) é converter essa tabela numa **lista de adjacência**, decidindo três coisas que a
teoria 01 discute: a relação é **dirigida**? O que fazer com **arestas repetidas**? E com
**laços** (um nó ligado a si mesmo)?

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente `construir_grafo(arestas, dirigido)` e `vizinhos(grafo, no)`.

```bash
cd modulos/22-grafos-conhecimento/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — sets durante, listas no fim
Acumule em `adj.setdefault(no, set())` — o set elimina repetição. Só no `return` converta para listas ordenadas.
:::
:::{dropdown} Dica 2 — os dois nós sempre existem
Crie a entrada de `a` **e** de `b` antes de qualquer `continue`; assim o destino de uma aresta dirigida e o nó de um laço aparecem no grafo.
:::
:::{dropdown} Dica 3 — direção
Adicione `b` em `adj[a]`; se não for dirigido, adicione também `a` em `adj[b]`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def construir_grafo(arestas: list, dirigido: bool = False) -> dict:
    adj = {}
    for a, b in arestas:
        if a is None or b is None:
            raise ValueError(f"aresta com nó nulo: {(a, b)}")
        adj.setdefault(a, set())
        adj.setdefault(b, set())
        if a == b:
            continue
        adj[a].add(b)
        if not dirigido:
            adj[b].add(a)
    return {no: sorted(v) for no, v in sorted(adj.items())}


def vizinhos(grafo: dict, no) -> list:
    if no not in grafo:
        raise KeyError(f"nó inexistente: {no}")
    return grafo[no]
```
Os testes mostram por que a direção é uma **decisão de modelagem**: em "segue" (Instagram), `ana →
caio` não implica `caio → ana`; tratar como não dirigido inventaria seguidores. Já em "é amigo de"
(Facebook), a relação é simétrica por definição.

No Neo4j, toda relação é gravada **com** direção, mas pode ser **consultada** ignorando-a
(`-[:SEGUE]-` em vez de `-[:SEGUE]->`) — o que fizemos aqui com a flag `dirigido`.
:::

---
**Revisado em:** 2026-09-30
