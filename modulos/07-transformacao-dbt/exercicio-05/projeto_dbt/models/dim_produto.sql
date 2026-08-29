-- Dimensão de produto (referência): 1 linha por produto.
select distinct
    produto_id,
    categoria
from {{ source('olist', 'raw_produtos') }}
