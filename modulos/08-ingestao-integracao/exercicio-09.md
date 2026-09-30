# Exercício 09 — Aplicar um changelog de CDC: ordem, idempotência e anomalias

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O CDC (teoria 05) entrega um **changelog**: cada evento diz "inseriu", "atualizou" ou "apagou" uma
chave, e carrega uma posição no log do banco (**LSN**, *log sequence number*). Aplicar esse log numa
tabela-espelho parece trivial — até lembrar que a entrega é **at-least-once**: eventos podem chegar
**repetidos** (reentrega depois de uma falha) e, entre partições, **fora de ordem**.

A aplicação correta ordena pelo LSN, **ignora** o que já foi aplicado (LSN menor ou igual ao último
aplicado) e registra **anomalias** — um UPDATE de chave que não existe no espelho significa que você
perdeu o INSERT em algum lugar.

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py), implemente `aplicar_cdc(estado, eventos)`.

```bash
cd modulos/08-ingestao-integracao/exercicio-09
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — ordene e filtre
`sorted(eventos, key=lambda e: e["lsn"])`; pule (e conte como ignorado) todo evento com `lsn <= ultimo`. Atualizar `ultimo` a cada aplicado já elimina repetições dentro do lote.
:::
:::{dropdown} Dica 2 — as três operações
I e U gravam; D remove com `pop(k, None)`. Antes de cada uma, verifique a situação anômala (chave existente no I, inexistente no U e no D).
:::
:::{dropdown} Dica 3 — não mexa na entrada
Trabalhe numa cópia: `dict(estado["tabela"])`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def aplicar_cdc(estado: dict, eventos: list) -> dict:
    tabela = dict(estado["tabela"])
    ultimo = estado["ultimo_lsn"]
    aplicados = ignorados = 0
    anomalias = []
    for ev in sorted(eventos, key=lambda e: e["lsn"]):
        if ev["lsn"] <= ultimo:
            ignorados += 1
            continue
        op, k = ev["op"], ev["chave"]
        if op == "I":
            if k in tabela:
                anomalias.append((ev["lsn"], "I_existente"))
            tabela[k] = ev["valor"]
        elif op == "U":
            if k not in tabela:
                anomalias.append((ev["lsn"], "U_inexistente"))
            tabela[k] = ev["valor"]
        elif op == "D":
            if k not in tabela:
                anomalias.append((ev["lsn"], "D_inexistente"))
            tabela.pop(k, None)
        else:
            raise ValueError(f"operação desconhecida: {op}")
        ultimo = ev["lsn"]
        aplicados += 1
    return {"tabela": tabela, "ultimo_lsn": ultimo, "aplicados": aplicados,
            "ignorados": ignorados, "anomalias": anomalias}
```
O segundo teste mostra por que a ordem importa: na ordem de chegada, o UPDATE (102) viria antes do
DELETE (101), e a Bia sumiria da tabela. Na ordem do LSN, o DELETE acontece primeiro e o UPDATE traz a
chave de volta — com a anomalia registrada, porque atualizar o que foi apagado é suspeito.

Guardar o `ultimo_lsn` **junto com a tabela** (no mesmo commit) é o que torna o processo idempotente:
uma reentrega inteira do lote vira zero aplicações. É a mesma ideia do offset + dedup atômico do
exercício 06 do M17 — e é o que ferramentas como o Debezium + sink connectors fazem por baixo.
:::

---
**Revisado em:** 2026-09-30
