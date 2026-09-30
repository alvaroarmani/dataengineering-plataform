# Exercício 06 — Service discovery: como o DNS do cluster resolve nomes

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Dentro do Kubernetes, um pod chama outro serviço pelo **nome** (teoria 03): `api`, `api.prod` ou o
nome completo `api.prod.svc.cluster.local`. Quem resolve é o DNS do cluster, usando uma lista de
**domínios de busca** que depende do namespace de quem pergunta. Por isso o mesmo nome curto `db`
aponta para bancos **diferentes** em `dev` e em `prod` — e por isso um serviço de dados que funciona
em staging pode quebrar em produção só por causa de um nome.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `resolver(nome, namespace_origem, servicos)`.

```bash
cd modulos/20-cloud-kubernetes/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — conte os rótulos
`nome.split(".")`: 1 rótulo = serviço no namespace de origem; 2 = serviço.namespace; 5 terminando em `svc.cluster.local` = nome completo.
:::
:::{dropdown} Dica 2 — chave de busca
Monte `(servico, namespace)` e procure no dict. Não achou → `KeyError` (o equivalente do NXDOMAIN).
:::
:::{dropdown} Dica 3 — o resto
Qualquer outro formato (3 ou 4 rótulos, vazio) → `ValueError`: é erro de configuração, não serviço ausente.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
SUFIXO = "svc.cluster.local"


def resolver(nome: str, namespace_origem: str, servicos: dict) -> str:
    if not nome:
        raise ValueError("nome vazio")
    partes = nome.split(".")
    if nome.endswith("." + SUFIXO) and len(partes) == 5:
        chave = (partes[0], partes[1])
    elif len(partes) == 2:
        chave = (partes[0], partes[1])
    elif len(partes) == 1:
        chave = (partes[0], namespace_origem)
    else:
        raise ValueError(f"formato de nome não suportado: {nome}")
    if chave not in servicos:
        raise KeyError(f"NXDOMAIN: {nome} (de {namespace_origem})")
    return servicos[chave]
```
O teste do `kafka` é o bug que aparece em produção: o job de ingestão roda no namespace `prod` e
aponta para `kafka`, mas o broker mora no namespace `dados`. Em staging funcionava porque tudo estava
no mesmo namespace. A correção é usar sempre `kafka.dados` (ou o nome completo) em configuração de
serviços que atravessam namespaces.

O nome curto dependente do namespace, por outro lado, é um recurso: o mesmo manifesto aponta para
`db` e cada ambiente resolve o banco certo — `dev` usa o banco de dev sem nenhum `if` na aplicação.
:::

---
**Revisado em:** 2026-09-30
