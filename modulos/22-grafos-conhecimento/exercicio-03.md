# Exercício 03 — Caminho mais curto e vizinhança de k saltos (BFS)

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Qual o caminho mais curto entre duas pessoas?" e "quem está a até 2 saltos de mim?" são as duas
consultas que justificam um banco de grafos (teoria 02: travessia de profundidade variável,
`-[*1..2]-` em Cypher). Por baixo, as duas são **busca em largura (BFS)**: explorar primeiro todos
os vizinhos a 1 salto, depois os de 2, e assim por diante.

Você vai implementar as duas — devolvendo o **caminho**, e não só a distância, que é o que um
produto realmente mostra ("você e fulano têm estes contatos no caminho").

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `caminho_mais_curto(grafo, origem, destino)` e `ate_k_saltos(grafo, origem, k)`.

```bash
cd modulos/22-grafos-conhecimento/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — fila e 'de onde vim'
Use `collections.deque` como fila e um dict `anterior = {origem: None}`. Ele serve de conjunto de visitados **e** permite reconstruir o caminho.
:::
:::{dropdown} Dica 2 — reconstruir
Ao tirar o destino da fila, siga `anterior` de trás para frente até `None` e inverta a lista (`[::-1]`).
:::
:::{dropdown} Dica 3 — parar em k
Em `ate_k_saltos`, guarde `dist`; ao tirar um nó com `dist == k`, não expanda os vizinhos dele.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from collections import deque


def caminho_mais_curto(grafo: dict, origem, destino):
    for n in (origem, destino):
        if n not in grafo:
            raise KeyError(f"nó inexistente: {n}")
    anterior = {origem: None}
    fila = deque([origem])
    while fila:
        atual = fila.popleft()
        if atual == destino:
            caminho = []
            while atual is not None:
                caminho.append(atual)
                atual = anterior[atual]
            return caminho[::-1]
        for v in sorted(grafo[atual]):
            if v not in anterior:
                anterior[v] = atual
                fila.append(v)
    return None


def ate_k_saltos(grafo: dict, origem, k: int) -> dict:
    if k < 0:
        raise ValueError("k negativo")
    dist = {origem: 0}
    fila = deque([origem])
    while fila:
        atual = fila.popleft()
        if dist[atual] == k:
            continue
        for v in grafo[atual]:
            if v not in dist:
                dist[v] = dist[atual] + 1
                fila.append(v)
    return dict(sorted(dist.items()))
```
A BFS garante o **menor** número de saltos porque visita os nós em camadas: todos a distância 1
antes de qualquer um a distância 2. Uma busca em profundidade (DFS) encontraria *um* caminho, não
necessariamente o mais curto.

Explorar vizinhos em ordem alfabética não é detalhe estético: sem uma ordem fixa, dois caminhos
de mesmo tamanho podem ser devolvidos alternadamente entre execuções — o mesmo problema do
`ROW_NUMBER` sem desempate (M04). Em Cypher, isso é o `shortestPath((a)-[*]-(b))`.
:::

---
**Revisado em:** 2026-09-30
