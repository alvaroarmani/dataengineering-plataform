# Exercício 03 — XCom: passar valores entre tasks (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Tasks são isoladas; para passar um valor de uma para a próxima, o Airflow usa **XCom** (o
`return` de um `@task` vira XCom). Modele isso.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py):

- **`rodar_tasks(tasks)`** — `tasks` = lista de `(nome, func)`. Cada `func(xcom)` recebe os
  retornos anteriores (por nome) e devolve seu resultado. Rode em ordem e retorne o `xcom` final.

```bash
cd modulos/09-orquestracao-airflow/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — acumule
Comece com `xcom = {}`; para cada `(nome, func)`, faça `xcom[nome] = func(xcom)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def rodar_tasks(tasks):
    xcom = {}
    for nome, func in tasks:
        xcom[nome] = func(xcom)
    return xcom
```
É a essência do XCom na TaskFlow API: o retorno de cada task fica disponível (por task_id) para
as seguintes. Lembre: XCom é para **valores pequenos** — datasets vão para storage.
:::

---
**Revisado em:** 2026-08-29
