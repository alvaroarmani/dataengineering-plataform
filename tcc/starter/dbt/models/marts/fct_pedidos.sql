-- Fato (gold). Grão: UM item de pedido. TODO: junte as staging e as dimensões.
with itens as (
    select * from {{ source('raw', 'raw_order_items') }}
),
pedidos as (
    select * from {{ ref('stg_pedidos') }}
)
select
    i.order_id      as pedido_id,
    i.order_item_id as item_id,
    i.product_id    as produto_id,
    i.seller_id     as vendedor_id,
    p.cliente_id,
    p.data_compra,
    -- medidas
    i.price         as valor,
    i.freight_value as frete,
    1               as quantidade,
    (p.data_entrega - p.data_compra) as tempo_entrega_dias
from itens i
left join pedidos p on p.pedido_id = i.order_id
