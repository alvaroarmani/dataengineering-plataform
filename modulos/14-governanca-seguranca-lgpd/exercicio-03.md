# Exercício 03 — Mascaramento por tipo de dado

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Mascaramento (teoria 02) deixa o dado **útil** sem expô-lo: o atendente confirma "o e-mail
terminado em @gmail.com?" sem ver o endereço inteiro; o analista vê o formato do CPF sem o número.
Cada tipo tem sua regra, e o formato precisa sobreviver — um CPF mascarado continua com cara de
CPF, para não quebrar telas e validações a jusante.

A parte difícil é a entrada real: CPF com e sem pontuação, telefone com parênteses e espaços, e-mail
malformado. A regra de ouro: **na dúvida, mascare tudo** — nunca devolva o valor original por
não ter conseguido interpretá-lo.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `mascarar(valor, tipo)`.

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — valide o tipo primeiro
Tipo desconhecido é erro de programação (levante), valor ruim é dado sujo (mascare tudo com `"***"`).
:::
:::{dropdown} Dica 2 — só os dígitos
`re.sub(r"\D", "", s)` remove tudo que não é dígito — serve para validar CPF e telefone independentemente da pontuação.
:::
:::{dropdown} Dica 3 — telefone preservando o formato
Percorra a string original; conte os dígitos vistos e troque por `*` enquanto `vistos < total - 4`. Os outros caracteres passam direto.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import re


def mascarar(valor, tipo: str):
    if tipo not in ("email", "cpf", "telefone"):
        raise ValueError(f"tipo desconhecido: {tipo}")
    if valor is None:
        return None
    s = str(valor).strip()
    if tipo == "email":
        partes = s.split("@")
        if len(partes) != 2 or not partes[0] or not partes[1]:
            return "***"
        return f"{partes[0][0]}***@{partes[1]}"
    digitos = re.sub(r"\D", "", s)
    if tipo == "cpf":
        if len(digitos) != 11:
            return "***"
        return f"***.{digitos[3:6]}.{digitos[6:9]}-**"
    if len(digitos) < 4:
        return "***"
    manter = len(digitos) - 4
    out, vistos = [], 0
    for ch in s:
        if ch.isdigit():
            out.append("*" if vistos < manter else ch)
            vistos += 1
        else:
            out.append(ch)
    return "".join(out)
```
Todo caso "estranho" dos testes devolve `***` em vez do valor original: um e-mail com dois `@`, um
CPF com 9 dígitos. É a regra *fail closed* — um mascarador que devolve a entrada quando não
entende o formato é exatamente o que vaza dados em produção.

Lembre da distinção da teoria 03: mascaramento **não** é anonimização. `a***@x.com` ainda pode ser
reidentificado cruzando com outras bases; o dado mascarado continua sendo dado pessoal para a LGPD.
Serve para reduzir exposição (telas, logs, ambientes de teste), não para tirar o dado do escopo da lei.
:::

---
**Revisado em:** 2026-09-30
