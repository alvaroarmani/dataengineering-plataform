-- SCD Tipo 2 (requisito do TCC) via snapshot do dbt.
-- Mantém histórico da categoria do produto ao longo do tempo.
-- TODO: aponte para sua staging de produtos e ajuste as colunas.
{% snapshot dim_produto_snapshot %}
{{
    config(
        target_schema='snapshots',
        unique_key='produto_id',
        strategy='check',
        check_cols=['categoria']
    )
}}
select
    product_id                       as produto_id,
    product_category_name            as categoria
from {{ source('raw', 'raw_products') }}
{% endsnapshot %}
