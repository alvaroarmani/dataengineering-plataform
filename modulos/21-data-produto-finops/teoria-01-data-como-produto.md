# Data como produto: pensar o dado como um produto

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você já sabe construir pipelines, warehouses e transformações. Mas uma tabela tecnicamente perfeita
que **ninguém confia, ninguém acha e ninguém sabe usar** não gera valor nenhum. O maior desperdício em
plataformas de dados não é código ruim — é dado que **existe mas não é usado**, porque não tem dono,
documentação, ou garantia de qualidade. A resposta que a indústria encontrou é uma mudança de
mentalidade: parar de tratar dado como um **subproduto** de pipelines e passar a tratá-lo como um
**produto** — com clientes, dono, SLA e qualidade garantida. Este é o conceito central do **Data Mesh**
e uma competência que separa quem "faz ETL" de quem **entrega valor de dados**.

## 💡 Conceito (o porquê)

### O que é um "data product"
Um **data product** é um dataset (ou conjunto de dados) tratado com o mesmo cuidado de um produto de
software: tem **usuários** (os consumidores — analistas, times, modelos), um **dono** responsável, e
promessas explícitas de qualidade e disponibilidade. Não é "a tabela que sobrou do pipeline"; é algo
**projetado para ser consumido**, mantido e evoluído.

### As qualidades de um bom data product (DATSIS)
Um data product maduro é:
- **Descobrível (Discoverable):** aparece no catálogo (M14); as pessoas o **encontram**.
- **Endereçável (Addressable):** tem um local/nome estável para acessar.
- **Confiável (Trustworthy):** tem qualidade garantida por testes e um SLA — o consumidor **confia** nele.
- **Auto-descritivo (Self-describing):** documentação, esquema e significado claros — dá para usar sem "perguntar pra alguém".
- **Interoperável (Interoperable):** segue padrões (nomes, formatos) que permitem combiná-lo com outros.
- **Seguro (Secure):** acesso controlado e conforme (M14).

Repare que isso reúne tudo que você já viu — catálogo/lineage (M14), qualidade/testes (M12), contratos
(M12) — sob uma **lente de produto**.

### Dono e ciclo de vida
Todo data product tem um **dono** (pessoa ou time) responsável por sua qualidade, documentação, suporte
e evolução (a governança federada do M14). E, como um produto de software, tem um **ciclo de vida**:
é lançado (com versão), evolui de forma compatível, é **deprecado** com aviso e aposentado — nunca
simplesmente "some" e quebra quem dependia dele. Mudanças respeitam **contratos de dados** (M12).

