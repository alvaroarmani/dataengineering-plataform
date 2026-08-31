# Rodando dados no Kubernetes: jobs, estado e IaC

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Você entendeu o Kubernetes para **serviços** que ficam no ar (unidade 2). Mas cargas de dados têm
formatos diferentes: um pipeline que **roda e termina** (não fica no ar), um banco que precisa de
**disco persistente e identidade fixa**, um Spark que sobe dezenas de workers temporários. Rodar dados
em k8s exige objetos e cuidados específicos — e saber **quando não vale a pena**. Esta unidade fecha o
módulo mostrando como dados vivem no Kubernetes e como você **provisiona** tudo isso com Infraestrutura
como Código (M13), amarrando cloud + contêineres + IaC.

## 💡 Conceito (o porquê)

### Jobs e CronJobs: cargas que terminam
Nem tudo é um serviço eterno. Um pipeline de ETL **roda até terminar** e para:
- **Job:** roda um pod até a tarefa **completar com sucesso** (com retries se falhar). É o análogo de
  uma task de pipeline — perfeito para um processamento batch pontual.
- **CronJob:** um Job **agendado** (sintaxe cron), como uma DAG diária do Airflow (M09), mas nativo do
  k8s. Ótimo para "rode este ETL toda madrugada".

O modelo é o mesmo: você **declara** o Job; o k8s o executa, tolera falhas e reporta conclusão.

### Estado: StatefulSets e volumes persistentes
Um pod é **efêmero** por padrão — some e leva os dados junto. Isso é ótimo para serviços sem estado,
mas fatal para um **banco de dados**. Para cargas com estado:
- **PersistentVolume (PV) / PersistentVolumeClaim (PVC):** desacoplam o **disco** do pod. O pod pede um
  volume (PVC); o dado **sobrevive** ao pod ser recriado.
- **StatefulSet:** como um Deployment, mas dá a cada pod uma **identidade estável** (nome fixo, disco
  próprio persistente, ordem de criação). É o que bancos e sistemas com estado (Kafka, Cassandra)
  precisam para saber "quem é quem".

Regra prática: **serviço sem estado → Deployment; com estado → StatefulSet + PVC.**

### Airflow e Spark no Kubernetes
As ferramentas do curso rodam nativamente em k8s:
- **Spark on Kubernetes:** cada job Spark sobe um *driver* e vários *executors* como pods **temporários**
  — sobem para o job, somem ao terminar. Elasticidade sem cluster fixo.
- **Airflow no k8s** (KubernetesExecutor): cada task de uma DAG vira um **pod** próprio, isolado e
  escalável. Une a orquestração do M09 com a elasticidade do k8s.

Isso dá **isolamento** (cada carga no seu contêiner), **escala** (mais pods sob demanda) e
**portabilidade** (a mesma stack em qualquer nuvem).

### Provisionar com IaC (Terraform) — fechando o ciclo
Você não cria cluster, nós, storage e serviços clicando no console — isso não é reprodutível nem
auditável (M13). Usa-se **Infraestrutura como Código**: um provedor gerenciado de k8s (GKE/EKS/AKS) e
os recursos de nuvem (buckets, redes, permissões) são declarados em **Terraform** e versionados no Git.
Assim, todo o ambiente — do cluster ao bucket — nasce de código revisável, com `plan`/`apply` (M13). É
a mesma filosofia declarativa do k8s, um nível acima: **IaC provisiona a infra, o k8s orquestra os
contêineres nela.**

### Quando NÃO usar Kubernetes
Kubernetes é poderoso e **complexo**. Ele **não** se justifica quando:
- Você tem poucos contêineres e pouca escala — `docker-compose` (M10) basta.
- Um serverless gerenciado resolve (BigQuery, Cloud Functions, Airflow/Spark gerenciados) com menos operação.
- O time é pequeno e não tem quem opere o cluster — prefira k8s **gerenciado** ou nem isso.

A maturidade é escolher a ferramenta **mais simples** que atende — não a mais impressionante.

## 🔎 Exemplo
Uma empresa provisiona toda a infra com **Terraform** (M13): um cluster **GKE gerenciado**, um bucket de
**object storage** e um Postgres gerenciado, tudo versionado no Git. No cluster, o **Airflow** roda com
KubernetesExecutor — cada task de ETL vira um **pod** isolado; o job noturno é um **CronJob**. Um job
**Spark** sobe executors **temporários** para processar o dia e some ao terminar. O metastore roda como
**StatefulSet** com **PVC** (disco que sobrevive). Resultado: pipelines isolados, elásticos e portáveis,
com a infra inteira nascendo de código — cloud + k8s + IaC costurados.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley defendem infraestrutura **reprodutível via IaC** e o uso de contêineres/orquestração como
padrão operacional do ciclo de vida do dado, sempre pesando a complexidade contra o benefício. Armbrust
et al. mostram plataformas de dados (Lakehouse) construídas sobre esses blocos na nuvem. — *Fundamentals
of Data Engineering*; *Lakehouse*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A combinação vencedora hoje é **IaC (Terraform) + Kubernetes gerenciado + object storage**: a infra
nasce de código revisável, os pipelines rodam isolados e elásticos, e nada depende de cliques manuais. O
erro caro é adotar k8s "porque é moderno" sem escala que o justifique — pagando complexidade sem retorno.
— prática de mercado; Reis & Housley.
:::

