# A entrevista técnica: SQL ao vivo e case de modelagem dimensional

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Currículo aprovado, agora vem a **entrevista técnica** — e é aqui que muita gente que "sabe" a
matéria trava. Não porque falte conhecimento, mas porque **resolver ao vivo, explicando o
raciocínio, sob observação** é uma habilidade própria. As duas provas mais comuns para Data
Engineer júnior/pleno são o **SQL ao vivo** (escrever queries num editor compartilhado enquanto
alguém assiste) e o **case de modelagem dimensional** (dado um cenário de negócio, desenhar o
star schema). A boa notícia: ambas seguem **padrões previsíveis** que dá para treinar.

## 💡 Conceito (o porquê)

### SQL ao vivo: pense em voz alta
O entrevistador não quer só a query certa — quer ver **como você pensa**. O erro clássico é
mergulhar em silêncio e escrever SQL torto. O método:
1. **Esclareça** os dados e o pedido ("essas datas têm timezone? pode haver pedido sem cliente?").
2. **Declare o plano** antes de escrever ("vou agrupar por cliente, somar o valor e ordenar").
3. **Escreva incrementalmente** e valide (rode um `SELECT` simples antes do agregado completo).
4. **Trate os casos de borda** (NULLs, duplicatas, empates no `ORDER BY`).

Pensar em voz alta transforma um teste de resposta num **diálogo** — e mesmo que você erre a
sintaxe, o raciocínio correto conta muito.

### O que cai em SQL: os padrões
O núcleo é sempre o mesmo: **JOINs** (e o cuidado com o que um join errado faz ao total),
**GROUP BY + agregações**, **window functions** (`ROW_NUMBER`, `RANK`, `LAG/LEAD`, running totals —
"o 2º maior por categoria", "variação mês a mês"), **CTEs** para quebrar o problema em passos
legíveis, e tratamento de **NULL/duplicatas**. Empates em `ORDER BY` pedem um critério de
desempate determinístico — detalhe que separa quem pensou no caso real.

### Case de modelagem dimensional: do negócio ao star schema
Dado "modele um DW para uma loja online", o roteiro (Kimball) é:
1. **Escolher o processo de negócio** (ex.: vendas).
2. **Definir o grão** ("uma linha por item de pedido") — a decisão mais importante; tudo depende dela.
3. **Identificar as dimensões** (quem/o quê/quando/onde: cliente, produto, data, loja).
4. **Identificar os fatos** (as medidas numéricas: quantidade, valor).

O resultado é uma **tabela fato** cercada de **dimensões** (star schema). Saber justificar o
**grão**, distinguir **fato vs dimensão** e lembrar de **SCD** (dimensões que mudam no tempo, M5)
é o que o entrevistador procura.

### Comunicar trade-offs
Tanto no SQL quanto na modelagem, dizer **por que** você escolheu algo — e o que abriria mão —
sinaliza senioridade: "usei uma CTE para legibilidade; em produção checaria o plano de execução";
"escolhi grão de item para permitir análises por produto, ao custo de mais linhas".

