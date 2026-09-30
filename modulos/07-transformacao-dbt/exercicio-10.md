# Exercício 10 — Watermark incremental: a linha perdida no empate e o lookback

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro — é o filtro do `is_incremental()`).

## Contexto
O filtro clássico de um modelo incremental é `where updated_at > (select max(updated_at) from {{ this }})`
— o **watermark** (teoria 05). Ele tem uma falha sutil: se chegam duas linhas com o **mesmo**
`updated_at` e só uma estava na carga anterior, a outra é **perdida para sempre** (ela não é `>` o
watermark). O mesmo acontece com dados que chegam atrasados, com `updated_at` antigo.

A solução usada em produção é o **lookback**: reprocessar uma pequena janela antes do watermark
(`> max - intervalo`) e contar com o `merge` idempotente (exercício 09) para não duplicar nada.

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py), implemente `selecionar_incremental(linhas, watermark, lookback)` e `simular_cargas(chegadas, lookback)`.

```bash
cd modulos/07-transformacao-dbt/exercicio-10
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — o corte
Com `watermark` `None`, pegue tudo. Senão, o corte é `watermark - lookback` e a condição é `updated_at > corte`.
:::
:::{dropdown} Dica 2 — o novo watermark
É o maior entre o watermark antigo e os `updated_at` selecionados — com lookback, você pode selecionar linhas **abaixo** do watermark, e ele não pode andar para trás.
:::
:::{dropdown} Dica 3 — simular
Mantenha a fonte acumulada, o watermark e um `set` de ids no destino (o set faz o papel do merge idempotente).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def selecionar_incremental(linhas: list, watermark, lookback: int = 0) -> tuple:
    if lookback < 0:
        raise ValueError("lookback negativo")
    corte = None if watermark is None else watermark - lookback
    sel = [r for r in linhas if corte is None or r["updated_at"] > corte]
    candidatos = [r["updated_at"] for r in sel] + ([] if watermark is None else [watermark])
    return sel, (max(candidatos) if candidatos else None)


def simular_cargas(chegadas: list, lookback: int) -> set:
    fonte, destino, wm = [], set(), None
    for lote in chegadas:
        fonte += lote
        sel, wm = selecionar_incremental(fonte, wm, lookback)
        destino |= {r["id"] for r in sel}
    return destino
```
Sem lookback, o destino termina **sem os ids 11 e 12**: o 11 tem o mesmo `updated_at` (100) que a
carga anterior já tinha visto, e o 12 chegou com um `updated_at` antigo (98). Nenhum erro, nenhum
alerta — só dados faltando, descobertos meses depois numa reconciliação (M12).

Com um lookback de 5, a segunda carga reprocessa a janela 95–100 e pega os dois. O custo é reler um
pouco de dado a cada execução; por isso o lookback só é seguro com um `merge` idempotente por chave
(exercício 09) — com `append`, ele **duplicaria** as linhas relidas. No dbt, é comum escrever
`where updated_at > (select max(updated_at) from {{ this }}) - interval '3 days'`.
:::

---
**Revisado em:** 2026-09-30
