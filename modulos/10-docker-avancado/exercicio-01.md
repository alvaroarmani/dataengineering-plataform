# Exercício 01 — Cache de camadas: o que reconstrói quando um arquivo muda

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Cada instrução do Dockerfile gera uma camada, e o build reaproveita as camadas do cache **até a primeira
que mudou** — dali em diante, tudo é refeito (teoria 01). Uma instrução "muda" se o **texto** dela mudou
ou, num `COPY`, se algum dos **arquivos copiados** mudou. É por isso que a ordem importa tanto: com
`COPY . /app` antes do `RUN pip install`, qualquer alteração num `.py` refaz a instalação das
dependências, e cada build leva minutos em vez de segundos.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente `passos_reconstruidos(dockerfile, alterados)` e `tempo_de_build(dockerfile, alterados)`.

```bash
cd modulos/10-docker-avancado/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — quando um COPY muda
Um passo copia o arquivo se a lista dele tem `"."`, o próprio caminho, ou uma pasta (terminada em `/`) que é prefixo do caminho.
:::
:::{dropdown} Dica 2 — o primeiro sujo
Percorra os passos em ordem; o primeiro com texto alterado **ou** que copia um arquivo alterado invalida ele e todos os seguintes.
:::
:::{dropdown} Dica 3 — tempo
Some a duração só dos passos reconstruídos.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def _copia(passo, arquivo):
    origem = passo.get("copia", [])
    return "." in origem or arquivo in origem or any(o.endswith("/") and arquivo.startswith(o) for o in origem)


def passos_reconstruidos(dockerfile: list, alterados: dict) -> list:
    for i, passo in enumerate(dockerfile):
        texto_mudou = i in alterados.get("instrucoes", [])
        arquivo_mudou = any(_copia(passo, a) for a in alterados.get("arquivos", []))
        if texto_mudou or arquivo_mudou:
            return list(range(i, len(dockerfile)))
    return []


def tempo_de_build(dockerfile: list, alterados: dict) -> int:
    return sum(dockerfile[i]["seg"] for i in passos_reconstruidos(dockerfile, alterados))
```
A mesma edição em `src/etl.py` custa **182 s** na ordem ruim e **1 s** na boa: separar
`COPY requirements.txt` + `RUN pip install` do `COPY` do código faz a camada cara (as dependências) só
ser refeita quando as dependências mudam. Num time que faz dezenas de builds por dia (e no CI, M13), é a
diferença entre um ciclo de feedback de segundos e um de minutos.

O último teste mostra outro ganho da ordem boa: copiar só `src/` (e não `.`) faz o `README.md` nem
entrar na imagem. O `.dockerignore` (exercício 02) completa o trabalho para quem precisa usar `COPY .`.
:::

---
**Revisado em:** 2026-09-30
