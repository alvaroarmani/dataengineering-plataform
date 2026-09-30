# Exercício 08 — Trigger rules: quem roda quando algo falha

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Por padrão, uma task só roda se **todas** as upstream tiveram sucesso (`all_success`). Quando uma
falha, as dependentes ficam em **`upstream_failed`** — e isso se propaga. Mas há tasks que **precisam**
rodar mesmo assim (teoria 05): a limpeza de arquivos temporários (`all_done`), o alerta que só deve
disparar se algo falhou (`one_failed`), o relatório que roda se nada falhou, mesmo com tasks puladas
(`none_failed`). Entender essa semântica é o que evita o "o cleanup não rodou e o disco encheu".

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py), implemente `estado_task(regra, upstreams)` e `executar_dag(dag, resultados)`.

```bash
cd modulos/09-orquestracao-airflow/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — a regra, isolada
Calcule uma vez `falhou = any(u in ("failed", "upstream_failed") ...)` e decida cada regra com poucos `if`. Sem upstreams, tudo roda.
:::
:::{dropdown} Dica 2 — executar em ondas
Como no exercício 03 do M13: a cada rodada, as tasks cujas upstreams já têm estado final ficam prontas (ordem alfabética).
:::
:::{dropdown} Dica 3 — rodou = sucesso ou falha
Se a decisão é `"run"`, o estado vem de `resultados` (ausente = sucesso); senão, é a própria decisão.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
FINAIS = {"success", "failed", "skipped", "upstream_failed"}


def estado_task(regra: str, upstreams: list):
    falhou = any(u in ("failed", "upstream_failed") for u in upstreams)
    if regra == "all_success":
        if not upstreams or all(u == "success" for u in upstreams):
            return "run"
        return "upstream_failed" if falhou else "skipped"
    if regra == "all_done":
        return "run"
    if regra == "one_failed":
        return "run" if falhou else "skipped"
    if regra == "none_failed":
        return "upstream_failed" if falhou else "run"
    raise ValueError(f"trigger rule desconhecida: {regra}")


def executar_dag(dag: dict, resultados: dict) -> dict:
    estados = {}
    pendentes = set(dag)
    while pendentes:
        prontas = sorted(t for t in pendentes if all(u in estados for u in dag[t]["upstream"]))
        if not prontas:
            raise ValueError("ciclo no DAG")
        for t in prontas:
            decisao = estado_task(dag[t]["regra"], [estados[u] for u in dag[t]["upstream"]])
            estados[t] = ("success" if resultados.get(t, True) else "failed") if decisao == "run" else decisao
            pendentes.discard(t)
    run = "failed" if "failed" in estados.values() else "success"
    return {"estados": dict(sorted(estados.items())), "run": run}
```
Com `transformar` falhando: `carregar` fica `upstream_failed` (não roda sobre dado inexistente), mas o
`limpar_tmp` (`all_done`) roda e libera o disco, e o `alertar` (`one_failed`) dispara — o comportamento
que você quer às 3 da manhã. No caminho feliz, o alerta é **pulado**, sem ruído.

O detalhe é que `upstream_failed` também conta como falha para `one_failed` e `none_failed` — a falha
se propaga pelo grafo. Uma DAG com cleanup em `all_success` é a origem clássica de discos cheios e
clusters esquecidos ligados (M21).
:::

---
**Revisado em:** 2026-09-30
