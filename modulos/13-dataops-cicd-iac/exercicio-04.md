# Exercício 04 — Slim CI: o que o dbt precisa rebuildar

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Rodar o projeto dbt inteiro a cada PR fica caro e lento quando ele passa de algumas centenas de
modelos. O **slim CI** (teoria 02, "CI/CD para dados") roda só o que mudou **e tudo que depende
disso** — no dbt, `dbt build --select state:modified+`.

Você vai implementar essa seleção a partir da lista de arquivos alterados no PR, com as regras
que evitam falsos negativos: uma macro alterada pode afetar qualquer modelo, então por segurança
tudo roda; mudança só em documentação não roda nada.

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), implemente `selecao_slim_ci(arquivos_mudados, dag)`.

```bash
cd modulos/13-dataops-cicd-iac/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — primeiro os curingas
Antes de tudo, se algum caminho começa com `macros/` ou é `dbt_project.yml`, devolva `sorted(dag)`.
:::
:::{dropdown} Dica 2 — do caminho ao modelo
`a.rsplit("/", 1)[-1][:-4]` pega o nome do arquivo sem `.sql`. Só conte arquivos em `models/` que terminam em `.sql`.
:::
:::{dropdown} Dica 3 — descendentes
Uma busca (pilha) a partir dos mudados, seguindo `dag[modelo]`, com um `set` de visitados para não repetir quem é alcançado por dois caminhos.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def selecao_slim_ci(arquivos_mudados: list, dag: dict) -> list:
    if any(a.startswith("macros/") or a == "dbt_project.yml" for a in arquivos_mudados):
        return sorted(dag)
    mudados = set()
    for a in arquivos_mudados:
        if a.startswith("models/") and a.endswith(".sql"):
            nome = a.rsplit("/", 1)[-1][:-4]
            if nome not in dag:
                raise ValueError(f"modelo desconhecido: {nome}")
            mudados.add(nome)
    selecao, pilha = set(mudados), list(mudados)
    while pilha:
        for filho in dag[pilha.pop()]:
            if filho not in selecao:
                selecao.add(filho)
                pilha.append(filho)
    return sorted(selecao)
```
Mudar `stg_pedidos` seleciona 4 dos 8 modelos: os outros 4 não podem ter sido afetados. Em projetos
grandes, isso reduz o CI de horas para minutos — e de muito dinheiro para pouco (M21).

As regras conservadoras são o que tornam o slim CI **seguro**: uma macro pode ser usada por qualquer
modelo, e o `dbt_project.yml` pode mudar configurações globais; na dúvida, roda tudo. Já o `schema.yml`
de documentação é tratado como sem efeito — no dbt real, ele também guarda **testes**, e o
`state:modified` os detecta; aqui simplificamos.
:::

---
**Revisado em:** 2026-09-30
