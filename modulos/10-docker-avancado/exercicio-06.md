# Exercício 06 — Referência de imagem: registry, tag, digest e reprodutibilidade

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
`postgres:16`, `ghcr.io/dbt-labs/dbt-postgres:1.8.2` e `localhost:5000/etl@sha256:ab12...` são todas
**referências de imagem** (teoria 03), e a forma curta esconde convenções: sem registry, é o Docker Hub
(`docker.io`), e imagens oficiais moram em `library/`; sem tag, é `latest`; e um `:` pode ser a porta do
registry, não a tag.

Para **reprodutibilidade**, só existe uma referência que nunca muda: o **digest** (`@sha256:...`). Uma
tag de versão (`16.4`) quase nunca muda; `latest` e tags "flutuantes" (`16`, `slim`) mudam o tempo todo.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `parse_imagem(ref)` e `reprodutivel(ref)`.

```bash
cd modulos/10-docker-avancado/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — digest primeiro
`ref.partition("@")` separa o digest. No que sobrou, decida se o primeiro segmento (antes da primeira `/`) é um registry: tem `.`, `:` ou é `localhost`.
:::
:::{dropdown} Dica 2 — tag
Depois de tirar o registry, um `:` no repositório separa a tag (`rsplit(":", 1)`). Sem tag e sem digest, é `latest`.
:::
:::{dropdown} Dica 3 — convenções do Docker Hub
No `docker.io`, um nome sem `/` ganha o prefixo `library/`. Repositórios são sempre minúsculos.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import re


def parse_imagem(ref: str) -> dict:
    if not ref or " " in ref:
        raise ValueError("referência inválida")
    resto, _, digest = ref.partition("@")
    partes = resto.split("/")
    if len(partes) > 1 and ("." in partes[0] or ":" in partes[0] or partes[0] == "localhost"):
        registry, repo = partes[0], "/".join(partes[1:])
    else:
        registry, repo = "docker.io", resto
    tag = None
    if ":" in repo:
        repo, tag = repo.rsplit(":", 1)
    if tag is None and not digest:
        tag = "latest"
    if registry == "docker.io" and "/" not in repo:
        repo = "library/" + repo
    if repo != repo.lower() or not repo:
        raise ValueError("repositório deve ser minúsculo")
    return {"registry": registry, "repositorio": repo, "tag": tag, "digest": digest or None}


def reprodutivel(ref: str) -> str:
    p = parse_imagem(ref)
    if p["digest"]:
        return "digest"
    if p["tag"] and re.search(r"\d+\.\d+", p["tag"]):
        return "versao"
    return "flutuante"
```
`localhost:5000/etl` mostra por que o parser precisa olhar o **primeiro segmento** antes de procurar a
tag: o `:5000` é a porta do registry local. E `postgres:16` é classificado como **flutuante**: a tag `16`
aponta para o último `16.x` publicado, então dois builds em semanas diferentes podem receber imagens
diferentes.

Em produção, a prática é pinar pelo menos a versão completa (`postgres:16.4`) e, em pipelines críticos,
o **digest** — que é o que o CI registra ao publicar a imagem (M13). Ferramentas como o Dependabot/
Renovate atualizam essas referências com PRs, para que a atualização seja uma decisão revisada.
:::

---
**Revisado em:** 2026-09-30
