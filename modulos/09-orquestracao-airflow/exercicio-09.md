# Exercício 09 — Dynamic Task Mapping sob um pool: quanto tempo leva

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Com **dynamic task mapping** (teoria 05), uma task vira N instâncias em tempo de execução — uma por
arquivo, por exemplo. Se todas forem ao mesmo banco, é preciso um **pool** que limite quantas rodam ao
mesmo tempo, senão você derruba a fonte. O pool cria uma fila: instâncias esperam um slot livre. Com
isso vêm as perguntas de planejamento: quanto tempo a execução leva com 4 slots? E com 8? E vale a
pena ordenar as tarefas, pondo as mais longas primeiro?

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py), implemente `simular_pool(duracoes, slots, maiores_primeiro)`.

```bash
cd modulos/09-orquestracao-airflow/exercicio-09
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — slots como fila de prioridade
Um heap de `(minuto_em_que_fica_livre, numero_do_slot)` — `heapq.heappop` devolve o slot que libera primeiro (e, no empate, o de menor número).
:::
:::{dropdown} Dica 2 — a ordem de entrada
Uma lista de índices: a original, ou ordenada por `(-duracao, indice)` se `maiores_primeiro`. Guarde o início em `inicio[i]` para devolver na ordem original.
:::
:::{dropdown} Dica 3 — o total
É o maior `inicio + duracao` entre todas as instâncias.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import heapq


def simular_pool(duracoes: list, slots: int, maiores_primeiro: bool = False) -> dict:
    if slots < 1:
        raise ValueError("pool precisa de ao menos 1 slot")
    ordem = list(range(len(duracoes)))
    if maiores_primeiro:
        ordem.sort(key=lambda i: (-duracoes[i], i))
    livres = [(0, s) for s in range(slots)]
    heapq.heapify(livres)
    inicio = [0] * len(duracoes)
    total = 0
    for i in ordem:
        t, s = heapq.heappop(livres)
        inicio[i] = t
        fim = t + duracoes[i]
        total = max(total, fim)
        heapq.heappush(livres, (fim, s))
    return {"inicio": inicio, "total": total}
```
Com 2 slots, o arquivo de 25 minutos entra tarde (minuto 9) e a execução termina no 34. Pondo os
maiores primeiro, ele começa no minuto 0 e o total cai para 31 — o *longest processing time first*, uma
heurística simples e muito boa para esse tipo de fila. Com 8 slots, o total bate no piso: nenhuma
paralelização termina antes do arquivo mais longo.

No Airflow, o `priority_weight` controla essa ordem dentro do pool, e o tamanho do pool é uma decisão
de capacidade da **fonte**, não do Airflow: mais slots só ajudam se o banco aguentar as conexões.
:::

---
**Revisado em:** 2026-09-30
