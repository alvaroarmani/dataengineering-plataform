# Exercício 05 — Broadcast ou sort-merge? A escolha do join

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
A escolha da estratégia de join (teoria 05) é uma das maiores alavancas de performance no Spark. Se um
lado cabe abaixo do limite `spark.sql.autoBroadcastJoinThreshold` (10 MB por padrão), ele é
**replicado** para todos os executores e o lado grande **não sofre shuffle**. Senão, os dois lados
são embaralhados (sort-merge).

Há uma restrição que pega muita gente: em joins externos, não se pode fazer broadcast do lado cujas
linhas precisam ser **preservadas**. Num `left join`, só o lado **direito** pode ir em broadcast; num
`full outer`, nenhum.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `estrategia_join(esquerda_mb, direita_mb, tipo, limite_mb)`.

```bash
cd modulos/11-spark-lakehouse/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — quem pode ir
Um dict `tipo -> lados que podem ser broadcast` resolve a restrição dos joins externos (`left` só a direita, `full` nenhum).
:::
:::{dropdown} Dica 2 — candidatos
Dos lados permitidos, fique com os que cabem no limite (e só se o limite for positivo).
:::
:::{dropdown} Dica 3 — escolha
Broadcast do menor candidato; sem candidatos, sort-merge com os dois lados embaralhados.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
BROADCASTAVEL = {"inner": {"esquerda", "direita"}, "left": {"direita"}, "right": {"esquerda"},
                 "left_semi": {"direita"}, "left_anti": {"direita"}, "full": set()}


def estrategia_join(esquerda_mb: float, direita_mb: float, tipo: str = "inner", limite_mb: float = 10) -> dict:
    if tipo not in BROADCASTAVEL:
        raise ValueError(f"tipo de join desconhecido: {tipo}")
    tamanhos = {"esquerda": esquerda_mb, "direita": direita_mb}
    candidatos = [l for l in BROADCASTAVEL[tipo] if limite_mb > 0 and tamanhos[l] <= limite_mb]
    if not candidatos:
        return {"estrategia": "sort_merge", "broadcast": None, "lados_com_shuffle": 2}
    lado = min(candidatos, key=lambda l: (tamanhos[l], l != "direita"))
    return {"estrategia": "broadcast_hash", "broadcast": lado, "lados_com_shuffle": 0}
```
O teste do `left join` é o "por que meu broadcast não aconteceu?" mais comum: a tabela pequena está do
lado **esquerdo**, que precisa ser preservado — o Spark não pode replicá-la. Inverter o join (`right`
com as tabelas trocadas, ou reescrever a lógica) devolve o broadcast.

O teste dos 50 MB mostra a outra alavanca: o limite padrão de 10 MB é conservador. Com executores
folgados, subir para 64–256 MB (ou usar `broadcast(df)` explicitamente) elimina o shuffle do lado grande
— no exemplo da teoria, é o que derruba um job de 40 minutos. Estatísticas desatualizadas também fazem
o Catalyst errar o tamanho; o AQE corrige em runtime.
:::

---
**Revisado em:** 2026-09-30
