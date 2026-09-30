# Exercício 01 — Um linter de README de portfólio

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O README é a interface do projeto (teoria 01): o recrutador passa 30 segundos nele. Um bom README de
engenharia de dados responde, nessa ordem, **o que** o projeto faz, **por que** (o problema), qual a
**arquitetura** (com um diagrama), **como rodar** (com comandos copiáveis) e **o que aprendi**. Você vai
escrever um linter que lê um README em Markdown e aponta o que falta — aceitando os títulos que as
pessoas realmente usam ("Como executar", "Setup", "Stack"...), não só o nome exato.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente `avaliar_readme(texto)`.

```bash
cd modulos/15-carreira-portfolio-entrevistas/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — só os títulos
Filtre as linhas que começam com `#`, tire os `#` e normalize (sem acento, minúsculas). Palavras no texto corrido não contam.
:::
:::{dropdown} Dica 2 — sinônimos
Uma seção está presente se **algum** título contém **algum** dos sinônimos dela (`any(any(x in t for x in sins) for t in titulos)`).
:::
:::{dropdown} Dica 3 — diagrama e comandos
Regex para imagem Markdown (`!\\[...\\](...)`) e para blocos cercados por três crases com `re.S`; o bloco precisa ter conteúdo além de espaços.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import re
import unicodedata

SECOES = {
    "o_que": ["sobre", "o que e", "visao geral", "resumo", "descricao"],
    "por_que": ["por que", "motivacao", "problema", "contexto"],
    "arquitetura": ["arquitetura", "stack", "desenho", "fluxo"],
    "como_rodar": ["como rodar", "como executar", "execucao", "setup", "instalacao", "quickstart"],
    "aprendizados": ["aprendi", "aprendizados", "licoes", "proximos passos"],
}


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()


def avaliar_readme(texto: str) -> dict:
    titulos = [_norm(l.lstrip("#")) for l in texto.splitlines() if l.lstrip().startswith("#")]
    presentes = {s for s, sins in SECOES.items() if any(any(x in t for x in sins) for t in titulos)}
    faltando = [s for s in SECOES if s not in presentes]
    diagrama = bool(re.search(r"!\[[^\]]*\]\([^)]+\)", texto))
    blocos = re.findall(r"```[^\n]*\n(.*?)```", texto, flags=re.S)
    comandos = any(b.strip() for b in blocos)
    atendidos = len(presentes) + diagrama + comandos
    return {"faltando": faltando, "diagrama": diagrama, "comandos": comandos, "nota": round(100 * atendidos / 7)}
```
O README fraco tem um título "Setup" — a seção de execução está lá —, mas o bloco de código está vazio:
o linter não se deixa enganar pela forma. A nota de 14% traduz o que o recrutador sente em 30 segundos:
não dá para saber o que o projeto faz nem como rodá-lo.

Esse linter cabe num workflow de CI (M13) do seu próprio repositório de portfólio: um check que falha se
o README perder uma seção. É uma forma de usar o próprio portfólio para mostrar DataOps.
:::

---
**Revisado em:** 2026-09-30
