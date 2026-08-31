# Valor, ROI e as métricas que provam o impacto dos dados

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Times de dados são caros — pessoas, nuvem, ferramentas — e cedo ou tarde alguém pergunta: **"isso está
valendo a pena?"**. Engenheiros que só falam em pipelines e tecnologia não sabem responder; e projetos
de dados que não demonstram valor são os primeiros a serem cortados. Saber **conectar o trabalho de
dados ao valor de negócio** — estimar retorno, medir impacto, comunicar em linguagem de ROI e TCO — é o
que faz um engenheiro crescer para pleno/sênior e liderança. Esta unidade fecha o módulo (e o eixo)
mostrando como pensar e provar o **valor** dos dados.

## 💡 Conceito (o porquê)

### O dado só vale pelo que ele muda
Um dataset não tem valor intrínseco — vale pela **decisão que ele melhora** ou pela **ação que ele
habilita**. Um pipeline lindo que ninguém usa vale zero; uma tabela simples que corta 2 horas de
trabalho manual por dia de dez analistas vale muito. A pergunta que orienta tudo: **que decisão de
negócio este dado apoia, e quanto isso vale?** Valor de dados costuma aparecer como: **receita** (mais
vendas, melhor preço), **economia** (menos trabalho manual, menos custo), **risco evitado** (fraude,
compliance) ou **velocidade** (decidir mais rápido).

### ROI: retorno sobre o investimento
O **ROI** mede o retorno de um projeto relativo ao que se investiu:
$$\text{ROI} = \frac{\text{retorno} - \text{investimento}}{\text{investimento}}$$
Um ROI de 2,0 significa 200% — para cada real investido, dois de retorno líquido. É a linguagem que a
liderança entende: um projeto de dados justificado por "vai economizar R$ 400k/ano custando R$ 100k" (ROI
= 3,0) tem prioridade sobre um justificado por "é uma tecnologia legal".

### TCO: o custo total, não só o inicial
Ao avaliar uma solução, o erro é olhar só o **custo inicial**. O **TCO (Total Cost of Ownership)** soma
tudo ao longo da vida:
$$\text{TCO} = \text{custo inicial} + \text{custo recorrente} \times \text{período}$$
Inclui nuvem mensal (M20), manutenção, licenças e o **tempo das pessoas** para operar. Uma ferramenta
"grátis" que exige um engenheiro em tempo integral para manter pode ter TCO maior que uma paga e
gerenciada. Comparar opções pelo TCO — não pelo preço de etiqueta — é decisão de engenharia madura.

### Métricas do próprio pipeline (as que você controla)
Além do valor de negócio, um data product tem métricas operacionais que você monitora (M12) e que
sustentam sua confiabilidade — e o SLA (unidade 1):
- **Frescor (freshness):** quão recente é o dado (atraso desde a fonte).
- **Disponibilidade (uptime):** % do tempo em que está acessível e no SLA.
- **Qualidade:** taxa de testes passando, % de nulos/duplicatas, violações de contrato.
- **Adoção/uso:** quantos consomem o produto — a métrica que revela se ele **gera valor** (produto sem
  usuários é candidato a aposentar).

### Comunicar valor: a habilidade que destrava a carreira
De nada adianta gerar valor e não saber mostrá-lo. Traduza o técnico para o de negócio: em vez de
"otimizei a partição e reduzi bytes varridos", diga "cortei R$ 8k/mês da fatura e o relatório agora sai
às 7h em vez das 10h". Ligue cada entrega a **receita, economia, risco ou velocidade**. Essa tradução —
do pipeline ao impacto — é o que diferencia o engenheiro que executa do que **influencia decisões**.

## 🔎 Exemplo
Um time propõe automatizar um relatório manual. Em vez de "vamos usar dbt e Airflow", constroem o caso
de valor: hoje três analistas gastam 6h/semana montando o relatório à mão (≈ R$ 90k/ano) e ele sai
atrasado. O projeto custa R$ 30k para construir + R$ 5k/ano de nuvem — **TCO de ~R$ 45k no primeiro ano**,
**ROI ≈ 1,0 já no ano 1** e crescente depois. Aprovado. Entregue, medem o **valor**: 0 horas manuais,
frescor de 1h, 100% de testes passando, e 12 áreas consumindo o produto. Comunicam à liderança em
reais e horas — não em nomes de ferramentas. O trabalho técnico virou **impacto provado**.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley enfatizam que o engenheiro de dados moderno pensa em **valor de negócio** e custo, não só
em tecnologia. Beauchemin, ao descrever a ascensão (e as armadilhas) do papel, alerta que times de dados
precisam demonstrar impacto para não virarem centros de custo invisíveis. — *Fundamentals of Data
Engineering*; *The Rise of the Data Engineer*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Projetos de dados que não conseguem articular seu valor são os primeiros cortados quando o orçamento
aperta. Os times que prosperam são os que ligam cada entrega a um número de negócio (receita, custo,
risco, tempo) e medem a **adoção** dos seus produtos. Comunicar valor em linguagem de negócio é tão
determinante para a carreira quanto a competência técnica. — Beauchemin; Reis & Housley.
:::

