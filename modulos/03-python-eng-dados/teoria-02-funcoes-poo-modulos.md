# Funções, classes e módulos: organizando código que cresce

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Um script de 20 linhas cabe na cabeça. Um pipeline real tem centenas — ingestão, limpeza,
validação, carga. Sem estrutura, isso vira um paredão impossível de testar ou reaproveitar.
**Funções, classes e módulos** são as três ferramentas para domar essa complexidade — e são
o que torna seu código *testável* (a base de como você corrige exercícios aqui) e
*reutilizável* entre pipelines.

## 💡 Conceito (o porquê)

### Funções bem-feitas
Uma boa função tem **uma responsabilidade** e um **contrato claro**:

```python
def limpar(registros: list[dict], *, remover_nulos: bool = True) -> list[dict]:
    ...
    return limpos
```

- **Argumentos com default** (`remover_nulos=True`) dão flexibilidade sem quebrar quem já chama.
- `*args` / `**kwargs` capturam argumentos extras posicionais/nomeados (útil em wrappers).
- **Funções puras** — sem efeito colateral, mesmo input → mesmo output — são fáceis de testar
  e casam com **idempotência** (M8/M9). Prefira-as; isole efeitos (I/O, escrita) nas bordas.

### Funções são valores (first-class)
Em Python, **funções são objetos**: você as guarda em variáveis, passa como argumento e
retorna de outras funções. Isso habilita um padrão central de ETL — **compor passos**:

```python
def rodar(dados, passos):
    for passo in passos:          # cada passo é uma função
        dados = passo(dados)
    return dados

rodar(brutos, [limpar, deduplicar, enriquecer])
```

### Classes: quando estado e comportamento andam juntos
Uma **classe** faz sentido quando você tem **estado** que evolui e **operações** sobre ele —
por exemplo, um agregador que acumula à medida que recebe dados:

```python
class Agregador:
    def __init__(self):
        self.total = 0.0
    def adicionar(self, valor):   # método: comportamento sobre o estado
        self.total += valor
```

Para **registros** (dados sem muito comportamento), use **`dataclasses`** — menos código:

```python
from dataclasses import dataclass

@dataclass
class Venda:
    estado: str
    valor: float
```

> Regra de bolso: se uma **função** resolve, não crie uma classe. Classe é para *estado + comportamento*.

### Módulos e pacotes: organização em arquivos
Cada arquivo `.py` é um **módulo**; uma pasta com `__init__.py` é um **pacote**. Você importa
o que precisa (`from ingestao import baixar`). O idioma `if __name__ == "__main__":` separa
"código que roda quando executo o arquivo" de "código importável".

## 🔎 Exemplo

```python
# transform.py  (um módulo)
def limpar(regs): ...
def deduplicar(regs): ...

# main.py
from transform import limpar, deduplicar
dados = deduplicar(limpar(brutos))
```

:::{admonition} 📖 Da literatura
:class: seealso
Ramalho destaca que, em Python, **funções são objetos de primeira classe** — podem ser
atribuídas, passadas e retornadas — o que sustenta padrões elegantes como *pipelines* de
transformação e decorators. — *Fluent Python*, cap. sobre funções.
:::

## ⚠️ Erros comuns
- Funções que fazem **coisas demais** (baixam, limpam e salvam) — difícil testar; separe.
- **Efeito colateral escondido** (a função altera a lista recebida) — surpreende quem chama.
- Criar **classe** onde uma função bastaria (over-engineering).
- Usar `*args`/`**kwargs` sem necessidade, escondendo o contrato da função.
- Um `default` **mutável** (`def f(x=[])`) — o mesmo objeto é reusado entre chamadas (armadilha clássica).

## 💼 O que o mercado espera
Código **modular e testável**: funções pequenas, classes quando fazem sentido, projeto
organizado em módulos. Saber compor passos (funções como valores) é sinal de maturidade.

:::{admonition} ✨ Em resumo
:class: resumo
- **Funções são valores** → compõem pipelines (cada passo é uma função).
- Use **classe** só quando há *estado + comportamento*; senão, função.
- **`dataclass`** para registros; cuidado com o **default mutável**.
- Organize o projeto em **módulos** por responsabilidade.
:::

## 🧠 Quiz de recall
1. O que significa "funções são objetos de primeira classe" em Python?
   :::{dropdown} Resposta
   Funções podem ser atribuídas a variáveis, passadas como argumento e retornadas de outras funções — como qualquer objeto. Isso habilita compor pipelines e usar decorators.
   :::
2. Quando usar uma classe em vez de funções soltas?
   :::{dropdown} Resposta
   Quando há **estado** que evolui junto com **comportamento** que opera sobre ele (ex.: um agregador que acumula). Se uma função resolve, não crie classe.
   :::
3. Por que preferir funções puras em pipelines?
   :::{dropdown} Resposta
   Mesmo input → mesmo output, sem efeitos colaterais: são fáceis de testar e casam com idempotência (reprocessar não corrompe).
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Qual a armadilha de usar uma lista como valor default de um parâmetro?"
  :::{dropdown} Resposta modelo
  O default é criado uma vez e **compartilhado** entre chamadas; mutá-lo acumula estado entre invocações. Use `None` como default e crie a lista dentro da função.
  :::
- **P:** "Como você organizaria um projeto de pipeline em Python?"
  :::{dropdown} Resposta modelo
  Em módulos por responsabilidade (`ingestao.py`, `transform.py`, `load.py`), funções pequenas e puras onde possível, um `main`/orquestrador que as compõe, testes com pytest e `if __name__ == "__main__"` para o ponto de entrada.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Ramalho — Fluent Python**, caps. de funções e orientação a objetos (Python idiomático).
- **Docs oficiais** — tutorial de módulos e de classes; `dataclasses`.
- **McKinney — Python for Data Analysis**, para aplicar em manipulação de dados.

## 📚 Referências
- Ramalho, L. *Fluent Python*, 2ª ed. (2022) — caps. de funções e POO. <!-- @ramalho2022 -->
- Python. *Documentação oficial* — [módulos e classes](https://docs.python.org/3/tutorial/). <!-- @docs-python -->
- McKinney, W. *Python for Data Analysis*, 3ª ed. (2022) — [leitura aberta](https://wesmckinney.com/book/). <!-- @mckinney2022 -->

*Acessado em: 2026-08-21.*

---
**Revisado em:** 2026-08-21
