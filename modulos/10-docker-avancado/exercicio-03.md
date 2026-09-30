# Exercício 03 — Compose: depends_on com condição e tempo até o stack ficar pronto

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
`depends_on` no Compose (teoria 02) só garante a **ordem de início** — o container do banco "iniciou",
mas o Postgres ainda está inicializando e recusa conexões por alguns segundos. Com
`condition: service_healthy`, o dependente espera o **healthcheck** do outro passar. Sem isso, o
Airflow sobe, tenta conectar ao banco, falha e fica reiniciando.

Você vai calcular quando cada serviço inicia e fica saudável, e quanto tempo o stack leva para ficar
pronto — o tipo de conta que explica por que a bancada "às vezes" falha na primeira subida.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `subir_stack(servicos)`.

```bash
cd modulos/10-docker-avancado/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — valide antes
Confira que toda dependência existe e que `service_healthy` só aponta para serviços com `health_seg`.
:::
:::{dropdown} Dica 2 — ordem de processamento
Processe em ondas: um serviço fica pronto para ser calculado quando todas as dependências já têm tempos. Nenhum pronto com pendentes = ciclo.
:::
:::{dropdown} Dica 3 — o instante de início
Começa no maior entre os tempos exigidos: `iniciado[dep]` para `service_started`, `saudavel[dep]` para `service_healthy` (0 se não depende de nada).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def subir_stack(servicos: dict) -> dict:
    for nome, cfg in servicos.items():
        for dep, cond in cfg.get("depende", {}).items():
            if dep not in servicos:
                raise ValueError(f"{nome} depende de {dep}, que não existe")
            if cond == "service_healthy" and servicos[dep].get("health_seg") is None:
                raise ValueError(f"{dep} não tem healthcheck")
    iniciado, saudavel = {}, {}
    pendentes = set(servicos)
    while pendentes:
        prontos = [s for s in sorted(pendentes)
                   if all(d in saudavel for d in servicos[s].get("depende", {}))]
        if not prontos:
            raise ValueError(f"ciclo entre {sorted(pendentes)}")
        for s in prontos:
            cfg = servicos[s]
            comeca = max([iniciado[d] if c == "service_started" else saudavel[d]
                          for d, c in cfg.get("depende", {}).items()], default=0)
            iniciado[s] = comeca + cfg["inicio_seg"]
            saudavel[s] = iniciado[s] + (cfg.get("health_seg") or 0)
            pendentes.discard(s)
    return {"iniciado": dict(sorted(iniciado.items())), "saudavel": dict(sorted(saudavel.items())),
            "pronto_em": max(saudavel.values()) if saudavel else 0}
```
O `airflow_init` só começa aos 10 s (quando o Postgres fica saudável) e o `airflow_web` só fica pronto
aos 50 s. Se o `airflow_init` usasse `service_started`, começaria aos 2 s, tentaria migrar o banco que
ainda não aceita conexões e falharia — o "às vezes funciona" clássico, que depende de quão rápido a sua
máquina é naquele dia.

Por isso a bancada do curso (`ambiente/docker-compose.yml`) define healthchecks nos serviços de base e
usa `service_healthy` nas dependências. E no Kubernetes (M20) o equivalente são as *readiness probes*.
:::

---
**Revisado em:** 2026-09-30