## 🔎 Exemplo
Pergunta de SQL ao vivo: "top 2 produtos por receita em cada categoria". Você pensa em voz alta:
"receita = soma de valor por produto; preciso rankear dentro da categoria → window function
`ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY receita DESC)`; depois filtro `rn <= 2`; uso
uma CTE para o agregado e outra para o rank". Escreve incrementalmente, valida o agregado antes do
rank, e menciona o empate ("se duas receitas empatam, `ROW_NUMBER` escolhe arbitrariamente; se o
negócio quer ambos, uso `RANK`"). Isso é uma resposta de nível pleno.

:::{admonition} 📖 Da literatura
:class: seealso
Tanimura organiza o SQL analítico exatamente em torno dos padrões cobrados: agregações, window
functions e análise temporal. Kimball & Ross fornecem o roteiro de quatro passos (processo → grão
→ dimensões → fatos) que estrutura qualquer case de modelagem. — *SQL for Data Analysis*; *The
Data Warehouse Toolkit*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Em entrevistas de dados, o candidato que **verbaliza o plano e trata bordas** (NULL, duplicata,
empate) costuma passar mesmo cometendo um deslize de sintaxe; o que escreve certo em silêncio, mas
não explica, gera dúvida. A comunicação do raciocínio é avaliada tanto quanto o resultado. — prática
de mercado; Tanimura.
:::

## ⚠️ Erros comuns
- **Codar em silêncio** — o entrevistador não vê seu raciocínio e não pode te ajudar a destravar.
- **Pular o esclarecimento** — resolver a pergunta errada por não checar premissas.
- **Ignorar bordas** — NULLs, duplicatas de join, empates no `ORDER BY`.
- **No case, esquecer o grão** — começar pelas tabelas sem definir "uma linha representa o quê".
- **Confundir fato e dimensão** — pôr medida em dimensão ou atributo descritivo no fato.

## 💼 O que o mercado espera
Escrever SQL analítico (joins, group by, window functions, CTEs) explicando o raciocínio, e conduzir
um case de modelagem pelos quatro passos de Kimball, justificando grão e a separação fato/dimensão.
São as duas provas técnicas mais frequentes para a vaga.

:::{admonition} ✨ Em resumo
:class: resumo
- **SQL ao vivo é diálogo**: esclareça → planeje → escreva incremental → trate bordas, pensando em voz alta.
- **Padrões que caem**: joins, group by, **window functions**, CTEs, NULL/duplicata/empate.
- **Case de modelagem (Kimball)**: processo → **grão** → dimensões → fatos = star schema.
- **Comunicar trade-offs** sinaliza senioridade em ambas as provas.
:::

## 🧠 Quiz de recall
1. Por que "pensar em voz alta" importa no SQL ao vivo?
   :::{dropdown} Resposta
   Porque o entrevistador avalia o raciocínio, não só a resposta; verbalizar transforma o teste em diálogo e permite crédito mesmo com deslizes de sintaxe.
   :::
2. Cite três padrões de SQL que costumam cair.
   :::{dropdown} Resposta
   JOINs, GROUP BY + agregações, e window functions (ROW_NUMBER/RANK/LAG-LEAD); também CTEs e tratamento de NULL/duplicata.
   :::
3. Quais são os quatro passos do case de modelagem dimensional (Kimball)?
   :::{dropdown} Resposta
   Escolher o processo de negócio → definir o grão → identificar as dimensões → identificar os fatos.
   :::
4. Por que o grão é a decisão mais importante do modelo?
   :::{dropdown} Resposta
   Porque define o que uma linha da fato representa; dimensões, medidas e o nível de detalhe das análises dependem dele.
   :::
5. Como tratar empate num `ORDER BY` de ranking?
   :::{dropdown} Resposta
   Adicionar um critério de desempate determinístico; e escolher entre ROW_NUMBER (um por posição) e RANK (mantém empatados) conforme o negócio.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Escreva a query do 2º maior salário por departamento." (como você conduz?)
  :::{dropdown} Resposta modelo
  Esclareço (pode haver empate? contar ou pular?). Planejo: rankear salários dentro do departamento e filtrar a 2ª posição. Uso `DENSE_RANK() OVER (PARTITION BY depto ORDER BY salario DESC)` numa CTE e filtro `= 2`. Explico por que DENSE_RANK (trata empates como mesma posição) e valido incrementalmente. Menciono NULLs em salário.
  :::
- **P:** "Modele um DW para uma rede de cinemas."
  :::{dropdown} Resposta modelo
  Sigo Kimball: processo = venda de ingressos; grão = uma linha por ingresso vendido; dimensões = filme, sessão/data-hora, sala/cinema, cliente, canal; fatos = valor, quantidade. Justifico o grão (permite análise por filme, sala e horário) e comento SCD (ex.: preço da sala mudando no tempo → dimensão com histórico). Fecho com o star schema.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Tanimura — SQL for Data Analysis** (window functions e padrões analíticos).
- **Kimball & Ross — The Data Warehouse Toolkit** (o roteiro de modelagem dimensional).
- **Reis & Housley — Fundamentals of Data Engineering** (queries e serving de dados).

## 📚 Referências
- Tanimura, C. *SQL for Data Analysis* (2021) — window functions, análise temporal. <!-- @tanimura2021 -->
- Kimball, R.; Ross, M. *The Data Warehouse Toolkit* (2013) — modelagem dimensional. <!-- @kimball2013 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — queries e serving. <!-- @reis2022 -->

*Acessado em: 2026-08-30.*

---
**Revisado em:** 2026-08-30
