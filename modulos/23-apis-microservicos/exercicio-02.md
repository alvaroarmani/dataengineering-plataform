# Exercício 02 — Paginação por offset x por cursor com dados mudando

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Paginar é a forma de ingerir uma API grande (teoria 01). Existem dois estilos: **offset**
(`?page=3&size=100`) e **cursor** (`?after=<id do último>&size=100`). No papel são equivalentes;
na vida real, a base **muda durante a ingestão** — chegam registros novos enquanto você lê as
páginas. Com offset, um registro inserido no começo empurra tudo uma posição, e você lê um item
**duas vezes** (ou, com exclusão, **pula** um). Com cursor, a próxima página começa depois do
último id visto, e mudanças anteriores não afetam.

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `pagina_offset`, `pagina_cursor` e `ingerir_com_cursor`.

```bash
cd modulos/23-apis-microservicos/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — offset
Página `p` com tamanho `t` começa no índice `(p - 1) * t`. Fatiar além do fim devolve lista vazia — não precisa tratar.
:::
:::{dropdown} Dica 2 — cursor
Ordene por id, filtre `id > depois_de` (ou tudo, se for `None`), pegue os `tamanho` primeiros. Só há próximo cursor se ainda sobrar item depois da página.
:::
:::{dropdown} Dica 3 — ingestão
Laço infinito: busque, acumule, pare quando o cursor voltar `None`. Se o novo cursor não for maior que o anterior, levante erro — senão a ingestão fica em loop para sempre.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def pagina_offset(itens: list, pagina: int, tamanho: int) -> list:
    if pagina < 1 or tamanho < 1:
        raise ValueError("página e tamanho começam em 1")
    ini = (pagina - 1) * tamanho
    return itens[ini:ini + tamanho]


def pagina_cursor(itens: list, depois_de, tamanho: int) -> tuple:
    if tamanho < 1:
        raise ValueError("tamanho começa em 1")
    ordenados = sorted(itens, key=lambda x: x["id"])
    resto = [x for x in ordenados if depois_de is None or x["id"] > depois_de]
    pagina = resto[:tamanho]
    tem_mais = len(resto) > tamanho
    return pagina, (pagina[-1]["id"] if pagina and tem_mais else None)


def ingerir_com_cursor(buscar, tamanho: int) -> list:
    ids, cursor = [], None
    while True:
        pagina, proximo = buscar(cursor, tamanho)
        ids += [x["id"] for x in pagina]
        if proximo is None:
            return ids
        if cursor is not None and proximo <= cursor:
            raise ValueError("cursor não avançou")
        cursor = proximo
```
O teste do offset reproduz o bug "silencioso" que a teoria descreve: um único pedido novo durante a
ingestão empurra tudo uma posição, e o registro 40 é lido **duas vezes**. Com uma **exclusão** no
lugar da inserção, o efeito é o inverso: tudo sobe uma posição e um registro é **pulado**. Em
ingestões longas, isso vira duplicidade e perda de dados — e só aparece na reconciliação.

O cursor depende de uma chave **estável e ordenável** (id crescente, ou `updated_at` + id para
desempatar). É por isso que APIs sérias (Stripe, GitHub) paginam por cursor, e é o mesmo princípio
da **ingestão incremental com watermark** do M08: "me dê tudo depois do último que eu vi".
:::

---
**Revisado em:** 2026-09-30
