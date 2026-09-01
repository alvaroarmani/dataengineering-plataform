-- fato (gold), grão = 1 linha por pedido. TODO: junte à dim_produto e calcule receita.
select
    -- SEU CÓDIGO AQUI: pedido_id, produto_sk, cliente_id, quantidade, valor*quantidade as receita
    pedido_id
from {{ ref('stg_pedidos') }}
