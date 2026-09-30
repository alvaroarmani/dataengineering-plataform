# Exercício 02 — Showback: quem gasta o quê

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Você não controla o que não mede" (teoria 02). O primeiro passo de FinOps em dados é o
**showback**: ratear a fatura por time e expor as consultas mais caras. Só com isso a conversa
muda de "a conta da nuvem subiu" para "a consulta X do time de ciência de dados varre 4 TiB por
dia — dá para particionar?".

Na prática, esse relatório sai das tabelas de auditoria do DW (no BigQuery, as views
`INFORMATION_SCHEMA.JOBS`), com uma etiqueta (*label*) de time em cada job. E sempre sobra o balde
**sem dono** — que é, ele mesmo, um achado.

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `ratear_custos(consultas, preco_por_tib)` e `maiores_ofensores(consultas, preco_por_tib, n)`.

```bash
cd modulos/21-data-produto-finops/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — o balde sem dono
`c.get("time") or "sem_dono"` trata `None`, `""` e chave ausente de uma vez.
:::
:::{dropdown} Dica 2 — some sem arredondar
Acumule o custo bruto por time e arredonde **só na saída** — arredondar consulta a consulta acumula erro.
:::
:::{dropdown} Dica 3 — dict ordenado
Em Python, o dict preserva a ordem de inserção: monte-o percorrendo os times já ordenados por `(-custo, nome)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
TIB = 2 ** 40


def _custo(c: dict, preco: float) -> float:
    return c["bytes"] / TIB * preco


def ratear_custos(consultas: list, preco_por_tib: float) -> dict:
    por_time = {}
    for c in consultas:
        t = c.get("time") or "sem_dono"
        por_time[t] = por_time.get(t, 0.0) + _custo(c, preco_por_tib)
    total = sum(por_time.values())
    ordem = sorted(por_time, key=lambda t: (-por_time[t], t))
    return {t: {"custo": round(por_time[t], 2),
                "pct": round(100 * por_time[t] / total, 1) if total else 0.0} for t in ordem}


def maiores_ofensores(consultas: list, preco_por_tib: float, n: int = 3) -> list:
    linhas = [(c["id"], c.get("time") or "sem_dono", round(_custo(c, preco_por_tib), 2)) for c in consultas]
    return sorted(linhas, key=lambda x: (-x[2], x[0]))[:n]
```
O resultado já conta a história para a reunião de custos: mais da metade da fatura vem de **uma**
consulta do time de ciência (`q3`), e 13% não têm dono — ninguém consegue otimizar o que ninguém
assume. A ação típica é dupla: revisar a `q3` (partição? colunas desnecessárias? materializar?) e
tornar a etiqueta de time **obrigatória** para rodar jobs.

Showback mostra o custo; *chargeback* vai além e cobra de fato de cada área. Começar pelo
showback evita briga e cria o hábito de olhar o número.
:::

---
**Revisado em:** 2026-09-30
