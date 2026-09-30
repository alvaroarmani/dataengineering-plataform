# Exercício 02 — Quantas réplicas? Capacidade que sobrevive à perda de uma zona

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Carga de 1.000 req/s, cada pod aguenta 100 → 10 réplicas" é a conta que derruba sistemas. Na
prática, ninguém roda pods a 100% (latência dispara perto do limite): planeja-se para uma
**utilização alvo**, tipo 70%. E numa nuvem com várias **zonas de disponibilidade** (teoria 01), a
pergunta de verdade é: se uma zona inteira cair, as réplicas das outras aguentam o pico?

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `planejar_replicas(carga_pico, capacidade_pod, utilizacao_alvo, zonas, tolerar_perda_zona)`.

```bash
cd modulos/20-cloud-kubernetes/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — capacidade útil
Cada pod aguenta de fato `capacidade_pod * utilizacao_alvo`. As necessárias são `ceil(carga / isso)`, nunca menos que 1.
:::
:::{dropdown} Dica 2 — por zona
Distribuição igual: `ceil(necessarias / zonas)` por zona — arredondar por zona pode dar mais que o mínimo no total, e está certo.
:::
:::{dropdown} Dica 3 — perdendo uma zona
Se uma zona pode cair, as `zonas - 1` restantes precisam somar as necessárias: divida por `zonas - 1`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import math


def planejar_replicas(carga_pico: float, capacidade_pod: float, utilizacao_alvo: float = 0.7,
                      zonas: int = 1, tolerar_perda_zona: bool = False) -> dict:
    if not 0 < utilizacao_alvo <= 1 or capacidade_pod <= 0 or zonas < 1:
        raise ValueError("parâmetros inválidos")
    if tolerar_perda_zona and zonas < 2:
        raise ValueError("tolerar perda de zona exige pelo menos 2 zonas")
    necessarias = max(1, math.ceil(carga_pico / (capacidade_pod * utilizacao_alvo)))
    divisor = zonas - 1 if tolerar_perda_zona else zonas
    por_zona = math.ceil(necessarias / divisor)
    total = por_zona * zonas
    return {"por_zona": por_zona, "total": total,
            "utilizacao_normal": round(carga_pico / (total * capacidade_pod), 2)}
```
Três zonas com tolerância a perder uma exigem **24** réplicas em vez de 15 — e no dia a dia elas
rodam a 42% de utilização. Parece desperdício até a zona cair: aí as 16 restantes ficam a 62%,
confortáveis. Com 2 zonas, o custo dobra (cada uma aguenta tudo sozinha); com mais zonas, o
"seguro" fica proporcionalmente mais barato.

Esse é um trade-off de custo (M21) × disponibilidade (SLO): nem todo serviço precisa sobreviver à
perda de uma zona. Uma API que alimenta o checkout provavelmente sim; um job de relatório noturno,
não — ele pode simplesmente rodar de novo.
:::

---
**Revisado em:** 2026-09-30
