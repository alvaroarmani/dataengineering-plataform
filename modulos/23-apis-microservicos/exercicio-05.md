# Exercício 05 — Saga orquestrada: compensar ou seguir em frente

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Sem transação distribuída, um processo que cruza serviços — reservar estoque, cobrar, emitir nota,
enviar — é coordenado por uma **saga** (teoria 03): cada passo tem uma **compensação** que o desfaz,
executada em ordem inversa se algo falhar. Mas nem todo passo pode ser desfeito: depois que a nota
fiscal é emitida ou o pacote sai do galpão, não se "des-envia". Esse é o **ponto sem volta**
(*pivot*): falhas antes dele são compensadas; falhas depois dele exigem **seguir em frente**,
repetindo o passo até conseguir.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `executar_saga(passos, pivo, resultados)`.

```bash
cd modulos/23-apis-microservicos/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — ache o pivô
`nomes.index(pivo)` dá a posição; passos com índice menor são reversíveis. Valide antes de executar qualquer coisa.
:::
:::{dropdown} Dica 2 — antes do pivô
Uma tentativa só. Guarde as compensações dos concluídos numa lista; na falha, registre `falha:passo` e depois `compensa:` de cada uma em `reversed(...)`.
:::
:::{dropdown} Dica 3 — depois do pivô
Percorra as tentativas até o primeiro sucesso. O `for ... else` do Python ajuda: o `else` roda quando o laço termina **sem** `break` — ou seja, nenhuma tentativa deu certo.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def executar_saga(passos: list, pivo: str, resultados: dict) -> dict:
    nomes = [n for n, _ in passos]
    if pivo not in nomes:
        raise ValueError(f"pivô desconhecido: {pivo}")
    idx_pivo = nomes.index(pivo)
    log, concluidos = [], []
    for i, (nome, compensacao) in enumerate(passos):
        tentativas = list(resultados.get(nome, [True]))
        if i < idx_pivo:
            if tentativas[0]:
                log.append(f"ok:{nome}")
                concluidos.append(compensacao)
                continue
            log.append(f"falha:{nome}")
            log += [f"compensa:{c}" for c in reversed(concluidos)]
            return {"status": "compensada", "log": log}
        for ok in tentativas:
            if ok:
                log.append(f"ok:{nome}")
                break
            log.append(f"falha:{nome}")
        else:
            return {"status": "pendente", "log": log}
    return {"status": "concluida", "log": log}
```
O teste do antifraude mostra por que a ordem inversa importa: primeiro se **estorna** a cobrança,
depois se **libera** o estoque — desfazer na mesma ordem liberaria o produto para outro cliente
enquanto o dinheiro deste ainda está preso.

E o status `pendente` é a decisão mais importante do padrão: depois da nota fiscal emitida, "desfazer
tudo" não é uma opção legal nem operacional. A saga para, registra, e o passo vai para uma fila de
retry com alerta — o mesmo papel da DLQ do M17. Na prática, orquestradores como Temporal, Step
Functions ou o próprio Airflow (M09) guardam esse estado entre tentativas.
:::

---
**Revisado em:** 2026-09-30
