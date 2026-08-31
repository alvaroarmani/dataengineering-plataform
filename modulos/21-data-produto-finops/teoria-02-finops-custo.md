# FinOps: o custo dos dados como responsabilidade de engenharia

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Na nuvem (M20), cada consulta, cada byte guardado e cada cluster ligado **vira dinheiro** — e a conta
chega no fim do mês, muitas vezes assustando. É comum uma única consulta mal escrita varrer terabytes e
custar centenas de reais, um cluster esquecido rodar 24/7 sem uso, ou dados frios apodrecerem em storage
caro. O engenheiro de dados que ignora custo entrega pipelines que **funcionam mas quebram o orçamento**.
**FinOps** (Finanças + DevOps) é a prática de tratar o **custo como uma métrica de engenharia** — tão
importante quanto performance ou qualidade. Saber estimar, atribuir e otimizar o custo de dados é uma
competência cada vez mais exigida.

## 💡 Conceito (o porquê)

### O custo é dirigido pelo uso (pay-per-use)
Na nuvem você paga pelo que consome, e os principais motores de custo em dados são:
- **Armazenamento:** por GB/mês, e varia por **classe** (quente/frio/arquivo — dados raramente acessados
  devem ir para classes mais baratas).
- **Computação/consulta:** por tempo de cluster ligado (Spark) ou por **bytes varridos** (BigQuery). Uma
  consulta que lê a tabela inteira custa muito mais que uma que lê uma partição.
- **Transferência de dados (egress):** mover dados **para fora** da nuvem/região custa — às vezes caro.
- **Requisições e operações:** cada chamada de API a um serviço tem preço (pequeno, mas escala).

Entender **o que dirige a fatura** é o primeiro passo para controlá-la.

### As alavancas de otimização (que você já conhece)
Boa parte da economia vem de técnicas que você aprendeu por **performance** — e que são, na verdade,
**redução de custo**:
- **Particionamento e clustering** (M06): a consulta lê só a fração relevante → menos bytes varridos →
  menos custo. Ler 10% em vez de 100% economiza ~90%.
- **Formato colunar (Parquet)** (M06/M11): lê só as colunas necessárias, comprimido → menos I/O e storage.
- **Classes de armazenamento:** mover dados frios para storage barato; deletar o que não serve mais
  (retenção, M14).
- **Right-sizing e autoscaling:** dimensionar clusters ao necessário e desligar o ocioso (o HPA do M20
  aplicado a custo).
- **Materializar com parcimônia:** cachear/pré-agregar o que é consultado muito; não recomputar tudo sempre.

### Visibilidade: você não controla o que não mede
FinOps começa por **enxergar** o gasto:
- **Tags/labels** em cada recurso (por time, projeto, ambiente) permitem **atribuir** o custo a quem o gera.
- **Orçamentos e alertas** avisam antes de estourar (ex.: "alertar se o projeto passar de X no mês").
- **Chargeback/showback:** mostrar a cada time quanto ele gasta cria responsabilidade (accountability).

Sem atribuição, o custo é "de todo mundo" — ou seja, de ninguém (o mesmo problema de ownership do M14).

### Custo é um trade-off, não só "gastar menos"
FinOps **não** é cortar custo cegamente — é **otimizar valor por real gasto**. Às vezes vale pagar mais
por mais frescor ou disponibilidade (se o negócio precisa); às vezes um dado pode ser diário em vez de
tempo real, cortando muito custo sem perda relevante. A decisão é **econômica**: o custo entra na
arquitetura como um requisito, ao lado de latência e qualidade (M15, system design).

## 🔎 Exemplo
Um dashboard executivo roda uma consulta que varre a tabela inteira de eventos (5 TB) a cada
atualização, várias vezes ao dia — uma fatura silenciosa de milhares por mês. O time aplica FinOps:
**particiona** a tabela por data (a consulta passa a ler só o dia → ~1% dos bytes), converte para
**Parquet**, e move os dados com mais de 1 ano para **storage frio**. Coloca **tags** por time e um
**alerta de orçamento**. Resultado: a mesma resposta de negócio por uma fração do custo — e agora o gasto
é **visível e atribuído**. Nenhuma mágica: as técnicas de performance do curso, aplicadas com a lente de custo.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley colocam o **custo (FinOps)** entre as *undercurrents* da engenharia de dados, defendendo
que o engenheiro considere o custo em cada decisão de arquitetura — e que otimizações de armazenamento
(particionamento, colunar) são também decisões financeiras. — *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A "fatura surpresa" da nuvem é tão comum que FinOps virou disciplina própria, com times dedicados em
grandes empresas. Mas a maior parte da economia vem de hábitos de engenharia simples: particionar,
usar colunar, desligar o ocioso, mover dados frios e **medir** o gasto com tags e alertas — coisas que o
engenheiro de dados controla diretamente. — Reis & Housley.
:::

