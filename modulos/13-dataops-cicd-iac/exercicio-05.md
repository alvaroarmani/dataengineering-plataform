# Exercício 05 — Plano do Terraform: atualizar, substituir e proteger

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O `terraform plan` (teoria 03) compara o estado desejado com o atual e diz o que vai acontecer.
A diferença que mais importa numa plataforma de dados não é entre criar e destruir — é entre
**atualizar no lugar** e **substituir** (destruir e recriar). Mudar a descrição de um bucket é
inofensivo; mudar a **região** dele força a recriação, e recriar um bucket ou um banco significa
**perder os dados**.

Por isso recursos críticos levam `prevent_destroy`: o plano que tentaria destruí-los (ou
substituí-los) é recusado antes de qualquer estrago.

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py), implemente `plano(atual, desejado, imutaveis)`.

```bash
cd modulos/13-dataops-cicd-iac/exercicio-05
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — conjuntos de nomes
Criar = `set(desejado) - set(atual)`; destruir = o contrário; os comuns são candidatos a atualizar ou substituir.
:::
:::{dropdown} Dica 2 — o que mudou
Compare na **união** das chaves dos dois lados (`a.get(k) != d.get(k)`): um atributo novo ou removido também é mudança. Ignore `prevent_destroy` na comparação.
:::
:::{dropdown} Dica 3 — substituir e proteger
Se a interseção entre os alterados e os imutáveis do tipo (mais o próprio `"tipo"`) não for vazia, é substituição. No fim, verifique `prevent_destroy` em tudo que seria destruído ou substituído.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def plano(atual: dict, desejado: dict, imutaveis: dict) -> dict:
    def _attrs(cfg):
        return {k: v for k, v in cfg.items() if k != "prevent_destroy"}

    criar = sorted(set(desejado) - set(atual))
    destruir = sorted(set(atual) - set(desejado))
    atualizar, substituir = {}, []
    for nome in sorted(set(atual) & set(desejado)):
        a, d = _attrs(atual[nome]), _attrs(desejado[nome])
        mudou = sorted(k for k in set(a) | set(d) if a.get(k) != d.get(k))
        if not mudou:
            continue
        fixos = set(imutaveis.get(a.get("tipo"), [])) | {"tipo"}
        if fixos & set(mudou):
            substituir.append(nome)
        else:
            atualizar[nome] = mudou
    for nome in destruir + substituir:
        if atual[nome].get("prevent_destroy"):
            raise ValueError(f"plano recusado: {nome} tem prevent_destroy")
    return {"criar": criar, "atualizar": atualizar, "substituir": substituir, "destruir": destruir}
```
O teste do `dw` mostra o `prevent_destroy` funcionando como deve: ele **permite** mudanças no lugar
(expiração das tabelas) e **recusa** qualquer plano que apagaria o dataset — inclusive a
substituição disfarçada por uma mudança de localização. Em produção, é essa linha no Terraform que
separa um PR mal revisado de uma perda de dados.

No plano real do Terraform, a substituição aparece como `-/+` com a anotação *forces replacement*
no atributo culpado — é a primeira coisa a procurar ao revisar um plano de infraestrutura de dados.
:::

---
**Revisado em:** 2026-09-30
