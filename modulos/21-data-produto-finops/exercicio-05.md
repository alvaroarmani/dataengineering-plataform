# Exercício 05 — SLO e orçamento de erro com incidentes sobrepostos

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Um SLO de disponibilidade de 99,9% num mês de 30 dias significa que você pode ficar fora do ar
**43,2 minutos** — esse é o **orçamento de erro** (*error budget*). A pergunta útil deixa de ser
"cumprimos o SLA?" (no fim do mês, tarde demais) e vira "quanto do orçamento já queimamos?".

A armadilha está na soma dos incidentes: quando dois alertas cobrem o **mesmo** período (o job
caiu e o dashboard ficou sem dado ao mesmo tempo), somar as durações conta a indisponibilidade
duas vezes. É preciso **unir os intervalos** antes de somar.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `minutos_indisponiveis(incidentes)` e `orcamento_de_erro(slo_pct, janela_dias, incidentes)`.

```bash
cd modulos/21-data-produto-finops/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — ordene e junte
Ordene os intervalos pelo início. Mantenha um intervalo "corrente"; se o próximo começa **antes ou no** fim do corrente, estenda o fim com `max`; senão, feche o corrente (some a duração) e comece outro.
:::
:::{dropdown} Dica 2 — não esqueça o último
Depois do laço, o último intervalo corrente ainda não foi somado.
:::
:::{dropdown} Dica 3 — o orçamento
Minutos no período: `janela_dias * 1440`. Permitido: `(1 - slo_pct / 100) * isso`. Queimado: `100 * consumido / permitido`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from datetime import datetime


def _ler(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace(" ", "T"))


def minutos_indisponiveis(incidentes: list) -> float:
    intervalos = []
    for ini, fim in incidentes:
        a, b = _ler(ini), _ler(fim)
        if b < a:
            raise ValueError(f"incidente termina antes de começar: {(ini, fim)}")
        intervalos.append((a, b))
    total, atual_ini, atual_fim = 0.0, None, None
    for a, b in sorted(intervalos):
        if atual_fim is None or a > atual_fim:
            if atual_fim is not None:
                total += (atual_fim - atual_ini).total_seconds() / 60
            atual_ini, atual_fim = a, b
        else:
            atual_fim = max(atual_fim, b)
    if atual_fim is not None:
        total += (atual_fim - atual_ini).total_seconds() / 60
    return total


def orcamento_de_erro(slo_pct: float, janela_dias: int, incidentes: list) -> dict:
    permitido = (1 - slo_pct / 100) * janela_dias * 1440
    consumido = minutos_indisponiveis(incidentes)
    return {"permitido_min": round(permitido, 1), "consumido_min": round(consumido, 1),
            "restante_min": round(permitido - consumido, 1),
            "queimado_pct": round(100 * consumido / permitido, 2) if permitido else None,
            "cumpre": consumido <= permitido}
```
Somar as durações daria 45 minutos e um SLO **violado**; a união dá 35 e 19% de orçamento ainda
disponível. Em times que usam error budget, essa diferença decide se a próxima release sai na
sexta ou se o time congela mudanças para priorizar confiabilidade — a política que torna o SLO
acionável.

Repare que 99,9% parece muito, mas são só 43 minutos por mês; e 99% (o último teste) já dá 7,2
horas. Escolher o SLO é escolher quanto o consumidor tolera — e quanto custa garantir cada "9" a
mais (FinOps de novo).
:::

---
**Revisado em:** 2026-09-30
