# Exercício 04 — Lendo o git status --porcelain

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
`git status` mostra em que área cada arquivo está (teoria 02). Scripts e hooks não leem a saída
"bonita" — leem o formato estável `git status --porcelain`, feito para máquinas. Cada linha tem
**duas letras** de estado e o caminho: a primeira letra é o **índice** (staging), a segunda é a
**árvore de trabalho**. Um mesmo arquivo pode estar nas duas: você deu `git add` e depois mudou de novo
(`MM`). Arquivos novos não rastreados aparecem como `??`, e renomeações como `R  antigo -> novo`.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `resumo_status(saida)`.

```bash
cd modulos/02-linux-git-ambiente/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — posições fixas
No formato porcelain, `linha[0]` é o índice, `linha[1]` é a árvore, `linha[2]` é um espaço e o caminho começa em `linha[3:]`.
:::
:::{dropdown} Dica 2 — duas perguntas independentes
O arquivo está staged se a letra do índice não é espaço nem `?`; está não-staged se a letra da árvore não é espaço nem `?`. Pode ser os dois.
:::
:::{dropdown} Dica 3 — renomeações
Com `X == "R"`, o caminho vem como `antigo -> novo`: `split(" -> ")` e use o novo nome daí em diante.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def resumo_status(saida: str) -> dict:
    res = {"staged": [], "nao_staged": [], "untracked": [], "renomeados": []}
    for linha in saida.splitlines():
        if not linha.strip():
            continue
        if len(linha) < 4 or linha[2] != " " or linha[0] not in " MADRCU?" or linha[1] not in " MADRCU?":
            raise ValueError(f"linha malformada: {linha!r}")
        x, y, caminho = linha[0], linha[1], linha[3:]
        if x == "?" and y == "?":
            res["untracked"].append(caminho)
            continue
        if x == "R":
            antigo, novo = caminho.split(" -> ")
            res["renomeados"].append((antigo, novo))
            caminho = novo
        if x not in " ?":
            res["staged"].append(caminho)
        if y not in " ?":
            res["nao_staged"].append(caminho)
    return {k: sorted(v) for k, v in res.items()}
```
O `MM` em `models/fct_vendas.sql` é a pegadinha que o formato resolve: você fez `git add` de uma
versão e depois continuou editando. O próximo `git commit` leva **a versão do índice**, não a que está
no seu editor — e é por isso que hooks de pre-commit (como o do exercício 02) varrem o que está
**staged**, não o que está na pasta.

Repare também no `.env` aparecendo como untracked: ele não está no `.gitignore` deste projeto
(exercício 01). Um hook que lê esta saída poderia avisar antes que alguém rode `git add .`.
:::

---
**Revisado em:** 2026-09-30
