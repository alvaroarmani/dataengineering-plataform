# Exercício 03 — Workflow com dependências: quem roda, quem é pulado

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Num workflow do GitHub Actions (teoria 02), jobs declaram dependências com `needs:`. O runner
executa em ordem de dependência e aplica uma regra simples: se uma dependência **falhou ou foi
pulada**, o job dependente é **pulado** (`skipped`), e isso se propaga. O resultado final do
workflow é falha se qualquer job falhou.

Entender essa semântica é o que permite desenhar um CI de dados em que o `deploy` nunca roda com
`dbt test` vermelho — e em que um job independente (a documentação) continua rodando mesmo assim.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `executar_workflow(jobs, resultados)`.

```bash
cd modulos/13-dataops-cicd-iac/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — rodadas
Mantenha `status = {}` e um conjunto de pendentes. A cada rodada, os prontos são os pendentes cujas dependências **todas** já têm status.
:::
:::{dropdown} Dica 2 — a regra do skip
Para um job pronto: se `any(status[d] != "success" for d in deps)`, ele é `skipped`; senão, olhe `resultados[job]`.
:::
:::{dropdown} Dica 3 — ciclo
Se numa rodada não houver nenhum job pronto mas ainda existirem pendentes, há um ciclo — levante `ValueError`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def executar_workflow(jobs: dict, resultados: dict) -> dict:
    for j, deps in jobs.items():
        for d in deps:
            if d not in jobs:
                raise ValueError(f"{j} depende de job inexistente: {d}")
    status = {}
    pendentes = set(jobs)
    while pendentes:
        prontos = sorted(j for j in pendentes if all(d in status for d in jobs[j]))
        if not prontos:
            raise ValueError(f"ciclo entre: {sorted(pendentes)}")
        for j in prontos:
            if any(status[d] != "success" for d in jobs[j]):
                status[j] = "skipped"
            else:
                status[j] = "success" if resultados[j] else "failure"
            pendentes.discard(j)
    conclusao = "failure" if "failure" in status.values() else "success"
    return {"jobs": dict(sorted(status.items())), "conclusao": conclusao}
```
O segundo teste é o desenho que você quer num CI de dados: `dbt-build` falhou, então `dbt-test` e
`deploy` são pulados (nada vai para produção), mas `docs` — que só depende do `lint` — roda
normalmente. Colocar tudo numa sequência linear (`lint → build → test → docs → deploy`) pularia a
documentação sem necessidade e deixaria o workflow mais lento.

O algoritmo é uma ordenação topológica em "ondas" (os jobs de uma mesma rodada poderiam rodar em
paralelo, como o Actions faz). É o mesmo raciocínio do agendador do Airflow (M09).
:::

---
**Revisado em:** 2026-09-30
