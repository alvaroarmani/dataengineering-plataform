# Exercício 01 — Serverless ou container? A decisão pelo custo

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Serverless é mais barato" e "container é mais barato" são as duas frases erradas mais repetidas em
arquitetura de nuvem. As duas estão certas — **em faixas diferentes de tráfego**. O modelo de
cobrança é o que muda (teoria 01, "Custo é um cidadão de primeira classe"):

- **serverless** cobra **por uso** (requisição + GB-segundo), com cota gratuita: ocioso custa zero;
- **container sempre ligado** cobra **por tempo**: custa o mesmo com 0 ou 1 milhão de requisições.

Então existe um **ponto de equilíbrio**: abaixo dele, serverless; acima, container. Seu trabalho é
calculá-lo — é o tipo de número que decide uma arquitetura numa revisão de design (e que o M21,
FinOps, aprofunda).

:::{admonition} Preços ilustrativos
:class: note
Os preços do `solucao.py` têm a ordem de grandeza das tabelas públicas, mas **não são** a tabela de
nenhum provedor numa data específica. Na vida real, pegue os preços da região e da data do seu
projeto — o método é o que importa.
:::

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente `custo_serverless`,
`custo_container`, `recomendar` e `ponto_de_equilibrio`.

```bash
cd modulos/20-cloud-kubernetes/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — a cota gratuita
Desconte a cota **antes** de multiplicar pelo preço e nunca deixe ficar negativo:
`max(0, req_mes - GRATIS_REQ)`. O mesmo vale para os GB-segundos.
:::
:::{dropdown} Dica 2 — economia percentual
É a diferença sobre a opção **mais cara**: `100 * abs(s - c) / max(s, c)`. Cuidado com a divisão
por zero quando as duas custam 0.
:::
:::{dropdown} Dica 3 — busca binária
Ache um `hi` em que o serverless já é mais caro (dobrando a partir de 1). Depois, busca binária:
se `custo_serverless(meio) > alvo`, a resposta está em `[lo, meio]`; senão, em `[meio + 1, hi]`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def custo_serverless(req_mes, duracao_ms, memoria_gb):
    if min(req_mes, duracao_ms, memoria_gb) < 0:
        raise ValueError("argumento negativo")
    gb_s = req_mes * (duracao_ms / 1000) * memoria_gb
    req_cobradas = max(0, req_mes - GRATIS_REQ)
    gb_s_cobrados = max(0, gb_s - GRATIS_GB_SEGUNDO)
    return round(req_cobradas / 1e6 * PRECO_POR_MILHAO_REQ + gb_s_cobrados * PRECO_GB_SEGUNDO, 2)

def custo_container(vcpu, memoria_gb, replicas=1):
    if vcpu <= 0 or memoria_gb <= 0 or replicas < 1:
        raise ValueError("recurso inválido")
    return round(replicas * HORAS_MES * (vcpu * PRECO_VCPU_HORA + memoria_gb * PRECO_GB_HORA), 2)

def recomendar(req_mes, duracao_ms, memoria_fn_gb, vcpu, memoria_ct_gb, replicas=1):
    s = custo_serverless(req_mes, duracao_ms, memoria_fn_gb)
    c = custo_container(vcpu, memoria_ct_gb, replicas)
    escolha = "serverless" if s <= c else "container"
    mais_cara = max(s, c)
    economia = 0.0 if mais_cara == 0 else round(100 * abs(s - c) / mais_cara, 1)
    return {"escolha": escolha, "serverless": s, "container": c, "economia_pct": economia}

def ponto_de_equilibrio(duracao_ms, memoria_fn_gb, vcpu, memoria_ct_gb, replicas=1):
    alvo = custo_container(vcpu, memoria_ct_gb, replicas)
    lo, hi = 0, 1
    while custo_serverless(hi, duracao_ms, memoria_fn_gb) <= alvo:
        hi *= 2                                    # acha um teto
    while lo < hi:                                 # menor req em que serverless > container
        meio = (lo + hi) // 2
        if custo_serverless(meio, duracao_ms, memoria_fn_gb) > alvo:
            hi = meio
        else:
            lo = meio + 1
    return lo
```
**O que os testes mostram:** com função de 200 ms/0,5 GB contra um container de 0,5 vCPU/1 GB, o
equilíbrio fica em ~13 milhões de requisições/mês — **uns 5 por segundo**, em média. É pouco! Por
isso APIs com tráfego constante tendem a container, e tarefas esporádicas (webhook, gatilho de
arquivo, cron) tendem a serverless.

Dois efeitos que viram pergunta de entrevista: **duração e memória** puxam o equilíbrio para baixo
(função lenta sai cara), e **réplicas** para alta disponibilidade puxam para cima (o container
dobra de preço; o serverless já é redundante sem custo extra).
:::

---
**Revisado em:** 2026-09-29
