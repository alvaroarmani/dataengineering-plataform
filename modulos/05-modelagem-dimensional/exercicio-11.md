# Exercício 11 — Star schema com corridas reais de táxi de NY (mini-caso · dados reais)

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python + pandas). **Dados reais:** amostra reproduzível de
2.617 corridas de jan/2024 da TLC de Nova York + a tabela oficial de 265 zonas —
[`datasets/amostras/`](../../datasets/amostras/) (gerada por `datasets/gerar_amostras.py`).

## Contexto
O time de mobilidade quer responder "quanto faturamos por região da cidade?" — **na origem** e **no
destino** da corrida. Você vai montar o star schema mínimo que responde a isso:

```
            dim_zona (role-playing)
           /                      \
 zona_embarque_sk          zona_desembarque_sk
           \                      /
            fato_corridas  (grão: 1 corrida válida)
```

Três armadilhas **reais** (nada foi plantado — estão na base oficial da TLC):

1. **Corridas inválidas:** tarifa negativa (estornos), desembarque *antes* do embarque (relógio do
   taxímetro) e corridas fora do mês do arquivo. Elas não entram na fato.
2. **Atributo nulo na dimensão:** na tabela oficial, a zona 265 ("Outside of NYC") tem borough
   `"N/A"` — e o `pd.read_csv` converte `"N/A"` em **nulo** por padrão. Se você deixar o nulo, o
   `groupby` do pandas **descarta a linha em silêncio** — e a receita dessas corridas some do
   relatório sem erro nenhum.
3. **Role-playing:** a mesma `dim_zona` responde a duas perguntas diferentes, conforme a chave
   estrangeira que você usa para o join.

## Tarefa
Em [`exercicio-11/solucao.py`](exercicio-11/solucao.py), implemente:

1. **`dim_zona(zonas)`** → dimensão com chave substituta `zona_sk` e **nenhum atributo nulo**
   (membro `"Desconhecido"`).
2. **`fato_corridas(corridas, dim)`** → fato no grão de corrida válida, com `data_sk` (AAAAMMDD) e as
   duas FKs de zona.
3. **`receita_por_borough(fato, dim, papel)`** → receita por borough no papel `"embarque"` ou
   `"desembarque"` (outro valor → `ValueError`).

O teste de **reconciliação** exige que a soma por borough bata com o total da fato, nos dois papéis.

```bash
cd modulos/05-modelagem-dimensional/exercicio-11
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — a dimensão
Ordene por `LocationID`, reinicie o índice e gere `zona_sk` com `range(1, n + 1)`. Para os
atributos, `fillna("Desconhecido")`. Confira: `dim.isna().sum()` tem de dar zero em tudo.
:::
:::{dropdown} Dica 2 — a fato
Filtre primeiro (três condições com `&`), depois troque as chaves naturais pelas substitutas com um
lookup: `sk = dim.set_index("location_id")["zona_sk"]` e `c["PULocationID"].map(sk)`. A duração sai de
`(dropoff - pickup).dt.total_seconds() / 60`; `data_sk` sai de `.dt.strftime("%Y%m%d").astype(int)`.
:::
:::{dropdown} Dica 3 — o papel e a reconciliação
O papel só escolhe a coluna do join: `col = f"zona_{papel}_sk"`. Faça `merge` com
`dim[["zona_sk", "borough"]]`, agregue com `.agg(corridas=("viagem_id", "count"),
receita=("valor_total", "sum"))` e ordene com `sort_values(["receita", "borough"],
ascending=[False, True])`. Se a reconciliação falhar, procure nulos na coluna de agrupamento.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import pandas as pd

def dim_zona(zonas):
    d = zonas.sort_values("LocationID").reset_index(drop=True)
    return pd.DataFrame({
        "zona_sk": range(1, len(d) + 1),                  # chave substituta: estável, sem significado
        "location_id": d["LocationID"].astype(int),       # chave natural fica como atributo
        "borough": d["Borough"].fillna("Desconhecido"),   # dimensão nunca tem atributo nulo
        "zona": d["Zone"].fillna("Desconhecido"),
    })

def fato_corridas(corridas, dim):
    c = corridas[
        (corridas["total_amount"] > 0)
        & (corridas["tpep_pickup_datetime"] >= "2024-01-01")
        & (corridas["tpep_pickup_datetime"] < "2024-02-01")          # intervalo semiaberto
        & (corridas["tpep_dropoff_datetime"] >= corridas["tpep_pickup_datetime"])
    ]
    sk = dim.set_index("location_id")["zona_sk"]                     # natural -> substituta
    return pd.DataFrame({
        "viagem_id": c["viagem_id"],
        "data_sk": c["tpep_pickup_datetime"].dt.strftime("%Y%m%d").astype(int),
        "zona_embarque_sk": c["PULocationID"].map(sk),               # mesmo lookup,
        "zona_desembarque_sk": c["DOLocationID"].map(sk),            # dois papéis
        "passageiros": c["passenger_count"],
        "distancia": c["trip_distance"],
        "valor_total": c["total_amount"],
        "gorjeta": c["tip_amount"],
        "duracao_min": ((c["tpep_dropoff_datetime"] - c["tpep_pickup_datetime"])
                        .dt.total_seconds() / 60).round(2),
    }).sort_values("viagem_id").reset_index(drop=True)

def receita_por_borough(fato, dim, papel):
    if papel not in ("embarque", "desembarque"):
        raise ValueError("papel deve ser 'embarque' ou 'desembarque'")
    col = f"zona_{papel}_sk"
    j = fato.merge(dim[["zona_sk", "borough"]], left_on=col, right_on="zona_sk")
    g = (j.groupby("borough")
          .agg(corridas=("viagem_id", "count"), receita=("valor_total", "sum"))
          .reset_index())
    g["receita"] = g["receita"].round(2)
    return g.sort_values(["receita", "borough"], ascending=[False, True]).reset_index(drop=True)
```

**Por que isso importa:** no destino, o membro "Desconhecido" (corridas que **saem** de Nova York)
é o **2º maior** borough em receita — US$ 6.000 em só 18 corridas, porque são as mais longas. Com o
nulo na dimensão, essa linha simplesmente não apareceria no relatório. É exatamente o erro que um
teste de reconciliação (soma dos grupos = total da fato) pega — e que, no M07, vira um teste de dbt.

Repare também que a base oficial tem **dois** "desconhecidos" diferentes: a zona 264 (borough
`"Unknown"`, zona `"N/A"`) e a 265 (borough `"N/A"`). O nulo nasceu **na leitura**, não na fonte —
por isso vale sempre olhar o arquivo bruto antes de confiar no DataFrame. Numa empresa, você decidiria com o negócio se
os dois viram um membro só — é decisão de modelagem, não de código.
:::

---
**Revisado em:** 2026-09-29
