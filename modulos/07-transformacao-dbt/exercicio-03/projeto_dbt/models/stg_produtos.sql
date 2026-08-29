-- Staging JÁ PRONTO (referência): produtos.
select
    produto_id,
    categoria
from {{ source('olist', 'raw_produtos') }}
