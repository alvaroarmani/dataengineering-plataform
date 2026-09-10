# Python avançado para dados: lazy, decorators, context managers e concorrência

<!-- tipo: pratico -->

## 🎯 O problema (motivação)

Seu script lê um CSV de 50 GB com `pd.read_csv` e o processo **morre por falta de memória**. Ou: um
job que baixa de 500 APIs leva 2 horas — quase todo o tempo **esperando a rede**, com a CPU ociosa.
Ou ainda: você repete o mesmo bloco de `try/retry/log` em dez funções. Esses são problemas de
**Python de produção**, e resolvê-los separa quem "sabe pandas" de quem escreve engenharia de dados
robusta. Esta unidade cobre as ferramentas avançadas do Python que a FIAP e o mercado esperam de um
engenheiro: processar **lazy** (sem estourar memória), **decorators** e **context managers** para
código reutilizável e seguro, e **concorrência** para não desperdiçar tempo esperando.

## 💡 Conceito (o porquê)

### Iteradores e generators: processar sem carregar tudo
Carregar 50 GB na memória é o erro. A saída é ser **lazy**: processar **um item por vez**, num fluxo.
- Um **iterador** produz valores sob demanda; um **generator** (função com `yield`) é a forma fácil de
  criar um. Ele **pausa** a cada `yield` e só produz o próximo quando pedido — memória **O(1)**, não
  O(n).
- `for linha in open(arquivo)` já é lazy: lê linha a linha. `pd.read_csv(..., chunksize=100_000)`
  devolve um iterador de pedaços. **Generator expressions** (`(f(x) for x in fonte)`) encadeiam
  transformações sem materializar listas intermediárias.

Regra de ouro: para dados grandes, **fluxo (stream) em vez de lista**. É o mesmo princípio da *lazy
evaluation* do Spark (M11), no Python puro.

### Decorators: comportamento reutilizável
Um **decorator** é uma função que **embrulha** outra, adicionando comportamento sem alterar o corpo
dela. É como você aplica `@retry`, `@timing`, `@cache` a várias funções sem copiar código:
```python
def com_retry(fn):
    def wrapper(*args, **kwargs):
        for tentativa in range(3):
            try:
                return fn(*args, **kwargs)
            except Exception:
                if tentativa == 2:
                    raise
    return wrapper

@com_retry
def baixar(url): ...
```
Decorators encapsulam *cross-cutting concerns* (retry, logging, medição, cache) — os mesmos padrões
de resiliência do M23, agora como sintaxe. `functools.wraps`, `lru_cache` e `cached_property` são do
kit padrão.

### Context managers: recursos que sempre fecham
Conexão de banco, arquivo, lock — tudo que **abre** precisa **fechar**, mesmo se der erro no meio. O
**context manager** (`with`) garante isso:
```python
with open(caminho) as f:      # __enter__
    processa(f)               # se estourar aqui...
# __exit__ fecha o arquivo de qualquer jeito
```
Você cria os seus com uma classe (`__enter__`/`__exit__`) ou, mais fácil, com `@contextmanager` +
`yield`. É o que evita **vazamento de recursos** (conexões que ficam abertas até derrubar o banco) —
um bug clássico de pipelines de longa duração.

