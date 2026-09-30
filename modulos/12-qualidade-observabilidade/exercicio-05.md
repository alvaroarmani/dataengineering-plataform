# Exercício 05 — Freshness com SLA e aviso antecipado

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Pipeline "verde" com dado de ontem é o incidente silencioso mais comum (teoria 03). O check de
**freshness** compara a última carga com o SLA — mas um check binário só avisa quando o SLA **já
foi** violado. Ferramentas como o `dbt source freshness` têm dois limiares, `warn_after` e
`error_after`, para dar tempo de agir antes.

Você vai implementar esse check em dois níveis, para várias tabelas, e apontar a pior.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `status_freshness(ultima, agora, sla_horas, aviso_pct)` e
`relatorio(tabelas, agora, sla_horas)`.

```bash
cd modulos/12-qualidade-observabilidade/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — datas
`datetime.fromisoformat` lê `'2026-09-30T10:00'`; troque o espaço por `T` antes. A diferença de dois `datetime` é um `timedelta`: `.total_seconds() / 3600` dá horas.
:::
:::{dropdown} Dica 2 — ordem dos ifs
Teste primeiro o futuro (erro), depois `> sla` (violado), depois `> aviso_pct * sla` (aviso). Repare que é `>` estrito: no limite exato, o status é o mais brando.
:::
:::{dropdown} Dica 3 — a pior tabela
Maior atraso = carga mais **antiga**: `min(tabelas, key=lambda n: (_ler(tabelas[n]), n))` resolve atraso e desempate de uma vez.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from datetime import datetime


def _ler(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace(" ", "T"))


def status_freshness(ultima: str, agora: str, sla_horas: float, aviso_pct: float = 0.8) -> str:
    atraso = (_ler(agora) - _ler(ultima)).total_seconds() / 3600
    if atraso < 0:
        raise ValueError("última carga no futuro: verifique o relógio/fuso da fonte")
    if atraso > sla_horas:
        return "violado"
    if atraso > aviso_pct * sla_horas:
        return "aviso"
    return "ok"


def relatorio(tabelas: dict, agora: str, sla_horas: float) -> dict:
    if not tabelas:
        raise ValueError("nenhuma tabela")
    status = {n: status_freshness(u, agora, sla_horas) for n, u in tabelas.items()}
    pior = min(tabelas, key=lambda n: (_ler(tabelas[n]), n))
    return {"status": status, "pior": pior}
```
O nível **aviso** é o que transforma o check em ferramenta de operação: com SLA de 6 h e aviso a
80%, você fica sabendo com 1 h 12 min de folga. É a mesma ideia do `warn_after`/`error_after` do
dbt.

O `ValueError` para carga "no futuro" não é detalhe: esse sintoma quase sempre é **fuso horário**
(a fonte grava em UTC e o check compara em horário local, ou o contrário). Um check que
simplesmente devolvesse "ok" esconderia o bug para sempre.
:::

---
**Revisado em:** 2026-09-30
