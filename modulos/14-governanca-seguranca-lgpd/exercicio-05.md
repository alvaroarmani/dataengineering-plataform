# Exercício 05 — Classificar dado (LGPD) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`classifica`** — Retorne 'sensivel' se o campo for categoria especial (raca, saude, religiao, orientacao_sexual, biometria); 'pessoal' se identificar a pessoa (cpf, email, nome, telefone, endereco); senão 'comum'.

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
dois conjuntos (sensiveis, pessoais); verifique sensível primeiro, depois pessoal, senão comum.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def classifica(campo):
    sensiveis = {'raca', 'saude', 'religiao', 'orientacao_sexual', 'biometria'}
    pessoais = {'cpf', 'email', 'nome', 'telefone', 'endereco'}
    if campo in sensiveis:
        return 'sensivel'
    if campo in pessoais:
        return 'pessoal'
    return 'comum'
```
:::

---
**Revisado em:** 2026-08-29
