# Exercício 08 — Macros: transformações reutilizáveis (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Um macro dbt encapsula SQL reutilizável (a ideia do Jinja). Implemente dois "macros" clássicos
em Python para entender o padrão.

## Tarefas
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py):

- **`centavos_para_reais(centavos)`** — `12345 → 123.45` (dividir por 100).
- **`surrogate_key(valores)`** — chave determinística a partir de uma lista de valores (como
  `dbt_utils.generate_surrogate_key`): mesmo input → mesma chave; inputs diferentes → chaves
  diferentes. Retorne uma string.

```bash
cd modulos/07-transformacao-dbt/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — centavos
`return centavos / 100.0`.
:::
:::{dropdown} Dica 2 — surrogate key
Junte os valores e passe por um hash estável: `hashlib.md5('|'.join(map(str, valores)).encode()).hexdigest()`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import hashlib

def centavos_para_reais(centavos):
    return centavos / 100.0

def surrogate_key(valores):
    return hashlib.md5("|".join(map(str, valores)).encode()).hexdigest()
```
No dbt, `centavos_para_reais` seria `{% macro %}` usado em vários models (`{{ centavos_para_reais('preco') }}`),
e `surrogate_key` é literalmente o que `dbt_utils.generate_surrogate_key(['a','b'])` faz —
gerando a chave substituta (M5) por hash das colunas naturais.
:::

---
**Revisado em:** 2026-08-24
