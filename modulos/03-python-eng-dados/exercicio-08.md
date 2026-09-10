# Exercicio 08 - Sessionizacao de eventos (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Exercicio **complexo** que aplica a [teoria 07](teoria-07-python-avancado-dados.md).

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py): implemente **`sessionizar`** - Sessionizacao (classico de analytics): eventos = lista de (usuario, timestamp). Por usuario, ordene por timestamp e agrupe em SESSOES: um gap entre eventos consecutivos maior que gap_max inicia uma nova sessao. Retorne {usuario: [tamanhos de cada sessao]}.

```bash
cd modulos/03-python-eng-dados/exercicio-08
pytest -q
```

## Dica
:::{dropdown} Dica
agrupe por usuario, ordene os timestamps; percorra somando na sessao atual enquanto o gap <= gap_max, senao feche e abra outra.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def sessionizar(eventos, gap_max):
    from collections import defaultdict
    por_user = defaultdict(list)
    for u, ts in eventos:
        por_user[u].append(ts)
    res = {}
    for u, tss in por_user.items():
        tss = sorted(tss)
        sessoes = []
        atual = 1
        for i in range(1, len(tss)):
            if tss[i] - tss[i - 1] <= gap_max:
                atual += 1
            else:
                sessoes.append(atual)
                atual = 1
        sessoes.append(atual)
        res[u] = sessoes
    return res
```
:::

---
**Revisado em:** 2026-09-09
