# Exercício 03 — Validar a ordem das etapas de um pipeline

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O ciclo de vida da engenharia de dados (teoria 01) — **geração → ingestão → armazenamento →
transformação → disponibilização** — é uma ferramenta de diagnóstico: ao desenhar um pipeline, cada
etapa deve pertencer a uma fase, e as fases precisam aparecer **em ordem**. Uma transformação
antes da ingestão, ou um dashboard lendo direto da fonte, são sinais de um desenho confuso. E as
"correntes de fundo" (segurança, qualidade, orquestração…) **não** são fases: atravessam todas.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `validar_pipeline(etapas)`.

```bash
cd modulos/01-fundamentos-eng-dados/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — a posição da fase
`FASES.index(fase)` transforma a fase num número. Uma etapa está fora de ordem se o número dela é **menor** que o maior visto até ali.
:::
:::{dropdown} Dica 2 — ausentes
Compare `FASES[1:]` (de ingestão em diante) com o conjunto de fases presentes.
:::
:::{dropdown} Dica 3 — reordenar
`sorted(etapas, key=lambda e: FASES.index(e[1]))` — o `sorted` do Python é **estável**, então etapas da mesma fase mantêm a ordem original.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
FASES = ["geracao", "ingestao", "armazenamento", "transformacao", "disponibilizacao"]
CORRENTES = {"seguranca", "gestao_de_dados", "dataops", "arquitetura", "orquestracao", "engenharia_de_software"}


def validar_pipeline(etapas: list) -> dict:
    for nome, fase in etapas:
        if fase in CORRENTES:
            raise ValueError(f"{fase} é corrente de fundo, não fase do ciclo ({nome})")
        if fase not in FASES:
            raise ValueError(f"fase desconhecida: {fase}")
    fora, maior = [], -1
    for nome, fase in etapas:
        i = FASES.index(fase)
        if i < maior:
            fora.append(nome)
        maior = max(maior, i)
    presentes = {f for _, f in etapas}
    ausentes = [f for f in FASES[1:] if f not in presentes]
    ordem = [n for n, _ in sorted(etapas, key=lambda e: FASES.index(e[1]))]
    return {"ok": not fora and not ausentes, "fora_de_ordem": fora,
            "fases_ausentes": ausentes, "ordem_correta": ordem}
```
O segundo teste mostra um anti-padrão comum: "limpar no script de extração" antes de gravar o dado
bruto. Parece economizar um passo, mas você perde o dado original — se a regra de limpeza estiver
errada, não há como reprocessar. A ordem ingestão → armazenamento → transformação é o que permite o
ELT (teoria 03): guarde o bruto, transforme depois, repita quando precisar.

E o `ValueError` para `orquestracao` reforça a distinção do Reis & Housley: o Airflow não é uma
etapa entre a ingestão e a transformação — ele coordena **todas** elas (M09).
:::

---
**Revisado em:** 2026-09-30
