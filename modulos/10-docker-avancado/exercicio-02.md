# Exercício 02 — .dockerignore com curingas e negação

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O `docker build` envia a pasta inteira (o **contexto**) para o builder, e é desse contexto que o
`COPY .` copia. Sem um bom `.dockerignore` (teoria 01), vão junto o `.git`, o `.venv`, os dados de
teste de 2 GB — e o `.env` com senhas, que acaba **dentro da imagem**.

As regras seguem uma lógica própria: curingas (`*.log`, `**/__pycache__`), pastas, e **negação** com
`!` para reincluir uma exceção (`!data/amostra.csv`). Quando várias regras casam com um caminho, vale a
**última**.

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `no_contexto(arquivos, regras)` e `tamanho_do_contexto(tamanhos, regras)`.

```bash
cd modulos/10-docker-avancado/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — uma função de casamento
Separe `_casa(regra, caminho)`: pasta (`/` no fim) é prefixo; `**/x` procura `x` em qualquer nível; o resto usa `fnmatch` no caminho inteiro.
:::
:::{dropdown} Dica 2 — a última vence
Para cada arquivo, percorra **todas** as regras em ordem, atualizando `ignorado` a cada uma que casar (`True` para normais, `False` para as com `!`).
:::
:::{dropdown} Dica 3 — comentários
Descarte linhas vazias e as que começam com `#` antes de tudo.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from fnmatch import fnmatch


def _casa(regra: str, caminho: str) -> bool:
    if regra.endswith("/"):
        return caminho.startswith(regra)
    if regra.startswith("**/"):
        base = regra[3:]
        partes = caminho.split("/")
        return any(fnmatch("/".join(partes[i:]), base) or fnmatch(p, base) for i, p in enumerate(partes))
    return fnmatch(caminho, regra) or caminho.startswith(regra + "/")


def no_contexto(arquivos: list, regras: list) -> list:
    ativas = [r.strip() for r in regras if r.strip() and not r.strip().startswith("#")]
    incluidos = []
    for arq in arquivos:
        ignorado = False
        for r in ativas:
            neg = r.startswith("!")
            if _casa(r[1:] if neg else r, arq):
                ignorado = not neg
        if not ignorado:
            incluidos.append(arq)
    return sorted(incluidos)


def tamanho_do_contexto(tamanhos: dict, regras: list) -> int:
    return sum(tamanhos[a] for a in no_contexto(list(tamanhos), regras))
```
Sem regras, o contexto tem 2 GB — e cada `docker build` envia os 2 GB ao builder antes de começar. Com o
`.dockerignore`, 53 KB. A regra `!data/amostra.csv` depois de `data/` é o padrão para levar só a
amostra de dados que o teste de integração precisa.

O item mais importante da lista, porém, é o `.env`: sem ele no `.dockerignore`, um `COPY . /app` grava
as credenciais **numa camada da imagem**. Quem tiver a imagem (ou acesso ao registry, exercício 06)
extrai o arquivo com um `docker cp`. Segredo vai por variável de ambiente ou secret do orquestrador, nunca
na imagem (teoria 03).
:::

---
**Revisado em:** 2026-09-30
