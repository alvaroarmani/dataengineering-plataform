# Exercício 05 — Teste de integridade referencial (TRACK REAL · dbt)

**Onde roda:** 🐳 Bancada Docker (dbt real). O grader estrutural também roda no navegador.
Sem bancada? Veja também o [Exercício 06](exercicio-06.md) (a lógica do `relationships` em Python).

O projeto em [`exercicio-05/projeto_dbt/`](exercicio-05/projeto_dbt/) tem `dim_produto` e
`fct_itens` prontos. Falta **declarar o teste** que garante que todo `produto_id` do fato
existe na dimensão.

## Tarefa
Em [`projeto_dbt/models/schema.yml`](exercicio-05/projeto_dbt/models/schema.yml), adicione em
`fct_itens.produto_id` um teste **`relationships`** apontando para `ref('dim_produto')`,
`field: produto_id`.

```bash
# grader estrutural (confere que o teste foi declarado):
pytest -q modulos/07-transformacao-dbt/exercicio-05
# na bancada, rode o teste de verdade contra os dados:
cd ambiente && docker compose up -d
docker compose --profile dbt run --rm dbt build \
  --project-dir  modulos/07-transformacao-dbt/exercicio-05/projeto_dbt \
  --profiles-dir modulos/07-transformacao-dbt/exercicio-05/projeto_dbt
```
✅ *Verde:* o `dbt build` roda o teste `relationships` e passa (os dados são íntegros). Se um
item apontasse para um produto inexistente, o teste **falharia** — que é o ponto.

## Dicas progressivas
:::{dropdown} Dica 1 — a sintaxe
```yaml
- name: produto_id
  tests:
    - relationships:
        to: ref('dim_produto')
        field: produto_id
```
:::
:::{dropdown} Dica 2 — por que importa
Sem `relationships`, um fato "órfão" (FK inexistente) passa silencioso e some do join com a dimensão.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```yaml
      - name: produto_id
        tests:
          - relationships:
              to: ref('dim_produto')
              field: produto_id
```
`relationships` é o teste de **integridade referencial** do dbt: por baixo, ele roda uma query
que busca `produto_id` do fato ausentes na dimensão; 0 linhas = passa. Combinado com
`unique`+`not_null` na chave da dimensão, garante joins corretos.
:::

---
**Revisado em:** 2026-08-24
