-- Model de STAGING: limpe/padronize a fonte crua (1:1, sem regra de negócio).
-- Colunas finais esperadas:
--   pedido_id (integer)  <- id
--   cliente              <- cliente
--   estado               <- uf em MAIÚSCULA
--   valor (numeric)      <- valor_str convertido
--
-- Complete o SELECT e rode o build (ver enunciado). O source já está declarado em sources.yml.

select
    -- SEU CÓDIGO AQUI (pedido_id, cliente, estado, valor)
    id as pedido_id
from {{ source('olist', 'raw_pedidos') }}
