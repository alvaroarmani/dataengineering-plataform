# Exercício 10 — Data-aware scheduling: DAGs disparadas por datasets

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Agendar a DAG de marketing "às 7h, torcendo para vendas já ter terminado" é o acoplamento frágil que o
**data-aware scheduling** (teoria 05) elimina: DAGs **produzem** datasets, e uma DAG consumidora é
disparada quando **todos** os datasets de que depende foram atualizados desde a última execução dela.
Se só um dos dois insumos chegou, ela espera; se um insumo é atualizado duas vezes antes do outro
chegar, ela ainda dispara **uma** vez.

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py), implemente `disparos(consumidores, atualizacoes)`.

```bash
cd modulos/09-orquestracao-airflow/exercicio-10
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — um conjunto por DAG
Guarde, para cada DAG, o conjunto de datasets atualizados desde o último disparo.
:::
:::{dropdown} Dica 2 — a cada atualização
Para cada DAG (em ordem alfabética) que depende do dataset: adicione ao conjunto; se o conjunto ficou igual ao conjunto de dependências, registre o disparo e zere.
:::
:::{dropdown} Dica 3 — atualização repetida
Como é um conjunto, a segunda atualização de `vendas` antes de `clientes` chegar não muda nada para o marketing — ele dispara uma vez.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def disparos(consumidores: dict, atualizacoes: list) -> list:
    for dag, deps in consumidores.items():
        if not deps:
            raise ValueError(f"{dag} sem datasets")
    vistos = {dag: set() for dag in consumidores}
    saida = []
    for i, ds in enumerate(atualizacoes):
        for dag in sorted(consumidores):
            deps = set(consumidores[dag])
            if ds in deps:
                vistos[dag].add(ds)
                if vistos[dag] == deps:
                    saida.append((i, dag))
                    vistos[dag] = set()
    return saida
```
No segundo teste, `vendas` é atualizada duas vezes antes de `clientes`: o financeiro (que só depende
de vendas) roda duas vezes, mas o marketing roda **uma** — quando o último insumo chega. E a diretoria,
que depende de três datasets, só dispara quando o `estoque` finalmente é atualizado.

É o fim do "agende às 7h e rezo": se vendas atrasar para as 9h, o marketing simplesmente roda às 9h.
Além disso, o grafo produtor → dataset → consumidor vira **lineage de execução** entre DAGs — o mesmo
grafo que a análise de impacto do M14 percorre.
:::

---
**Revisado em:** 2026-09-30
