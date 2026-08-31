# Kubernetes: orquestração de contêineres em escala

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

No M10 você aprendeu Docker: empacotar uma aplicação num contêiner reproduzível. Ótimo para uma
máquina. Mas e quando você tem **dezenas de contêineres** rodando em **muitas máquinas** — um pipeline
com vários serviços, réplicas para aguentar carga, contêineres que travam e precisam reiniciar,
tráfego que precisa ser distribuído? Fazer isso na mão (subir, monitorar, reiniciar, escalar,
conectar) é inviável. **Kubernetes (k8s)** é o **orquestrador de contêineres** que virou padrão da
indústria para exatamente isso: você declara o estado desejado e ele mantém — reiniciando, escalando e
conectando contêineres por você. Dados rodam cada vez mais em k8s (Airflow, Spark, serviços de
ingestão), então entender seus conceitos é competência de mercado.

## 💡 Conceito (o porquê)

### O modelo declarativo: estado desejado
A ideia central do Kubernetes: você **declara** o que quer ("quero 3 réplicas deste contêiner, sempre
no ar") num arquivo (YAML), e o k8s trabalha continuamente para **fazer a realidade bater com a
declaração** — um *control loop* que compara desejado × atual e age. Se um contêiner morre, ele sobe
outro; se você pede mais réplicas, ele cria. Você descreve o **quê**, não o **como** — o oposto de
rodar comandos imperativos. (É a mesma filosofia do Terraform/IaC, M13, aplicada a contêineres.)

### Os objetos essenciais
- **Pod:** a menor unidade — um (ou poucos) contêineres que rodam juntos, compartilhando rede/armazenamento.
  É o contêiner do M10, "embrulhado" para o k8s gerenciar.
- **Deployment:** declara **quantas réplicas** de um pod você quer e cuida de mantê-las, além de fazer
  **rolling updates** (trocar a versão sem downtime) e rollback. É onde você diz "3 réplicas da app X".
- **Service:** um endereço **estável** (nome DNS + IP virtual) que **balanceia** o tráfego entre os pods
  de um Deployment. Como pods vêm e vão (IPs mudam), o Service dá um ponto fixo — `nome.namespace.svc.cluster.local`.
- **Namespace:** uma divisão lógica do cluster (ex.: `dev`, `prod`) para isolar e organizar recursos.
- **ConfigMap / Secret:** configuração e segredos (M14) injetados nos pods sem embutir na imagem.

### Nós, cluster e o scheduler
Um **cluster** k8s é um conjunto de máquinas (**nós**) coordenadas por um **control plane**. O
**scheduler** decide **em qual nó** cada pod roda, encaixando-o onde há CPU/memória disponíveis (um
problema de *bin packing*). O estado de todo o cluster vive no **etcd** — um armazenamento distribuído
por **consenso** (M19): é o Kubernetes se apoiando nos fundamentos distribuídos que você acabou de ver.

### Self-healing e escalabilidade
Duas superpotências que caem direto do modelo declarativo:
- **Self-healing:** se um pod trava ou um nó cai, o k8s recria os pods em outro lugar para voltar ao
  estado desejado — sem intervenção humana. **Health checks** (liveness/readiness probes) dizem ao k8s
  se um pod está vivo e pronto a receber tráfego.
- **Autoscaling (HPA):** o *HorizontalPodAutoscaler* ajusta o número de réplicas conforme uma métrica
  (ex.: CPU). A regra: `desejado = ceil(replicas_atuais × métrica_atual / métrica_alvo)` — se a CPU
  passa do alvo, sobem réplicas; se sobra, descem. Escala elástica, automática.

### Por que isso importa para dados
Kubernetes é a base para rodar **plataformas de dados** de forma portável e escalável: Airflow (M09),
Spark (M11) e serviços de ingestão rodam como contêineres orquestrados, com self-healing e autoscaling
"de graça". E, por ser um padrão aberto, roda igual na sua máquina, na nuvem gerenciada (EKS/GKE/AKS)
ou on-prem`.

## 🔎 Exemplo
Um serviço de ingestão de API precisa aguentar picos e nunca cair. Você declara um **Deployment** com 3
réplicas do contêiner (a imagem do M10) e um **Service** que dá um endereço estável e balanceia o
tráfego entre elas. Um pod trava às 3h da manhã? O k8s **recria** automaticamente (self-healing) — sem
acordar ninguém. Chega um pico e a CPU passa do alvo? O **HPA** sobe para 6 réplicas; passado o pico,
volta a 3. Uma nova versão? **Rolling update** troca os pods um a um, sem downtime. Você declarou o
estado desejado uma vez; o Kubernetes mantém.

:::{admonition} 📖 Da literatura
:class: seealso
O modelo declarativo de estado desejado e o control loop do Kubernetes são a aplicação prática dos
princípios de sistemas distribuídos — tolerância a falhas, coordenação por consenso (etcd), replicação —
que Kleppmann formaliza. Reis & Housley situam contêineres e orquestração como infraestrutura padrão do
ciclo de vida do dado. — *Designing Data-Intensive Applications*; *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Kubernetes virou o "sistema operacional da nuvem": rodar Airflow, Spark e serviços de dados em k8s dá
portabilidade (mesma config em qualquer nuvem) e resiliência (self-healing) sem código extra. O custo é
a **complexidade** — por isso muitos times usam k8s **gerenciado** (GKE/EKS/AKS) e só o adotam quando a
escala justifica. — prática de mercado; Reis & Housley.
:::

## ⚠️ Erros comuns
- **Pensar imperativo** (rodar comandos) em vez de declarar o estado desejado em YAML versionado.
- **Esquecer health checks** — sem liveness/readiness, o k8s não sabe reiniciar nem quando mandar tráfego.
- **Service errado/ausente** — apontar para IPs de pods (que mudam) em vez do nome estável do Service.
- **Usar k8s cedo demais** — a complexidade não se paga para 1–2 contêineres; comece simples (M10).
- **Não definir requests/limits** — o scheduler não consegue encaixar bem e nós ficam sobre/subutilizados.

## 💼 O que o mercado espera
Entender o modelo declarativo (estado desejado), os objetos (pod, deployment, service, namespace),
self-healing e autoscaling — e saber que Airflow/Spark rodam em k8s. Não se espera administrar um
cluster do zero, mas **raciocinar** sobre ele. Kubernetes aparece em muitas vagas de pleno/sênior.

:::{admonition} ✨ Em resumo
:class: resumo
- Kubernetes é **declarativo**: você declara o **estado desejado** e um control loop o mantém (self-healing).
- **Pod** (contêiner gerenciado) · **Deployment** (réplicas + rolling update) · **Service** (endereço estável + balanceamento) · **Namespace** (isolamento).
- **Scheduler** encaixa pods nos nós; o estado do cluster vive no **etcd** (consenso, M19).
- **HPA** escala réplicas por métrica: `ceil(replicas × atual / alvo)`; roda igual on-prem e em nuvem gerenciada.
:::

## 🧠 Quiz de recall
1. O que significa o Kubernetes ser "declarativo"?
   :::{dropdown} Resposta
   Você declara o estado desejado (ex.: 3 réplicas) e um control loop trabalha continuamente para fazer a realidade bater com a declaração — você descreve o quê, não o como.
   :::
2. Diferencie Pod, Deployment e Service.
   :::{dropdown} Resposta
   Pod = a menor unidade (contêiner(es) gerenciados). Deployment = mantém N réplicas de um pod e faz rolling updates. Service = endereço DNS/IP estável que balanceia tráfego entre os pods.
   :::
3. O que é self-healing no k8s?
   :::{dropdown} Resposta
   Se um pod trava ou um nó cai, o k8s recria os pods em outro lugar para voltar ao estado desejado, sem intervenção — guiado por health checks (liveness/readiness).
   :::
4. Como o HPA decide o número de réplicas?
   :::{dropdown} Resposta
   Pela fórmula ceil(replicas_atuais × métrica_atual / métrica_alvo): se a métrica (ex.: CPU) passa do alvo, sobe réplicas; se sobra, desce.
   :::
5. O que o etcd guarda e por que ele conecta com o M19?
   :::{dropdown} Resposta
   O estado de todo o cluster; é um armazenamento distribuído por consenso — o Kubernetes se apoiando nos fundamentos de consenso/tolerância a falhas do M19.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Por que usar Kubernetes em vez de rodar contêineres com docker-compose?"
  :::{dropdown} Resposta modelo
  Compose é ótimo para uma máquina e poucos serviços (M10). Kubernetes entra quando preciso de escala e resiliência em muitas máquinas: réplicas com balanceamento, self-healing automático, autoscaling, rolling updates sem downtime e portabilidade entre nuvens — tudo pelo modelo declarativo. O custo é a complexidade, então só adoto quando a escala justifica, geralmente via k8s gerenciado.
  :::
- **P:** "Como você rodaria Airflow ou Spark de forma resiliente e escalável?"
  :::{dropdown} Resposta modelo
  Em Kubernetes: declaro os componentes como Deployments/Services, com health checks para self-healing e HPA para escalar workers conforme a carga. Ganho portabilidade (mesma config em qualquer nuvem) e resiliência sem código extra. Uso k8s gerenciado (GKE/EKS/AKS) para não operar o control plane, e defino requests/limits para o scheduler encaixar bem os pods.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Documentação do Kubernetes** — conceitos (Pods, Deployments, Services, HPA).
- **Kleppmann — Designing Data-Intensive Applications** (os fundamentos distribuídos por baixo do k8s).
- **Reis & Housley — Fundamentals of Data Engineering** (contêineres e orquestração na infra de dados).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — orquestração de contêineres. <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — coordenação e tolerância a falhas. <!-- @kleppmann2017 -->
- Armbrust, M. et al. *Lakehouse* (2021) — plataformas de dados na nuvem. <!-- @armbrust2020 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