### Concorrência: não desperdiçar a espera
Quando o gargalo é **esperar** (rede, disco), rodar sequencial é desperdício. Python oferece três
modelos, e escolher o certo depende do gargalo:
- **I/O-bound** (esperar rede/disco): **threads** (`ThreadPoolExecutor`) ou **asyncio**. O **GIL**
  (Global Interpreter Lock) impede dois *bytecodes* Python ao mesmo tempo, mas ele é **liberado
  durante I/O** — então threads/async paralelizam a espera muito bem (baixar 500 APIs "ao mesmo
  tempo").
- **CPU-bound** (cálculo pesado em Python puro): **multiprocessing**. Como o GIL serializa CPU, você
  precisa de **processos** (cada um com seu interpretador) para usar vários núcleos — ou empurrar o
  cálculo para bibliotecas vetorizadas (NumPy/pandas) que soltam o GIL.

Errar isso é comum: usar threads para trabalho CPU-bound (não acelera, por causa do GIL) ou processos
para I/O (overhead à toa).

### Vetorização: o loop que você não deve escrever
Em dados, o loop Python explícito costuma ser o gargalo. **Vetorizar** (operar na coluna inteira com
NumPy/pandas) é ordens de grandeza mais rápido, porque roda em C e solta o GIL. `df["a"] * df["b"]`
vence `for` sempre. A regra: se você está iterando linha a linha num DataFrame, quase sempre há uma
operação vetorizada melhor.

## 🔎 Exemplo
Um pipeline precisa somar a receita de um arquivo de 50 GB e enriquecer via uma API por cliente. A
solução em Python de produção: **generator** lê o arquivo linha a linha (memória O(1)) e uma
*generator expression* soma a receita em fluxo; a chamada às APIs, sendo **I/O-bound**, roda num
`ThreadPoolExecutor` (o GIL libera na espera, então 50 chamadas ocorrem concorrentes); cada conexão
usa `with` (context manager) para nunca vazar; e a função de download tem `@com_retry` para tolerar
falhas transitórias. O que estouraria a memória e levaria horas roda enxuto e rápido — sem truque,
só Python avançado bem aplicado.

## ⚠️ Erros comuns
- **Carregar tudo na memória** (`read_csv` de um arquivo gigante) em vez de processar em fluxo (chunks/generators).
- **Threads para trabalho CPU-bound** — o GIL serializa; use multiprocessing ou vetorização.
- **Esquecer de fechar recursos** — conexões/arquivos vazando; use `with` (context manager).
- **Loop linha a linha em DataFrame** — quase sempre há vetorização mais rápida.
- **Copiar o mesmo retry/log em N funções** — extraia para um decorator.

## 💼 O que o mercado espera
Processar dados grandes de forma **lazy** (generators/chunks), usar **decorators** e **context
managers** idiomaticamente, e escolher o modelo de concorrência certo (threads/async para I/O,
multiprocessing/vetorização para CPU) entendendo o **GIL**. É o que distingue Python "de script" de
Python "de engenharia".

:::{admonition} ✨ Em resumo
:class: resumo
- **Generators/iteradores** processam em **fluxo** (memória O(1)) — essencial para dados grandes.
- **Decorators** embrulham comportamento reutilizável (retry, timing, cache); **context managers** (`with`) garantem fechamento de recursos.
- **Concorrência pelo gargalo**: threads/asyncio para **I/O-bound** (o GIL libera na espera); **multiprocessing** para **CPU-bound**.
- **Vetorize** (NumPy/pandas) em vez de loops linha a linha.
:::

## 🧠 Quiz de recall
1. Por que usar um generator para processar um arquivo enorme?
   :::{dropdown} Resposta
   Porque ele produz um item por vez (lazy), mantendo memória O(1) em vez de carregar o arquivo inteiro (O(n)) e estourar a RAM.
   :::
2. O que um decorator faz?
   :::{dropdown} Resposta
   Embrulha uma função, adicionando comportamento (retry, logging, cache, medição) sem alterar o corpo dela — encapsulando preocupações transversais.
   :::
3. Para que serve um context manager (`with`)?
   :::{dropdown} Resposta
   Garantir que um recurso (arquivo, conexão, lock) seja liberado ao final do bloco, mesmo se ocorrer um erro no meio — evitando vazamento de recursos.
   :::
4. Threads ou multiprocessing: quando usar cada um, e por causa de quê?
   :::{dropdown} Resposta
   Threads/asyncio para I/O-bound (o GIL é liberado durante a espera de rede/disco); multiprocessing para CPU-bound (o GIL serializa cálculo Python, então processos separados usam vários núcleos).
   :::
5. Por que vetorizar em vez de fazer loop linha a linha num DataFrame?
   :::{dropdown} Resposta
   Operações vetorizadas (NumPy/pandas) rodam em C e liberam o GIL, sendo ordens de grandeza mais rápidas que o loop Python explícito.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Você precisa processar um arquivo de 100 GB numa máquina com 16 GB de RAM. Como faz?"
  :::{dropdown} Resposta modelo
  Processo em fluxo, nunca carregando tudo: leio o arquivo com generators/`chunksize`, encadeio transformações com generator expressions (sem materializar listas) e agrego incrementalmente. Assim a memória fica O(1)/O(chunk). Se ainda for pesado, particiono o trabalho ou uso uma engine distribuída (Spark, M11), mas em Python puro a chave é lazy evaluation em vez de list na memória.
  :::
- **P:** "Um job que chama muitas APIs está lento. Como acelerar, e qual a pegadinha do GIL?"
  :::{dropdown} Resposta modelo
  É I/O-bound (o tempo é esperar a rede), então paralelizo com ThreadPoolExecutor ou asyncio: o GIL é liberado durante o I/O, então dezenas de chamadas acontecem concorrentes. A pegadinha é achar que threads não ajudam por causa do GIL — ajudam em I/O; o GIL só é problema para trabalho CPU-bound em Python puro, onde eu usaria multiprocessing ou vetorização.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Ramalho — Fluent Python** (generators, decorators, context managers, concorrência).
- **McKinney — Python for Data Analysis** (vetorização e performance em pandas).
- **Documentação do Python** — `itertools`, `functools`, `contextlib`, `concurrent.futures`, `asyncio`.

## 📚 Referências
- Ramalho, L. *Fluent Python* (2022) — recursos avançados de Python. <!-- @ramalho2022 -->
- McKinney, W. *Python for Data Analysis* (2022) — vetorização e desempenho. <!-- @mckinney2022 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — Python em pipelines. <!-- @reis2022 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
