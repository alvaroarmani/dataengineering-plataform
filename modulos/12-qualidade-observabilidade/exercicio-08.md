# Exercício 08 — Faixa esperada aprendida do histórico (IQR)

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Limiar fixo (`valor entre 0 e 10`) só funciona quando alguém sabe a faixa certa — e ela muda com o
tempo. A alternativa robusta (teoria 03) é **aprender a faixa do histórico**: o método do
intervalo interquartil (IQR), o mesmo do boxplot, considera anômalo o que fica além de
1,5 × IQR dos quartis. Diferente de média e desvio-padrão, ele não é arrastado por um único valor
absurdo que já esteja no histórico.

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py), implemente `faixa_iqr(historico, k)` e `pontos_anomalos(serie, janela, k)`.

```bash
cd modulos/12-qualidade-observabilidade/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — quartis prontos
`statistics.quantiles(h, n=4, method="inclusive")` devolve `[Q1, Q2, Q3]`. IQR = Q3 − Q1.
:::
:::{dropdown} Dica 2 — janela móvel
Para cada `i` a partir de `janela`, a referência é `serie[i - janela:i]` — só o passado, nunca o próprio ponto (senão ele puxa a faixa para si).
:::
:::{dropdown} Dica 3 — limites
Use a comparação encadeada `lo <= x <= hi` para "normal"; anômalo é o `not` disso.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from statistics import quantiles


def faixa_iqr(historico: list, k: float = 1.5) -> tuple:
    if len(historico) < 4:
        raise ValueError("histórico curto demais para quartis")
    q1, _, q3 = quantiles(historico, n=4, method="inclusive")
    iqr = q3 - q1
    return round(q1 - k * iqr, 2), round(q3 + k * iqr, 2)


def pontos_anomalos(serie: list, janela: int, k: float = 1.5) -> list:
    anom = []
    for i in range(janela, len(serie)):
        lo, hi = faixa_iqr(serie[i - janela:i], k)
        if not lo <= serie[i] <= hi:
            anom.append(i)
    return anom
```
O segundo teste mostra a robustez: um 500 dentro do histórico mexe o limite superior só de 14,12
para 16,62. Com média ± 3 desvios, o mesmo 500 inflaria o desvio-padrão a ponto de **nenhum** valor
futuro parecer anômalo — o histórico "envenenado" cega o detector.

No teste da janela móvel, o 180 e o 40 são pegos, e o 101 logo depois do 180 **não** vira falso
alarme — o IQR da janela quase não se move com um único ponto extremo. Já o 97 (índice 8) **é**
sinalizado: a janela anterior é tão estável que a faixa fica entre 98,5 e 102,5. É o trade-off do
tamanho da janela e do `k` — janela curta e `k` baixo deixam o detector sensível; calibre olhando
quantos alertas por semana a equipe consegue investigar.
:::

---
**Revisado em:** 2026-09-30
