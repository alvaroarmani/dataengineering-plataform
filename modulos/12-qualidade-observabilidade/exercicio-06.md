# Exercício 06 — Anomalia de volume com z-score

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Chegou metade das linhas de ontem" é um incidente que nenhum teste de schema pega — o dado está
bem formado, só está **faltando**. A detecção de anomalia de volume (teoria 03) compara o lote de
hoje com o histórico. Tolerância fixa ("±50%") falha dos dois lados: tabelas estáveis deixam
passar quedas de 20%, e tabelas voláteis disparam alarme todo dia.

O **z-score** mede o desvio em unidades do próprio histórico: z = (atual − média) / desvio-padrão.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `avaliar_volume(historico, atual, z_max, min_historico)`.

```bash
cd modulos/12-qualidade-observabilidade/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — média e desvio
`statistics.fmean` e `statistics.pstdev` (populacional). Valide o tamanho do histórico **antes** de calcular.
:::
:::{dropdown} Dica 2 — o caso degenerado
Se `pstdev` der 0, dividir quebra. Trate antes: `z = None` e anomalia se `atual != média`.
:::
:::{dropdown} Dica 3 — direção
Só preencha `direcao` quando `anomalia` for verdadeira: `"queda" if z < 0 else "alta"`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from statistics import fmean, pstdev


def avaliar_volume(historico: list, atual: int, z_max: float = 3.0, min_historico: int = 7) -> dict:
    if len(historico) < min_historico:
        raise ValueError(f"histórico insuficiente: {len(historico)} < {min_historico}")
    media, dp = fmean(historico), pstdev(historico)
    if dp == 0:
        anom = atual != media
        return {"anomalia": anom, "z": None,
                "direcao": ("queda" if atual < media else "alta") if anom else None}
    z = (atual - media) / dp
    anom = abs(z) > z_max
    return {"anomalia": anom, "z": round(z, 2),
            "direcao": ("queda" if z < 0 else "alta") if anom else None}
```
Os dois primeiros testes são o argumento do exercício: **a mesma queda de 5%** é anomalia gritante
(z = −8,37) numa tabela estável e ruído normal (z = −0,25) numa volátil. Uma tolerância fixa não
consegue acertar os dois casos; o z-score se adapta ao comportamento de cada tabela.

Em produção, dois refinamentos são comuns: comparar com o **mesmo dia da semana** (segunda-feira
tem volume de segunda-feira) e usar mediana/MAD em vez de média/desvio, para que um dia anômalo no
histórico não "contamine" a régua.
:::

---
**Revisado em:** 2026-09-30
