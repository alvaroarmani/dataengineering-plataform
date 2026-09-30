# Exercício 02 — Branch → ambiente e schema de deploy

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Ambientes **dev → staging → prod** (teoria 01) só funcionam se cada execução escreve no lugar
certo. No dbt, isso se resolve com o **schema de destino**: produção escreve em `analytics`,
staging em `analytics_staging` e cada desenvolvedor num schema próprio — `dev_ana_nova_metrica` —
para que dois PRs em paralelo não sobrescrevam as tabelas um do outro.

O nome do schema sai do nome do branch, que chega sujo: maiúsculas, acentos, espaços, barras. Um
schema inválido quebra o deploy; dois branches que viram o mesmo schema causam o pior tipo de bug
(um sobrescreve o outro em silêncio).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), implemente `alvo_de_deploy(branch, usuario)`.

```bash
cd modulos/13-dataops-cicd-iac/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — tirar acentos
`unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()` transforma `Métrica` em `Metrica`.
:::
:::{dropdown} Dica 2 — normalizar com regex
Depois de `.lower()`, `re.sub(r"[^a-z0-9]+", "_", s)` troca qualquer sequência inválida por um único `_`; finalize com `.strip("_")`.
:::
:::{dropdown} Dica 3 — corte e validação
Corte em 30 caracteres e remova um `_` que tenha ficado no fim (`rstrip`). Use `re.fullmatch(r"(feature|fix)/(.+)", branch)` para reconhecer o padrão.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import re
import unicodedata


def _slug(texto: str, limite: int) -> str:
    ascii_ = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "_", ascii_.lower()).strip("_")
    return s[:limite].rstrip("_")


def alvo_de_deploy(branch: str, usuario: str) -> dict:
    if branch == "main":
        return {"ambiente": "prod", "schema": "analytics"}
    if branch == "develop":
        return {"ambiente": "staging", "schema": "analytics_staging"}
    m = re.fullmatch(r"(feature|fix)/(.+)", branch)
    if not m:
        raise ValueError(f"branch fora do padrão: {branch}")
    nome, user = _slug(m.group(2), 30), _slug(usuario or "", 30)
    if not nome or not user:
        raise ValueError("nome de branch ou usuário vazio após normalização")
    return {"ambiente": "dev", "schema": f"dev_{user}_{nome}"}
```
O teste com o nome longo mostra por que o corte vem **depois** da normalização e por que se
remove o `_` final: `modelo_de_receita_recorrentes_` (30 caracteres) viraria um schema feio e
diferente do esperado. E o limite existe porque bancos limitam o tamanho de identificadores (63 no
Postgres) — o prefixo `dev_<usuario>_` também ocupa espaço.

No dbt, essa lógica mora na macro `generate_schema_name`, e o `usuario` costuma vir do
`target.user` do profile. Incluir o usuário garante que dois desenvolvedores no mesmo branch não se
atropelem.
:::

---
**Revisado em:** 2026-09-30
