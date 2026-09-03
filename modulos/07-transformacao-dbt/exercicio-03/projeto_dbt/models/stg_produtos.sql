-- Staging JÁ PRONTO (referência): produtos.
select
    produto_id,
    categoria
from {{ ref('raw_produtos') }}
