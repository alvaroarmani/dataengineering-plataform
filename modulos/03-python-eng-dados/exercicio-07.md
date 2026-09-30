# Exercício 07 — Estatísticas em uma passada (streaming de verdade)

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
A teoria 07 mostra por que generators importam: um arquivo de 50 GB não cabe na memória, então ele
é lido **uma vez**, linha a linha. Toda estatística que você quiser tem de ser calculada nessa única
passada — sem guardar a lista para depois.

Contagem, soma, mínimo e máximo são fáceis. **Média e desvio-padrão** também parecem ("soma dos
quadrados menos o quadrado da soma"), mas essa fórmula **perde precisão** quando os valores são
grandes e parecidos (timestamps em milissegundos, valores em centavos acumulados) — o resultado pode
até sair negativo. O algoritmo de **Welford** atualiza média e variância a cada valor, de forma
estável.

## Tarefa
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py), implemente `agrega_stream(eventos)`.

```bash
cd modulos/03-python-eng-dados/exercicio-07
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — uma passada, um dict
Para cada chave, guarde num dict os acumuladores: `n`, `soma`, `min`, `max`, `media` e `m2`. Não guarde a lista de valores — o teste com `UmaVez` quebra se você tentar percorrer duas vezes.
:::
:::{dropdown} Dica 2 — Welford
A cada valor: `n += 1`, `delta = x - media`, `media += delta / n`, `m2 += delta * (x - media)` (repare: o segundo fator usa a média **já atualizada**).
:::
:::{dropdown} Dica 3 — o final
Desvio populacional = `sqrt(m2 / n)`. Monte a saída só no fim, sem o `m2`, arredondando média e desvio.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import math


def agrega_stream(eventos) -> dict:
    est = {}
    for chave, x in eventos:
        if x is None:
            continue
        e = est.setdefault(chave, {"n": 0, "soma": 0, "min": x, "max": x, "media": 0.0, "m2": 0.0})
        e["n"] += 1
        e["soma"] += x
        e["min"] = min(e["min"], x)
        e["max"] = max(e["max"], x)
        delta = x - e["media"]
        e["media"] += delta / e["n"]
        e["m2"] += delta * (x - e["media"])
    return {k: {"n": e["n"], "soma": e["soma"], "min": e["min"], "max": e["max"],
                "media": round(e["media"], 4), "desvio": round(math.sqrt(e["m2"] / e["n"]), 4)}
            for k, e in est.items()}
```
Para ver o problema que Welford resolve, rode no terminal a fórmula ingênua com os timestamps do
terceiro teste:
```python
xs = [1_700_000_000_000 + d for d in (1, 2, 3, 4)]
n = len(xs); s = sum(xs); s2 = sum(x * x for x in xs)
print(s2 / n - (s / n) ** 2)      # deveria ser 1.25 — imprime 0.0
```
Os quadrados têm ~25 dígitos, mais do que um `float` guarda (~16); a diferença entre dois números
enormes quase iguais vira ruído — aqui, zero; com outros valores, pode até sair **negativa**. Welford trabalha com desvios em relação à média
corrente — números pequenos — e por isso é o algoritmo usado em bancos de dados e em bibliotecas de
estatística. É também a base do check de anomalia por z-score (M12).
:::

---
**Revisado em:** 2026-09-30
