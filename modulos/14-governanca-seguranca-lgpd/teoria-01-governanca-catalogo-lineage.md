# Governança de dados: catálogo, lineage e ownership

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Numa empresa com centenas de tabelas, surgem perguntas simples e sem resposta: "que tabela uso
para receita?", "de onde vem esse número?", "posso confiar nela?", "quem é o dono?". Sem
**governança**, o data warehouse vira um labirinto onde ninguém confia em nada. Governança é o
conjunto de práticas que torna os dados **encontráveis, compreensíveis, confiáveis e
responsabilizados** — o que faz uma plataforma de dados **escalar** para muitas pessoas.

## 💡 Conceito (o porquê)

### Catálogo de dados
Um **catálogo** é o "índice" dos dados da empresa: quais datasets existem, o que cada tabela/
coluna significa (descrições), tags, e como encontrá-los (busca). Sem catálogo, o conhecimento
é **tribal** ("pergunta pra fulano"). Ferramentas: DataHub, Amundsen, Unity Catalog — mas o
`dbt docs` (M7) já é um catálogo do seu projeto.

### Glossário de negócio
Um **glossário** define os **termos** de negócio ("o que é um 'cliente ativo'?", "como
calculamos 'receita líquida'?") e os liga às tabelas/métricas. Alinha times e evita que cada
área calcule "receita" de um jeito.

### Lineage (linhagem)
**Lineage** é o mapa de **de onde vem** e **para onde vai** cada dado — o grafo fonte → staging
→ marts → dashboard (o DAG do dbt/Airflow, M7/M9). Serve para:
- **Impact analysis:** "se eu mudar esta tabela, o que quebra a jusante?"
- **Root cause:** "este número está errado — subindo o lineage, onde nasceu o problema?"

### Ownership (dono)
Cada dataset precisa de um **dono** (pessoa/time) responsável por sua qualidade, documentação e
suporte. Sem ownership, um dado quebrado é "problema de todo mundo" (ou seja, de ninguém). O
dono responde por SLAs, contratos (M12) e mudanças.

### Governança federada
Em escala (data mesh), a governança é **federada**: um padrão central (nomes, qualidade,
segurança) + **ownership distribuído** por domínio (cada time é dono dos seus dados como
"produtos de dados"). Equilibra padronização com autonomia.

## 🔎 Exemplo
Um analista precisa de "receita por região". No **catálogo**, busca "receita" e acha
`marts.fato_vendas` com descrição e **dono** (time de Vendas). O **glossário** confirma a
definição de receita. O **lineage** mostra que ela vem de `stg_pedidos` ← `raw.pedidos`. Se o
número parecer errado, ele sobe o lineage até a origem; se quiser mudar a tabela, o impact
analysis mostra os 3 dashboards afetados.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley tratam **governança** (catálogo, lineage, qualidade, ownership) como fundamento
para dados confiáveis em escala. Dehghani, no **Data Mesh**, propõe governança **federada** com
dados tratados como **produtos** de propriedade dos domínios. — *Fundamentals of Data
Engineering*; *Data Mesh Principles*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
`dbt docs` gera catálogo + lineage do seu projeto de graça; empresas maiores somam DataHub/
Amundsen/Unity Catalog. Ownership explícito (um time dono de cada dataset) é o que faz a
qualidade ter responsável — sem dono, ninguém conserta. — Reis & Housley.
:::

## ⚠️ Erros comuns
- **Sem catálogo/glossário** — conhecimento tribal; cada um reinventa (e diverge) as métricas.
- **Sem lineage** — impossível fazer impact analysis ou achar a causa de um número errado.
- **Sem dono** — dado quebrado vira problema de ninguém.
- Documentar uma vez e **deixar apodrecer** — catálogo desatualizado engana.
- Governança **centralizada demais** vira gargalo; distribua ownership (federada).

## 💼 O que o mercado espera
Saber o que é catálogo, glossário, lineage e ownership — e por que importam em escala — é
esperado. "Como você faria impact analysis?" e "quem é responsável por um dataset?" aparecem em
entrevistas de níveis pleno/sênior.

:::{admonition} ✨ Em resumo
:class: resumo
- **Governança** torna os dados encontráveis, compreensíveis, confiáveis e **responsabilizados**.
- **Catálogo** (índice + descrições) e **glossário** (termos de negócio) combatem o conhecimento tribal.
- **Lineage** (de onde vem / para onde vai) habilita **impact analysis** e **root cause**.
- **Ownership**: cada dataset tem um dono; em escala, governança **federada** por domínio (data mesh).
:::

## 🧠 Quiz de recall
1. Para que serve um catálogo de dados?
   :::{dropdown} Resposta
   Ser o índice dos datasets (o que existe, o que significa, como achar), combatendo o conhecimento tribal.
   :::
2. O que é lineage e para que serve?
   :::{dropdown} Resposta
   O mapa de origem→destino de cada dado; serve para impact analysis (o que quebra se eu mudar) e root cause (onde nasceu um erro).
   :::
3. Por que ownership importa?
   :::{dropdown} Resposta
   Sem um dono responsável, dado quebrado é problema de ninguém; o dono responde por qualidade, docs, SLAs e mudanças.
   :::
4. O que é um glossário de negócio?
   :::{dropdown} Resposta
   A definição dos termos de negócio (ex.: "cliente ativo", "receita líquida") ligada às tabelas/métricas, para alinhar times.
   :::
5. O que é governança federada?
   :::{dropdown} Resposta
   Um padrão central + ownership distribuído por domínio (data mesh): dados como produtos, cada time dono dos seus, equilibrando padronização e autonomia.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você faria impact analysis antes de mudar uma tabela?"
  :::{dropdown} Resposta modelo
  Consulto o lineage (o DAG de dbt/Airflow ou o catálogo) para ver tudo a jusante — models, dashboards, jobs — que dependem dela. Aviso os donos, ajusto/testo e uso o CI (M13) para pegar quebras. Sem lineage, seria adivinhação.
  :::
- **P:** "Como garantir que as métricas não divergem entre áreas?"
  :::{dropdown} Resposta modelo
  Glossário de negócio com a definição única de cada métrica, ligada a models certificados no dbt (uma fonte da verdade), catálogo para achá-los e ownership claro. Assim "receita" é calculada num só lugar e reutilizada.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (governança, catálogo, lineage).
- **Dehghani — Data Mesh Principles** (governança federada, dados como produto).
- **dbt docs** — catálogo e lineage do seu projeto.

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — governança de dados. <!-- @reis2022 -->
- Dehghani, Z. *Data Mesh Principles and Logical Architecture* (2020) — governança federada. <!-- @dehghani2020 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — proveniência/derivação de dados. <!-- @kleppmann2017 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
