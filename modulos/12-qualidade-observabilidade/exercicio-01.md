# Exercício 01 — Perfil de completude de um lote

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Completude é a dimensão de qualidade mais checada (teoria 01) — e a mais mal medida. "Contar
`None`" deixa passar o que realmente chega das fontes: string vazia de formulário, espaço em
branco de sistema legado, `NaN` que o pandas cria ao ler um CSV. Você vai escrever o **perfil de
completude** de um lote inteiro (todas as colunas de uma vez), que é o primeiro relatório que um
check de qualidade produz.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente `perfil_completude(linhas, campos)` (fração preenchida por campo) e
`campos_abaixo(perfil, limiar)` (os campos que reprovam).

```bash
cd modulos/12-qualidade-observabilidade/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — uma função para 'ausente'
Escreva `_ausente(v)`: `None`, `NaN` (`isinstance(v, float) and math.isnan(v)`) e string com `v.strip() == ""`. Cuidado: `if not v` trataria `0` e `False` como ausentes — errado.
:::
:::{dropdown} Dica 2 — contar com sum()
`sum(not _ausente(r.get(c)) for r in linhas)` conta os presentes (True vale 1). `r.get(c)` devolve `None` quando a chave não existe — e isso já é ausência.
:::
:::{dropdown} Dica 3 — ordenar do pior
`sorted(..., key=lambda c: (perfil[c], c))` ordena pela fração e desempata pelo nome.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import math


def _ausente(v) -> bool:
    if v is None:
        return True
    if isinstance(v, float) and math.isnan(v):
        return True
    return isinstance(v, str) and v.strip() == ""


def perfil_completude(linhas: list, campos: list) -> dict:
    if not linhas:
        raise ValueError("lote vazio: completude indefinida")
    total = len(linhas)
    return {c: round(sum(not _ausente(r.get(c)) for r in linhas) / total, 4) for c in campos}


def campos_abaixo(perfil: dict, limiar: float) -> list:
    return sorted((c for c, v in perfil.items() if v < limiar), key=lambda c: (perfil[c], c))
```
Os testes cobrem as quatro formas de "vazio" que aparecem de verdade: chave ausente (JSON que omite
o campo), `None`, `""`/`"  "` (formulário e sistemas legados) e `NaN` (o `pd.read_csv` cria para
célula vazia — lembre do `"N/A"` no exercício 11 do M05). E o contrário também importa: `0` e
`False` **são** informação. Um check que usa `if not valor` reprova descontos zerados e aprova
e-mails em branco.

Lote vazio levanta erro de propósito: 0/0 não é "100% completo" nem "0%" — é um lote que não
chegou, e isso é assunto do check de **volume** (exercício 06).
:::

---
**Revisado em:** 2026-09-30
