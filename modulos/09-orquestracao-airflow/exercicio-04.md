# Exercício 04 — Sensor: esperar uma condição (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Um sensor segura o pipeline até algo acontecer, "pokando" até liberar. Implemente essa mecânica.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py):

- **`poke_ate(condicao, max_pokes)`** — chame `condicao()` até retornar `True` e devolva o
  número de pokes; se atingir `max_pokes` sem sucesso, levante `TimeoutError`.

```bash
cd modulos/09-orquestracao-airflow/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — o laço
`for i in range(1, max_pokes+1): if condicao(): return i`. Fora do laço, `raise TimeoutError`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def poke_ate(condicao, max_pokes):
    for i in range(1, max_pokes + 1):
        if condicao():
            return i
    raise TimeoutError("condição não satisfeita dentro do limite de pokes")
```
É o coração de um sensor: verifica periodicamente até a condição valer (arquivo chegou,
partição existe...) ou estourar o timeout. Na prática, entre os pokes há um intervalo, e para
esperas longas usa-se o modo `reschedule` para não segurar um worker.
:::

---
**Revisado em:** 2026-08-29
