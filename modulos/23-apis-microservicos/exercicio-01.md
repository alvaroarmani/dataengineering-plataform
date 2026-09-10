# Exercicio 01 - Status HTTP da operacao (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`status_http`** - Mapeie o resultado da operacao ao status HTTP: 'ok'->200, 'criado'->201, 'sem_conteudo'->204, 'requisicao_invalida'->400, 'nao_autorizado'->401, 'nao_encontrado'->404; qualquer outro -> 500.

```bash
cd modulos/23-apis-microservicos/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
dict de resultado->status, com default 500 (erro de servidor).
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def status_http(resultado):
    mapa = {'ok': 200, 'criado': 201, 'sem_conteudo': 204, 'requisicao_invalida': 400, 'nao_autorizado': 401, 'nao_encontrado': 404}
    return mapa.get(resultado, 500)
```
:::

---
**Revisado em:** 2026-09-09
