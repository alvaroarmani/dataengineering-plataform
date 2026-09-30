# Exercício 05 — Imagem, container e volume: o que sobrevive a um `docker rm`?

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro — e depois confira na bancada real).

## Contexto
O erro mais caro de quem começa com Docker: subir um Postgres, carregar dados, recriar o container
e descobrir que **tudo sumiu**. Decorar "imagem = molde, container = instância, volume = dado
persistente" não evita esse erro; **prever o que acontece** evita.

Você vai escrever um simulador de bolso das regras que importam:

- a **imagem** é somente leitura e compartilhada por vários containers;
- cada **container** tem a própria **camada gravável** — que morre junto com ele no `rm`;
- um **volume** vive fora do container: sobrevive ao `rm` e pode ser montado de novo;
- o Docker **protege** o que está em uso: não remove imagem nem volume de container existente.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente **`simular(comandos)`**
seguindo as regras da docstring.

```bash
cd modulos/02-linux-git-ambiente/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — o estado
Três estruturas bastam: `imagens = set()`, `containers = {nome: {"imagem", "volume", "camada"}}`
e `volumes = {nome: set()}`. Cada comando é `linha.split()`; despache pelo primeiro token.
:::
:::{dropdown} Dica 2 — onde o arquivo cai
No `escrever`, pergunte duas coisas: "o container tem volume?" **e** "o caminho começa com
`/dados/`?". Só com as duas o arquivo vai para o volume; senão, para `camada`.
:::
:::{dropdown} Dica 3 — as proteções
Antes de `rmi` e `volume rm`, use `any(...)` sobre `containers.values()` para ver se alguém usa o
alvo. Todo "não pode" vira `raise ValueError(...)` com uma mensagem que diga o porquê.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def simular(comandos):
    imagens, containers, volumes = set(), {}, {}
    for linha in comandos:
        p = linha.split()
        if len(p) == 2 and p[0] == "pull":
            imagens.add(p[1])
        elif p[0] == "run" and len(p) in (3, 5):
            nome, img = p[1], p[2]
            if img not in imagens:
                raise ValueError(f"imagem ausente: {img}")      # docker run faria o pull; aqui não
            if nome in containers:
                raise ValueError(f"container já existe: {nome}")
            vol = None
            if len(p) == 5:
                if p[3] != "-v" or not p[4].endswith(":/dados"):
                    raise ValueError(f"montagem inválida: {linha}")
                vol = p[4].split(":")[0]
                volumes.setdefault(vol, set())                  # volume nomeado nasce no 1º uso
            containers[nome] = {"imagem": img, "volume": vol, "camada": set()}
        elif len(p) == 3 and p[0] == "escrever":
            c = containers.get(p[1])
            if c is None:
                raise ValueError(f"container inexistente: {p[1]}")
            if c["volume"] and p[2].startswith("/dados/"):
                volumes[c["volume"]].add(p[2])                  # fora do container: persiste
            else:
                c["camada"].add(p[2])                           # camada gravável: efêmera
        elif len(p) == 2 and p[0] == "rm":
            if p[1] not in containers:
                raise ValueError(f"container inexistente: {p[1]}")
            del containers[p[1]]                                # a camada vai junto
        elif len(p) == 2 and p[0] == "rmi":
            if p[1] not in imagens:
                raise ValueError(f"imagem inexistente: {p[1]}")
            if any(c["imagem"] == p[1] for c in containers.values()):
                raise ValueError(f"imagem em uso: {p[1]}")
            imagens.discard(p[1])
        elif len(p) == 3 and p[:2] == ["volume", "rm"]:
            if p[2] not in volumes:
                raise ValueError(f"volume inexistente: {p[2]}")
            if any(c["volume"] == p[2] for c in containers.values()):
                raise ValueError(f"volume em uso: {p[2]}")
            del volumes[p[2]]
        else:
            raise ValueError(f"comando desconhecido: {linha}")
    return {"imagens": sorted(imagens), "containers": sorted(containers),
            "volumes": {v: sorted(a) for v, a in volumes.items()},
            "camadas": {n: sorted(c["camada"]) for n, c in containers.items()}}
```
**Agora confira na bancada real** (o simulador tem de bater com o Docker):

```bash
docker run -d --name db -e POSTGRES_PASSWORD=x -v pgdata:/var/lib/postgresql/data postgres:16
docker rm -f db && docker volume ls        # o pgdata continua lá
docker volume rm pgdata                    # agora pode: nenhum container o usa
```
Uma diferença proposital: o `docker run` real **baixa** a imagem se ela faltar; o simulador exige o
`pull` explícito para deixar a dependência visível.
:::

---
**Revisado em:** 2026-09-29