## ⚠️ Erros comuns
- **Consulta que varre tudo** — ignora particionamento/colunar; a fatura silenciosa mais comum.
- **Cluster/recurso ocioso ligado** — pagar por computação que ninguém usa.
- **Dado frio em storage caro** — nunca mover para classes baratas nem deletar o inútil.
- **Sem tags/orçamento** — custo não atribuído a ninguém, sem alerta antes de estourar.
- **Cortar custo cegamente** — degradar frescor/qualidade que o negócio precisava; FinOps é valor/custo, não só menos gasto.

## 💼 O que o mercado espera
Estimar o custo de consultas/armazenamento, aplicar as alavancas (particionamento, colunar, classes,
right-sizing), e defender visibilidade (tags, orçamentos). "Como você reduziria o custo deste pipeline?"
é pergunta real em entrevistas de pleno/sênior.

:::{admonition} ✨ Em resumo
:class: resumo
- **FinOps** = tratar **custo como métrica de engenharia**; na nuvem, tudo é pay-per-use.
- Motores de custo: **armazenamento** (classe), **computação/bytes varridos**, **egress**, requisições.
- Alavancas (já conhecidas): **particionar/clustering**, **Parquet**, classes frias, **right-sizing/autoscaling**.
- **Visibilidade** (tags, orçamentos, chargeback) atribui o custo; a meta é **valor por real**, não cortar cego.
:::

## 🧠 Quiz de recall
1. Quais são os principais motores de custo em dados na nuvem?
   :::{dropdown} Resposta
   Armazenamento (por GB/mês e classe), computação/consulta (tempo de cluster ou bytes varridos), transferência de dados (egress) e requisições/operações.
   :::
2. Por que particionar economiza dinheiro, não só tempo?
   :::{dropdown} Resposta
   Porque o custo é por bytes varridos; particionar faz a consulta ler só a fração relevante — ler 10% em vez de 100% economiza ~90% do custo daquela consulta.
   :::
3. Como se dá visibilidade ao custo?
   :::{dropdown} Resposta
   Com tags/labels por time/projeto (atribuição), orçamentos e alertas (aviso antes de estourar) e chargeback/showback (mostrar a cada time seu gasto).
   :::
4. FinOps é cortar custo ao máximo?
   :::{dropdown} Resposta
   Não; é otimizar valor por real gasto. Às vezes vale pagar mais por frescor/disponibilidade que o negócio exige; às vezes reduzir frescor corta custo sem perda relevante.
   :::
5. Cite três alavancas de otimização de custo que você já conhecia por performance.
   :::{dropdown} Resposta
   Particionamento/clustering, formato colunar (Parquet) e right-sizing/autoscaling (desligar o ocioso); também mover dados frios para classes baratas.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Este pipeline custa caro demais. Como você reduziria a fatura?"
  :::{dropdown} Resposta modelo
  Primeiro meço onde o dinheiro vai (tags, análise de custo por consulta/recurso). Depois ataco os motores: particiono e uso colunar para varrer menos bytes, movo dados frios para storage barato e deleto o inútil (retenção), faço right-sizing e desligo recursos ociosos, e materializo/pré-agrego o que é muito consultado. Ponho orçamentos e alertas. Sempre pesando valor: não degrado frescor que o negócio precisa só para cortar custo.
  :::
- **P:** "Por que custo é responsabilidade do engenheiro de dados, e não só do financeiro?"
  :::{dropdown} Resposta modelo
  Porque as decisões que dirigem a fatura são de engenharia: como a consulta varre os dados, o formato, o particionamento, o tamanho e o tempo de vida dos clusters, a classe de storage. O financeiro não pode otimizar isso — o engenheiro sim. Tratar custo como métrica de primeira classe (FinOps), com visibilidade e ownership, é parte de entregar valor, não só código que funciona.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (custo/FinOps como *undercurrent*).
- **Documentação de billing/cost de AWS/GCP/Azure** — orçamentos, tags e análise de custo.
- **FinOps Foundation** — princípios e práticas de FinOps.

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — FinOps e custo. <!-- @reis2022 -->
- Dehghani, Z. *Data Mesh Principles and Logical Architecture* (2020) — plataforma e custo. <!-- @dehghani2020 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — trade-offs de armazenamento/computação. <!-- @kleppmann2017 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
