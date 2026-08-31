# Flashcards — Módulo 20

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** IaaS vs PaaS vs serverless? / **R:** IaaS: você opera a máquina. PaaS: entrega o código, o provedor cuida do runtime. Serverless: sem servidor visível, paga pelo uso, escala automática.
- **P:** O que é object storage e seu papel? / **R:** Armazenamento de arquivos por chave (S3/GCS/Blob), barato e durável — o alicerce do data lake (o MinIO em escala de nuvem).
- **P:** Região vs zona de disponibilidade? / **R:** Região = geografia; zonas = data centers isolados dentro dela. Replicar por zonas dá HA; a região afeta latência, custo e compliance.
- **P:** Por que custo é engenharia na nuvem? / **R:** Tudo é pay-per-use (bytes guardados/varridos, requisições); particionar/colunar economiza; observe desde o dia 1.
- **P:** O que significa o k8s ser declarativo? / **R:** Você declara o estado desejado (ex.: 3 réplicas) e um control loop mantém a realidade batendo com isso.
- **P:** Pod, Deployment, Service? / **R:** Pod = contêiner(es) gerenciados; Deployment = mantém N réplicas + rolling update; Service = endereço estável que balanceia entre pods.
- **P:** O que é self-healing? / **R:** Se um pod/nó cai, o k8s recria os pods para voltar ao estado desejado, guiado por health checks — sem intervenção.
- **P:** Fórmula do HPA? / **R:** desejado = ceil(replicas_atuais × métrica_atual / métrica_alvo) — sobe réplicas se a métrica passa do alvo.
- **P:** O que o etcd guarda? / **R:** O estado do cluster; é armazenamento distribuído por consenso (liga com o M19).
- **P:** Job vs CronJob vs Deployment? / **R:** Job roda até completar; CronJob = Job agendado (como uma DAG); Deployment = serviço que fica no ar.
- **P:** Como rodar banco/estado no k8s? / **R:** StatefulSet (identidade estável) + PVC/PV (disco que sobrevive ao pod); pod é efêmero por padrão.
- **P:** Como Spark roda no k8s? / **R:** Driver + executors como pods temporários, que sobem para o job e somem ao terminar (elasticidade sem cluster fixo).
- **P:** Papel do Terraform/IaC aqui? / **R:** Provisionar cluster gerenciado, buckets e redes como código versionado (plan/apply), em vez de cliques no console.
- **P:** Quando NÃO usar Kubernetes? / **R:** Poucos contêineres/pouca escala (compose basta), quando serverless resolve, ou sem time para operar. Escolha o mais simples que atende.

---
**Revisado em:** 2026-08-31
