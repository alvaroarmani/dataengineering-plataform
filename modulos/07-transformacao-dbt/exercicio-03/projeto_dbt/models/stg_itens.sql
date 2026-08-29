-- Staging JÁ PRONTO (referência): limpeza 1:1 dos itens.
select
    cast(item_id as integer)   as item_id,
    produto_id,
    cast(price_str as numeric) as price
from {{ source('olist', 'raw_itens') }}
