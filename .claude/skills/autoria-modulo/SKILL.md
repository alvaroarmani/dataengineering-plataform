---
name: autoria-modulo
description: >
  Padrão de autoria de módulos e unidades da Especialização em Engenharia de Dados
  (este repositório). Use SEMPRE que for criar ou completar um módulo, uma aula de
  teoria, um lab (.ipynb) ou um exercício com correção automática do curso — mesmo que
  o pedido não diga "use a skill". Garante que todo conteúdo saia consistente: ementa no
  padrão MEC, teoria com o porquê + referências datadas, prática que roda, correção
  "faça o pytest passar", flashcards de revisão espaçada e critério de maestria.
---

# Autoria de Módulo

Esta skill codifica **como** escrever conteúdo do curso para que tudo saia consistente.
Leia `CONTRIBUTING.md` e `ARCHITECTURE.md` na raiz do repo para o contexto maior.

## Quando usar

Ao criar/completar: um módulo novo, uma página de teoria, um lab, um exercício, ou o
baralho de flashcards de um módulo.

## Princípios (o porquê antes do como)

1. **Ensine o *porquê*, linke o *como* volátil.** Conceitos (modelagem, idempotência, particionamento) são estáveis; APIs de dbt/Airflow/BigQuery mudam. Explique o conceito; para detalhes de versão, aponte a **doc oficial**.
2. **Prática que roda.** Toda unidade termina com um lab executável e um exercício autocorrigível.
3. **Datasets reais** (ver `datasets/README.md`), nunca fictícios.
4. **Progressão por maestria:** cada módulo declara um critério objetivo de conclusão.
5. **Datar:** toda página termina com `**Revisado em:** AAAA-MM-DD`.

## Referências e registro (obrigatório)

Toda teoria é ancorada em fontes — e o linter `scripts/verificar-conteudo.py` impõe isto.

- **Tipo da página:** declare no topo `<!-- tipo: conceitual | pratico | ferramenta -->`. A régua muda:
  - `conceitual` → ≥3 refs + Quiz + (box "📖 Da literatura" **ou** seção "Para ir além").
  - `pratico` → ≥2 refs + Quiz.
  - `ferramenta` → ≥2 refs + **≥1 doc oficial** (chave `docs-*`).
- **Registro é a fonte única:** cite **apenas** obras de `referencias.yaml`. Marque cada referência com a chave em comentário: `- Autor, *Título* ... <!-- @chave -->`. Fonte fora do registro **reprova no linter** (combate citação inventada). Falta uma obra? **Adicione-a primeiro ao `referencias.yaml`** (com dados verificados).
- **Política:** paráfrase fiel + citação precisa (autor, livro, **capítulo**); citações curtas atribuídas; **verbatim só de fonte aberta** (doc/paper/blog do autor) — nunca reproduzir trechos longos de livro protegido; **nunca inventar** página/citação; ≥1 fonte aberta por conceito central; `acessado em` nos links.
- **Enriquecimentos** (quando fizer sentido): box `🏭 Do mundo real` (caso/arquitetura/postmortem real, fonte aberta), bloco **"Perguntas essenciais"** no `index.md`, entrada no banco de questões, seção no `troubleshooting.md`.

## Tom e leitura (dose "média")

- **Emojis pontuais** nos títulos de seção padrão: `## 🎯 O problema`, `## 💡 Conceito`, `## 🔎 Exemplo`, `## ⚠️ Erros comuns`, `## 💼 O que o mercado espera`, `## 🧠 Quiz de recall`, `## 🎤 Q&A estilo entrevista`, `## 🚀 Para ir além`, `## 📚 Referências`. (Substring-safe para o linter.)
- **Parágrafos curtos** e tom **amigável/encorajador**, sem perder rigor.
- Uma caixa **`:::{admonition} ✨ Em resumo / :class: resumo`** (3–4 bullets) logo antes do Quiz.
- Emojis com parcimônia (dose média) — no corpo, só quando ajudam; nada de poluição visual.

## Profundidade por unidade (a partir do M4)

- **≥2 exercícios `pytest` por unidade** (não 1) — fluência exige repetição.
- **Datasets reais** nos labs/exercícios quando o tópico permitir (NYC Taxi, Olist) — ver `datasets/`.

## Fluxo para criar um módulo

1. Copie `templates/template-modulo.md` para `modulos/NN-nome/index.md` e preencha a ementa.
2. Para cada unidade: uma página de teoria (`templates/template-teoria.md`) + um lab + um exercício.
3. Crie `recursos.md` (livros, papers, vídeos, docs oficiais) e `flashcards.md`.
4. Registre o módulo no `_toc.yml` e o critério de maestria no `progresso.md`.
5. Rode `jupyter-book build .` e garanta que não há novos warnings.

## Padrão de cada artefato

### Página de teoria
Estrutura: problema motivador → conceito com o *porquê* → exemplo → "erros comuns" →
"o que o mercado espera" → quiz de recall → Q&A estilo entrevista → referências datadas.

### Lab (.ipynb)
Primeira célula (markdown) declara **onde roda**: `Browser (JupyterLite)` ou
`Bancada Docker`. Fundamentos de Python/pandas/SQL-DuckDB → browser. Qualquer coisa com
Postgres/Airflow/dbt/Spark/MinIO/rede → Docker.

### Exercício ("faça o pytest passar")
Pasta `exercicio-NN/` com:
- `enunciado.md` — o que fazer + hint ladder (dicas progressivas em `<details>`).
- `solucao.py` — assinatura + `# SEU CÓDIGO AQUI`.
- `tests/test_*.py` — asserts objetivos. Meta do aluno: `pytest -q` verde.
- Ao final do enunciado, uma seção `<details>` com a **solução comentada** (liberada após passar).

Para checagem rápida **no browser**, use `verificar(resposta)` com `assert` que imprime ✅/❌ + dica.

### Flashcards
`flashcards.md` — pares Pergunta/Resposta curtos para revisão espaçada. Uma linha por card:
`- **P:** ... / **R:** ...`

## Barra de qualidade (Definition of Done)

- [ ] Teoria com o *porquê* + `<!-- tipo: ... -->` declarado.
- [ ] **Referências no registro** (`referencias.yaml`), marcadas com `<!-- @chave -->`; mínimos do tipo atingidos.
- [ ] `index.md` com **Perguntas essenciais** + critério de maestria; `progresso.md` atualizado.
- [ ] Tom "médio": emojis pontuais nos títulos + caixa "✨ Em resumo" antes do Quiz.
- [ ] Lab que roda (declara browser vs Docker).
- [ ] Exercício com correção automática + hint ladder + solução comentada (**≥2 por unidade a partir do M4**).
- [ ] Dataset real quando o tópico permitir (a partir do M4).
- [ ] Flashcards adicionados.
- [ ] **`python scripts/verificar-conteudo.py` verde.**
- [ ] Build sem novos warnings; `CHANGELOG.md` atualizado.
