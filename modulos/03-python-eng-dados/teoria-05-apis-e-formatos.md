# APIs e formatos: de onde vêm os dados e como guardá-los

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Boa parte dos dados de uma empresa não está num arquivo prontinho — está atrás de uma
**API** (câmbio, pagamentos, CRM) ou espalhada em arquivos de formatos diferentes. Saber
**buscar** dados de uma API (com paginação, autenticação e limites) e **escolher o formato**
certo para guardá-los (CSV vs Parquet) é o primeiro passo de todo pipeline de ingestão.

## 💡 Conceito (o porquê)

### Consumir uma API REST
Uma **API REST** devolve dados (geralmente **JSON**) quando você faz uma requisição HTTP a
uma URL. Em Python, a biblioteca `requests` é o padrão:

```python
import requests
r = requests.get("https://api.exemplo.com/pedidos", params={"page": 1})
r.raise_for_status()          # levanta erro se o status não for 2xx
dados = r.json()              # JSON -> dict/list do Python
```

O que separa um script de brinquedo de uma ingestão de verdade:
- **Paginação:** a API devolve os dados em "páginas"; você percorre `page=1,2,3…` até acabar.
- **Rate limit:** há um limite de requisições por minuto — respeite (espere, faça *retry*).
- **Autenticação:** muitas exigem uma chave/token no cabeçalho (`Authorization`).
- **Ingestão incremental:** em vez de baixar tudo sempre, peça só o **novo** (ex.: `?desde=<data>`).

### De JSON aninhado para tabela
APIs adoram JSON **aninhado** (um pedido com um cliente dentro e uma lista de itens). Para
analisar, você **achata** isso numa tabela. `pandas.json_normalize` ajuda, mas muitas vezes
um laço simples resolve.

### Formatos de arquivo: CSV vs Parquet
Onde guardar o que você ingeriu?

| | CSV | Parquet |
|---|---|---|
| Layout | linha, texto | **coluna, binário** |
| Schema/tipos | não guarda | **guarda** |
| Compressão | ruim | **ótima** |
| Ler só algumas colunas | não | **sim** |
| Uso | troca simples, humanos | **analytics em escala** |

Em pipelines sérios, os dados brutos costumam pousar como **Parquet** (colunar, tipado,
comprimido). Em pandas: `df.to_parquet("dados.parquet")` e `pd.read_parquet(...)`.

## 🔎 Exemplo

```python
# baixa todas as páginas de uma API paginada
todos = []
page = 1
while True:
    r = requests.get(URL, params={"page": page}, headers={"Authorization": f"Bearer {TOKEN}"})
    r.raise_for_status()
    lote = r.json()["data"]
    if not lote:
        break                 # acabou
    todos.extend(lote)
    page += 1
```

:::{admonition} 📖 Da literatura
:class: seealso
Densmore descreve a extração via API como um dos padrões centrais de ingestão, destacando o
tratamento de paginação e a extração **incremental** (só o que mudou) como chave para
pipelines eficientes e reexecutáveis. — *Data Pipelines Pocket Reference*, cap. de extração.
:::

## ⚠️ Erros comuns
- Não checar o **status** da resposta (`raise_for_status`) e seguir com dados vazios/erro.
- Ignorar **paginação** e pegar só a primeira página.
- Estourar o **rate limit** (sem espera/retry) e ser bloqueado.
- Guardar tudo como **CSV** onde Parquet economizaria tempo e espaço.
- Colocar **token/segredo** no código (use variável de ambiente!).

## 💼 O que o mercado espera
Ingerir de uma API com paginação e salvar em Parquet é tarefa quase certa. Saber fazer
extração **incremental** e tratar erros de rede é sinal de maturidade.

:::{admonition} ✨ Em resumo
:class: resumo
- API REST → HTTP → **JSON**; use `requests` e cheque o status (`raise_for_status`).
- Trate **paginação**, **rate limit**, **auth** e prefira ingestão **incremental**.
- JSON aninhado → **achatar** em tabela para analisar.
- Guarde dados brutos como **Parquet** (colunar, tipado, comprimido), não CSV.
:::

## 🧠 Quiz de recall
1. O que é paginação e por que ela importa na ingestão de uma API?
   :::{dropdown} Resposta
   A API devolve os dados em páginas (lotes); é preciso percorrer todas (`page=1,2,3…`) até acabar, senão você pega só parte dos dados.
   :::
2. Por que preferir Parquet a CSV para dados brutos em escala?
   :::{dropdown} Resposta
   Parquet é colunar e binário: guarda schema/tipos, comprime muito melhor e permite ler só as colunas necessárias — mais rápido e barato. CSV não guarda tipos e é ineficiente.
   :::
3. O que é ingestão incremental?
   :::{dropdown} Resposta
   Baixar apenas o que é novo/mudou (ex.: `?desde=<data>`) em vez de reprocessar tudo sempre — mais eficiente e reexecutável.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você lidaria com o rate limit de uma API ao ingerir muitos dados?"
  :::{dropdown} Resposta modelo
  Respeitando o limite: espaçar as requisições, ler os cabeçalhos de rate limit quando existirem, e implementar *retry* com *backoff* exponencial em respostas 429. Idealmente, ingestão incremental para reduzir o volume.
  :::
- **P:** "Onde você guardaria os dados brutos de uma ingestão diária?"
  :::{dropdown} Resposta modelo
  Em object storage (S3/GCS/MinIO) no formato **Parquet**, particionado por data (ex.: `ano=2026/mes=08/dia=22`), formando a camada *raw/bronze* de um lake/lakehouse.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Densmore — Data Pipelines Pocket Reference**, capítulos de extração e de armazenamento.
- **Docs do pandas** — `read_csv`, `to_parquet`/`read_parquet`.
- **Docs do Python** — módulo `json`.

## 📚 Referências
- Densmore, J. *Data Pipelines Pocket Reference* (O'Reilly, 2021) — extração e formatos. <!-- @densmore2021 -->
- pandas. *Documentação oficial* — [IO tools (CSV, Parquet)](https://pandas.pydata.org/docs/user_guide/io.html). <!-- @docs-pandas -->
- Python. *Documentação oficial* — [módulo json](https://docs.python.org/3/library/json.html). <!-- @docs-python -->

*Acessado em: 2026-08-22.*

---
**Revisado em:** 2026-08-22
