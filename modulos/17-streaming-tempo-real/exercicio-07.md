# Exercício 07 — Particionamento por chave no Kafka (TRACK REAL · Kafka)

**Onde roda:** 🐳 Bancada Docker (**Kafka de verdade**, profile `kafka`). O grader **produz e
consome de um tópico real** e verifica a garantia de ordem por partição. Sem bancada? Os
exercícios 01–06 cobrem a mesma lógica (partição, lag, janelas) no navegador.

## Tarefa
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py), implemente **`preparar_mensagens(eventos)`**.
Cada evento é um dict com `cliente_id` e `acao`. Retorne uma lista de tuplas **`(chave, valor)`**
para produzir no Kafka, de modo que **todos os eventos de um mesmo cliente caiam na mesma
partição** (ordem por cliente) — e clientes diferentes se espalhem entre partições.

Lembre (teoria 02): a **chave** define a partição (`hash(chave) % nº_partições`); a ordem é
garantida **por partição**.

## Como rodar o grader
```bash
cd ambiente && docker compose --profile kafka up -d      # sobe o broker Kafka
pip install kafka-python                                  # cliente (se ainda não tiver)
pytest -q modulos/17-streaming-tempo-real/exercicio-07
```
> O grader cria um tópico de 3 partições, produz as suas mensagens, consome de volta e verifica:
> (1) **nada se perde**; (2) cada cliente ficou numa **única partição** (ordem preservada);
> (3) **mais de uma partição** foi usada (chave por cliente, não constante).
> **Fora da bancada, faz *skip*.**

## Dica
:::{dropdown} Dica
A chave precisa identificar o cliente: `[(str(e["cliente_id"]), e["acao"]) for e in eventos]`.
Chave constante jogaria tudo numa partição só; chave por ação espalharia um mesmo cliente.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def preparar_mensagens(eventos):
    # chave = cliente -> mesma chave cai sempre na mesma partição (ordem por cliente),
    # e clientes diferentes se espalham (paralelismo). O valor é a ação.
    return [(str(e["cliente_id"]), e["acao"]) for e in eventos]
```
:::

---
**Revisado em:** 2026-09-03
