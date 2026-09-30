# Exercício 06 — Evolução de contrato: o que quebra os consumidores

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O contrato de uma API (teoria 01) muda com o tempo, e a pergunta de todo PR que mexe nele é: **isso
quebra quem consome?** A regra é assimétrica. Na **resposta**, adicionar um campo é seguro
(consumidores ignoram o que não conhecem), mas remover ou mudar o tipo quebra. Na **requisição**, é o
contrário: passar a **exigir** um campo quebra os clientes antigos, que não o enviam; aceitar um
campo novo opcional é seguro.

Essa classificação decide a versão pelo **versionamento semântico**: mudança incompatível → versão
*major*; só adições compatíveis → *minor*; nada visível → *patch*.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `mudancas(antigo, novo)` e `proxima_versao(versao, mudancas)`.

```bash
cd modulos/23-apis-microservicos/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — dois lados, duas regras
Trate resposta e requisição em blocos separados. Na resposta, o que some ou muda de tipo quebra; o que aparece não.
:::
:::{dropdown} Dica 2 — requisição
Percorra os campos **novos**: ausente no antigo → depende de ser obrigatório; existente → compare tipo e a mudança de obrigatoriedade. Depois, os que sumiram do novo (compatível).
:::
:::{dropdown} Dica 3 — semver
`versao.split(".")` com 3 partes numéricas; incompatível zera minor e patch, compatível zera patch.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def mudancas(antigo: dict, novo: dict) -> dict:
    inc, comp = [], []
    ra, rn = antigo["resposta"], novo["resposta"]
    for c in ra:
        if c not in rn:
            inc.append(f"resposta.{c}:removido")
        elif ra[c]["tipo"] != rn[c]["tipo"]:
            inc.append(f"resposta.{c}:tipo")
    comp += [f"resposta.{c}:adicionado" for c in rn if c not in ra]
    qa, qn = antigo["requisicao"], novo["requisicao"]
    for c, spec in qn.items():
        if c not in qa:
            (inc if spec["obrigatorio"] else comp).append(
                f"requisicao.{c}:" + ("novo_obrigatorio" if spec["obrigatorio"] else "adicionado"))
            continue
        if qa[c]["tipo"] != spec["tipo"]:
            inc.append(f"requisicao.{c}:tipo")
        if spec["obrigatorio"] and not qa[c]["obrigatorio"]:
            inc.append(f"requisicao.{c}:virou_obrigatorio")
        elif qa[c]["obrigatorio"] and not spec["obrigatorio"]:
            comp.append(f"requisicao.{c}:virou_opcional")
    comp += [f"requisicao.{c}:removido" for c in qa if c not in qn]
    return {"incompativeis": sorted(inc), "compativeis": sorted(comp)}


def proxima_versao(versao: str, m: dict) -> str:
    partes = versao.split(".")
    if len(partes) != 3 or not all(p.isdigit() for p in partes):
        raise ValueError(f"versão inválida: {versao}")
    ma, mi, pa = map(int, partes)
    if m["incompativeis"]:
        return f"{ma + 1}.0.0"
    if m["compativeis"]:
        return f"{ma}.{mi + 1}.0"
    return f"{ma}.{mi}.{pa + 1}"
```
O teste da assimetria resume a regra que pega times desprevenidos: tornar o `cupom` **obrigatório**
parece uma melhoria de qualidade, mas todo cliente que ainda não envia cupom passa a receber erro — é
uma quebra de contrato. Já afrouxar o `canal` para opcional é seguro.

Em dados, a mesma lógica vale para schemas de eventos no Kafka (M17) e para contratos de dados (M12):
registros de schema como o do Confluent verificam exatamente essas regras de compatibilidade
(*backward*, *forward*) antes de aceitar uma versão nova — e o M08 (schema evolution) é o lado
consumidor desse mesmo problema.
:::

---
**Revisado em:** 2026-09-30
