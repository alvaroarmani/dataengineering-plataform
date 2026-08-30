# Exercício 02 — Projetos prontos para o portfólio (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`projetos_prontos`** — projetos = lista de dicts com chaves nome, tem_readme, tem_teste, versionado (bool). Retorne a lista ORDENADA dos nomes que têm os TRÊS requisitos True.

```bash
cd modulos/15-carreira-portfolio-entrevistas/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
filtre por readme AND teste AND versionado; retorne os nomes ordenados.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def projetos_prontos(projetos):
    return sorted(p['nome'] for p in projetos if p['tem_readme'] and p['tem_teste'] and p['versionado'])
```
:::

---
**Revisado em:** 2026-08-30
