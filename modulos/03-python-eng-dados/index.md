# Módulo 03 — Python para Engenharia de Dados

> Do básico ao avançado: escrever Python de qualidade para manipular e mover dados, com testes.

## Perguntas essenciais
Ao final deste módulo, você saberá responder:
1. Qual estrutura de dados (list/dict/set/tuple) usar em cada situação — e por quê?
2. Como escrever funções pequenas, testáveis e com tratamento de erros?
3. Como manipular dados tabulares com pandas e consumir uma API?

## Identificação
- **Eixo:** 1 — Fundamentos
- **Carga horária:** 60h
- **Pré-requisitos:** M02
- **Onde roda:** Browser (fundamentos) + Bancada Docker (projetos)

## Ementa
Fundamentos de Python: tipos, estruturas de dados, controle de fluxo, funções. Programação
orientada a objetos, módulos e pacotes. Tratamento de erros e logging. Manipulação de
dados com pandas. Consumo de APIs (requests) e formatos (JSON, CSV, Parquet). Boas práticas:
ambientes virtuais, type hints, estilo (PEP 8), testes com pytest.

## Competências e habilidades
- C1 — programar em Python para dados, com testes e boas práticas.

## Objetivos de aprendizagem
1. **Escrever** funções e classes Python idiomáticas e testáveis.
2. **Manipular** dados tabulares com pandas (filtros, joins, groupby).
3. **Consumir** uma API e persistir os dados em formatos adequados.
4. **Testar** o código com pytest e tratar erros de forma robusta.

## Plano de aulas (unidades)

**Unidade 1 — Estruturas de dados**
1. **Teoria:** [Python para dados: estruturas que você usa todo dia](teoria-01-python-fundamentos.md)
2. **Lab:** [Python para dados na prática](lab-01-python-para-dados.ipynb)
3. **Exercício:** [Top categorias por receita](exercicio-01.md)

**Unidade 2 — Funções, POO e módulos**
4. **Teoria:** [Funções, classes e módulos](teoria-02-funcoes-poo-modulos.md)
5. **Lab:** [Funções que compõem e uma classe](lab-02-funcoes-e-classes.ipynb)
6. **Exercício:** [Um Pipeline de transformações](exercicio-02.md)

**Unidade 3 — Erros, logging e type hints**
7. **Teoria:** [Erros, logging e type hints](teoria-03-erros-logging-typing.md)
8. **Lab:** [Tratando erros e registrando](lab-03-erros-e-logging.ipynb)
9. **Exercício:** [Quarentena de valores](exercicio-03.md)

**Unidade 4 — pandas**
10. **Teoria:** [pandas: manipulando dados tabulares](teoria-04-pandas.md)
11. **Lab:** [pandas na prática](lab-04-pandas-na-pratica.ipynb)
12. **Exercício:** [Receita por categoria com pandas](exercicio-04.md)

**Revisão:** [Flashcards](flashcards.md)

_Próximas unidades (em construção): APIs/Parquet, testes com pytest._

## Metodologia e avaliação
**Maestria:** série de exercícios `pytest` verdes + um mini-ETL em Python conforme rubrica +
quiz ≥ 80%.

## O que o mercado espera
Python é a segunda competência mais pedida (após SQL). Esperam código limpo, com testes e
tratamento de erros — não scripts frágeis de notebook.

## Erros comuns
- Não usar ambientes virtuais/pinagem de versões.
- Ignorar tratamento de erros e logging.
- Abusar de pandas onde SQL/DuckDB seria melhor.

## Recursos
A curar em `recursos.md` (McKinney *Python for Data Analysis*; Ramalho *Fluent Python*; docs oficiais).

---
**Revisado em:** 2026-08-20
