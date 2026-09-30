# Exercício 09 — Fato de snapshot acumulado: lead times, pedidos em aberto e gargalo

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro — no dbt, o mesmo modelo vira um `incremental` com `merge`).

## Contexto
Um **fato de snapshot acumulado** (teoria 05) tem **uma linha por processo** (um pedido) e uma
coluna por **marco** (criado, pago, enviado, entregue) — a linha é **atualizada** conforme o pedido
avança, diferente do fato transacional, em que cada evento é uma linha nova. É o modelo certo para
perguntas de **processo**: quanto tempo leva cada etapa? Onde está o gargalo? Quantos pedidos estão
parados há mais de uma semana?

Os dados reais trazem os problemas de sempre: marcos ausentes (o pedido ainda não chegou lá, ou a
integração perdeu o evento) e marcos **inconsistentes** (enviado antes de pago — relógio de um
sistema, fuso de outro).

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py), implemente `snapshot_acumulado(pedidos, data_ref)` e `gargalo(snapshot)`.

```bash
cd modulos/05-modelagem-dimensional/exercicio-09
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — status e lead times
Status: `[e for e in ETAPAS if p.get(e)][-1]`. Um helper `_dias(a, b)` que devolve `None` quando falta alguma data resolve os quatro lead times.
:::
:::{dropdown} Dica 2 — em aberto e inconsistência
Em aberto só para não entregues: `data_ref - criado`. Inconsistente: a lista das datas presentes, na ordem das etapas, não está ordenada (`presentes != sorted(presentes)` — datas ISO ordenam como texto).
:::
:::{dropdown} Dica 3 — gargalo
Para cada coluna de lead time, a média dos valores não nulos de linhas **consistentes**; devolva a maior.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from datetime import date

ETAPAS = ["criado", "pago", "enviado", "entregue"]


def _dias(a, b):
    if not a or not b:
        return None
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


def snapshot_acumulado(pedidos: list, data_ref: str) -> list:
    linhas = []
    for p in sorted(pedidos, key=lambda x: x["pedido_id"]):
        if not p.get("criado"):
            raise ValueError(f"pedido {p['pedido_id']} sem data de criação")
        status = [e for e in ETAPAS if p.get(e)][-1]
        presentes = [p[e] for e in ETAPAS if p.get(e)]
        linhas.append({
            "pedido_id": p["pedido_id"],
            "status": status,
            "dias_pago": _dias(p.get("criado"), p.get("pago")),
            "dias_envio": _dias(p.get("pago"), p.get("enviado")),
            "dias_entrega": _dias(p.get("enviado"), p.get("entregue")),
            "dias_total": _dias(p.get("criado"), p.get("entregue")),
            "dias_em_aberto": None if p.get("entregue") else _dias(p["criado"], data_ref),
            "inconsistente": presentes != sorted(presentes),
        })
    return linhas


def gargalo(snapshot: list) -> tuple:
    medias = {}
    for col in ("dias_pago", "dias_envio", "dias_entrega"):
        vals = [l[col] for l in snapshot if l[col] is not None and not l["inconsistente"]]
        if vals:
            medias[col] = sum(vals) / len(vals)
    if not medias:
        raise ValueError("sem lead times para avaliar")
    pior = max(medias, key=lambda c: medias[c])
    return pior, round(medias[pior], 1)
```
O pedido 5 mostra por que a flag `inconsistente` existe: sem ela, o `dias_envio = -2` entraria na
média e **esconderia** o gargalo real. A etapa mais lenta é o envio (4,5 dias em média) — a pergunta de
negócio que o snapshot acumulado responde e que o fato transacional só responderia com vários self-joins.

O `dias_em_aberto` é a métrica operacional: o pedido 3 está parado em "criado" há 14 dias. No dbt,
esse modelo costuma ser um `incremental` com `unique_key = pedido_id` e estratégia `merge`: a cada
carga, a linha do pedido é **atualizada** com os novos marcos (M07).
:::

---
**Revisado em:** 2026-09-30
