# Exercício 01 — Receita por estado (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (é Python puro). Para rodar os testes você
precisa dos arquivos em `exercicio-01/` (no repositório).

## Tarefa

Implemente, em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), a função
`receita_por_estado(vendas)` que recebe uma lista de dicionários de vendas e retorna um
**dicionário** `{estado: receita_total}`. Ignore vendas com `valor` ausente/`None`.

Rode os testes até tudo ficar verde:

```bash
cd modulos/01-fundamentos-eng-dados/exercicio-01
pytest -q
```

Exemplo:

```python
receita_por_estado([
    {"estado": "SP", "valor": 100.0},
    {"estado": "SP", "valor": 50.0},
    {"estado": "RJ", "valor": 30.0},
])
# -> {"SP": 150.0, "RJ": 30.0}
```

## Dicas progressivas (abra só se precisar)

:::{dropdown} Dica 1 — por onde começar
Crie um dicionário vazio e percorra a lista com um `for`. Para cada venda, acumule o valor
no estado correspondente.
:::
:::{dropdown} Dica 2 — acumular
`acc[estado] = acc.get(estado, 0.0) + valor` evita ter que checar se a chave já existe.
:::
:::{dropdown} Dica 3 — valores ausentes
Antes de somar, pule a venda se `venda.get("valor") is None`.
:::

## Solução comentada (abra só DEPOIS de passar)

:::{dropdown} Ver solução comentada
```python
def receita_por_estado(vendas):
    acc = {}
    for v in vendas:
        valor = v.get("valor")
        if valor is None:      # ignora vendas sem valor
            continue
        estado = v["estado"]
        acc[estado] = acc.get(estado, 0.0) + valor
    return acc
```
Usamos `.get(estado, 0.0)` para inicializar o acumulador na primeira ocorrência de cada
estado, e `continue` para pular linhas inválidas — um padrão de **limpeza** que você repetirá
muito em ingestão de dados. Alternativa idiomática: `collections.defaultdict(float)`.
:::

---
**Revisado em:** 2026-08-20
