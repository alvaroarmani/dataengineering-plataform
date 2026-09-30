# Exercício 02 — Catalyst: column pruning e predicate pushdown

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Como o plano é montado antes de executar, o otimizador **Catalyst** (teoria 05) pode reescrevê-lo.
Duas otimizações que valem ouro com Parquet: **column pruning** (ler da fonte só as colunas que o plano
realmente usa, mesmo que o código peça `select *` no começo) e **predicate pushdown** (empurrar filtros
para a leitura, para que arquivos e *row groups* que não passam no filtro nem sejam lidos).

Um filtro só pode ser empurrado se usa colunas **da fonte**. Filtrar por uma coluna **derivada**
(`withColumn`) obriga a ler tudo primeiro — o mesmo motivo pelo qual filtrar por uma coluna calculada
derruba a poda de partição (M06).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `otimizar(plano, colunas_fonte)`.

```bash
cd modulos/11-spark-lakehouse/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — de onde vem cada coluna
Mantenha `origem = {coluna: {colunas da fonte de que ela depende}}`. Para colunas da fonte, é ela mesma; um `withColumn` herda a união das origens das colunas que usa.
:::
:::{dropdown} Dica 2 — o que é necessário
Tudo que os filtros usam **e** tudo que o resultado final usa, traduzido para colunas da fonte pela `origem`.
:::
:::{dropdown} Dica 3 — pushdown
Um filtro desce para a leitura se **todas** as colunas dele são colunas originais da fonte (não derivadas).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def otimizar(plano: list, colunas_fonte: list) -> dict:
    disponiveis = set(colunas_fonte)
    origem = {c: {c} for c in colunas_fonte}
    necessarias, empurrados, final = set(), [], None
    for i, passo in enumerate(plano):
        tipo = passo[0]
        usadas = passo[2] if tipo == "withColumn" else passo[1]
        faltando = [c for c in usadas if c not in disponiveis]
        if faltando:
            raise ValueError(f"passo {i} usa colunas inexistentes: {faltando}")
        if tipo == "withColumn":
            origem[passo[1]] = set().union(*(origem[c] for c in usadas)) if usadas else set()
            disponiveis.add(passo[1])
        elif tipo == "filter":
            for c in usadas:
                necessarias |= origem[c]
            if all(c in colunas_fonte and origem[c] == {c} for c in usadas):
                empurrados.append(i)
        elif tipo == "select":
            disponiveis = set(usadas)
            final = list(usadas)
        else:
            raise ValueError(f"passo desconhecido: {tipo}")
    for c in (final if final is not None else disponiveis):
        necessarias |= origem[c]
    return {"colunas_lidas": sorted(necessarias & set(colunas_fonte)), "filtros_empurrados": empurrados}
```
No primeiro plano, o código nunca menciona `desconto` nem `payload` depois da fonte — o Catalyst lê só
4 das 6 colunas (e, em Parquet, se `payload` é um JSON grande, é aí que está quase todo o ganho). O filtro
por `data` vai para a leitura: row groups inteiros com datas fora do intervalo nem são abertos.

No segundo plano, o filtro por `liquido` **não** desce — ele depende de um cálculo que só existe depois
da leitura. Reescrever como `filter(preco - desconto > 100)` também não ajudaria: o pushdown do Parquet
só entende comparações simples de uma coluna com um valor. Para ver o que desceu de fato, use
`df.explain()` e procure `PushedFilters` e `ReadSchema` no plano físico.
:::

---
**Revisado em:** 2026-09-30
