# Exercício 03 — XCom: dependências, e o limite do que se passa entre tasks

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Na TaskFlow API, o `return` de uma task vira **XCom** e chega como argumento às tasks seguintes
(teoria 02). O erro clássico de quem começa é devolver o **dataset** inteiro por XCom: ele vai parar
no banco de metadados do Airflow, que não foi feito para isso — o scheduler fica lento, o banco
cresce, e em algum momento a task falha por tamanho. A regra: XCom carrega **metadados** (um caminho,
uma contagem, uma data); o dado vai para o storage.

Você vai simular a execução com um limite de tamanho — e ver na prática qual padrão passa.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `executar(tasks, limite_bytes)`.

```bash
cd modulos/09-orquestracao-airflow/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — uma task por vez
Para cada `(nome, ups, func)`: confira que todos os upstreams já têm XCom, monte `{u: xcoms[u] for u in ups}` e chame `func`.
:::
:::{dropdown} Dica 2 — medir o tamanho
`len(json.dumps(valor).encode("utf-8"))` é o tamanho que o XCom ocupa serializado. Compare com o limite **antes** de guardar.
:::
:::{dropdown} Dica 3 — mensagem útil
Inclua o nome da task no erro (o teste procura por ele) — em produção, é o que diz a quem ler o log onde está o problema.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import json


def executar(tasks: list, limite_bytes: int = 1024) -> dict:
    xcoms = {}
    for nome, ups, func in tasks:
        faltando = [u for u in ups if u not in xcoms]
        if faltando:
            raise KeyError(f"{nome} depende de tasks que não rodaram: {faltando}")
        valor = func({u: xcoms[u] for u in ups})
        tamanho = len(json.dumps(valor).encode("utf-8"))
        if tamanho > limite_bytes:
            raise ValueError(f"XCom de {nome} tem {tamanho} bytes (> {limite_bytes}): "
                             "grave no storage e passe só o caminho")
        xcoms[nome] = valor
    return xcoms
```
O primeiro teste é o desenho certo: `extrair` grava o arquivo no storage e devolve **o caminho** e a
contagem; as tasks seguintes trabalham com referências. O terceiro é o anti-padrão: 500 linhas já
passam de 1 KB por XCom — com um dia real de vendas, seriam megabytes no banco de metadados a cada
execução.

O limite existe também no Airflow real (depende do banco de metadados), e há *XCom backends*
customizados que gravam o valor no S3/GCS e guardam só a referência — que é, no fundo, o mesmo padrão
feito por baixo dos panos.
:::

---
**Revisado em:** 2026-09-30
