"""Exercício 03 (M21) — ROI e payback: o horizonte muda a resposta.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""


def avaliar_investimento(investimento: float, beneficio_mensal: float, custo_mensal: float, meses: int) -> dict:
    """Retorne {"roi": ..., "payback_mes": ..., "resultado": ...} no horizonte de `meses`:
      custo_total  = investimento + custo_mensal * meses
      resultado    = beneficio_mensal * meses - custo_total        (2 casas)
      roi          = resultado / custo_total                        (4 casas)
      payback_mes  = primeiro mês m (1..meses) em que (beneficio_mensal - custo_mensal) * m >= investimento;
                     None se não acontecer dentro do horizonte
    investimento < 0, custos/benefícios negativos ou meses < 1 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
