# Exercício 04 — Sensor: modo poke x reschedule e o custo de esperar

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Um sensor espera uma condição (teoria 02): o arquivo pousar no bucket, a partição existir. **Como**
ele espera faz toda a diferença de custo. No modo **poke**, o sensor ocupa um slot de worker o tempo
inteiro, dormindo entre as verificações. No modo **reschedule** (e nos *deferrable operators*, teoria
05), ele libera o slot entre as verificações e só o ocupa durante a checagem.

Com um sensor, não faz diferença. Com 200 sensores esperando arquivos de parceiros, o modo poke
prende 200 workers — e as tasks de verdade ficam na fila.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `simular_sensor(disponivel_em, intervalo, timeout, modo)`.

```bash
cd modulos/09-orquestracao-airflow/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — as checagens
Um laço com `minuto` começando em 0 e somando `intervalo`, enquanto `minuto <= timeout`. Cada volta é um poke; pare na primeira com `minuto >= disponivel_em`.
:::
:::{dropdown} Dica 2 — o custo do slot
No poke, o slot fica ocupado do início até o fim da última checagem: `minuto_fim + 1`. No reschedule, só 1 minuto por checagem.
:::
:::{dropdown} Dica 3 — valide
Intervalo menor que 1 faria o laço nunca andar; modo fora de `poke`/`reschedule` é erro de configuração.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def simular_sensor(disponivel_em, intervalo: int, timeout: int, modo: str) -> dict:
    if intervalo < 1 or modo not in ("poke", "reschedule"):
        raise ValueError("parâmetros inválidos")
    pokes, minuto, sucesso, fim = 0, 0, False, 0
    while minuto <= timeout:
        pokes += 1
        fim = minuto
        if disponivel_em is not None and minuto >= disponivel_em:
            sucesso = True
            break
        minuto += intervalo
    slot = fim + 1 if modo == "poke" else pokes
    return {"sucesso": sucesso, "pokes": pokes, "minuto_fim": fim, "minutos_de_slot": slot}
```
Para o arquivo que chega às 3 horas da manhã, 200 sensores em modo **poke** ocupam 36.200
minutos de worker — 600 horas de slot numa madrugada; em **reschedule**, 7.400. Para um cluster com
16 slots, é a diferença entre as DAGs de verdade rodarem ou ficarem esperando na fila.

Os *deferrable operators* levam a ideia ao extremo: entre as checagens, a espera nem ocupa um slot
de worker — fica num processo leve (o *triggerer*) que monitora milhares de condições de uma vez.
:::

---
**Revisado em:** 2026-09-30
