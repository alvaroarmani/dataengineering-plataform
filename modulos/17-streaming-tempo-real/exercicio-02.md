# Exercício 02 — Batch x streaming: medindo a latência de verdade

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Batch de hora em hora" não significa que o dado chega com 1 hora de atraso. Um evento que acontece
logo depois do início de um ciclo espera quase o ciclo inteiro, mais o tempo de execução do job;
um evento que acontece logo antes do corte espera pouco. A latência do batch é uma **distribuição**,
e o que o negócio sente é o **pior caso** — o percentil 95, não a média.

Neste exercício você mede isso para eventos reais de um dia e compara com streaming. Com os números
na mão, a regra da teoria 01 ("a latência exigida decide") vira uma decisão objetiva.

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `latencias_batch`, `latencias_streaming` e `percentil`.

```bash
cd modulos/17-streaming-tempo-real/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — o próximo job
O primeiro job que pega o evento `t` começa em `(floor(t / intervalo) + 1) * intervalo` — o **próximo** múltiplo estritamente maior que `t` (o job que começa exatamente em `t` só pega eventos anteriores a ele).
:::
:::{dropdown} Dica 2 — streaming
Aqui é uma constante: `atraso_seg / 60` para cada evento.
:::
:::{dropdown} Dica 3 — percentil
Ordene; posição = `ceil(p / 100 * n)` (no mínimo 1); pegue `ordem[pos - 1]`. É o método mais simples e o mais fácil de explicar para o negócio.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import math


def latencias_batch(eventos_min: list, intervalo_min: int, duracao_job_min: float) -> list:
    out = []
    for t in eventos_min:
        inicio = (math.floor(t / intervalo_min) + 1) * intervalo_min
        out.append(inicio + duracao_job_min - t)
    return out


def latencias_streaming(eventos_min: list, atraso_seg: float) -> list:
    return [atraso_seg / 60 for _ in eventos_min]


def percentil(valores: list, p: float) -> float:
    if not valores:
        raise ValueError("sem valores")
    ordem = sorted(valores)
    pos = max(1, math.ceil(p / 100 * len(ordem)))
    return round(ordem[pos - 1], 2)
```
Com batch horário e job de 10 minutos, a latência **mediana** é de 53 minutos e o p95 é de **70
minutos** — quem prometer "dados de até 1 hora" vai descumprir a promessa todo dia. Com batch de 15
minutos (e job de 3), o p95 cai para 18 minutos; com streaming, para 5 segundos.

Essa tabela é o argumento numa decisão de arquitetura: se o requisito é "até 30 minutos", um
micro-batch de 15 minutos atende, com a simplicidade do batch (M09). Streaming só se paga quando o
requisito está na faixa de segundos — ou quando o valor está em **reagir** a cada evento, não em ter
a tabela atualizada.
:::

---
**Revisado em:** 2026-09-30
