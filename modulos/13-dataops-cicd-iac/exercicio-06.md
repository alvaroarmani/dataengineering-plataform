# Exercício 06 — Resumo do plano e detecção de drift

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Duas rotinas de quem opera infraestrutura como código (teoria 03). A primeira é ler o **resumo** do
plano: `Plan: 2 to add, 1 to change, 1 to destroy.` — onde uma substituição conta como **uma
criação e uma destruição**. A segunda é detectar **drift**: alguém mudou um recurso "na mão" pelo
console, e agora o mundo real não bate com o *state* do Terraform. Drift não detectado é o que faz
o próximo `apply` desfazer, sem aviso, a correção que alguém fez às pressas.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `resumo_plano(plano)` e `detectar_drift(estado, real)`.

```bash
cd modulos/13-dataops-cicd-iac/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — contas do resumo
Adições = criar + substituir; destruições = destruir + substituir; mudanças = quantidade de chaves em `atualizar`.
:::
:::{dropdown} Dica 2 — drift por recurso
Para os nomes nos dois lados, compare atributo a atributo na união das chaves — um atributo que só existe na nuvem também é drift.
:::
:::{dropdown} Dica 3 — os de fora
Não gerenciados = `set(real) - set(estado)`; sumidos = o contrário. Devolva tudo ordenado.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def resumo_plano(plano: dict) -> str:
    add = len(plano["criar"]) + len(plano["substituir"])
    change = len(plano["atualizar"])
    destroy = len(plano["destruir"]) + len(plano["substituir"])
    if add == change == destroy == 0:
        return "No changes."
    return f"Plan: {add} to add, {change} to change, {destroy} to destroy."


def detectar_drift(estado: dict, real: dict) -> dict:
    alterados = {}
    for nome in sorted(set(estado) & set(real)):
        e, r = estado[nome], real[nome]
        dif = sorted(k for k in set(e) | set(r) if e.get(k) != r.get(k))
        if dif:
            alterados[nome] = dif
    return {"alterados": alterados,
            "nao_gerenciados": sorted(set(real) - set(estado)),
            "sumidos": sorted(set(estado) - set(real))}
```
O `bucket_teste_do_joao` é o drift mais comum na vida real: um recurso criado pelo console que
ninguém importou para o Terraform — continua gerando custo (M21) e fica fora de qualquer revisão.
O `versionamento` desligado é o mais perigoso: o próximo `apply` vai religá-lo (bom), mas se a
mudança manual tivesse sido uma correção necessária, ela seria desfeita sem ninguém perceber.

Em pipelines maduros, um job agendado roda `terraform plan -detailed-exitcode` todo dia: código de
saída 2 significa "há diferença" e dispara um alerta de drift.
:::

---
**Revisado em:** 2026-09-30
