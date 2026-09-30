# Exercício 01 — Roteamento de eventos com padrões de tópico e DLQ

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Na arquitetura orientada a eventos (teoria 01), quem publica não sabe quem consome. Os consumidores
**assinam** tipos de evento — muitas vezes por **padrão**: o antifraude quer todo `pagamento.*`, a
auditoria quer **tudo** (`#`). E todo sistema de eventos sério tem uma **fila de mensagens mortas**
(*dead-letter queue*, DLQ): o evento que ninguém assina não pode sumir em silêncio — ele vai para a
DLQ, onde alguém investiga (quase sempre é um produtor publicando um tipo novo ou com erro de
digitação).

Os padrões seguem a convenção dos brokers de mensagens (como os *topic exchanges* do RabbitMQ):
`*` casa **exatamente um** segmento, `#` casa **zero ou mais**.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente `casa(padrao, tipo)` e `entregar(eventos, assinaturas)`.

```bash
cd modulos/17-streaming-tempo-real/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — segmentos
Quebre padrão e tipo com `.split(".")` e compare segmento a segmento. Sem `#`, é uma comparação direta com `*` valendo qualquer segmento — mas os tamanhos precisam bater.
:::
:::{dropdown} Dica 2 — o # recursivo
Uma função recursiva `rec(i, j)` (posição no padrão, posição no tipo) resolve: se `p[i] == "#"`, tente pular 0, 1, 2… segmentos do tipo (`any(rec(i + 1, k) for k in range(j, len(t) + 1))`).
:::
:::{dropdown} Dica 3 — entrega e DLQ
Inicialize a saída com todos os consumidores (lista vazia) e a `"DLQ"`. Para cada evento, cada consumidor recebe se `any(casa(p, tipo) ...)`; se ninguém recebeu, vai para a DLQ.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def casa(padrao: str, tipo: str) -> bool:
    p, t = padrao.split("."), tipo.split(".")

    def rec(i, j):
        if i == len(p):
            return j == len(t)
        if p[i] == "#":
            return any(rec(i + 1, k) for k in range(j, len(t) + 1))
        if j == len(t):
            return False
        return (p[i] == "*" or p[i] == t[j]) and rec(i + 1, j + 1)

    return rec(0, 0)


def entregar(eventos: list, assinaturas: dict) -> dict:
    saida = {c: [] for c in assinaturas}
    saida["DLQ"] = []
    for id_, tipo in eventos:
        entregue = False
        for consumidor, padroes in assinaturas.items():
            if any(casa(p, tipo) for p in padroes):
                saida[consumidor].append(id_)
                entregue = True
        if not entregue:
            saida["DLQ"].append(id_)
    return saida
```
O evento 5 (`pedido.criado.v2`) é o caso real que a DLQ existe para pegar: o time de pedidos
lançou uma versão nova do evento, e **nenhum** consumidor casa com ela — `pedido.*` exige
exatamente dois segmentos. Sem DLQ, o faturamento pararia de receber pedidos novos sem nenhum erro.
Com DLQ, um alerta sobre "mensagens na DLQ > 0" avisa no mesmo dia.

No Kafka, o roteamento é mais simples: o consumidor assina **tópicos** inteiros (ou por regex de
nome de tópico), e a DLQ é um tópico separado para onde o consumidor manda o que não conseguiu
processar. A ideia — nunca descartar em silêncio — é a mesma.
:::

---
**Revisado em:** 2026-09-30
