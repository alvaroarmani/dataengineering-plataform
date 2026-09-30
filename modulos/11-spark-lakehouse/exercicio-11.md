# Exercício 11 — Skew: detectar e dividir partições como o AQE

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Um stage só termina quando a tarefa **mais lenta** termina (teoria 05). Com *skew*, uma partição tem
10× o tamanho das outras e o job inteiro espera por ela. O **AQE** (Adaptive Query Execution) do Spark
detecta isso em tempo de execução, depois do shuffle, quando já conhece o tamanho real de cada
partição: uma partição é considerada *skewed* se for maior que **fator × a mediana** **e** maior que um
**limiar absoluto** (nos padrões do Spark 3.5, 5× e 256 MB — confira a documentação da sua versão). As
partições skewed são **divididas** em pedaços próximos do tamanho alvo.

## Tarefa
Em [`exercicio-11/solucao.py`](exercicio-11/solucao.py), implemente `particoes_skewed(tamanhos_mb, fator, limiar_mb)` e `dividir_skew(tamanhos_mb, fator, limiar_mb, alvo_mb)`.

```bash
cd modulos/11-spark-lakehouse/exercicio-11
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — mediana, não média
`statistics.median`: a partição gigante puxaria a média para cima e esconderia a si mesma.
:::
:::{dropdown} Dica 2 — dois critérios
Relativo (`> fator * mediana`) **e** absoluto (`> limiar_mb`): dividir uma partição de 200 MB não compensa o overhead.
:::
:::{dropdown} Dica 3 — dividir
Para cada skewed, `k = ceil(tamanho / alvo)` pedaços de `tamanho / k`, no lugar da original.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import math
from statistics import median


def particoes_skewed(tamanhos_mb: list, fator: float = 5, limiar_mb: float = 256) -> list:
    if not tamanhos_mb:
        return []
    m = median(tamanhos_mb)
    return [i for i, t in enumerate(tamanhos_mb) if t > fator * m and t > limiar_mb]


def dividir_skew(tamanhos_mb: list, fator: float = 5, limiar_mb: float = 256, alvo_mb: float = 128) -> dict:
    skew = set(particoes_skewed(tamanhos_mb, fator, limiar_mb))
    nova = []
    for i, t in enumerate(tamanhos_mb):
        if i in skew:
            k = math.ceil(t / alvo_mb)
            nova += [round(t / k, 1)] * k
        else:
            nova.append(t)
    return {"particoes": nova, "maior_antes": max(tamanhos_mb) if tamanhos_mb else 0,
            "maior_depois": max(nova) if nova else 0}
```
A partição de 2 GB vira 16 pedaços de 125 MB, e a maior partição do stage passa a ser a de 130 MB: o
stage termina no tempo de uma tarefa normal, em vez de esperar uma tarefa 15× mais longa. É o que o AQE
faz sozinho num *skew join* — por isso a recomendação da teoria é simplesmente **ligá-lo**
(`spark.sql.adaptive.enabled`, já ligado por padrão nas versões recentes).

O critério absoluto evita trabalho inútil: dividir uma partição de 200 MB em pedaços custa mais em
agendamento do que economiza. Quando o AQE não resolve (skew antes do shuffle, ou uma chave `null`
dominante), entram o *salting* e o tratamento separado da chave problemática.
:::

---
**Revisado em:** 2026-09-30
