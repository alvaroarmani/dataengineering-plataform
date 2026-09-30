# Exercício 05 — System design: requisitos em números (estimativa de capacidade)

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
A teoria 03 insiste: **requisitos primeiro**. Numa entrevista de system design, a pessoa que
responde "Kafka + Spark + Delta" antes de perguntar o volume já perdeu pontos. Quem vai bem faz uma
**estimativa de bolso** (*back-of-the-envelope*) em voz alta:

> "50 milhões de eventos por dia dá uns 580 por segundo em média — com pico de 3×, uns 1.700/s.
> A 1 KB por evento, um ano de retenção são ~18 TB brutos; em Parquet, com compressão de 5×
> e 3 réplicas, uns 11 TB. Um warehouse aguenta isso sem cluster Spark."

Neste exercício você transforma esse raciocínio em código — e fixa as ordens de grandeza que
precisa ter de cabeça (1 dia = 86.400 s; 1 milhão/dia ≈ 12/s).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente:

1. **`vazao(eventos_dia, fator_pico)`** — média e pico em eventos por segundo.
2. **`armazenamento_tb(...)`** — disco necessário, com réplicas e compressão.
3. **`proposta(req)`** — processamento (batch / micro-batch / streaming) e motor
   (warehouse SQL ou Spark), com os números que justificam a escolha.

```bash
cd modulos/15-carreira-portfolio-entrevistas/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — vazão
`media = eventos_dia / 86_400`; o pico é `media * fator_pico`. Arredonde **no fim** — arredondar a
média antes de multiplicar muda a última casa do pico.
:::
:::{dropdown} Dica 2 — fronteiras
Leia com atenção os operadores: latência `>= 3600` é batch (exatamente 1 hora já tolera batch
horário); volume `> 500 GB` é Spark (exatamente 500 GB ainda não). Fronteira errada é o bug mais
comum em regra de negócio.
:::
:::{dropdown} Dica 3 — valide os requisitos
Monte a lista dos obrigatórios que faltam (`[k for k in obrig if k not in req]`) e levante
`ValueError` com ela na mensagem — em entrevista, o equivalente é **perguntar** o que falta.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def vazao(eventos_dia, fator_pico=3.0):
    if eventos_dia < 0 or fator_pico < 1:
        raise ValueError("entrada inválida")
    media = eventos_dia / 86_400
    return {"media_s": round(media, 1), "pico_s": round(media * fator_pico, 1)}

def armazenamento_tb(eventos_dia, bytes_evento, retencao_dias, replicas=1, compressao=1.0):
    if min(eventos_dia, bytes_evento, retencao_dias) < 0 or replicas < 1 or compressao <= 0:
        raise ValueError("entrada inválida")
    return round(eventos_dia * bytes_evento * retencao_dias * replicas / compressao / 1e12, 3)

def proposta(req):
    obrig = ("eventos_dia", "bytes_evento", "latencia_seg", "retencao_dias")
    faltando = [k for k in obrig if k not in req]
    if faltando:
        raise ValueError(f"requisitos faltando: {faltando}")
    lat = req["latencia_seg"]
    proc = "batch" if lat >= 3600 else ("micro-batch" if lat >= 60 else "streaming")
    gb_dia = req["eventos_dia"] * req["bytes_evento"] / 1e9
    motor = "spark" if gb_dia > 500 else "sql-warehouse"
    return {
        "processamento": proc,
        "motor": motor,
        "pico_s": vazao(req["eventos_dia"], req.get("fator_pico", 3.0))["pico_s"],
        "armazenamento_tb": armazenamento_tb(req["eventos_dia"], req["bytes_evento"],
                                             req["retencao_dias"], req.get("replicas", 1),
                                             req.get("compressao", 1.0)),
    }
```
Os limiares (1 hora, 500 GB/dia) são **heurísticas de conversa**, não leis — warehouses modernos
processam bem mais que isso. O que o entrevistador avalia é você **chegar a um número, dizer o
limiar que está usando e justificar**. Para praticar, refaça em voz alta os três cenários dos testes
(relatório diário, telemetria em tempo real, painel de 15 minutos) em até 2 minutos cada.

A classificação fina de latência (tempo real × quase real) e as janelas de streaming são
aprofundadas no M17.
:::

---
**Revisado em:** 2026-09-29
