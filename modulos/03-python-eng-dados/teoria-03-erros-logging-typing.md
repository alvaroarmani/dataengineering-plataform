# Erros, logging e type hints: código que aguenta produção

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Em produção, um pipeline **sempre** encontra o inesperado: um CSV com uma linha corrompida,
uma API que caiu, um campo nulo onde não devia. Duas reações erradas: **ignorar** tudo (dados
silenciosamente corrompidos) ou **explodir** ao primeiro problema (pipeline frágil que morre
por causa de uma linha). O caminho profissional é **tratar erros com intenção** e **registrar
o que aconteceu** (logging) para você conseguir depurar depois. E **type hints** deixam o
contrato do código explícito — para você, para o time e para as ferramentas.

## 💡 Conceito (o porquê)

### Exceções: trate o específico, não o genérico
```python
try:
    valor = float(campo)
except ValueError:              # capture o erro ESPERADO, não tudo
    valor = None
```
- Capture exceções **específicas** (`ValueError`, `KeyError`), nunca um `except:` pelado —
  ele engole até erros de programação e esconde bugs.
- `else` roda se **não** houve exceção; `finally` roda **sempre** (fechar arquivo/conexão).
- **Levante** erros de verdade com `raise`; crie exceções próprias para domínios (`class DadoInvalido(Exception): ...`).
- Estilo pythônico: **EAFP** ("é mais fácil pedir perdão que permissão") — tente e trate a
  exceção, em vez de checar tudo antes (LBYL).

### Padrão de dados: quarentena, não queda
Numa ingestão, uma linha ruim **não deve derrubar** o lote. O padrão é **separar** válidos de
inválidos e seguir:
```python
validos, invalidos = [], []
for linha in linhas:
    try:
        validos.append(parse(linha))
    except ValueError:
        invalidos.append(linha)     # "quarentena" para inspecionar depois
```
Isso é resiliência: você processa o que dá e **registra** o que falhou.

### Logging: por que não `print`
`print` some no vazio em produção. O módulo **`logging`** dá **níveis** (`DEBUG`, `INFO`,
`WARNING`, `ERROR`), timestamps e destino configurável (arquivo, stdout, coletor):
```python
import logging
log = logging.getLogger(__name__)
log.warning("Linha inválida ignorada: %s", linha)
```
Logs são a base da **observabilidade** (M12): sem eles, um pipeline "verde" pode estar
descartando metade dos dados sem ninguém perceber.

### Type hints: o contrato explícito
```python
def receita_por_estado(vendas: list[dict]) -> dict[str, float]:
    ...
```
Anotações **não mudam a execução** (Python não força tipos em runtime), mas: documentam o
contrato, ligam o autocomplete do editor e permitem checagem estática (ex.: `mypy`) que pega
erros antes de rodar. `Optional[int]` (ou `int | None`) sinaliza "pode ser nulo".

## 🔎 Exemplo

```python
import logging
log = logging.getLogger(__name__)

def carregar(linhas: list[str]) -> tuple[list[float], list[str]]:
    validos, invalidos = [], []
    for l in linhas:
        try:
            validos.append(float(l))
        except ValueError:
            invalidos.append(l)
            log.warning("valor inválido: %r", l)
    return validos, invalidos
```

:::{admonition} 📖 Da literatura
:class: seealso
Ramalho trata os *type hints* como documentação executável: não alteram o comportamento em
tempo de execução, mas habilitam ferramentas (checadores estáticos, IDEs) que aumentam a
confiabilidade do código. — *Fluent Python*, cap. sobre type hints.
:::

## ⚠️ Erros comuns
- `except:` pelado ou `except Exception` amplo — esconde bugs; capture o erro específico.
- Usar `print` em vez de `logging` num pipeline.
- Deixar uma linha ruim derrubar o lote inteiro (falta de quarentena).
- Achar que type hints são validados em runtime (não são — precisa de `mypy`/pydantic).
- `finally` esquecido: recursos (arquivos/conexões) que não são fechados.

## 💼 O que o mercado espera
Código **resiliente e observável**: trata o inesperado, não perde dados em silêncio, e loga
o suficiente para depurar. Type hints são cada vez mais padrão em bases profissionais.

:::{admonition} ✨ Em resumo
:class: resumo
- Capture o erro **específico** — nunca `except:` pelado.
- **Quarentena**: separe válidos de inválidos, não derrube o lote por uma linha ruim.
- **`logging`** > `print` (níveis, timestamps, observabilidade).
- **Type hints** documentam o contrato (validados por mypy, não em runtime).
:::

## 🧠 Quiz de recall
1. Por que evitar `except:` pelado?
   :::{dropdown} Resposta
   Ele captura **qualquer** exceção — inclusive erros de programação (typos, `KeyError`) e até `KeyboardInterrupt` — escondendo bugs. Capture o erro específico esperado.
   :::
2. Qual o padrão para lidar com linhas inválidas numa ingestão?
   :::{dropdown} Resposta
   Separar válidos de inválidos (quarentena): processar o que dá certo e coletar/registrar o que falhou, sem derrubar o lote inteiro.
   :::
3. Type hints são validados em tempo de execução?
   :::{dropdown} Resposta
   Não. Python não força tipos em runtime; hints documentam o contrato e habilitam ferramentas estáticas (mypy) e o editor. Para validar de verdade, use mypy ou pydantic.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Por que usar `logging` em vez de `print`?"
  :::{dropdown} Resposta modelo
  `logging` tem níveis (DEBUG/INFO/WARNING/ERROR), timestamps, e destino/formatação configuráveis (arquivo, stdout, coletor central). É a base da observabilidade; `print` não é controlável nem filtrável em produção.
  :::
- **P:** "O que é EAFP em Python?"
  :::{dropdown} Resposta modelo
  "Easier to Ask Forgiveness than Permission" — o estilo idiomático de tentar a operação e tratar a exceção, em vez de checar todas as pré-condições antes (LBYL). Costuma ser mais limpo e rápido em Python.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Docs oficiais** — tutorial de *Errors and Exceptions* e o *Logging HOWTO*.
- **Ramalho — Fluent Python**, cap. de type hints em funções.
- **McKinney — Python for Data Analysis** — para aplicar tratamento de erros em ingestão real.

## 📚 Referências
- Python. *Documentação oficial* — [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html) e [Logging HOWTO](https://docs.python.org/3/howto/logging.html). <!-- @docs-python -->
- Ramalho, L. *Fluent Python*, 2ª ed. (2022) — cap. de type hints. <!-- @ramalho2022 -->
- McKinney, W. *Python for Data Analysis*, 3ª ed. (2022) — [leitura aberta](https://wesmckinney.com/book/). <!-- @mckinney2022 -->

*Acessado em: 2026-08-21.*

---
**Revisado em:** 2026-08-21
