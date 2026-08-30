# Portfólio, GitHub, currículo e LinkedIn para engenharia de dados

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você pode dominar dbt, Airflow e modelagem dimensional — mas se ninguém **vê** isso, a vaga vai
para outra pessoa. A maioria dos candidatos a Data Engineer júnior/pleno erra no mesmo ponto: um
currículo genérico ("conhecimento em Python e SQL"), um GitHub vazio ou com notebooks bagunçados,
e um LinkedIn que só repete o currículo. O recrutador tem **segundos** por perfil. Este módulo
trata a **empregabilidade como uma skill de engenharia**: você tem projetos reais (os deste curso
+ o TCC) — falta empacotá-los de um jeito que **prove competência em 30 segundos**.

## 💡 Conceito (o porquê)

### Portfólio prova; currículo afirma
Qualquer um pode *escrever* "sei Airflow". Um **repositório no GitHub** com um pipeline que roda,
um README claro e commits reais **demonstra**. Por isso o portfólio é o ativo mais forte de quem
está migrando de carreira: substitui a experiência formal por **evidência verificável**. A regra:
para cada skill que você reivindica, deve existir **um artefato público** que a comprove.

### O README é a interface do projeto
Um recrutador (e um futuro colega) julga o projeto **pelo README antes do código**. Um bom README
responde, em ordem: **o que** o projeto faz, **por que** existe (problema de negócio), **qual a
arquitetura** (um diagrama do pipeline), **como rodar** (comandos), e **o que você aprendeu**.
Sem isso, mesmo um projeto excelente parece abandonado. O README é onde a engenharia vira
**narrativa** — a mesma habilidade que você usará em stand-ups e docs no trabalho.

### Poucos projetos bons > muitos projetos rasos
Três projetos **completos, versionados e documentados** valem mais que vinte notebooks soltos. O
avaliador procura **profundidade e cuidado** (testes, estrutura, commits com mensagem, CI verde),
não volume. Idealmente o portfólio cobre o pipeline inteiro: ingestão → transformação (dbt) →
orquestração (Airflow) → um DW modelado (o TCC). Isso conta uma história: "sei construir uma
plataforma de dados de ponta a ponta".

