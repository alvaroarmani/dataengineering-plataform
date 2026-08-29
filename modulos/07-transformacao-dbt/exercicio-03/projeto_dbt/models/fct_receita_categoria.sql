{{ config(materialized='table') }}

-- MART (você completa): receita por categoria.
-- Junte os DOIS staging models com ref() (nunca a fonte crua) por produto_id,
-- e some price por categoria. Colunas finais: categoria, receita.

-- SEU CÓDIGO AQUI
-- Dica: from {{ ref('stg_itens') }} i join {{ ref('stg_produtos') }} p on i.produto_id = p.produto_id
select
    p.categoria,
    0 as receita   -- troque pela agregação correta
from {{ ref('stg_produtos') }} p
group by p.categoria
