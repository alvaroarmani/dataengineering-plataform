# Exercício 05 — Linha x coluna: quantos bytes a consulta lê

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Colunar lê só as colunas necessárias" (teoria 02) é o argumento; aqui você vai colocar número nele.
Num formato por linha (como CSV ou a tabela de um banco OLTP), ler uma coluna obriga a ler a linha
inteira. No colunar (Parquet, BigQuery), a consulta lê só as colunas que usa — e cada coluna ainda
vem **comprimida**, porque valores do mesmo tipo se repetem.

A tabela do exercício tem o formato típico de uma tabela de fatos real: dezenas de colunas, mas a
consulta analítica usa três.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `bytes_lidos(tabela, colunas_da_consulta, formato)` e `ganho(tabela, colunas_da_consulta)`.

```bash
cd modulos/01-fundamentos-eng-dados/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — formato por linha
Não importa quais colunas a consulta usa: `linhas * soma(bytes de todas as colunas)`.
:::
:::{dropdown} Dica 2 — formato colunar
Só as colunas da consulta, cada uma `linhas * bytes / compressao`. Some e converta para `int`.
:::
:::{dropdown} Dica 3 — ganho
Divida um pelo outro e arredonde. Valide as colunas **antes** de calcular.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def bytes_lidos(tabela: dict, colunas_da_consulta: list, formato: str) -> int:
    cols = tabela["colunas"]
    faltando = [c for c in colunas_da_consulta if c not in cols]
    if faltando:
        raise ValueError(f"colunas inexistentes: {faltando}")
    n = tabela["linhas"]
    if formato == "linha":
        return n * sum(c["bytes"] for c in cols.values())
    if formato == "coluna":
        return int(sum(n * cols[c]["bytes"] / cols[c]["compressao"] for c in colunas_da_consulta))
    raise ValueError(f"formato desconhecido: {formato}")


def ganho(tabela: dict, colunas_da_consulta: list) -> float:
    return round(bytes_lidos(tabela, colunas_da_consulta, "linha") /
                 bytes_lidos(tabela, colunas_da_consulta, "coluna"), 1)
```
A mesma consulta — "receita por estado e data" — lê **2,3 GB** no formato por linha e **46 MB** no
colunar: 50 vezes menos. Numa nuvem que cobra por byte lido (M21), é 50 vezes mais barato.

O teste do `SELECT *` mostra o outro lado: ler todas as colunas no colunar só ganha o que vem da
compressão (1,5×). Por isso o `SELECT *` é o anti-padrão número 1 em warehouse: ele joga fora a
principal vantagem do formato. E a coluna `estado` comprime 20× porque tem poucos valores
distintos — o próximo exercício mostra por quê.
:::

---
**Revisado em:** 2026-09-30
