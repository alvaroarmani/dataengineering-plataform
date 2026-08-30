# Exercício 04 — Separar fatos e dimensões (modelagem) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`separar_fato_dim`** — colunas = lista de (nome, natureza) com natureza em {'medida','descritivo'}. Retorne {'fato': [medidas ordenadas], 'dimensao': [descritivos ordenados]}.

```bash
cd modulos/15-carreira-portfolio-entrevistas/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
medidas (numéricas aditivas) vão na fato; atributos descritivos, nas dimensões.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def separar_fato_dim(colunas):
    fato = sorted(n for n, nat in colunas if nat == 'medida')
    dimensao = sorted(n for n, nat in colunas if nat == 'descritivo')
    return {'fato': fato, 'dimensao': dimensao}
```
:::

---
**Revisado em:** 2026-08-30
