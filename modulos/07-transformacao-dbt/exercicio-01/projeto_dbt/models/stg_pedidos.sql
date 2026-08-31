select
    cast(id as integer) as pedido_id,
    cliente,
    upper(uf) as estado,
    cast(valor_str as numeric) as valor
from {{ source('olist', 'raw_pedidos') }}
