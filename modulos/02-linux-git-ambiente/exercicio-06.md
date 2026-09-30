# Exercício 06 — Portas publicadas: parse e conflitos

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
`docker run -p 8080:80` publica a porta 80 do container na 8080 da máquina (teoria 03). A
especificação completa aceita mais: IP de escuta (`127.0.0.1:5432:5432`, que só aceita conexões
locais — o jeito certo de expor um banco de desenvolvimento) e protocolo (`5353:53/udp`). Na bancada
com vários serviços, o erro mais comum é dois serviços pedindo **a mesma porta do host** — o segundo
não sobe, com um "port is already allocated".

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `parse_porta(spec)` e `conflitos(servicos)`.

```bash
cd modulos/02-linux-git-ambiente/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — protocolo primeiro
`spec.partition("/")` separa o protocolo (vazio → tcp). O resto, `split(":")`, tem 1, 2 ou 3 partes.
:::
:::{dropdown} Dica 2 — validar portas
Uma função interna `porta(p)` que exige dígitos e faixa 1–65535 evita repetir a validação.
:::
:::{dropdown} Dica 3 — conflitos
Colete `(host, protocolo, ip, servico)` de todos; compare os pares. Colidem se host e protocolo são iguais e os IPs são iguais ou um deles é `0.0.0.0`. Agrupe por `(host, protocolo)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def parse_porta(spec: str) -> dict:
    corpo, _, proto = spec.partition("/")
    proto = proto or "tcp"
    if proto not in ("tcp", "udp"):
        raise ValueError(f"protocolo inválido: {proto}")
    partes = corpo.split(":")
    if len(partes) == 1:
        ip, host, cont = "0.0.0.0", None, partes[0]
    elif len(partes) == 2:
        ip, host, cont = "0.0.0.0", partes[0], partes[1]
    elif len(partes) == 3:
        ip, host, cont = partes
    else:
        raise ValueError(f"formato inválido: {spec}")

    def porta(p):
        if not p.isdigit() or not 1 <= int(p) <= 65535:
            raise ValueError(f"porta inválida: {p}")
        return int(p)

    return {"ip": ip, "host": porta(host) if host is not None else None,
            "container": porta(cont), "protocolo": proto}


def conflitos(servicos: dict) -> list:
    usos = []
    for servico, specs in servicos.items():
        for s in specs:
            p = parse_porta(s)
            if p["host"] is not None:
                usos.append((p["host"], p["protocolo"], p["ip"], servico))
    grupos = {}
    for i, (h, pr, ip, sv) in enumerate(usos):
        for h2, pr2, ip2, sv2 in usos[i + 1:]:
            if h == h2 and pr == pr2 and (ip == ip2 or "0.0.0.0" in (ip, ip2)):
                grupos.setdefault((h, pr), set()).update({sv, sv2})
    return sorted((h, pr, sorted(svs)) for (h, pr), svs in grupos.items())
```
O conflito do Postgres é o mais sutil: um serviço escuta só em `127.0.0.1:5432` e o outro em
`0.0.0.0:5432`, que inclui o `127.0.0.1` — o Docker recusa o segundo. Já `127.0.0.1` e
`192.168.0.10` na mesma porta convivem, porque são interfaces diferentes.

Na bancada do curso (`ambiente/docker-compose.yml`), o banco é publicado em `127.0.0.1`: acessível
do seu computador, invisível para a rede do café. É a versão de desenvolvimento do princípio do menor
privilégio (M14).
:::

---
**Revisado em:** 2026-09-30
