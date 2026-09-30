# Exercício 08 — Sessionização: início, fim e duração de cada sessão

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Quanto tempo o usuário passa no app?" não é uma coluna — é uma **transformação**: agrupar os
eventos de cada usuário em **sessões**, quebrando quando há um intervalo de inatividade maior que um
limite (30 minutos é o padrão do Google Analytics). É um clássico de engenharia de dados para
analytics, e aparece em SQL (com `LAG` e soma acumulada) e em Python.

Os dados reais vêm bagunçados: eventos fora de ordem (o celular reenvia depois) e eventos
**duplicados** no mesmo instante. A sessionização precisa ser robusta aos dois.

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py), implemente `sessionizar(eventos, gap_max)` e `resumo_por_usuario(sessoes)`.

```bash
cd modulos/03-python-eng-dados/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — limpe e agrupe
`set(eventos)` elimina duplicatas exatas. Depois agrupe os timestamps por usuário num dict de listas.
:::
:::{dropdown} Dica 2 — percorra ordenado
Ordene os timestamps do usuário. Guarde `inicio`, `anterior` e `n`; quando `ts - anterior > gap_max`, feche a sessão `(inicio, anterior, n)` e comece outra.
:::
:::{dropdown} Dica 3 — não esqueça a última
Depois do laço, a sessão corrente ainda está aberta — feche-a. No resumo, a duração é `fim - inicio`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def sessionizar(eventos: list, gap_max: float) -> dict:
    if gap_max <= 0:
        raise ValueError("gap_max deve ser positivo")
    por_usuario = {}
    for u, ts in set(eventos):
        por_usuario.setdefault(u, []).append(ts)
    saida = {}
    for u in sorted(por_usuario):
        tss = sorted(por_usuario[u])
        sessoes = []
        inicio = anterior = tss[0]
        n = 1
        for ts in tss[1:]:
            if ts - anterior > gap_max:
                sessoes.append((inicio, anterior, n))
                inicio, n = ts, 0
            n += 1
            anterior = ts
        sessoes.append((inicio, anterior, n))
        saida[u] = sessoes
    return saida


def resumo_por_usuario(sessoes: dict) -> dict:
    return {u: {"sessoes": len(s), "eventos": sum(x[2] for x in s),
                "duracao_media": round(sum(x[1] - x[0] for x in s) / len(s), 1)}
            for u, s in sessoes.items()}
```
Sem descartar a duplicata `("ana", 605)`, a primeira sessão da Ana teria 5 eventos em vez de 4 — o
tipo de inflação que faz o time de produto comemorar um engajamento que não existe. E sem ordenar,
o `612` depois do `700` abriria sessões fantasmas.

Em SQL, a mesma lógica é o padrão *gaps and islands*:
```sql
WITH e AS (
  SELECT DISTINCT usuario, ts FROM eventos
), marcados AS (
  SELECT *, CASE WHEN ts - LAG(ts) OVER (PARTITION BY usuario ORDER BY ts) > 30
                 THEN 1 ELSE 0 END AS nova
  FROM e
)
SELECT usuario, SUM(nova) OVER (PARTITION BY usuario ORDER BY ts) AS sessao, ts FROM marcados
```
Repare na fronteira: com gap de 30, os eventos da Bia a exatos 30 minutos ficam na **mesma** sessão.
O `>` (e não `>=`) é uma decisão de definição — documente-a, porque muda o número de sessões.
:::

---
**Revisado em:** 2026-09-30
