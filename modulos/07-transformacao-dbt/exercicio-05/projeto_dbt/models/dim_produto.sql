-- Dimensão de produto (referência): 1 linha por produto.
select distinct
    produto_id,
    categoria
from {{ ref('raw_produtos') }}
