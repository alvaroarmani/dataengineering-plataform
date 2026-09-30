# Exercício 09 — Qualidade de dados em corridas reais (mini-caso · dados reais)

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python + pandas). **Dados reais:** 2.617 corridas de táxi
de Nova York de janeiro/2024, da TLC (Taxi & Limousine Commission) —
[`datasets/amostras/nyc_taxi_2024_01_amostra.csv`](../../datasets/amostras/nyc_taxi_2024_01_amostra.csv).

## Contexto
Você recebeu o lote de corridas do mês para carregar no warehouse. Antes de carregar, o time exige um
**portão de qualidade**: perfilar os problemas, separar o que é inválido numa **quarentena** (com o
motivo) e só aprovar o lote se a taxa de inválidos estiver dentro do limite.

Nada aqui é inventado: o arquivo oficial da TLC tem **37 mil tarifas negativas, 140 mil corridas
sem nº de passageiros, corridas que terminam antes de começar e registros de outro mês**. A amostra
preserva exemplos reais de cada um.

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py), implemente:

1. **`perfilar(df)`** → `{regra: nº de linhas que violam}` para as 5 regras (cada regra conta de
   forma independente).
2. **`separar_quarentena(df)`** → `(validas, quarentena)`; a quarentena ganha a coluna `motivo` = a
   regra de **maior prioridade** violada.
3. **`aprovar_lote(df, max_invalidos_pct)`** → `True` se o % em quarentena ≤ limite (lote vazio passa).

| Prioridade | Regra | Condição |
|---|---|---|
| 1 | `fora_do_periodo` | embarque fora de jan/2024 |
| 2 | `desembarque_antes_embarque` | `tpep_dropoff_datetime < tpep_pickup_datetime` |
| 3 | `tarifa_negativa` | `fare_amount < 0` |
| 4 | `passageiros_invalidos` | `passenger_count` nulo **ou** ≤ 0 |
| 5 | `distancia_absurda` | `trip_distance > 100` |

```bash
cd modulos/12-qualidade-observabilidade/exercicio-09
pytest -q
```

## Para pensar (depois de passar)
Rode `perfilar` só no `VendorID == 2`: **todas** as tarifas negativas e corridas fora do período vêm
de um único fornecedor. Isso muda a ação — em vez de "limpar o dado", você **abre um chamado com a
fonte**. Qualidade de dados é, muitas vezes, um problema de *contrato com quem produz* (M12, teoria 04).

## Dicas progressivas
:::{dropdown} Dica 1 — uma regra = uma máscara booleana
Escreva cada regra como uma função que recebe o `df` e devolve uma `Series` booleana. Com uma lista
`[(nome, regra), ...]` na ordem de prioridade, `perfilar` vira um loop somando cada máscara.
Atenção: `passenger_count` tem nulos — use `.isna()` além de `<= 0`.
:::
:::{dropdown} Dica 2 — o motivo de maior prioridade
Crie uma `Series` de motivos vazia (`pd.NA`). Percorra as regras **da menor para a maior prioridade**
e use `motivo.mask(mascara, nome)`: quem vem por último (a de maior prioridade) sobrescreve.
:::
:::{dropdown} Dica 3 — dividir e aprovar
`quarentena = df[motivo.notna()]` (com `.assign(motivo=...)`), `validas = df[motivo.isna()]`, ambas com
`reset_index(drop=True)`. No portão, trate o lote vazio **antes** de dividir por `len(df)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import pandas as pd

REGRAS = [  # a ordem da lista É a prioridade
    ("fora_do_periodo", lambda d: (d["tpep_pickup_datetime"] < "2024-01-01")
                                  | (d["tpep_pickup_datetime"] >= "2024-02-01")),
    ("desembarque_antes_embarque", lambda d: d["tpep_dropoff_datetime"] < d["tpep_pickup_datetime"]),
    ("tarifa_negativa", lambda d: d["fare_amount"] < 0),
    ("passageiros_invalidos", lambda d: d["passenger_count"].isna() | (d["passenger_count"] <= 0)),
    ("distancia_absurda", lambda d: d["trip_distance"] > 100),
]

def perfilar(df):
    return {nome: int(regra(df).sum()) for nome, regra in REGRAS}

def separar_quarentena(df):
    motivo = pd.Series(pd.NA, index=df.index, dtype="object")
    for nome, regra in reversed(REGRAS):      # a de maior prioridade é aplicada por último
        motivo = motivo.mask(regra(df), nome)
    quarentena = df[motivo.notna()].assign(motivo=motivo[motivo.notna()])
    validas = df[motivo.isna()]
    return validas.reset_index(drop=True), quarentena.reset_index(drop=True)

def aprovar_lote(df, max_invalidos_pct):
    if len(df) == 0:
        return True                           # nada a reprovar
    _, q = separar_quarentena(df)
    return 100 * len(q) / len(df) <= max_invalidos_pct
```
Repare que as regras viraram **dados** (uma lista): adicionar uma regra nova não muda o resto do
código — é assim que frameworks como Great Expectations e testes do dbt organizam validações.
:::

---
**Revisado em:** 2026-09-29
