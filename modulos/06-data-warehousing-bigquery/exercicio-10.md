# Exercício 10 — Layout físico a partir do workload

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Escolher partição e clustering (teoria 02) não é gosto: é olhar o **workload** — quais colunas as
consultas filtram, e **com que frequência**. Uma consulta de painel que roda 500 vezes por dia pesa
mais que uma análise mensal. E há restrições do próprio warehouse: no BigQuery, só colunas de
**data/timestamp** ou **inteiro** podem particionar, e o clustering aceita até **4 colunas**, na
ordem de importância.

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py), implemente `layout_recomendado(consultas, tipos)`.

```bash
cd modulos/06-data-warehousing-bigquery/exercicio-10
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — peso por frequência
Some `execucoes_por_dia` em cada coluna filtrada (não conte só quantas consultas a usam). Valide o tipo de cada coluna aqui.
:::
:::{dropdown} Dica 2 — partição com restrição
Ordene por `(-peso, nome)` e pegue a **primeira particionável** — pode não ser a mais filtrada.
:::
:::{dropdown} Dica 3 — cluster
As colunas restantes, na mesma ordem, sem a de partição, cortadas em 4.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
PARTICIONAVEIS = {"date", "timestamp", "int"}


def layout_recomendado(consultas: list, tipos: dict) -> dict:
    peso = {}
    for cols, execs in consultas:
        for c in cols:
            if c not in tipos:
                raise ValueError(f"coluna sem tipo: {c}")
            peso[c] = peso.get(c, 0) + execs
    ordem = sorted(peso, key=lambda c: (-peso[c], c))
    part = next((c for c in ordem if tipos[c] in PARTICIONAVEIS), None)
    cluster = [c for c in ordem if c != part][:4]
    return {"particao": part, "cluster": cluster}
```
O segundo teste é a armadilha: a coluna mais filtrada (`cliente_id`, uma string) não pode particionar;
ela vai para o **cluster**, que é justamente a ferramenta certa para colunas de alta cardinalidade
usadas em filtros de igualdade. A partição fica com a melhor candidata permitida.

E o teste de frequência mostra por que olhar o **log de consultas** (as views de auditoria de jobs do
warehouse) vence qualquer intuição: 10 consultas raras perdem para 1 consulta que roda 100 vezes por
dia. Esse layout volta a ser revisado quando o workload muda — ele não é uma decisão para sempre.
:::

---
**Revisado em:** 2026-09-30
