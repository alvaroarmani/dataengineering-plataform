# Exercício 03 — ROI e payback: o horizonte muda a resposta

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Qual o ROI do projeto?" não tem resposta sem **horizonte**. Um projeto de dados costuma ter
investimento alto no começo (construção) e benefício mensal depois — então o mesmo projeto tem
ROI negativo em 4 meses e ótimo em 12. O **payback** (em que mês o acumulado se paga) completa a
leitura: é o número que a diretoria financeira pergunta primeiro (teoria 03).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `avaliar_investimento(investimento, beneficio_mensal, custo_mensal, meses)`.

```bash
cd modulos/21-data-produto-finops/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — três números
Calcule `custo_total`, depois `resultado` e por fim `roi = resultado / custo_total`. Arredonde só no retorno.
:::
:::{dropdown} Dica 2 — payback
O saldo líquido por mês é `beneficio_mensal - custo_mensal`. O payback é o primeiro `m` em que `liquido * m >= investimento` — `next((m for m in ...), None)` resolve com um gerador.
:::
:::{dropdown} Dica 3 — valide cedo
Levante `ValueError` antes de qualquer conta para parâmetros negativos ou horizonte menor que 1.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def avaliar_investimento(investimento: float, beneficio_mensal: float, custo_mensal: float, meses: int) -> dict:
    if investimento < 0 or beneficio_mensal < 0 or custo_mensal < 0 or meses < 1:
        raise ValueError("parâmetros inválidos")
    custo_total = investimento + custo_mensal * meses
    resultado = beneficio_mensal * meses - custo_total
    liquido = beneficio_mensal - custo_mensal
    payback = next((m for m in range(1, meses + 1) if liquido * m >= investimento), None)
    return {"roi": round(resultado / custo_total, 4) if custo_total else None,
            "payback_mes": payback, "resultado": round(resultado, 2)}
```
Os dois primeiros testes são o mesmo projeto: em 12 meses, ROI de 50% e payback no mês 6; em 4
meses, ROI de −25% e nenhum payback. Nenhum dos dois números está "errado" — o erro é apresentar
um sem o horizonte. Ao defender um projeto, mostre a curva (resultado acumulado mês a mês) e o
payback, não só um percentual.

Este é um modelo **simples**, sem valor do dinheiro no tempo. Para horizontes longos, finanças vai
pedir o **VPL** (valor presente líquido), que desconta os fluxos futuros por uma taxa — a mesma
estrutura de cálculo, com um fator `(1 + taxa) ** m` no denominador.
:::

---
**Revisado em:** 2026-09-30
