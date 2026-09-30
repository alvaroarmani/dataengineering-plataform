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

## Dicas progressivas
:::{dropdown} Dica 1 — o que a chave decide
No Kafka, a partição é `hash(chave) % partições` (teoria 02): mensagens com a **mesma chave** vão para a **mesma partição**, e só dentro de uma partição há ordem garantida. A pergunta é: que chave faz os eventos de um cliente ficarem em ordem?
:::
:::{dropdown} Dica 2 — as armadilhas
Chave **constante** joga tudo numa partição só (ordem garantida, mas zero paralelismo). Chave **por ação** espalha os eventos de um mesmo cliente por várias partições (paralelismo, mas a ordem do cliente se perde). Sem chave, é round-robin.
:::
:::{dropdown} Dica 3 — quase lá
A chave precisa identificar o cliente e ser texto (o produtor serializa bytes): `[(str(e["cliente_id"]), e["acao"]) for e in eventos]`, mantendo a ordem de entrada.
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
**Revisado em:** 2026-09-30
