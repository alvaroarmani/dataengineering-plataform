# Lab 03 — Ingerir uma API real: Banco Central (walkthrough guiado)

**Onde roda:** 🐳 Bancada Docker (Python + `requests`, com rede). É uma API **pública e sem
chave**. Confira os **self-checks** ✅. A lógica de paginação/retry você fixa nos
[Exercícios 05](exercicio-05.md) e [06](exercicio-06.md) (no navegador).

> Rode no JupyterLab da bancada (`http://localhost:8888`) — o navegador do curso (JupyterLite)
> costuma **bloquear** requisições externas por CORS; a bancada não.

---

## 1. Uma requisição simples (série do dólar)
O SGS do Banco Central expõe séries temporais em JSON. A série **1** é o câmbio USD/BRL:
```python
import requests

url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/5"
r = requests.get(url, params={"formato": "json"}, timeout=15)
r.raise_for_status()
dados = r.json()
dados
```
✅ *Self-check:* `dados` é uma lista de dicts com `data` e `valor` (os últimos 5 dias úteis).

---

## 2. Robustez: timeout, status e erro
```python
def buscar_serie(serie_id, ultimos=10):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie_id}/dados/ultimos/{ultimos}"
    r = requests.get(url, params={"formato": "json"}, timeout=15)
    r.raise_for_status()          # levanta em 4xx/5xx
    return r.json()

serie = buscar_serie(1, ultimos=10)
len(serie), serie[0], serie[-1]
```
✅ *Self-check:* retorna 10 registros; `raise_for_status()` protegeria de um 4xx/5xx.

---

## 3. Ingestão incremental (por intervalo de datas)
O SGS aceita `dataInicial`/`dataFinal` (dd/MM/aaaa) — a base do incremental por marca d'água:
```python
r = requests.get(
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados",
    params={"formato": "json", "dataInicial": "01/08/2026", "dataFinal": "15/08/2026"},
    timeout=15,
)
r.raise_for_status()
len(r.json())
```
✅ *Self-check:* volta só os registros do intervalo pedido. Guardando a última `data`, amanhã
você pede só o que veio depois — **incremental** (U1).

---

## 4. (Opcional) Salvar no Postgres da bancada
```python
import psycopg2, os
con = psycopg2.connect(host="postgres", user="curso", password="curso", dbname="curso")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS cambio(data DATE PRIMARY KEY, valor NUMERIC)")
for reg in serie:
    d = "-".join(reversed(reg["data"].split("/")))  # dd/MM/aaaa -> aaaa-MM-dd
    cur.execute(
        "INSERT INTO cambio(data, valor) VALUES (%s, %s) ON CONFLICT (data) DO UPDATE SET valor = EXCLUDED.valor",
        (d, reg["valor"]),
    )
con.commit()
cur.execute("SELECT COUNT(*) FROM cambio"); print(cur.fetchone())
```
✅ *Self-check:* a tabela `cambio` recebe os dados; o `ON CONFLICT` torna a carga **idempotente**
(rodar de novo não duplica).

---

## O que você levou daqui
Ingeriu de uma **API real** com timeout e tratamento de status, filtrou por intervalo
(incremental) e salvou de forma idempotente. Agora fixe a **paginação** e o **retry/backoff** nos
[Exercícios 05](exercicio-05.md) e [06](exercicio-06.md).

---
**Revisado em:** 2026-08-29
