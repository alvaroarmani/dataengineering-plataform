-- staging (silver): tipe e padronize. TODO: complete o SELECT.
select
    -- SEU CÓDIGO AQUI: pedido_id (int), cliente_id, produto_id, quantidade (int), valor (numeric)
    pedido_id
from {{ ref('raw_pedidos') }}
