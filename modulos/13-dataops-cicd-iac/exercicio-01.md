# Exercício 01 — Proteção de branch: o PR pode entrar?

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"CI verde" é só uma das regras que protegem a `main` (teoria 01). Num repositório de dados sério,
o botão de merge só libera quando **todas** as regras de proteção passam: checks obrigatórios
verdes, número mínimo de aprovações (o autor não aprova o próprio PR), aprovação do **dono do
código** para arquivos sensíveis (o `CODEOWNERS` do GitHub) e branch atualizado com a `main`.

O que torna o exercício realista: o merge bloqueado precisa dizer **por quê**, com todos os
motivos de uma vez — ninguém quer descobrir um bloqueio por vez.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente `avaliar_pr(pr, regras)`.

```bash
cd modulos/13-dataops-cicd-iac/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — último status por check
Percorra os checks guardando `ultimo[nome] = status`; um obrigatório bloqueia se `ultimo.get(nome) != "pass"` (ausente dá `None`).
:::
:::{dropdown} Dica 2 — aprovações válidas
`set(aprovacoes) - {autor}` elimina a autoaprovação e as repetidas de uma vez.
:::
:::{dropdown} Dica 3 — CODEOWNERS
Para cada `prefixo, dono`: se algum arquivo começa com o prefixo e o dono não está nas aprovações válidas (e não é o próprio autor), bloqueie. Junte tudo num `set` e devolva ordenado.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def avaliar_pr(pr: dict, regras: dict) -> dict:
    bloqueios = set()
    ultimo = {}
    for nome, status in pr["checks"]:
        ultimo[nome] = status
    for nome in regras["checks_obrigatorios"]:
        if ultimo.get(nome) != "pass":
            bloqueios.add(f"check:{nome}")
    validas = set(pr["aprovacoes"]) - {pr["autor"]}
    if len(validas) < regras["aprovacoes_min"]:
        bloqueios.add(f"aprovacoes:{len(validas)}/{regras['aprovacoes_min']}")
    for prefixo, dono in regras["codeowners"].items():
        if any(a.startswith(prefixo) for a in pr["arquivos"]) and dono not in validas and dono != pr["autor"]:
            bloqueios.add(f"codeowner:{dono}")
    if not pr["atualizado"]:
        bloqueios.add("desatualizado")
    return {"pode": not bloqueios, "bloqueios": sorted(bloqueios)}
```
Dois detalhes vêm do comportamento real do GitHub. **Re-execução**: um job que falhou e passou no
retry libera o merge — o que vale é o último resultado. **Autor dono do código**: o CODEOWNERS não
exige que a Carla aprove o próprio PR, mas o mínimo de aprovações continua exigindo outra pessoa —
revisão é sempre de um segundo par de olhos.

Devolver **todos** os bloqueios de uma vez é o que faz a ferramenta ajudar em vez de irritar; é o
mesmo princípio do validador de contrato do M12.
:::

---
**Revisado em:** 2026-09-30
