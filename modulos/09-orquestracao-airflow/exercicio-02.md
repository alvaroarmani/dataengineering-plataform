# Exercício 02 — Detectar ciclo (o "A" de DAG) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Uma DAG é **acíclica**. Um ciclo (a → b → a) tornaria o pipeline impossível de terminar.
Detecte isso.

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py):

- **`tem_ciclo(tasks, arestas)`** — retorne `True` se houver ciclo, `False` se for acíclico.

```bash
cd modulos/09-orquestracao-airflow/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — Kahn detecta ciclo
Se a ordenação topológica (Kahn) **não consegue processar todas** as tasks, sobrou algo preso num ciclo.
:::
:::{dropdown} Dica 2 — a conta
Conte quantas tasks você conseguiu ordenar; se for menos que o total, há ciclo.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def tem_ciclo(tasks, arestas):
    from collections import defaultdict
    dep = defaultdict(int)
    saintes = defaultdict(list)
    for a, b in arestas:
        dep[b] += 1
        saintes[a].append(b)
    fila = [t for t in tasks if dep[t] == 0]
    processadas = 0
    while fila:
        t = fila.pop(0)
        processadas += 1
        for viz in saintes[t]:
            dep[viz] -= 1
            if dep[viz] == 0:
                fila.append(viz)
    return processadas < len(tasks)   # sobrou algo => ciclo
```
Reaproveita o algoritmo de Kahn (Exercício 01): se nem todas as tasks foram processadas, as que
sobraram estão num ciclo. É por isso que o Airflow **recusa** uma DAG com ciclo.
:::

---
**Revisado em:** 2026-08-29