### SLA e SLO: a promessa explícita
O que torna um dado "confiável" não é fé — é uma **promessa mensurável**:
- **SLO (objetivo):** a meta interna (ex.: "atualizado até as 8h em 99,9% dos dias"; "0 valores nulos
  na chave").
- **SLA (acordo):** o compromisso com o consumidor, muitas vezes com consequência se quebrado.

Dimensões típicas: **frescor** (freshness — quão recente), **disponibilidade** (uptime), **completude**
e **acurácia**. Um data product declara essas garantias e as **monitora** (M12) — assim o consumidor
sabe exatamente com o que pode contar.

### Data Mesh: produtos donos por domínio
O **Data Mesh** (Dehghani) leva isso ao extremo organizacional: em vez de um time central de dados
virar gargalo, **cada domínio de negócio** (vendas, logística, marketing) é **dono dos seus dados como
produtos**, publicados para o resto da empresa consumir. Uma **plataforma de autosserviço** dá as
ferramentas comuns, e uma **governança federada** define padrões globais. É a mesma ideia de ownership
distribuído do M14, agora como princípio de arquitetura.

## 🔎 Exemplo
O time de Vendas passa a tratar `fato_vendas` como um **data product**: tem um **dono** (o próprio time),
está no **catálogo** com documentação e lineage (M14), tem **testes** de qualidade no CI (M12/M13), e
declara um **SLA** ("atualizado até 8h, 99,9% dos dias; chave sem nulos"). Quando precisam mudar o
esquema, seguem o **contrato de dados** e avisam os consumidores com antecedência — nada quebra. Outros
times **descobrem e confiam** no produto sem perguntar a ninguém. A mesma tabela de antes, agora com
dono, promessa e cuidado de produto — e por isso **usada**.

:::{admonition} 📖 Da literatura
:class: seealso
Dehghani define o **dado como produto** como um dos quatro princípios do **Data Mesh**, com ownership
por domínio e as qualidades DATSIS. Reis & Housley situam a entrega de **valor** e o pensamento de
produto entre as responsabilidades do engenheiro de dados moderno. — *Data Mesh Principles*;
*Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Empresas que adotam "data as a product" reduzem o desperdício de datasets órfãos: cada produto tem dono,
SLA e docs, então é encontrado, confiado e reutilizado — em vez de cada time reconstruir a mesma métrica.
O maior obstáculo raramente é técnico; é **organizacional** (definir donos e responsabilidades). — 
Dehghani; Reis & Housley.
:::

## ⚠️ Erros comuns
- **Dado como subproduto** — "a tabela que sobrou", sem dono, docs nem SLA → ninguém usa.
- **Confiança sem garantia** — prometer qualidade sem SLO/monitoramento que a comprove.
- **Quebrar consumidores** — mudar esquema/semântica sem contrato nem aviso (deprecação).
- **Achar que é só tecnologia** — data product é também ownership e processo (o difícil é organizacional).
- **Data Mesh como bala de prata** — em empresas pequenas, um time central ainda faz mais sentido.

## 💼 O que o mercado espera
Entender o dado como produto (dono, SLA/SLO, DATSIS, ciclo de vida) e o Data Mesh, ligando isso a
catálogo/qualidade/contratos (M12/M14). É linguagem de times de dados maduros e aparece em entrevistas
de pleno/sênior e de liderança.

:::{admonition} ✨ Em resumo
:class: resumo
- **Data product**: dado tratado como produto — com **usuários, dono, SLA e qualidade** garantida.
- Qualidades **DATSIS**: descobrível, endereçável, confiável, auto-descritivo, interoperável, seguro.
- **SLO/SLA** tornam a confiança **mensurável** (frescor, disponibilidade, completude) e monitorada (M12).
- **Data Mesh**: cada domínio é **dono dos seus dados como produtos**, com plataforma de autosserviço e governança federada.
:::

## 🧠 Quiz de recall
1. O que diferencia um "data product" de uma tabela qualquer?
   :::{dropdown} Resposta
   É tratado como produto: tem usuários, dono responsável, documentação, e promessas explícitas de qualidade e disponibilidade (SLA) — projetado para ser consumido e mantido.
   :::
2. Cite três qualidades DATSIS de um bom data product.
   :::{dropdown} Resposta
   Descobrível (no catálogo), confiável (qualidade/SLA), auto-descritivo (documentado) — também endereçável, interoperável e seguro.
   :::
3. Qual a diferença entre SLO e SLA?
   :::{dropdown} Resposta
   SLO é o objetivo interno (meta mensurável, ex.: atualizado até 8h em 99,9% dos dias); SLA é o acordo/compromisso com o consumidor, muitas vezes com consequência se quebrado.
   :::
4. O que o ciclo de vida de um data product implica?
   :::{dropdown} Resposta
   Ele é versionado, evolui de forma compatível (contratos de dados), e é deprecado com aviso — nunca some quebrando quem dependia dele.
   :::
5. O que o Data Mesh propõe sobre ownership?
   :::{dropdown} Resposta
   Que cada domínio de negócio seja dono dos seus dados como produtos, com plataforma de autosserviço e governança federada — em vez de um time central gargalo.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "O que significa tratar dado como produto?"
  :::{dropdown} Resposta modelo
  Dar ao dataset o cuidado de um produto: um dono responsável, usuários claros, documentação e esquema (auto-descritivo), presença no catálogo (descobrível) e uma promessa mensurável de qualidade/disponibilidade (SLA/SLO) monitorada. Mudanças respeitam contratos e deprecação. O efeito é que o dado é encontrado, confiado e reutilizado em vez de virar tabela órfã.
  :::
- **P:** "Quando o Data Mesh faz sentido e quando não?"
  :::{dropdown} Resposta modelo
  Faz sentido em organizações grandes onde um time central de dados vira gargalo e há domínios com conhecimento próprio: distribuir ownership por domínio (dados como produto) com plataforma comum e governança federada escala melhor. Em empresas menores, um time central ainda é mais simples e eficiente — Data Mesh adiciona overhead organizacional que só se paga na escala certa.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Dehghani — Data Mesh Principles** (dado como produto, ownership por domínio).
- **Reis & Housley — Fundamentals of Data Engineering** (entrega de valor e pensamento de produto).
- **Beauchemin — The Rise of the Data Engineer** (a disciplina e sua responsabilidade de valor).

## 📚 Referências
- Dehghani, Z. *Data Mesh Principles and Logical Architecture* (2020) — dado como produto. <!-- @dehghani2020 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — valor e produto de dados. <!-- @reis2022 -->
- Beauchemin, M. *The Rise of the Data Engineer* (2017) — a disciplina e o valor. <!-- @beauchemin2017 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
