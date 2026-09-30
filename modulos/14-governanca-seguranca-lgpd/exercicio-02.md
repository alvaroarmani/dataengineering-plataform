# Exercício 02 — Auditoria do catálogo de dados

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Um catálogo (teoria 01) só ajuda se estiver **mantido**. A auditoria periódica procura quatro
problemas: ativo sem dono, sem descrição, **abandonado** (ninguém consulta há meses) e — o
crítico — ativo com dado pessoal **sem dono**: ninguém responde por ele se o titular pedir
exclusão (LGPD) ou se houver vazamento.

A saída da auditoria vira uma fila de trabalho: os críticos primeiro.

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `auditar_catalogo(catalogo, hoje, dias_abandono)`.

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — texto vazio
`(valor or "").strip()` trata `None`, `""` e `"  "` do mesmo jeito.
:::
:::{dropdown} Dica 2 — datas
`date.fromisoformat` e a subtração dá um `timedelta` com `.days`. Nunca acessado (`None`) já é abandono.
:::
:::{dropdown} Dica 3 — críticos
Depois de montar os problemas do ativo, marque como crítico se `pii` for verdadeiro **e** `"sem_dono"` estiver na lista.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from datetime import date


def auditar_catalogo(catalogo: dict, hoje: str, dias_abandono: int = 90) -> dict:
    ref = date.fromisoformat(hoje)
    problemas, criticos = {}, []
    for ativo in sorted(catalogo):
        info = catalogo[ativo]
        p = []
        if not (info.get("dono") or "").strip():
            p.append("sem_dono")
        if not (info.get("descricao") or "").strip():
            p.append("sem_descricao")
        acesso = info.get("ultimo_acesso")
        if acesso is None or (ref - date.fromisoformat(acesso)).days > dias_abandono:
            p.append("abandonado")
        if p:
            problemas[ativo] = sorted(p)
        if info.get("pii") and "sem_dono" in p:
            criticos.append(ativo)
    return {"problemas": problemas, "criticos": criticos}
```
A `dim_cliente` é o caso que justifica a auditoria: tem descrição, é usada todo dia, parece
saudável — mas o dono é um campo com espaços. Ela guarda CPF e e-mail; se um titular pedir a
exclusão dos dados, não há ninguém responsável por executá-la. Por isso é crítica, à frente da
`tmp_export_2025`, que tem mais problemas mas nenhum dado pessoal.

Os abandonados (`tmp_export_2025`, `stg_leads`) são candidatos a arquivamento ou exclusão —
**minimização** e **retenção** da LGPD (teoria 03) e economia de armazenamento (M21) ao mesmo tempo.
:::

---
**Revisado em:** 2026-09-30
