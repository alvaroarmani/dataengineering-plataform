# Exercício 04 — Controle de acesso (RBAC) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`pode_acessar`** — politicas = {papel: [recursos permitidos]}. Retorne True se `recurso` está na lista do `papel` (menor privilégio: nega por padrão).

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
use politicas.get(papel, []) para negar por padrão quando o papel não existe.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def pode_acessar(papel, recurso, politicas):
    return recurso in politicas.get(papel, [])
```
:::

---
**Revisado em:** 2026-08-29
