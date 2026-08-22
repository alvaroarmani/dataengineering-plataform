# Exercício 01 — O que o `.gitignore` ignora (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Entender o `.gitignore` evita o erro nº 1 de iniciantes: **versionar segredos e lixo**.
Aqui você implementa a lógica de correspondência de padrões — e de quebra fixa a semântica.

## Tarefa

Implemente, em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), a função
`arquivos_ignorados(arquivos, padroes)` que recebe uma lista de caminhos e uma lista de
padrões de `.gitignore` (versão simplificada) e retorna a lista dos caminhos **ignorados**,
na ordem de entrada. Suporte três tipos de padrão:

1. **Nome exato:** `.env` casa com o caminho `.env`.
2. **Curinga de extensão:** `*.log` casa com qualquer caminho terminado em `.log`.
3. **Pasta:** `data/` casa com qualquer caminho que comece com `data/`.

Rode os testes até tudo ficar verde:

```bash
cd modulos/02-linux-git-ambiente/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — estrutura
Para cada arquivo, verifique se **algum** padrão casa; se sim, inclua-o no resultado.
:::
:::{dropdown} Dica 2 — os três casos
`padrao.startswith("*.")` → compare o sufixo com `str.endswith`. `padrao.endswith("/")` →
use `str.startswith`. Caso contrário, é igualdade exata.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def arquivos_ignorados(arquivos, padroes):
    def casa(caminho, padrao):
        if padrao.startswith("*."):
            return caminho.endswith(padrao[1:])      # "*.log" -> ".log"
        if padrao.endswith("/"):
            return caminho.startswith(padrao)         # "data/" -> prefixo
        return caminho == padrao                      # nome exato
    return [c for c in arquivos if any(casa(c, p) for p in padroes)]
```
Repare no padrão `any(... for p in padroes)`: um arquivo é ignorado se **qualquer** regra
casar — exatamente como o Git avalia o `.gitignore`.
:::

---
**Revisado em:** 2026-08-21
