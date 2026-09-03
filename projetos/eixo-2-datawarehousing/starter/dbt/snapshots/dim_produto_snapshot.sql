-- SCD Tipo 2 da categoria do produto (via snapshot dbt). TODO: ajuste a fonte de histórico.
{% snapshot dim_produto_snapshot %}
{{ config(target_schema='snapshots', unique_key='produto_id',
          strategy='check', check_cols=['categoria']) }}
select produto_id, categoria from {{ ref('raw_produtos') }}
{% endsnapshot %}
