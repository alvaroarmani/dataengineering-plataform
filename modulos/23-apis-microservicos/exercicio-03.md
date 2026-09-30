# Exercício 03 — Idempotency-Key do lado do servidor

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Em comunicação síncrona entre serviços (teoria 02), o cliente não sabe se um `POST` que deu timeout
foi processado ou não. Se ele repetir, pode cobrar o cartão duas vezes. A solução usada por APIs de
pagamento é o cabeçalho **Idempotency-Key**: o cliente gera uma chave por operação e a reenvia nos
retries. O servidor guarda a resposta da primeira execução e, ao ver a mesma chave, devolve **a mesma
resposta** sem executar de novo.

Os detalhes que tornam isso seguro: reusar a chave com um **corpo diferente** é erro do cliente (não
pode devolver a resposta de outra operação), e as chaves **expiram** depois de um tempo.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `tratar(armazem, chave, corpo, agora, ttl_seg)`.

```bash
cd modulos/23-apis-microservicos/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — busque a chave
Pegue `armazem["chaves"].get(chave)` e verifique se ainda vale: `agora - criado_em < ttl_seg`.
:::
:::{dropdown} Dica 2 — comparar corpos
Compare os corpos de forma independente da ordem das chaves — `json.dumps(corpo, sort_keys=True)` dos dois lados resolve.
:::
:::{dropdown} Dica 3 — executar
Chave nova ou expirada: monte a cobrança com `proximo_id`, incremente, guarde `{corpo, resposta, criado_em}` e devolva 201.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import json


def tratar(armazem: dict, chave: str, corpo: dict, agora: int, ttl_seg: int = 86_400) -> tuple:
    if not chave:
        raise ValueError("Idempotency-Key obrigatória")
    salvo = armazem["chaves"].get(chave)
    if salvo and agora - salvo["criado_em"] < ttl_seg:
        if json.dumps(salvo["corpo"], sort_keys=True) != json.dumps(corpo, sort_keys=True):
            return 422, {"erro": "chave reutilizada com outro corpo"}, False
        return 200, salvo["resposta"], True
    cobranca = {"id": armazem["proximo_id"], **corpo}
    armazem["proximo_id"] += 1
    armazem["cobrancas"].append(cobranca)
    armazem["chaves"][chave] = {"corpo": corpo, "resposta": cobranca, "criado_em": agora}
    return 201, cobranca, False
```
O primeiro teste é o incidente que a chave evita: o cliente mandou o `POST`, a resposta se perdeu
num timeout, ele repetiu — e a cobrança continua sendo **uma**. Repare que o retry devolve **a mesma
resposta** (mesmo id), para que o cliente siga como se a primeira tivesse chegado.

O `422` por corpo diferente é o que impede um bug do cliente (reusar a chave de uma cobrança de
R$ 10 numa de R$ 1.000) de virar uma resposta mentirosa. E o TTL limita o armazenamento: depois de
24 h, a chave pode ser reciclada. Do lado de quem **consome** (M08), a Idempotency-Key e o upsert por
chave são as duas faces da mesma ideia.
:::

---
**Revisado em:** 2026-09-30
