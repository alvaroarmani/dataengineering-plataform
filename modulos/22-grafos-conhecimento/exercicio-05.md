# Exercício 05 — Centralidade: quem são os hubs da rede

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Quem é o nó mais importante?" depende da definição de importância. A mais simples é a
**centralidade de grau** (quantas conexões diretas), normalizada por `n − 1` para comparar redes
de tamanhos diferentes. Mas grau empata muito — então um segundo critério ajuda: o **alcance em
2 saltos** (quantos nós você atinge com um intermediário), que aproxima a influência de
alguém numa campanha de indicação ou a área de impacto de um nó que falha.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `ranking_centralidade(grafo, top_n)`.

```bash
cd modulos/22-grafos-conhecimento/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — grau normalizado
`len(vizinhos) / (n - 1)`: o máximo possível é estar ligado a todos os outros `n − 1` nós. Proteja o caso `n == 1`.
:::
:::{dropdown} Dica 2 — alcance em 2 saltos
Comece com `set(vizinhos)`, acrescente os vizinhos de cada vizinho (`update`) e remova o próprio nó (`discard`).
:::
:::{dropdown} Dica 3 — ordenar por vários critérios
`sorted(linhas, key=lambda x: (-x[1], -x[3], x[0]))` — negativos para decrescente.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def _alcance2(grafo: dict, no) -> int:
    alcance = set(grafo[no])
    for v in grafo[no]:
        alcance.update(grafo[v])
    alcance.discard(no)
    return len(alcance)


def ranking_centralidade(grafo: dict, top_n: int = 3) -> list:
    if not grafo:
        raise ValueError("grafo vazio")
    n = len(grafo)
    linhas = []
    for no, viz in grafo.items():
        g = len(set(viz))
        norm = round(g / (n - 1), 3) if n > 1 else 0.0
        linhas.append((no, g, norm, _alcance2(grafo, no)))
    return sorted(linhas, key=lambda x: (-x[1], -x[3], x[0]))[:top_n]
```
Três nós empatam em grau 3, mas `bruno` e `eva` alcançam 5 pessoas em 2 saltos e `caio`, só 4:
`bruno` e `eva` são **pontes** entre o grupo de cima (`ana`, `caio`) e o `fabio`. Essa intuição é
formalizada por medidas mais caras, como *betweenness* (quantos caminhos mais curtos passam pelo
nó) e *PageRank* — disponíveis prontas na biblioteca GDS do Neo4j e no `networkx`.

Note que `gil` e `hugo` têm centralidade baixa **nesta** rede, mas são o centro da própria
componente: métricas globais escondem comunidades isoladas (exercício 06).
:::

---
**Revisado em:** 2026-09-30
