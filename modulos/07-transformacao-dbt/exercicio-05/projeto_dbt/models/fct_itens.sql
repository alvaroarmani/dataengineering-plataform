-- Fato no grão do item (referência).
select
    item_id,
    produto_id,
    price
from {{ ref('stg_itens') }}
