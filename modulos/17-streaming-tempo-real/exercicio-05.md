# Exercício 05 — Janelas por tempo de evento com watermark

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Contexto
Calcular a janela de um evento é uma linha (`ts // 60 * 60`). O problema difícil de streaming é
outro (teoria 03): **quando fechar a janela**, se eventos chegam fora de ordem e atrasados?

- Fechar **cedo** → a métrica sai rápido, mas **incompleta** (os atrasados se perdem).
- Fechar **tarde** → a métrica sai completa, mas **atrasada**.

O **watermark** é essa decisão, explícita: "já vi tudo até `max(ts) - atraso_permitido`". Janelas que
terminam antes dele fecham e são emitidas; eventos que chegam para uma janela já fechada são
**atrasados** e vão para um tratamento à parte (descarte, *side output*, reprocessamento).

Você vai escrever um motor de streaming de bolso e **ver o trade-off nos números**: o mesmo stream
com tolerância de 0 s, 10 s e 30 s dá três respostas diferentes.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `janela_tumbling` e
**`processar_stream(eventos, tamanho_seg, atraso_permitido_seg)`** seguindo os 3 passos da docstring.

```bash
cd modulos/17-streaming-tempo-real/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — o estado do motor
Três coisas: `abertas = {inicio: soma}`, `watermark = None` e as listas de saída. O watermark
**só avança** — use `max`.
:::
:::{dropdown} Dica 2 — atrasado primeiro
Para cada evento, calcule `inicio` e cheque **antes de somar**: se `watermark is not None and
inicio + tamanho <= watermark`, é atrasado — anote o id e `continue`.
:::
:::{dropdown} Dica 3 — emitir sem quebrar o dict
Depois de atualizar o watermark, percorra `sorted(abertas)` (uma cópia das chaves) e use
`abertas.pop(ini)` para as que fecharam. No fim, emita o que sobrou, também em ordem.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def janela_tumbling(event_ts, tamanho_seg):
    if tamanho_seg <= 0:
        raise ValueError("tamanho inválido")
    return (event_ts // tamanho_seg) * tamanho_seg

def processar_stream(eventos, tamanho_seg, atraso_permitido_seg):
    if atraso_permitido_seg < 0:
        raise ValueError("atraso inválido")
    abertas, emitidas, atrasados = {}, [], []
    watermark = None
    for ev in eventos:
        inicio = janela_tumbling(ev["ts"], tamanho_seg)
        if watermark is not None and inicio + tamanho_seg <= watermark:
            atrasados.append(ev["id"])             # janela já emitida: não dá para "desemitir"
            continue
        abertas[inicio] = abertas.get(inicio, 0) + ev["valor"]
        novo = ev["ts"] - atraso_permitido_seg
        watermark = novo if watermark is None else max(watermark, novo)
        for ini in sorted(abertas):
            if ini + tamanho_seg <= watermark:
                emitidas.append((ini, abertas.pop(ini)))
    for ini in sorted(abertas):                    # fim do stream: flush
        emitidas.append((ini, abertas[ini]))
    return {"janelas": emitidas, "atrasados": atrasados}
```
**Lendo os testes:** com 0 s de tolerância, a janela `[0, 60)` sai com soma 1 — perdeu 12 de 13.
Com 30 s, sai completa (13), mas só depois de chegar um evento com `ts >= 90`: **completude custa
latência**. Em produção (Flink, Spark Structured Streaming), essa tolerância é um parâmetro que você
calibra olhando a distribuição real dos atrasos — e os atrasados vão para um *side output* em vez de
sumir.

Compare com o *downsample* do M18 (exercício 05): lá o dado já está todo gravado (batch sobre série
temporal); aqui você decide **enquanto** ele chega.
:::

---
**Revisado em:** 2026-09-29
