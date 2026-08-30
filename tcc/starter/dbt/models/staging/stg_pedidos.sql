-- Staging (silver): padroniza e tipa a fonte raw. Sem joins pesados aqui.
-- TODO: repita o padrão para cada fonte (customers, products, sellers, reviews...).
with fonte as (
    select * from {{ source('raw', 'raw_orders') }}
)
select
    order_id                                as pedido_id,
    customer_id                             as cliente_id,
    order_status                            as status,
    cast(order_purchase_timestamp as date)  as data_compra,
    cast(order_delivered_customer_date as date) as data_entrega
from fonte
