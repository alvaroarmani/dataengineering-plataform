# Exercício 07 — A lógica de um snapshot SCD2 (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Um snapshot do dbt versiona o que **mudou**. Implemente a detecção que a `check strategy` faz
por baixo — assim você entende o que o `dbt snapshot` automatiza.

## Tarefas
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py) (entradas são dicts `{chave: atributo}`):

- **`detectar_mudancas(atual, incoming)`** — chaves nos dois cujo atributo **mudou** (nova versão), ordenadas.
- **`detectar_novos(atual, incoming)`** — chaves só em `incoming` (entidades novas), ordenadas.

```bash
cd modulos/07-transformacao-dbt/exercicio-07
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — mudanças
`sorted(k for k in atual if k in incoming and atual[k] != incoming[k])`.
:::
:::{dropdown} Dica 2 — novos
`sorted(k for k in incoming if k not in atual)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def detectar_mudancas(atual, incoming):
    return sorted(k for k in atual if k in incoming and atual[k] != incoming[k])

def detectar_novos(atual, incoming):
    return sorted(k for k in incoming if k not in atual)
```
É isso que o `dbt snapshot` faz: para as **mudanças**, fecha a linha antiga (`dbt_valid_to`) e
insere a nova; para os **novos**, insere a primeira versão. O resultado é o SCD2 do M5,
automático e versionado.
:::

---
**Revisado em:** 2026-08-24
