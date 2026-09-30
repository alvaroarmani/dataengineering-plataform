# Exercício 08 — Schema enforcement x schema evolution no Delta

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Uma tabela Delta **recusa** escritas cujo schema não bate com o da tabela (teoria 04, *schema
enforcement*): é o que impede um job com bug de gravar `valor` como texto e envenenar a tabela. Quando a
mudança é intencional — uma coluna nova —, a escrita pode pedir **evolução** com
`.option("mergeSchema", "true")`, e o schema da tabela ganha a coluna.

Mas nem `mergeSchema` aceita tudo: **mudar o tipo** de uma coluna existente continua sendo recusado
(exceto alargamentos seguros), e colunas que faltam no DataFrame viram `null` — o que só é aceitável
se a coluna for anulável.

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py), implemente `validar_escrita(tabela, df, merge_schema)`.

```bash
cd modulos/11-spark-lakehouse/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — colunas do df
Para cada coluna do DataFrame: se existe na tabela, compare tipos (aceite só igual ou `(df, tabela)` em `ALARGAMENTOS`); se não existe, só passa com `merge_schema`.
:::
:::{dropdown} Dica 2 — colunas da tabela
As que faltam no DataFrame precisam ser anuláveis — senão, recusa.
:::
:::{dropdown} Dica 3 — schema final
Só muda se a escrita foi aceita **e** `merge_schema` está ligado: acrescente as colunas novas como anuláveis. Devolva uma cópia.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
ALARGAMENTOS = {("int", "long"), ("float", "double"), ("int", "double")}


def validar_escrita(tabela: dict, df: dict, merge_schema: bool = False) -> dict:
    motivos = []
    for col, tipo_df in df.items():
        if col in tabela:
            tipo_tab = tabela[col]["tipo"]
            if tipo_tab != tipo_df and (tipo_df, tipo_tab) not in ALARGAMENTOS:
                motivos.append(f"tipo:{col}")
        elif not merge_schema:
            motivos.append(f"nova:{col}")
    for col, regra in tabela.items():
        if col not in df and not regra["nulo"]:
            motivos.append(f"obrigatoria:{col}")
    aceita = not motivos
    final = {c: dict(r) for c, r in tabela.items()}
    if aceita and merge_schema:
        for col, tipo_df in df.items():
            if col not in final:
                final[col] = {"tipo": tipo_df, "nulo": True}
    return {"aceita": aceita, "motivos": sorted(motivos), "schema_final": final}
```
O teste `mudanca_de_tipo_recusada_mesmo_com_merge` é a proteção que importa: `mergeSchema` é uma
permissão para **adicionar**, não para reinterpretar. Transformar `valor` de `double` em `string`
quebraria todas as consultas e agregações existentes — no Delta, isso exige reescrever a tabela
explicitamente (`overwriteSchema`), uma decisão consciente.

O DataFrame com `int` numa coluna `long` entra porque o valor cabe sem perda; o contrário
(`long` numa coluna `int`) não. É a mesma regra de compatibilidade do schema drift na ingestão (M08) e
do versionamento de contratos (M23) — agora aplicada no armazenamento.
:::

---
**Revisado em:** 2026-09-30