## ⚠️ Erros comuns
- **Rodar banco como Deployment** (efêmero) em vez de StatefulSet + PVC — perde os dados ao recriar o pod.
- **Usar Job onde é serviço** (ou vice-versa) — Job termina, Deployment fica no ar; confundir quebra o comportamento.
- **Provisionar clicando no console** em vez de IaC — não reprodutível, não auditável.
- **Adotar k8s sem escala que justifique** — complexidade sem retorno; compose/serverless bastariam.
- **Ignorar persistência/backup do estado** — PVC sem estratégia de backup ainda perde dados num desastre.

## 💼 O que o mercado espera
Saber que pipelines batch viram Jobs/CronJobs, que estado exige StatefulSet + PVC, que Airflow/Spark
rodam em k8s, e que a infra é provisionada com **IaC**. E — importante — **julgar quando k8s não vale**.
Aparece em system design e em vagas de plataformas de dados.

:::{admonition} ✨ Em resumo
:class: resumo
- Cargas que **terminam** → **Job** (batch) e **CronJob** (agendado, como uma DAG); serviços eternos → Deployment.
- **Estado** (bancos, Kafka) → **StatefulSet + PVC/PV** (identidade e disco persistentes); pod é efêmero por padrão.
- **Airflow/Spark em k8s**: tasks/executors viram pods isolados e elásticos, portáveis entre nuvens.
- **IaC (Terraform, M13) provisiona** o cluster e a nuvem; o **k8s orquestra** os contêineres. Use k8s só quando a escala justifica.
:::

## 🧠 Quiz de recall
1. Qual objeto do k8s usar para um ETL que roda e termina, agendado toda madrugada?
   :::{dropdown} Resposta
   Um CronJob (Job agendado): roda um pod até completar, com retries, na hora marcada — como uma DAG diária, nativo do k8s.
   :::
2. Por que um banco de dados não pode ser um Deployment comum?
   :::{dropdown} Resposta
   Porque pods são efêmeros e perdem os dados ao serem recriados. Bancos precisam de StatefulSet (identidade estável) + PVC/PV (disco que sobrevive ao pod).
   :::
3. Como Spark roda no Kubernetes?
   :::{dropdown} Resposta
   Cada job sobe um driver e vários executors como pods temporários, que sobem para o job e somem ao terminar — elasticidade sem cluster fixo.
   :::
4. Qual o papel do Terraform/IaC nesse cenário?
   :::{dropdown} Resposta
   Provisionar a infra (cluster k8s gerenciado, buckets, redes, permissões) como código versionado e auditável, com plan/apply — em vez de cliques no console.
   :::
5. Quando NÃO usar Kubernetes?
   :::{dropdown} Resposta
   Com poucos contêineres/pouca escala (compose basta), quando um serverless gerenciado resolve, ou sem time para operar o cluster. Escolha a ferramenta mais simples que atende.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você rodaria um banco/metastore com estado no Kubernetes?"
  :::{dropdown} Resposta modelo
  Com um StatefulSet, que dá a cada pod identidade estável e disco próprio, mais PersistentVolumeClaims para que os dados sobrevivam à recriação do pod. Defino estratégia de backup do volume, porque PVC sozinho não protege contra desastre. Para serviços sem estado, usaria Deployment; a distinção estado/sem-estado guia a escolha.
  :::
- **P:** "Descreva uma stack de dados moderna amarrando cloud, k8s e IaC."
  :::{dropdown} Resposta modelo
  Terraform provisiona um cluster k8s gerenciado (GKE/EKS/AKS), object storage e bancos gerenciados, tudo versionado. No cluster, Airflow (KubernetesExecutor) roda cada task como pod; jobs batch são Jobs/CronJobs; Spark sobe executors temporários; componentes com estado usam StatefulSet + PVC. Infra como código, pipelines isolados e elásticos, portáveis entre nuvens — e uso serverless onde ele simplifica.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Documentação do Kubernetes** — Jobs, CronJobs, StatefulSets, PersistentVolumes.
- **Reis & Housley — Fundamentals of Data Engineering** (IaC e operação de infraestrutura de dados).
- **Documentação do Terraform** — provisionar clusters gerenciados e recursos de nuvem (M13).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — IaC e orquestração. <!-- @reis2022 -->
- Armbrust, M. et al. *Lakehouse* (2021) — plataformas de dados na nuvem/k8s. <!-- @armbrust2020 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — estado e persistência distribuída. <!-- @kleppmann2017 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
