# Exercício 11 — Ingerindo a PTAX real do Banco Central (mini-caso · dados reais)

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro). **Dados reais:** resposta **sem edição** da API
OData PTAX do Banco Central (dólar, jan/2024) —
[`datasets/amostras/ptax_2024_01.json`](../../datasets/amostras/ptax_2024_01.json).

## Contexto
O time de finanças quer a cotação oficial do dólar (PTAX) no warehouse, atualizada todo dia. Você vai
escrever o núcleo do pipeline de ingestão — o que roda dentro da task do Airflow (M09):
**normalizar** a resposta da API, **carregar de forma idempotente**, checar a **completude** e
calcular uma métrica de monitoramento.

Detalhe real que o exercício explora: jan/2024 tem **23 dias de segunda a sexta, mas só 22
cotações** — porque 1º de janeiro é feriado. Uma checagem de completude sem calendário de feriados
dispara um alarme falso todo ano.

> Quer ver a API ao vivo? Rode (fora dos testes):
> `curl "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='01-01-2024'&@dataFinalCotacao='01-31-2024'&$format=json"`

## Tarefa
Em [`exercicio-11/solucao.py`](exercicio-11/solucao.py), implemente:

1. **`normalizar_ptax(payload)`** → registros `{"data", "compra", "venda"}` ordenados por data;
   `ValueError` se o payload não tiver `value` (contrato quebrado).
2. **`upsert_por_data(destino, novos)`** → integração idempotente por data (reprocessar não duplica).
3. **`dias_sem_cotacao(registros, inicio, fim, feriados)`** → dias úteis sem registro.
4. **`maior_variacao_diaria(registros)`** → `(data, variação %)` da maior oscilação da venda entre
   dias consecutivos (4 casas; `None` se houver menos de 2 registros).

```bash
cd modulos/08-ingestao-integracao/exercicio-11
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — normalizar com contrato
Cheque o contrato **antes** de ler: `if "value" not in payload: raise ValueError(...)`. A data é
`dataHoraCotacao[:10]`; converta as cotações com `float(...)`; ordene com `sorted(..., key=...)`.
:::
:::{dropdown} Dica 2 — upsert idempotente
Indexe o destino num dict `{data: registro}`, sobrescreva com os novos e devolva os valores na ordem
das chaves ordenadas. Aplicar o mesmo lote duas vezes tem que dar o mesmo resultado.
:::
:::{dropdown} Dica 3 — completude e variação
Percorra o calendário com `datetime.date` + `timedelta(days=1)`; `weekday() < 5` é seg–sex. Para a
variação, use `zip(registros, registros[1:])` e compare por `abs(...)`, guardando o sinal.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import datetime as dt

def normalizar_ptax(payload):
    if not isinstance(payload, dict) or "value" not in payload:
        raise ValueError("payload fora do contrato: falta a chave 'value'")   # falha alto e cedo
    regs = [{"data": v["dataHoraCotacao"][:10],
             "compra": float(v["cotacaoCompra"]),
             "venda": float(v["cotacaoVenda"])} for v in payload["value"]]
    return sorted(regs, key=lambda r: r["data"])

def upsert_por_data(destino, novos):
    por_data = {r["data"]: r for r in destino}
    for r in novos:
        por_data[r["data"]] = r               # mesma data = substitui (idempotente)
    return [por_data[d] for d in sorted(por_data)]

def dias_sem_cotacao(registros, inicio, fim, feriados):
    tem, fer = {r["data"] for r in registros}, set(feriados)
    d, f = dt.date.fromisoformat(inicio), dt.date.fromisoformat(fim)
    faltando = []
    while d <= f:
        s = d.isoformat()
        if d.weekday() < 5 and s not in fer and s not in tem:
            faltando.append(s)
        d += dt.timedelta(days=1)
    return faltando

def maior_variacao_diaria(registros):
    if len(registros) < 2:
        return None
    melhor = None
    for ant, atual in zip(registros, registros[1:]):
        var = round(100 * (atual["venda"] - ant["venda"]) / ant["venda"], 4)
        if melhor is None or abs(var) > abs(melhor[1]):
            melhor = (atual["data"], var)
    return melhor
```
No mundo real, o calendário de feriados vem de uma tabela de referência (ex.: `dim_data` com a
flag `eh_util`) — a mesma dimensão de data do seu star schema (M05).
:::

---
**Revisado em:** 2026-09-29
