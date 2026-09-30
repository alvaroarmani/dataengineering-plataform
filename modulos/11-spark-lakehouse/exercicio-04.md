# Exercício 04 — Pipeline imutável de transformações

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
DataFrames do Spark são **imutáveis** (teoria 02): `df.withColumn(...)` não altera `df`, devolve um
DataFrame novo. É o que permite ao Spark reexecutar qualquer pedaço do plano depois de uma falha — e o
que faz um código como `df.withColumn("x", ...)` sem atribuição simplesmente não ter efeito.

Você vai implementar um mini-pipeline com a mesma semântica: cada passo produz linhas **novas**, um
`withColumn` pode **sobrescrever** uma coluna existente, e um passo pode usar uma coluna criada por um
passo anterior — mas não uma que foi removida.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `aplicar(linhas, passos)`.

```bash
cd modulos/11-spark-lakehouse/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — cópias
Comece com `[dict(l) for l in linhas]` e, em cada passo, construa dicts **novos** (`{**l, nome: valor}`), nunca `l[nome] = ...`.
:::
:::{dropdown} Dica 2 — três passos
`withColumn` adiciona/sobrescreve; `filter` mantém as linhas; `drop` monta dicts sem a chave. Valide o `drop` contra as colunas atuais.
:::
:::{dropdown} Dica 3 — erros com contexto
Envolva cada passo em `try/except KeyError` e relance como `ValueError` com o índice do passo — é o que torna o erro depurável.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def aplicar(linhas: list, passos: list) -> list:
    atual = [dict(l) for l in linhas]
    for i, passo in enumerate(passos):
        tipo = passo[0]
        try:
            if tipo == "withColumn":
                _, nome, func = passo
                atual = [{**l, nome: func(l)} for l in atual]
            elif tipo == "filter":
                atual = [dict(l) for l in atual if passo[1](l)]
            elif tipo == "drop":
                nome = passo[1]
                if atual and nome not in atual[0]:
                    raise ValueError(f"passo {i}: coluna inexistente {nome}")
                atual = [{k: v for k, v in l.items() if k != nome} for l in atual]
            else:
                raise ValueError(f"passo {i}: tipo desconhecido {tipo}")
        except KeyError as e:
            raise ValueError(f"passo {i}: coluna inexistente {e}") from None
    return atual
```
O teste `entrada_intacta` é o que a imutabilidade garante: mesmo um passo que "zera o preço" não toca
nos dados de origem. No Spark, isso vale em escala — e o custo de copiar é evitado porque o que se
encadeia são **planos**, não dados.

O erro mais comum de quem vem do pandas é escrever `df.withColumn("receita", ...)` numa linha solta e
estranhar que a coluna "não apareceu": sem reatribuir (`df = df.withColumn(...)`), o novo DataFrame é
descartado. E referenciar uma coluna removida falha já na **análise** do plano (antes de executar) —
aqui, simulamos isso com a mensagem que aponta o passo.
:::

---
**Revisado em:** 2026-09-30
