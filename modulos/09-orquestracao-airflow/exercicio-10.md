# Exercicio 10 - Tarefas prontas para rodar (fronteira) (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Aplica a [teoria 05](teoria-05-airflow-avancado.md).

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py): implemente **`tarefas_prontas`** - A cada momento, o scheduler roda a FRONTEIRA: tasks ainda nao concluidas cujas dependencias JA foram concluidas. grafo = {task: [dependencias]}; concluidas = lista de tasks ja feitas. Retorne a lista ORDENADA das tasks prontas.

```bash
cd modulos/09-orquestracao-airflow/exercicio-10
pytest -q
```

## Dica
:::{dropdown} Dica
uma task esta pronta se nao foi concluida e TODAS as suas dependencias estao em concluidas.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def tarefas_prontas(grafo, concluidas):
    feitas = set(concluidas)
    return sorted(t for t, deps in grafo.items() if t not in feitas and all(d in feitas for d in deps))
```
:::

---
**Revisado em:** 2026-09-09
