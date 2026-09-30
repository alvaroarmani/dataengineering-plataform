# Exercício 03 — Conventional Commits: validar e calcular a próxima versão

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O padrão **Conventional Commits** (teoria 02) não é só estética: como a mensagem tem estrutura
(`tipo(escopo)!: descrição`), ferramentas conseguem **ler o histórico** e decidir sozinhas a próxima
versão do projeto (semantic-release, release-please). `fix` gera versão de correção, `feat` gera
versão menor, e uma mudança incompatível — marcada com `!` ou com o rodapé `BREAKING CHANGE:` —
gera versão maior.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `analisar_commit(mensagem)` e `proxima_versao(versao, mensagens)`.

```bash
cd modulos/02-linux-git-ambiente/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — uma regex com grupos
`^(?P<tipo>[a-z]+)(\((?P<escopo>...)\))?(?P<quebra>!)?: (?P<desc>\S.*)$` — grupos nomeados deixam o código legível. Repare no espaço obrigatório depois dos dois-pontos.
:::
:::{dropdown} Dica 2 — breaking de dois jeitos
`!` no cabeçalho **ou** uma linha do corpo começando com `BREAKING CHANGE:`.
:::
:::{dropdown} Dica 3 — a versão
Analise todos os commits (um inválido derruba tudo) e aplique a regra da maior mudança: breaking > feat > fix/perf > nada.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import re

TIPOS = {"feat", "fix", "docs", "chore", "refactor", "test", "perf", "ci", "build", "style"}
CABECALHO = re.compile(r"^(?P<tipo>[a-z]+)(\((?P<escopo>[a-z0-9_\-/]+)\))?(?P<quebra>!)?: (?P<desc>\S.*)$")


def analisar_commit(mensagem: str) -> dict:
    linhas = mensagem.strip().splitlines()
    if not linhas:
        raise ValueError("mensagem vazia")
    cab = linhas[0]
    if len(cab) > 72:
        raise ValueError("primeira linha com mais de 72 caracteres")
    m = CABECALHO.match(cab)
    if not m or m.group("tipo") not in TIPOS:
        raise ValueError(f"cabeçalho fora do padrão: {cab!r}")
    breaking = bool(m.group("quebra")) or any(l.startswith("BREAKING CHANGE:") for l in linhas[1:])
    return {"tipo": m.group("tipo"), "escopo": m.group("escopo"), "breaking": breaking,
            "descricao": m.group("desc")}


def proxima_versao(versao: str, mensagens: list) -> str:
    ma, mi, pa = map(int, versao.split("."))
    commits = [analisar_commit(m) for m in mensagens]
    if any(c["breaking"] for c in commits):
        return f"{ma + 1}.0.0"
    if any(c["tipo"] == "feat" for c in commits):
        return f"{ma}.{mi + 1}.0"
    if any(c["tipo"] in ("fix", "perf") for c in commits):
        return f"{ma}.{mi}.{pa + 1}"
    return versao
```
O teste `fix: ` com 70 `x` passa de 72 caracteres na primeira linha — o limite existe porque
`git log --oneline`, interfaces de PR e e-mails cortam linhas longas. E `Feat:` com maiúscula é
recusado de propósito: o padrão é minúsculo, e a ferramenta de release não reconheceria.

A função `proxima_versao` é, em miniatura, o que o semantic-release faz no CI (M13): lê os commits
desde a última tag e publica a versão certa, sem ninguém decidir "de cabeça". É o mesmo raciocínio
de compatibilidade do versionamento de contratos de API (M23).
:::

---
**Revisado em:** 2026-09-30
