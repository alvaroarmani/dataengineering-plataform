# Exercício 04 — Política de retry: quem tentar de novo e quanto esperar

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Backoff exponencial (teoria 03) é só metade de uma política de retry. A outra metade é saber **o que
não repetir**: um `400` (requisição malformada) vai falhar igual para sempre, e insistir só gera
carga. `429` (rate limit) e `5xx` são transitórios e merecem retry — e quando o servidor manda o
cabeçalho **Retry-After**, ele diz exatamente quanto esperar, e isso vale mais que o seu cálculo.
Tudo com um **teto** de espera e um número máximo de tentativas, para uma dependência fora do ar não
prender o pipeline para sempre.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `espera(tentativa, base, teto)` e `executar_com_retry(respostas, base, teto, max_tentativas)`.

```bash
cd modulos/23-apis-microservicos/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — backoff
`min(teto, base * 2 ** (tentativa - 1))` — sem o teto, a 20ª tentativa esperaria 6 dias.
:::
:::{dropdown} Dica 2 — classifique a resposta
2xx é sucesso; fora de `RETENTAVEIS` é definitivo (pare **sem** esperar); só os retentáveis seguem para a espera.
:::
:::{dropdown} Dica 3 — não espere depois da última
Se a tentativa atual é a última permitida, não registre espera — só saia com "esgotado". O `Retry-After`, quando vem, substitui o backoff (limitado ao teto).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
RETENTAVEIS = {429, 500, 502, 503, 504}


def espera(tentativa: int, base: float, teto: float) -> float:
    if tentativa < 1:
        raise ValueError("tentativa começa em 1")
    return min(teto, base * 2 ** (tentativa - 1))


def executar_com_retry(respostas: list, base: float, teto: float, max_tentativas: int) -> dict:
    esperas = []
    for n, (status, retry_after) in enumerate(respostas[:max_tentativas], start=1):
        if 200 <= status < 300:
            return {"resultado": "sucesso", "tentativas": n, "esperas": esperas}
        if status not in RETENTAVEIS:
            return {"resultado": "falha_definitiva", "tentativas": n, "esperas": esperas}
        if n == max_tentativas:
            break
        esperas.append(min(teto, retry_after) if retry_after is not None else espera(n, base, teto))
    return {"resultado": "esgotado", "tentativas": min(len(respostas), max_tentativas), "esperas": esperas}
```
O teste do `Retry-After` mostra a hierarquia: o servidor pediu 10 s e você espera 10 (não 1); depois
pediu 120, e o teto de 60 corta. Ignorar o `Retry-After` de um `429` costuma render um bloqueio mais
longo da API — o servidor está dizendo exatamente quando voltar.

Em produção, some ao backoff um **jitter** (um valor aleatório na espera) para que mil clientes que
falharam juntos não voltem todos no mesmo segundo, e combine com um **circuit breaker** (teoria 03):
depois de muitas falhas seguidas, pare de tentar por um tempo em vez de martelar um serviço que já
está caído.
:::

---
**Revisado em:** 2026-09-30
