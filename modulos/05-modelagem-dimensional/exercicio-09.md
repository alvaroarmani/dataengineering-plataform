# Exercício 09 — Fato de snapshot acumulado (mini-caso · nível avançado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Exercício **complexo, multi-etapa** —
aplica o *accumulating snapshot fact* da [teoria 05](teoria-05-modelagem-avancada.md).

## Contexto (o caso)
Você modela o **processo de entrega** de um e-commerce como um **accumulating snapshot fact**: uma
linha por pedido, com uma coluna de data para cada **marco** do pipeline —
`criado → pago → enviado → entregue` — preenchidas conforme o pedido avança. Pedidos incompletos têm
marcos **ausentes**. O negócio quer os **lead times** (tempo entre marcos) para achar gargalos, e o
**status atual** de cada pedido.

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py), implemente **`snapshot_acumulado(pedidos)`**.
Cada `pedido` é um dict com `pedido_id` e os marcos como datas `'AAAA-MM-DD'` (alguns ausentes).
Para **cada** pedido, retorne um dict com:

| Campo | Regra |
|---|---|
| `pedido_id` | o id do pedido |
| `status` | a **última** etapa que tem data (`criado`/`pago`/`enviado`/`entregue`) |
| `dias_pago` | dias de `criado` → `pago` |
| `dias_envio` | dias de `pago` → `enviado` |
| `dias_entrega` | dias de `enviado` → `entregue` |
| `dias_total` | dias de `criado` → `entregue` |

Onde faltar um dos marcos do intervalo, o lead time é **`None`** (o pedido ainda não chegou lá).

```bash
cd modulos/05-modelagem-dimensional/exercicio-09
pytest -q
```

Exemplo:
```python
snapshot_acumulado([
    {"pedido_id": 1, "criado": "2026-01-01", "pago": "2026-01-02", "enviado": "2026-01-05", "entregue": "2026-01-10"},
    {"pedido_id": 2, "criado": "2026-01-01", "pago": "2026-01-03"},
])
# pedido 1: status 'entregue', dias 1/3/5, total 9
# pedido 2: status 'pago', dias_pago 2, envio/entrega/total = None
```

## Dicas progressivas
:::{dropdown} Dica 1 — status
Percorra as etapas em ordem e guarde a última que tiver data — esse é o `status`.
:::
:::{dropdown} Dica 2 — lead times com marcos ausentes
Faça um helper `dias(a, b)` que retorna `None` se `a` ou `b` faltarem, senão
`(date.fromisoformat(b) - date.fromisoformat(a)).days`. Assim os pedidos incompletos ficam com `None`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from datetime import date

def snapshot_acumulado(pedidos):
    etapas = ["criado", "pago", "enviado", "entregue"]

    def dias(a, b):
        if not a or not b:
            return None
        return (date.fromisoformat(b) - date.fromisoformat(a)).days

    out = []
    for p in pedidos:
        status = "criado"
        for e in etapas:
            if p.get(e):
                status = e           # última etapa com data
        out.append({
            "pedido_id": p["pedido_id"],
            "status": status,
            "dias_pago": dias(p.get("criado"), p.get("pago")),
            "dias_envio": dias(p.get("pago"), p.get("enviado")),
            "dias_entrega": dias(p.get("enviado"), p.get("entregue")),
            "dias_total": dias(p.get("criado"), p.get("entregue")),
        })
    return out
```
:::

---
**Revisado em:** 2026-09-09