## ⚠️ Erros comuns
- **Valor intrínseco** — achar que o dado vale por existir, sem ligar a uma decisão/ação de negócio.
- **Olhar só o custo inicial** — ignorar o TCO (recorrente + tempo das pessoas).
- **Não medir adoção** — manter produtos que ninguém usa; nunca aposentar.
- **Comunicar em jargão técnico** — falar de partições e DAGs para quem quer ouvir reais e horas.
- **Prometer ROI sem base** — números inventados; estime com premissas explícitas e verificáveis.

## 💼 O que o mercado espera
Justificar projetos por **ROI/TCO**, medir valor (adoção, economia, frescor) e **comunicar impacto** em
linguagem de negócio. É o que separa o executor do profissional que influencia decisões — e é esperado
já no pleno, essencial no sênior/liderança.

:::{admonition} ✨ Em resumo
:class: resumo
- O dado vale pela **decisão que melhora / ação que habilita** — receita, economia, risco evitado, velocidade.
- **ROI** = (retorno − investimento) / investimento; a linguagem que justifica projetos à liderança.
- **TCO** = inicial + recorrente × período — compare opções pelo custo total (incl. tempo das pessoas), não pelo preço de etiqueta.
- Meça **frescor, disponibilidade, qualidade e adoção**; e **comunique valor** em reais/horas, não em jargão.
:::

## 🧠 Quiz de recall
1. De onde vem o valor de um dataset?
   :::{dropdown} Resposta
   Da decisão que ele melhora ou da ação que habilita — receita, economia, risco evitado ou velocidade. Um dado que ninguém usa vale zero.
   :::
2. Como se calcula o ROI e o que ele comunica?
   :::{dropdown} Resposta
   ROI = (retorno − investimento) / investimento. Comunica o retorno relativo em linguagem que a liderança entende (ex.: 2,0 = 200% de retorno líquido).
   :::
3. O que o TCO inclui além do custo inicial?
   :::{dropdown} Resposta
   Custos recorrentes ao longo da vida: nuvem mensal, manutenção, licenças e o tempo das pessoas para operar. Uma opção "grátis" pode ter TCO alto.
   :::
4. Por que medir a adoção de um data product?
   :::{dropdown} Resposta
   Porque adoção revela se ele gera valor; um produto sem usuários é candidato a ser aposentado, mesmo que tecnicamente perfeito.
   :::
5. Como comunicar valor à liderança?
   :::{dropdown} Resposta
   Traduzindo o técnico para o de negócio: reais economizados, horas poupadas, risco evitado, decisões mais rápidas — não nomes de ferramentas ou detalhes de pipeline.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você justificaria um projeto de dados para a liderança?"
  :::{dropdown} Resposta modelo
  Construo o caso de valor: qual decisão/ação de negócio ele melhora e quanto isso vale (receita, economia, risco, tempo). Estimo o ROI = (retorno − investimento)/investimento com premissas explícitas, e comparo opções pelo TCO (inicial + recorrente + tempo das pessoas), não só pelo preço. Apresento em reais e horas, não em jargão. Depois de entregue, meço o valor real (economia, adoção, frescor) para provar o impacto.
  :::
- **P:** "Um data product tem qualidade técnica ótima mas ninguém usa. O que você faz?"
  :::{dropdown} Resposta modelo
  Trato adoção como sinal de valor: investigo por que não é usado — não é descobrível (catálogo/docs), não resolve uma dor real, ou os consumidores não confiam (sem SLA/qualidade visível). Ajusto o que faltar; se, mesmo assim, não há demanda de negócio, considero aposentá-lo com deprecação. Manter produtos sem uso só gera custo e ruído — valor por real também é saber cortar.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (valor de negócio e custo).
- **Beauchemin — The Rise of the Data Engineer** (impacto e as armadilhas do papel).
- **Dehghani — Data Mesh Principles** (produtos de dados e sua adoção).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — valor e custo de dados. <!-- @reis2022 -->
- Beauchemin, M. *The Rise of the Data Engineer* (2017) — impacto do trabalho de dados. <!-- @beauchemin2017 -->
- Dehghani, Z. *Data Mesh Principles and Logical Architecture* (2020) — adoção de produtos de dados. <!-- @dehghani2020 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
