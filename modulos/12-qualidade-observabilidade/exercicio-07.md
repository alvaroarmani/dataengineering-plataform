# Exercício 07 — Roteamento de alertas por severidade

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Um alerta que acorda alguém às 3 h da manhã por um aviso cosmético treina a equipe a **ignorar
alertas** — o *alert fatigue* da teoria 04. O roteamento certo depende de **severidade** e de
**criticidade** do que falhou: falha num check crítico chama o plantão; falha comum vira
notificação no canal; avisos isolados só vão para o relatório.

## Tarefa
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py), implemente `decidir_alerta(resultados, criticos, limite_avisos)`.

```bash
cd modulos/12-qualidade-observabilidade/exercicio-07
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — consolide primeiro
Percorra os resultados guardando `final[check] = status` — o último sobrescreve. Valide o status nesse mesmo laço.
:::
:::{dropdown} Dica 2 — listas ordenadas
`sorted(c for c, s in final.items() if s == "fail")` e o mesmo para `"warn"`.
:::
:::{dropdown} Dica 3 — a decisão
Na ordem: algum crítico em `falhas` → plantão; senão, falhas ou avisos suficientes → canal; senão, nada.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
STATUS = {"pass", "warn", "fail"}


def decidir_alerta(resultados: list, criticos: set, limite_avisos: int = 3) -> dict:
    final = {}
    for check, status in resultados:
        if status not in STATUS:
            raise ValueError(f"status desconhecido: {status}")
        final[check] = status
    falhas = sorted(c for c, s in final.items() if s == "fail")
    avisos = sorted(c for c, s in final.items() if s == "warn")
    if any(c in criticos for c in falhas):
        acao = "plantao"
    elif falhas or len(avisos) >= limite_avisos:
        acao = "canal"
    else:
        acao = "nada"
    return {"acao": acao, "falhas": falhas, "avisos": avisos}
```
O teste de **re-execução** é o que mais evita ruído na vida real: o check falhou às 2 h, o retry
automático passou às 2 h 05 — ninguém deveria ser acordado. Consolidar pelo último status é o
equivalente a olhar o estado atual, e não o histórico de tentativas.

A lista de críticos é uma decisão de negócio documentada (qual tabela alimenta faturamento, qual
dashboard a diretoria abre às 8 h) — é o que conecta o alerta ao **SLO** do produto de dados.
:::

---
**Revisado em:** 2026-09-30
