# Exercício 06 — Direito ao esquecimento em várias tabelas

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Quando um titular pede a exclusão dos dados (teoria 03, direitos do titular), o pipeline precisa
agir em **todas** as tabelas onde ele aparece — e não da mesma forma em todas. O cadastro de
marketing é **apagado**; os pedidos são **anonimizados** (o faturamento histórico precisa continuar
batendo); e as notas fiscais são **mantidas**, porque há obrigação legal de guarda (a própria LGPD
prevê bases legais que se sobrepõem ao pedido).

O resultado precisa de um **relatório** do que foi feito em cada tabela — é a evidência de
atendimento do pedido.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `esquecer_titular(tabelas, titular_id, politica)`.

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — valide a cobertura
Antes de alterar qualquer coisa, confira que **toda** tabela tem política (`set(tabelas) - set(politica)`). Esquecimento pela metade é pior do que nenhum — dá a falsa impressão de atendido.
:::
:::{dropdown} Dica 2 — cópias
Use `copy.deepcopy` em cada registro que for para a saída; assim nenhuma alteração vaza para a entrada (nem a do teste que edita o resultado).
:::
:::{dropdown} Dica 3 — anonimizar
Nos registros do titular: troque os campos listados que existirem por `"***"` e zere o `cliente_id` — manter o id permitiria religar tudo à pessoa.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import copy


def esquecer_titular(tabelas: dict, titular_id, politica: dict) -> tuple:
    faltando = sorted(set(tabelas) - set(politica))
    if faltando:
        raise ValueError(f"tabelas sem política de esquecimento: {faltando}")
    novas, relatorio = {}, {}
    for nome, registros in tabelas.items():
        regra = politica[nome]
        do_titular = [r for r in registros if r.get("cliente_id") == titular_id]
        relatorio[nome] = {"acao": regra["acao"], "registros": len(do_titular)}
        if regra["acao"] == "apagar":
            novas[nome] = [copy.deepcopy(r) for r in registros if r.get("cliente_id") != titular_id]
        elif regra["acao"] == "anonimizar":
            linhas = []
            for r in registros:
                r = copy.deepcopy(r)
                if r.get("cliente_id") == titular_id:
                    for c in regra.get("campos", []):
                        if c in r:
                            r[c] = "***"
                    r["cliente_id"] = None
                linhas.append(r)
            novas[nome] = linhas
        elif regra["acao"] == "manter":
            novas[nome] = copy.deepcopy(registros)
        else:
            raise ValueError(f"ação desconhecida: {regra['acao']}")
    return novas, relatorio
```
O teste do faturamento mostra por que **anonimizar** e não apagar os pedidos: a receita de R$ 180
continua batendo com a contabilidade, mas não há mais como saber que 130 deles foram da Ana. Já a
nota fiscal é mantida intacta — há obrigação legal de guarda —, e o relatório registra isso como
decisão consciente, não como esquecimento.

Zerar o `cliente_id` é o detalhe que separa anonimização de fachada da real: com o id preservado,
bastaria um join com qualquer outra tabela para reidentificar. Em lakes com arquivos imutáveis
(Parquet), esse tipo de exclusão é caro; é um dos motivos para formatos com `DELETE`/`MERGE`
transacional, como o Delta Lake (M11).
:::

---
**Revisado em:** 2026-09-30
