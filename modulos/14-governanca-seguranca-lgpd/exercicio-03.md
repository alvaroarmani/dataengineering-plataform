# Exercício 03 — Mascarar email (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`mascarar_email`** — Mantenha só a 1ª letra da parte local, troque o resto por '***' e preserve o domínio. Ex.: 'ana@x.com' -> 'a***@x.com'.

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
separe no '@' (partition), pegue local[0] e recomponha com '***@' + domínio.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def mascarar_email(email):
    local, _, dominio = email.partition('@')
    return local[0] + '***@' + dominio
```
:::

---
**Revisado em:** 2026-08-29
