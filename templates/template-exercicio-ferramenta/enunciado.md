# Exercício NN — <título> (TRACK REAL · Postgres na bancada)

**Onde roda:** 🐳 Bancada Docker (Postgres real). Não roda no navegador.

Antes de começar, suba a bancada (uma vez):
```bash
cd ambiente && cp .env.example .env && docker compose up -d
```

## Tarefa
Edite [`solucao.sql`](solucao.sql) e escreva a query pedida. Rode até o `pytest` passar:
```bash
pip install psycopg2-binary pytest    # se ainda não tiver
pytest -q modulos/NN-modulo/exercicio-NN
```
> O teste cria os dados de fixture numa tabela temporária, executa sua query no
> Postgres e confere o resultado. O banco não fica sujo (rollback ao final).

## Dicas progressivas
:::{dropdown} Dica 1
...
:::
:::{dropdown} Dica 2
...
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- solução aqui
```
Explicação do porquê.
:::

---
**Revisado em:** AAAA-MM-DD
