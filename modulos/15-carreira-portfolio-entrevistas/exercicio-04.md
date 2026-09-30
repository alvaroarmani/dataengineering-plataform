# Exercício 04 — Case de modelagem: da tabela achatada ao star schema

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
No case de modelagem da entrevista (teoria 02), é comum receber uma planilha **achatada** — uma linha
por item vendido, com nome do cliente, cidade, nome do produto, categoria, quantidade e valor, tudo
repetido. O primeiro passo é descobrir as **dependências funcionais**: quais colunas são determinadas
por uma chave (a cidade depende do cliente; a categoria depende do produto). Essas vão para as
**dimensões**; o que varia linha a linha (quantidade, valor, desconto) fica no **fato**.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `depende_de(linhas, chave)` e `propor_star(linhas, chaves)`.

```bash
cd modulos/15-carreira-portfolio-entrevistas/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — dependência funcional
Para cada `(valor_da_chave, coluna)`, guarde o primeiro valor visto. Se aparecer um valor diferente para o mesmo par, a coluna **não** depende da chave.
:::
:::{dropdown} Dica 2 — dimensões
Para cada chave, as colunas que dependem dela (e ainda não foram usadas) vão para `dim_<nome>`, junto com a chave.
:::
:::{dropdown} Dica 3 — fato
As chaves mais tudo que não foi para nenhuma dimensão — medidas e atributos do próprio evento (como o número do pedido).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def depende_de(linhas: list, chave: str) -> list:
    colunas = [c for c in linhas[0] if c != chave] if linhas else []
    visto = {}
    dependentes = set(colunas)
    for l in linhas:
        k = l[chave]
        for c in colunas:
            if (k, c) in visto and visto[(k, c)] != l[c]:
                dependentes.discard(c)
            visto.setdefault((k, c), l[c])
    return sorted(dependentes)


def propor_star(linhas: list, chaves: list) -> dict:
    usadas = set(chaves)
    star = {}
    for ch in chaves:
        cols = [c for c in depende_de(linhas, ch) if c not in usadas]
        usadas |= set(cols)
        star[f"dim_{ch.removesuffix('_id')}"] = [ch] + cols
    resto = sorted(c for c in (linhas[0] if linhas else {}) if c not in usadas)
    return {"fato": list(chaves) + resto, **star}
```
O `pedido` fica no fato: ele não depende de nenhuma das chaves candidatas (é uma **dimensão degenerada**,
teoria 05 do M05). E o `valor` também: o mesmo produto foi vendido por preços diferentes — preço **da
venda** é medida do fato, não atributo do produto.

O último teste é a conversa que diferencia candidatos na entrevista: quando a Ana muda de cidade, a
cidade deixa de ser função só do `cliente_id` — ela depende também do **tempo**. Isso não significa que
a cidade vai para o fato: significa que a `dim_cliente` precisa de histórico, com uma **SCD tipo 2**
(M05). Dizer isso em voz alta mostra que você entende a modelagem além do diagrama.
:::

---
**Revisado em:** 2026-09-30
