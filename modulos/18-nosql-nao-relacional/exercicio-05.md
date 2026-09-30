# Exercício 05 — Série temporal: rollup, reagregação e retenção

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Contexto
Um sensor que reporta a cada 10 segundos gera 3,1 milhões de pontos por ano. Mil sensores, 3
bilhões. Por isso todo banco de série temporal (teoria 03) tem uma **política de retenção**: o dado
recente fica **bruto**; o antigo vira **rollup** (n, mínimo, máximo, média por minuto → por hora →
por dia) e o bruto é apagado.

Depois que o bruto some, o banco só consegue descer de resolução **combinando rollups** — e aí
mora a armadilha clássica: **média de médias está errada** quando os buckets têm quantidades
diferentes de pontos. No exemplo dos testes, ela diria 23,0 °C para a primeira hora; o correto é
21,33 °C.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente:

1. **`rollup(pontos, bucket_seg)`** — n/min/max/média por bucket.
2. **`reagregar(rollups, bucket_seg)`** — rollup fino → grosso, **sem** os pontos brutos.
3. **`aplicar_retencao(pontos, agora, janela_bruta_seg, bucket_seg)`** — separa o que fica bruto do
   que vira rollup.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — acumule a soma, não a média
No `rollup`, guarde `n`, `min`, `max` e **`soma`** por bucket; só calcule `media = soma / n` na saída.
Para a ordem das chaves, monte o dict final a partir de `sorted(acc.items())`.
:::
:::{dropdown} Dica 2 — reagregar é média ponderada
Cada bucket fino contribui com `media * n` para a soma do grosso, e `n` para a contagem. Mínimo e
máximo combinam direto (`min` dos mínimos, `max` dos máximos).
:::
:::{dropdown} Dica 3 — retenção
`corte = agora - janela_bruta_seg`. Recentes: `ts >= corte` (ordenados). Antigos: o resto, passados
por `rollup`. O teste confere que a soma dos `n` + os recentes dá o total — nada some sem rastro.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def rollup(pontos, bucket_seg):
    if bucket_seg <= 0:
        raise ValueError("bucket inválido")
    acc = {}
    for ts, v in pontos:
        ini = ts // bucket_seg * bucket_seg
        a = acc.setdefault(ini, {"n": 0, "min": v, "max": v, "soma": 0})
        a["n"] += 1
        a["min"] = min(a["min"], v)
        a["max"] = max(a["max"], v)
        a["soma"] += v
    return {ini: {"n": a["n"], "min": a["min"], "max": a["max"], "media": round(a["soma"] / a["n"], 2)}
            for ini, a in sorted(acc.items())}

def reagregar(rollups, bucket_seg):
    if bucket_seg <= 0:
        raise ValueError("bucket inválido")
    acc = {}
    for ini_fino, r in rollups.items():
        ini = ini_fino // bucket_seg * bucket_seg
        a = acc.setdefault(ini, {"n": 0, "min": r["min"], "max": r["max"], "soma": 0})
        a["n"] += r["n"]
        a["min"] = min(a["min"], r["min"])
        a["max"] = max(a["max"], r["max"])
        a["soma"] += r["media"] * r["n"]          # média PONDERADA: nunca média de médias
    return {ini: {"n": a["n"], "min": a["min"], "max": a["max"], "media": round(a["soma"] / a["n"], 2)}
            for ini, a in sorted(acc.items())}

def aplicar_retencao(pontos, agora, janela_bruta_seg, bucket_seg):
    corte = agora - janela_bruta_seg
    recentes = sorted(p for p in pontos if p[0] >= corte)
    antigos = [p for p in pontos if p[0] < corte]
    return recentes, rollup(antigos, bucket_seg)
```
**Detalhe de produção:** como o rollup guarda a média **arredondada**, cada reagregação acumula um
pouco de erro. TSDBs de verdade guardam **soma e contagem** (não a média) exatamente por isso — a
média é calculada na leitura. Mediana e percentis são piores: **não** se reagregam a partir de
rollups; exigem estruturas próprias (sketches como t-digest).

Compare com o exercício 05 do M17: lá as janelas são decididas **enquanto** os eventos chegam
(watermark); aqui o dado já está gravado e a questão é **quanto** dele guardar.
:::

---
**Revisado em:** 2026-09-29