### Currículo: impacto, não lista de tecnologias
Um bom currículo de dados descreve **realizações com resultado** ("construí um pipeline dbt+Airflow
que reduziu o tempo de atualização do relatório de 6h para 20min"), não uma sopa de siglas. Cada
bullet: **o que você fez + com que ferramenta + qual o resultado**. Verbos de ação, números quando
houver, e alinhamento às palavras-chave da vaga (muitos filtros são automáticos).

### LinkedIn e presença: ser encontrável
LinkedIn não é o currículo repetido: é onde recrutadores **buscam** (headline com "Data Engineer"
e as stacks), onde seu trabalho aparece (posts sobre os projetos — *build in public*) e onde a
rede acontece. Estar **encontrável e ativo** gera oportunidades que você não vê no mural de vagas.

## 🔎 Exemplo
Ao terminar o TCC (M16), você publica um repo `dw-ecommerce`: README com o problema (analytics de
e-commerce), um diagrama mermaid do pipeline, instruções `docker compose up`, os models dbt com
testes, a DAG do Airflow e o modelo dimensional. No currículo: "Projetei um Data Warehouse
dimensional (star schema) com dbt e Airflow sobre dados reais (Olist), com testes de qualidade e
CI". No LinkedIn: headline "Data Engineer | Python · dbt · Airflow · SQL" + um post explicando uma
decisão de arquitetura do projeto. Agora a mesma competência aparece em três lugares que o
recrutador olha — e **linkada ao código que a prova**.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley descrevem o engenheiro de dados como quem integra o ciclo de vida do dado com as
*undercurrents* (segurança, gestão, qualidade) — competências que o portfólio deve **evidenciar**,
não só listar. Beauchemin, em "The Rise of the Data Engineer", argumenta que a disciplina é
**engenharia de software aplicada a dados** — daí o peso de Git, testes e documentação no
portfólio. — *Fundamentals of Data Engineering*; *The Rise of the Data Engineer*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Recrutadores técnicos frequentemente abrem o GitHub antes da entrevista. Um repo com README claro,
commits reais e CI verde é um sinal forte de senioridade — mostra que você trabalha como
engenheiro, não só "roda notebooks". O inverso (repo vazio ou "final_v3_ok.ipynb") derruba
candidatos tecnicamente bons. — prática de mercado; Beauchemin.
:::

## ⚠️ Erros comuns
- **Reivindicar sem provar** — "sei Airflow" sem um repo com uma DAG que roda.
- **README ausente ou pobre** — o melhor projeto parece morto sem explicação e diagrama.
- **Volume > profundidade** — muitos notebooks rasos em vez de 3 projetos completos.
- **Currículo lista de siglas** — sem realização, sem resultado, sem número.
- **LinkedIn = cópia do currículo** — sem headline buscável nem sinal de atividade.

## 💼 O que o mercado espera
Para júnior/pleno em migração, o portfólio é decisivo: projetos versionados no GitHub com README e,
de preferência, o pipeline completo (ingestão→dbt→Airflow→DW). Currículo com impacto e palavras-
chave da vaga; LinkedIn encontrável. "Me conta sobre um projeto seu" é quase certo numa entrevista.

:::{admonition} ✨ Em resumo
:class: resumo
- **Portfólio prova, currículo afirma**: cada skill reivindicada tem um artefato público.
- **README é a interface**: o quê, por quê, arquitetura, como rodar, o que aprendi.
- **Profundidade > volume**: 3 projetos completos contando a história do pipeline inteiro.
- **Currículo = impacto** (o que + ferramenta + resultado); **LinkedIn = ser encontrável e ativo**.
:::

## 🧠 Quiz de recall
1. Por que o portfólio é mais forte que o currículo para quem migra de carreira?
   :::{dropdown} Resposta
   Porque prova competência com evidência verificável (código que roda), substituindo a experiência formal que o candidato ainda não tem.
   :::
2. O que um bom README deve responder?
   :::{dropdown} Resposta
   O quê o projeto faz, por que existe (problema), a arquitetura (diagrama), como rodar (comandos) e o que você aprendeu.
   :::
3. Por que "poucos projetos bons" vence "muitos projetos rasos"?
   :::{dropdown} Resposta
   O avaliador procura profundidade e cuidado (testes, estrutura, docs, CI), não volume; projetos completos demonstram maturidade de engenharia.
   :::
4. Como deve ser um bullet de currículo de dados?
   :::{dropdown} Resposta
   O que você fez + com que ferramenta + qual o resultado (com número quando houver), alinhado às palavras-chave da vaga — não uma lista de siglas.
   :::
5. Qual o papel do LinkedIn, diferente do currículo?
   :::{dropdown} Resposta
   Ser encontrável (headline com cargo e stacks), mostrar seu trabalho (build in public) e permitir networking — não repetir o currículo.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Me conta sobre um projeto de dados que você construiu."
  :::{dropdown} Resposta modelo
  Estruturo em: problema de negócio → arquitetura (ingestão, transformação com dbt, orquestração com Airflow, DW dimensional) → decisões e trade-offs (por que ELT, por que star schema) → resultado e o que eu faria diferente. Aponto o repo com README e diagrama. O segredo é contar como engenheiro: decisões justificadas, não só "usei tal ferramenta".
  :::
- **P:** "Você não tem experiência formal na área. Por que devemos te considerar?"
  :::{dropdown} Resposta modelo
  Mostro o portfólio: pipelines de ponta a ponta versionados, com testes e CI, sobre dados reais — o mesmo tipo de trabalho da vaga, feito publicamente. Trato a migração como vantagem (trago contexto de negócio) e demonstro que já trabalho com as práticas de engenharia que vocês esperam.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (o papel e as competências do DE).
- **Beauchemin — The Rise of the Data Engineer** (a disciplina como engenharia de software).
- **Chacon & Straub — Pro Git** (dominar Git/GitHub, base do portfólio).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — papel e competências do DE. <!-- @reis2022 -->
- Beauchemin, M. *The Rise of the Data Engineer* (2017) — a disciplina como engenharia. <!-- @beauchemin2017 -->
- Chacon, S.; Straub, B. *Pro Git* (2014) — Git/GitHub para o portfólio. <!-- @chacon2014 -->

*Acessado em: 2026-08-30.*

---
**Revisado em:** 2026-08-30
