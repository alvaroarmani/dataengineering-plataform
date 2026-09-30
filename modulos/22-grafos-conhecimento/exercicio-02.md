# Exercício 02 — Grau de entrada e saída: fontes e sumidouros do lineage

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Num grafo **dirigido**, o grau se divide em dois: **entrada** (quantas arestas chegam) e **saída**
(quantas partem). No grafo de **lineage** de um data warehouse — a mesma estrutura que o dbt monta
com `ref()` —, isso responde perguntas práticas:

- grau de entrada 0 → **fontes** (tabelas raw, que ninguém produz dentro do DW);
- grau de saída 0 → **sumidouros** (marts e dashboards finais);
- grau de saída alto → tabela da qual **muita coisa depende** (mexer nela é arriscado).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `graus(lineage)` e `fontes_e_sumidouros(lineage)`.

```bash
cd modulos/22-grafos-conhecimento/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — dois contadores
Mantenha `ent` e `sai` (dicts). Para cada origem, `sai[origem] += len(set(destinos))` e cada destino ganha `ent[d] += 1`.
:::
:::{dropdown} Dica 2 — nós que só aparecem como destino
Garanta que todo nó exista nos dois dicts com `setdefault(no, 0)` — senão `dash_diretoria` não teria grau de saída.
:::
:::{dropdown} Dica 3 — classificar
Fontes: entrada 0. Sumidouros: saída 0. Mais dependida: `min(g, key=lambda n: (-saida, n))`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def graus(lineage: dict) -> dict:
    ent, sai = {}, {}
    for origem, destinos in lineage.items():
        dest = set(destinos)
        sai[origem] = sai.get(origem, 0) + len(dest)
        ent.setdefault(origem, 0)
        for d in dest:
            ent[d] = ent.get(d, 0) + 1
            sai.setdefault(d, 0)
    return {n: (ent[n], sai[n]) for n in sorted(ent)}


def fontes_e_sumidouros(lineage: dict) -> dict:
    g = graus(lineage)
    if not g:
        raise ValueError("lineage vazio")
    return {
        "fontes": [n for n, (e, _) in g.items() if e == 0],
        "sumidouros": [n for n, (_, s) in g.items() if s == 0],
        "mais_dependida": min(g, key=lambda n: (-g[n][1], n)),
    }
```
A `tabela_orfa` aparece como fonte **e** sumidouro ao mesmo tempo: ninguém a alimenta e ela não
alimenta nada. Num projeto real, esse é um candidato a limpeza (custo de armazenamento e
confusão sem uso — M21, FinOps).

Repare que `mais_dependida` desempatou `stg_clientes` e `stg_pedidos` (ambos com saída 2) pela
ordem alfabética. Em ferramentas de catálogo (DataHub, OpenMetadata), essa métrica de "fan-out" é
usada para marcar tabelas críticas que exigem revisão extra antes de mudanças.
:::

---
**Revisado em:** 2026-09-30
