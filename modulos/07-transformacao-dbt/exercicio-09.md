# Exercício 09 — Merge incremental: dado atrasado, duplicata no lote e exclusão lógica

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro — é o que o `merge` do dbt faz no warehouse).

## Contexto
Um modelo dbt `incremental` com estratégia `merge` (teoria 05) faz *upsert* do lote novo na tabela
de destino pela `unique_key`. Três situações reais quebram a versão ingênua:

1. **Dado atrasado:** chega uma versão **mais antiga** de um registro que já foi atualizado — ela não
   pode sobrescrever a nova.
2. **Duplicata no lote:** a fonte manda a mesma chave duas vezes no mesmo lote. No warehouse, o
   `MERGE` falha com "mais de uma linha de origem para a mesma linha de destino" — é preciso
   deduplicar **antes**, ficando com a versão mais recente.
3. **Exclusão lógica:** a fonte marca `_deleted = True`; o registro precisa sair do destino.

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py), implemente `merge_incremental(destino, lote, chave)`.

```bash
cd modulos/07-transformacao-dbt/exercicio-09
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — deduplique primeiro
Percorra o lote guardando, por chave, o registro de maior `updated_at` (use `>=` para que, no empate, o último vença).
:::
:::{dropdown} Dica 2 — destino como dict
`final = {r[chave]: dict(r) for r in destino}` — cópias, para não mexer na entrada. Para cada registro deduplicado, ignore se for mais antigo que o do destino.
:::
:::{dropdown} Dica 3 — exclusão
Se o registro vencedor tiver `_deleted`, remova a chave (`pop(k, None)` tolera chave inexistente); senão, grave sem o campo `_deleted`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def merge_incremental(destino: list, lote: list, chave: str) -> list:
    ultimo = {}
    for r in lote:
        k = r[chave]
        if k not in ultimo or r["updated_at"] >= ultimo[k]["updated_at"]:
            ultimo[k] = r
    final = {r[chave]: dict(r) for r in destino}
    for k, r in ultimo.items():
        atual = final.get(k)
        if atual is not None and r["updated_at"] < atual["updated_at"]:
            continue
        if r.get("_deleted"):
            final.pop(k, None)
        else:
            final[k] = {c: v for c, v in r.items() if c != "_deleted"}
    return [final[k] for k in sorted(final)]
```
No dbt, isso corresponde a:
```sql
{{ config(materialized='incremental', unique_key='id', incremental_strategy='merge') }}
select * from (
  select *, row_number() over (partition by id order by updated_at desc) as rn
  from {{ ref('stg_pedidos') }}
  {% if is_incremental() %} where updated_at > (select max(updated_at) from {{ this }}) {% endif %}
) where rn = 1
```
O `row_number ... rn = 1` é a deduplicação do lote — sem ela, o `MERGE` do warehouse falha. A proteção
contra atrasados e as exclusões lógicas costumam ir numa cláusula `merge_update_columns` / num
`post_hook`, ou no modelo seguinte.

O teste de idempotência é o critério que torna o incremental seguro: rodar o mesmo lote duas vezes
(um retry do Airflow, M09) não muda o resultado.
:::

---
**Revisado em:** 2026-09-30
