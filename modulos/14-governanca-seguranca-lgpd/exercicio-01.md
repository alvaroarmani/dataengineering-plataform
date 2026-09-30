# Exercício 01 — Análise de impacto: quem avisar antes da mudança

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Vou renomear uma coluna da `stg_pedidos` — o que quebra?" A resposta vem do **lineage** (teoria
01): tudo que está a jusante, direta ou indiretamente. Mas a lista de tabelas é só metade da
análise; a outra metade é **quem avisar**: os donos dos ativos afetados. E a distância importa —
um dashboard a 3 saltos quebra do mesmo jeito, só que mais tarde e com mais gente olhando.

Lineage real também tem sujeira: tabelas sem dono cadastrado e, às vezes, **ciclos** (uma tabela
de reconciliação que lê o mart que ela mesma alimenta). A análise não pode entrar em loop.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente `analise_de_impacto(lineage, tabela, donos)`.

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — BFS com distância
Uma fila (`deque`) e um dict `dist = {tabela: 0}`. O dict também serve de visitados — é isso que faz o ciclo não travar.
:::
:::{dropdown} Dica 2 — agrupar por distância
Depois da busca, remova a própria tabela e agrupe com `por_dist.setdefault(d, []).append(no)`.
:::
:::{dropdown} Dica 3 — donos
Um set de `donos.get(n)` ignorando valores vazios (`if donos.get(n)`) — `None` e `""` contam como sem dono.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from collections import deque


def analise_de_impacto(lineage: dict, tabela, donos: dict) -> dict:
    if tabela not in lineage:
        raise KeyError(f"ativo desconhecido: {tabela}")
    dist = {tabela: 0}
    fila = deque([tabela])
    while fila:
        atual = fila.popleft()
        for v in lineage.get(atual, []):
            if v not in dist:
                dist[v] = dist[atual] + 1
                fila.append(v)
    dist.pop(tabela)
    por_dist = {}
    for no, d in dist.items():
        por_dist.setdefault(d, []).append(no)
    impactados = sorted(dist)
    return {
        "impactados": impactados,
        "por_distancia": {d: sorted(v) for d, v in sorted(por_dist.items())},
        "notificar": sorted({donos.get(n) for n in impactados if donos.get(n)}),
        "sem_dono": [n for n in impactados if not donos.get(n)],
    }
```
A `reconciliacao` é o ciclo do teste: ela consome o `mart_receita` e o alimenta de volta. Sem o
controle de visitados, a busca ficaria girando entre os dois para sempre. Com BFS, cada ativo
recebe a **menor** distância — o `mart_receita` está a 2 saltos, mesmo sendo alcançável também
pela volta do ciclo.

O campo `sem_dono` é tão importante quanto a lista de notificação: são os ativos que vão quebrar
sem que ninguém seja avisado. Em ferramentas de catálogo (DataHub, OpenMetadata), essa análise vira
um comentário automático no PR com a lista de afetados e seus donos.
:::

---
**Revisado em:** 2026-09-30
