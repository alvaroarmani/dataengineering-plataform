# Exercício 06 — Exactly-once de efeito: offset, falha e reprocessamento

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
A teoria 03 diz que **at-least-once + idempotência** entrega o efeito de exactly-once. Este
exercício mostra por que — simulando a falha que acontece em produção: o consumidor processa
mensagens, aplica o efeito (credita um saldo) e **cai antes de commitar o offset**. Ao reiniciar, ele
relê do último offset commitado e **reprocessa** as mesmas mensagens.

Sem proteção, o saldo é creditado duas vezes. Com um registro dos ids já aplicados, gravado **junto
com o efeito**, o reprocessamento vira no-op.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `processar(log, estado, commit_a_cada, falha_apos, idempotente)`.

```bash
cd modulos/17-streaming-tempo-real/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — copie o estado
`copy.deepcopy(estado)` — o set de aplicados também precisa ser uma cópia, senão a "execução que caiu" altera o estado de quem chamou.
:::
:::{dropdown} Dica 2 — a ordem dentro do laço
Para cada posição: aplique o efeito (checando `aplicados` se for idempotente), conte a mensagem, verifique a falha **antes** do commit e só então commite quando `feitas % commit_a_cada == 0`.
:::
:::{dropdown} Dica 3 — o fim
Sem falha, depois do laço, o offset vai para `len(log)` (o commit final).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import copy


def processar(log: list, estado: dict, commit_a_cada: int, falha_apos=None, idempotente: bool = True) -> dict:
    est = copy.deepcopy(estado)
    feitas = 0
    for pos in range(est["offset"], len(log)):
        id_, valor = log[pos]
        if not (idempotente and id_ in est["aplicados"]):
            est["saldo"] += valor
            est["aplicados"].add(id_)
        feitas += 1
        if falha_apos is not None and feitas == falha_apos:
            return est
        if feitas % commit_a_cada == 0:
            est["offset"] = pos + 1
    est["offset"] = len(log)
    return est
```
O teste do meio é o incidente: o consumidor aplicou `m3`, caiu antes do commit (que só aconteceria
na 4ª mensagem), e ao voltar releu a partir do offset 2. Sem o registro de ids, `m3` foi creditada
duas vezes — o saldo fica 180 em vez de 150, e nenhum erro foi lançado.

A palavra-chave na docstring é **atômico**: o id aplicado precisa ser gravado **na mesma transação**
do efeito (a mesma tabela, o mesmo `MERGE`). Se o registro de ids ficasse num lugar e o saldo em
outro, uma falha entre os dois recriaria o problema. É por isso que sinks idempotentes (upsert por
chave, M08) e as transações do Kafka existem.
:::

---
**Revisado em:** 2026-09-30
