# Testes com pytest e boas práticas: código em que se confia

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Dados mudam, requisitos mudam, e uma alteração inocente numa função de limpeza pode
**quebrar** o pipeline sem ninguém perceber — até o relatório sair errado. **Testes**
automatizados são a rede de segurança: eles falham na sua máquina, não na produção. E
**boas práticas** de projeto mantêm o código legível e sustentável quando ele cresce. Não
por acaso, é assim que você corrige os exercícios deste curso: *fazendo o `pytest` passar*.

## 💡 Conceito (o porquê)

### pytest em 1 minuto
Um teste é uma função `test_*` que faz uma afirmação com `assert`:

```python
# solucao.py
def media(nums):
    return sum(nums) / len(nums)

# test_media.py
from solucao import media

def test_media_basica():
    assert media([2, 4]) == 3
```

Rode com `pytest -q`. Se o `assert` for verdadeiro, passa (verde); senão, o pytest mostra
**exatamente** o que era esperado vs. o que veio.

### Casos de borda importam
Bugs vivem nas bordas: lista vazia, `None`, valores negativos, duplicatas. Um bom conjunto
de testes cobre o caso comum **e** os de borda:

```python
def test_media_um_elemento():
    assert media([10]) == 10
```

### `parametrize`: muitos casos, um teste
Para não repetir, teste vários casos de uma vez:

```python
import pytest

@pytest.mark.parametrize("entrada, esperado", [([2, 4], 3), ([10], 10), ([1, 2, 3], 2)])
def test_media(entrada, esperado):
    assert media(entrada) == esperado
```

### `fixtures`: preparar o cenário
Quando vários testes precisam do mesmo dado, uma **fixture** cria esse cenário uma vez:

```python
@pytest.fixture
def vendas():
    return [{"estado": "SP", "valor": 100}, {"estado": "RJ", "valor": 30}]

def test_receita(vendas):
    assert receita_total(vendas) == 130
```

### Por que funções puras são fáceis de testar
Funções **puras** (mesmo input → mesmo output, sem efeito colateral) são triviais de testar —
você chama e compara. Por isso o padrão do curso: isole a lógica em funções puras e teste-as.

## 🔎 Exemplo — testando uma transformação
```python
def limpar(regs):
    return [r for r in regs if r.get("valor") is not None]

def test_limpar_remove_nulos():
    entrada = [{"valor": 1}, {"valor": None}, {"valor": 2}]
    assert limpar(entrada) == [{"valor": 1}, {"valor": 2}]
```

## ✅ Boas práticas de projeto (o resto que o mercado espera)
- **Ambiente virtual** (`venv`) + **`requirements.txt` com versões pinadas** → reprodutível.
- **Estrutura em módulos** por responsabilidade (`ingestao.py`, `transform.py`, `load.py`).
- **Nomes claros** e **funções pequenas** (uma responsabilidade); PEP 8 como guia de estilo.
- **Docstrings** dizendo o contrato (o que recebe, o que retorna).
- **Nunca** versionar segredos (`.env`) nem dados grandes (`.gitignore`).
- **Testes junto do código**, rodando no **CI** a cada PR (visto no M13).

:::{admonition} 📖 Da literatura
:class: seealso
A documentação do pytest enfatiza a simplicidade: testes são funções comuns com `assert`,
e recursos como *fixtures* e *parametrize* reduzem repetição sem esconder o que está sendo
verificado. — *pytest — documentação oficial*.
:::

## ⚠️ Erros comuns
- Só testar o **caminho feliz** e ignorar os casos de borda (onde moram os bugs).
- Testes que dependem de **ordem** ou de **estado global** (frágeis).
- Misturar lógica com I/O, tornando a função difícil de testar (isole efeitos).
- `requirements.txt` sem versões → "funcionava semana passada".
- Escrever muito código antes de rodar o primeiro teste.

## 💼 O que o mercado espera
Código **testado** e projeto **organizado** separam Júnior de Pleno. Saber escrever um teste
com pytest (e ler a falha) é esperado — e é exatamente o que você já vem praticando aqui.

:::{admonition} ✨ Em resumo
:class: resumo
- Teste = função `test_*` com **`assert`**; rode com `pytest -q`.
- Cubra **casos de borda** (vazio, None, negativos); use **`parametrize`** e **`fixtures`**.
- **Funções puras** são fáceis de testar — isole os efeitos nas bordas.
- Boas práticas: venv + requirements pinado, módulos, nomes claros, docstrings, segredos fora do git.
:::

## 🧠 Quiz de recall
1. O que é um teste em pytest, na forma mais simples?
   :::{dropdown} Resposta
   Uma função com nome começando por `test_` que faz uma afirmação com `assert`; se a afirmação for verdadeira, o teste passa.
   :::
2. Para que serve `@pytest.mark.parametrize`?
   :::{dropdown} Resposta
   Rodar o mesmo teste com vários pares de entrada/esperado, sem repetir código — cada caso vira um teste independente.
   :::
3. Por que funções puras são mais fáceis de testar?
   :::{dropdown} Resposta
   Porque, sem efeitos colaterais e com saída determinada só pela entrada, basta chamar e comparar o resultado — sem preparar estado externo.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você testaria uma função de transformação de dados?"
  :::{dropdown} Resposta modelo
  Isolando-a como função pura e escrevendo casos com pytest: o caminho feliz e os de borda (vazio, nulos, tipos inesperados, duplicatas), comparando a saída esperada. Se possível, `parametrize` para cobrir vários casos e `fixtures` para dados compartilhados.
  :::
- **P:** "O que você garante num projeto Python profissional além de testes?"
  :::{dropdown} Resposta modelo
  Ambiente reprodutível (venv + requirements pinado), estrutura em módulos por responsabilidade, nomes claros e funções pequenas, docstrings, estilo (PEP 8), segredos fora do repositório, e testes rodando em CI.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Docs do pytest** — "Get Started", *fixtures* e *parametrize*.
- **Ramalho — Fluent Python** — para escrever funções e classes idiomáticas (mais fáceis de testar).

## 📚 Referências
- pytest. *Documentação oficial* — [docs.pytest.org](https://docs.pytest.org/). <!-- @docs-pytest -->
- Ramalho, L. *Fluent Python*, 2ª ed. (2022) — funções e boas práticas. <!-- @ramalho2022 -->

*Acessado em: 2026-08-22.*

---
**Revisado em:** 2026-08-22
