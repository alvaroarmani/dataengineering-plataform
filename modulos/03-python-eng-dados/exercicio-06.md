# Exercício 06 — Validação de registro (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Testar dados é metade do trabalho. Aqui você escreve uma **checagem de qualidade** — o tipo
de função que vira um teste de dados no pipeline (prévia do M12).

## Tarefa

Implemente, em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), a função
`validar_registro(reg)` que recebe um dicionário e retorna uma **lista de mensagens de erro**
(vazia se o registro for válido), **na ordem das regras abaixo**:

1. Falta a chave `"id"` → `"id ausente"`.
2. Falta a chave `"valor"` → `"valor ausente"`.
3. Existe `"valor"`, mas é **negativo** → `"valor negativo"`.
4. Existe `"estado"` e **não** está em `{"SP", "RJ", "MG"}` → `"estado inválido"`.

```bash
cd modulos/03-python-eng-dados/exercicio-06
pytest -q
```

Exemplos:
```python
validar_registro({"id": 1, "valor": 10, "estado": "SP"})   # -> []
validar_registro({"valor": -5, "estado": "XX"})
# -> ["id ausente", "valor negativo", "estado inválido"]
```

## Dicas progressivas
:::{dropdown} Dica 1 — acumule erros
Comece com `erros = []` e vá dando `erros.append(...)` conforme as regras falham, na ordem dada.
:::
:::{dropdown} Dica 2 — presença vs. valor
Use `"id" not in reg` para presença. Para o valor negativo, cheque **só se** `"valor"` existe.
:::
:::{dropdown} Dica 3 — estado
Cheque o estado **só se** a chave existir: `if "estado" in reg and reg["estado"] not in {...}`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
ESTADOS_OK = {"SP", "RJ", "MG"}

def validar_registro(reg):
    erros = []
    if "id" not in reg:
        erros.append("id ausente")
    if "valor" not in reg:
        erros.append("valor ausente")
    elif reg["valor"] < 0:            # só checa negativo se existe
        erros.append("valor negativo")
    if "estado" in reg and reg["estado"] not in ESTADOS_OK:
        erros.append("estado inválido")
    return erros
```
A ordem dos `if` reflete a ordem das regras (por isso a saída é previsível). O `elif` evita
checar "negativo" quando o valor nem existe. Esse tipo de função é a semente de um **teste de
qualidade de dados** — dado que não passa na validação vai para a quarentena.
:::

---
**Revisado em:** 2026-08-22
