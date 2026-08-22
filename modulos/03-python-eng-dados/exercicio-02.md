# Exercício 02 — Um Pipeline de transformações (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Você vai construir uma pequena classe `Pipeline` que **encadeia funções de transformação** —
o coração conceitual de qualquer ETL. Exercita **classe + funções como valores**.

## Tarefa

Implemente, em [`exercicio-02/solucao.py`](exercicio-02/solucao.py), a classe `Pipeline`:

- `Pipeline(passos=None)` — guarda uma lista de funções (vazia se `None`).
- `adicionar(self, f)` — anexa a função `f` e **retorna `self`** (permite encadear: `p.adicionar(a).adicionar(b)`).
- `rodar(self, dados)` — aplica os passos **na ordem**, passando o resultado de um para o próximo, e retorna o final. Sem passos, retorna `dados` inalterado.

```bash
cd modulos/03-python-eng-dados/exercicio-02
pytest -q
```

Exemplo:
```python
p = Pipeline().adicionar(lambda xs: [x for x in xs if x > 0]).adicionar(lambda xs: [x*10 for x in xs])
p.rodar([-1, 2, 3])   # -> [20, 30]
```

## Dicas progressivas
:::{dropdown} Dica 1 — guardar os passos
No `__init__`, use `self.passos = list(passos) if passos else []` (cuidado com default mutável!).
:::
:::{dropdown} Dica 2 — encadear
`adicionar` deve fazer `self.passos.append(f)` e terminar com `return self`.
:::
:::{dropdown} Dica 3 — rodar
Percorra `self.passos` reatribuindo `dados = passo(dados)`; retorne `dados`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
class Pipeline:
    def __init__(self, passos=None):
        self.passos = list(passos) if passos else []

    def adicionar(self, f):
        self.passos.append(f)
        return self          # permite encadear chamadas

    def rodar(self, dados):
        for passo in self.passos:
            dados = passo(dados)
        return dados
```
`list(passos) if passos else []` evita a armadilha do default mutável e copia a lista
recebida. `return self` em `adicionar` habilita a API fluente. `rodar` é a mesma composição
que você viu no lab, agora encapsulada num objeto com estado (os passos).
:::

---
**Revisado em:** 2026-08-21
