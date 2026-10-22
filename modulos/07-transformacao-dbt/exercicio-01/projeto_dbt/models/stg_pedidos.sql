-- Model de STAGING: limpe/padronize a fonte crua (1:1, sem regra de negócio).
-- Colunas finais esperadas:
--   pedido_id (integer)  <- id
--   cliente              <- cliente
--   estado               <- uf sem espaços nas pontas e em MAIÚSCULA
--   valor (numeric)      <- valor_str convertido
--
-- Complete o SELECT e rode o build (ver enunciado). A fonte crua é o seed raw_pedidos: leia com ref().

select
    -- SEU CÓDIGO AQUI (pedido_id, cliente, estado, valor)
    id as pedido_id
from {{ ref('raw_pedidos') }}
