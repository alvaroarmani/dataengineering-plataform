# Exercício 02 — Quais projetos vão para o currículo

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Poucos projetos bons > muitos projetos rasos" (teoria 01). Com vários repositórios no GitHub, a pergunta
é quais **três** destacar. Alguns critérios são eliminatórios (sem README, sem versionamento de verdade,
parado há mais de um ano); os outros somam pontos — dados reais, testes, CI, algo rodando que dá para
ver. E há um critério de diversidade: três projetos da mesma stack mostram menos que três que cobrem
partes diferentes do ciclo de vida.

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `escolher_projetos(projetos, hoje, n)`.

```bash
cd modulos/15-carreira-portfolio-entrevistas/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — eliminar primeiro
README < 50, menos de 5 commits ou último commit há mais de 365 dias (`(hoje - data).days`) saem antes de qualquer pontuação.
:::
:::{dropdown} Dica 2 — pontuar
Bools viram 1/0 (`int(bool(...))`); a nota do README entra multiplicada por 0,03 (uma nota 100 vale 3 pontos).
:::
:::{dropdown} Dica 3 — guloso em duas passadas
Ordene por `(-pontos, nome)`. Primeira passada: pegue um por foco. Segunda: complete as vagas com os melhores que sobraram.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from datetime import date

PESOS = {"dados_reais": 3, "testes": 2, "ci": 2, "demo": 2, "readme_nota": 0.03}


def escolher_projetos(projetos: list, hoje: str, n: int = 3) -> list:
    ref = date.fromisoformat(hoje)
    validos = []
    for p in projetos:
        if p["readme_nota"] < 50 or p["commits"] < 5:
            continue
        if (ref - date.fromisoformat(p["ultimo_commit"])).days > 365:
            continue
        pts = sum(PESOS[k] * (p[k] if k == "readme_nota" else int(bool(p[k]))) for k in PESOS)
        validos.append((p["nome"], round(pts, 2), p["foco"]))
    validos.sort(key=lambda x: (-x[1], x[0]))
    escolhidos, focos = [], set()
    for nome, pts, foco in validos:
        if len(escolhidos) < n and foco not in focos:
            escolhidos.append((nome, pts))
            focos.add(foco)
    for nome, pts, _ in validos:
        if len(escolhidos) >= n:
            break
        if (nome, pts) not in escolhidos:
            escolhidos.append((nome, pts))
    return escolhidos
```
O `dbt-nyc-taxi` (9,7 pontos) fica de fora dos três, mesmo tendo mais pontos que o `kafka-cliques`
(7,1): ele repete o foco "modelagem" do `pipeline-olist`. Três projetos de modelagem mostram uma
habilidade três vezes; modelagem + orquestração + streaming mostram o ciclo de vida inteiro — é o que
a entrevista de system design (unidade 3) vai explorar.

E o `tcc-dw`, o projeto com a maior nota, sai por estar parado há mais de um ano: repositório
abandonado lê como "não mantenho o que construo". Um commit de atualização (dependências, README) resolve.
:::

---
**Revisado em:** 2026-09-30
