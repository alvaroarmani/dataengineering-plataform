# Exercício 02 — OLTP ou OLAP? Classificando pela carga real

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
A teoria 02 descreve os dois perfis: OLTP faz **muitas operações pequenas**, com muita escrita;
OLAP faz **poucas consultas grandes**, que leem e agregam milhões de linhas. Na prática, ninguém
diz "este banco é OLAP" — você olha o **log de consultas** e o perfil aparece nos números. É assim,
por exemplo, que se descobre que o banco de produção do app está sendo usado para relatórios pesados
(o "erro clássico" da teoria).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `perfil_carga(consultas)`.

```bash
cd modulos/01-fundamentos-eng-dados/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — frações
`sum(condicao for c in consultas) / len(consultas)` — em Python, `True` soma como 1.
:::
:::{dropdown} Dica 2 — mediana, não média
Use `statistics.median`. Uma única consulta de 12 milhões de linhas distorceria a média; a mediana mostra a consulta **típica**.
:::
:::{dropdown} Dica 3 — a ordem das regras
Teste OLTP primeiro, depois OLAP, e o que sobrar é misto. Valide a lista e os tipos antes de calcular.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from statistics import median


def perfil_carga(consultas: list) -> dict:
    if not consultas:
        raise ValueError("sem consultas")
    tipos = {"SELECT", "INSERT", "UPDATE", "DELETE"}
    if any(c["tipo"] not in tipos for c in consultas):
        raise ValueError("tipo de consulta desconhecido")
    n = len(consultas)
    pct_escrita = round(sum(c["tipo"] != "SELECT" for c in consultas) / n, 2)
    pct_agregacao = round(sum(bool(c["agrega"]) for c in consultas) / n, 2)
    mediana = median(c["linhas_lidas"] for c in consultas)
    if pct_escrita >= 0.3 and mediana <= 100:
        classe = "OLTP"
    elif pct_agregacao >= 0.5 or mediana >= 10_000:
        classe = "OLAP"
    else:
        classe = "misto"
    return {"classe": classe, "pct_escrita": pct_escrita, "pct_agregacao": pct_agregacao,
            "mediana_lidas": mediana}
```
O terceiro teste é o diagnóstico que interessa: um banco com cara de OLTP (27% de escrita), mas em
que quase metade das consultas são relatórios que leem milhares de linhas e agregam. Ele cai em **misto** — o sinal de que é hora de
**copiar** os dados para um ambiente analítico (M08, M06) em vez de deixar o relatório disputar
recursos com o app.

Repare que usamos a **mediana**: no warehouse, a consulta típica lê 800 mil linhas, mesmo com uma
inserção pequena no meio. Métricas robustas a extremos reaparecem em qualidade de dados (M12).
:::

---
**Revisado em:** 2026-09-30
