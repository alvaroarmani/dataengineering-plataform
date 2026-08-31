# A nuvem para dados: modelos de serviço e serviços gerenciados

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Praticamente toda plataforma de dados moderna roda na **nuvem** — AWS, Google Cloud, Azure. E não é
só "o servidor de outra pessoa": a nuvem mudou como se faz engenharia de dados, oferecendo
armazenamento praticamente infinito, warehouses que escalam sozinhos e serviços que você **aluga por
uso** em vez de comprar e manter. Você já provou isso no curso: BigQuery (M06) é um warehouse
serverless na nuvem, MinIO (a bancada) imita o **object storage** da nuvem. Mas para trabalhar de
verdade — e não estourar a fatura — é preciso entender **o modelo de serviço**, **quais serviços
gerenciados** existem para dados, e as noções de **região, disponibilidade e custo** que definem toda
arquitetura cloud.

## 💡 Conceito (o porquê)

### IaaS, PaaS, SaaS e serverless: quem cuida do quê
A nuvem oferece níveis de abstração — quanto mais alto, menos você opera:
- **IaaS (infraestrutura):** você aluga máquinas virtuais e discos, e cuida de SO, patches, tudo
  acima. Máximo controle, máximo trabalho (ex.: uma VM EC2).
- **PaaS (plataforma):** você entrega o código/consulta; o provedor cuida do runtime, escala e
  patches (ex.: um banco gerenciado).
- **SaaS (software):** software pronto, você só usa (ex.: uma ferramenta de BI).
- **Serverless:** você não vê servidor nenhum — envia a função/consulta, paga **pelo que usa**, e a
  escala é automática (ex.: BigQuery, AWS Lambda). Ideal para cargas intermitentes.

A tendência em dados é **subir de nível**: usar serviços gerenciados/serverless e gastar tempo com
dados, não com administração de servidores.

### Os serviços de dados que você precisa conhecer
Cada provedor tem nomes diferentes, mas as **categorias** são universais:
- **Object storage** (S3, GCS, Azure Blob): o alicerce do data lake — barato, durável, "infinito",
  guarda arquivos (Parquet, CSV) por chave. É o MinIO da bancada, na escala da nuvem.
- **Data warehouse gerenciado** (BigQuery, Redshift, Snowflake): SQL analítico serverless/escalável (M06).
- **Serverless compute** (Lambda, Cloud Functions): rodar código sob demanda, sem gerenciar servidor.
- **Mensageria/streaming** (Kinesis, Pub/Sub, MSK): o Kafka gerenciado (M17).
- **Bancos gerenciados** (RDS, Cloud SQL): Postgres/MySQL sem administrar a máquina.
- **Orquestração** (serviços de Kubernetes e de Airflow gerenciado): rodar contêineres/DAGs em escala.

### Região, zona e disponibilidade
Recursos vivem numa **região** (localização geográfica) dividida em **zonas de disponibilidade** (data
centers isolados). Espalhar réplicas por zonas dá **alta disponibilidade** (uma zona cai, o serviço
continua — é replicação, M19, na infra). A escolha de região afeta **latência** (perto dos usuários),
**custo** (preços variam) e **compliance** (LGPD/soberania de dados, M14 — onde os dados podem residir).

### Custo é um cidadão de primeira classe
Na nuvem, cada byte guardado, cada TB varrido e cada requisição **custa**. O modelo é **pay-per-use**:
ótimo para começar barato (free-tier), perigoso se você não observa. Uma consulta que varre a tabela
inteira, um dado esquecido em storage caro, um cluster que ninguém desligou — tudo vira fatura. Por
isso técnicas como **particionamento** e formatos colunares (M06) não são só performance: são
**economia**. O aprofundamento em custo/ROI é o M21 (FinOps).

## 🔎 Exemplo
Uma startup monta sua plataforma **sem comprar servidor**: os arquivos brutos caem em **object storage**
(S3/GCS) — o data lake; um **warehouse serverless** (BigQuery) roda o SQL analítico, pagando pelos
bytes varridos; **funções serverless** processam eventos sob demanda; um **Postgres gerenciado** guarda
o operacional. Tudo replicado por **zonas** para alta disponibilidade, na **região** mais próxima dos
usuários (e permitida pela LGPD). Começam no **free-tier** e observam o custo desde o dia 1. Zero
administração de máquina — a nuvem opera; eles fazem engenharia de dados.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley tratam a **nuvem** como o ambiente padrão da engenharia de dados moderna, com o custo
(FinOps) entre as *undercurrents*, e defendem preferir serviços gerenciados/serverless. Armbrust et al.
descrevem o **Lakehouse** sobre object storage barato da nuvem como a arquitetura que unifica lake e
warehouse. — *Fundamentals of Data Engineering*; *Lakehouse: A New Generation of Open Platforms*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A conta de nuvem surpreende quem não observa: um job esquecido rodando 24/7, uma consulta que varre
petabytes, storage em classe cara para dados frios. Times maduros tratam **custo como métrica de
engenharia** (tags, orçamentos, alertas) desde o começo — e escolhem serverless para cargas
intermitentes justamente para não pagar por servidor ocioso. — Reis & Housley.
:::

## ⚠️ Erros comuns
- **Operar tudo em IaaS** (VMs cruas) quando um serviço gerenciado/serverless resolveria com menos trabalho.
- **Ignorar região/zona** — latência ruim, custo maior ou violação de residência de dados (LGPD).
- **Não observar custo** — jobs esquecidos, consultas que varrem tudo, storage frio em classe cara.
- **Confundir os níveis** — achar que serverless não tem limites/custo, ou que SaaS dá controle de infra.
- **Lock-in acidental** — usar serviços proprietários sem perceber o custo de sair; formatos abertos (Parquet) ajudam.

## 💼 O que o mercado espera
Conhecer os modelos de serviço (IaaS/PaaS/SaaS/serverless) e as categorias de serviços de dados
(object storage, warehouse, serverless, mensageria), entender região/zona/HA e tratar **custo** como
requisito. Quase toda vaga cita ao menos uma nuvem (AWS/GCP/Azure).

:::{admonition} ✨ Em resumo
:class: resumo
- **Modelos de serviço**: IaaS→PaaS→SaaS→**serverless** — quanto mais alto, menos você opera; em dados, suba de nível.
- **Serviços de dados** (categorias universais): **object storage** (lake), **warehouse** gerenciado, serverless, mensageria, bancos gerenciados, orquestração.
- **Região/zona** dão HA e afetam latência, custo e **compliance** (residência de dados, LGPD).
- **Custo é engenharia**: pay-per-use; particionar/colunar economiza; observe desde o dia 1 (FinOps, M21).
:::

## 🧠 Quiz de recall
1. Qual a diferença entre IaaS, PaaS e serverless?
   :::{dropdown} Resposta
   IaaS: você aluga a máquina e opera tudo acima do hardware. PaaS: entrega o código, o provedor cuida do runtime/escala. Serverless: sem servidor visível, paga pelo uso, escala automática.
   :::
2. O que é object storage e qual seu papel em dados?
   :::{dropdown} Resposta
   Armazenamento de arquivos por chave (S3/GCS/Blob), barato, durável e "infinito" — o alicerce do data lake. É o MinIO da bancada em escala de nuvem.
   :::
3. Para que servem regiões e zonas de disponibilidade?
   :::{dropdown} Resposta
   Região = localização geográfica; zonas = data centers isolados dentro dela. Espalhar réplicas por zonas dá alta disponibilidade; a região afeta latência, custo e compliance.
   :::
4. Por que particionar/usar colunar economiza na nuvem?
   :::{dropdown} Resposta
   Porque o custo é por bytes varridos/guardados; particionar e formato colunar fazem a consulta ler só o necessário, reduzindo a fatura (não é só performance).
   :::
5. Quando serverless é especialmente vantajoso?
   :::{dropdown} Resposta
   Em cargas intermitentes/variáveis: você paga só pelo uso e a escala é automática, evitando pagar por servidor ocioso.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você montaria uma plataforma de dados na nuvem, do zero, com custo em mente?"
  :::{dropdown} Resposta modelo
  Object storage como data lake (barato, formatos abertos como Parquet), um warehouse serverless (BigQuery) pagando por bytes varridos, funções serverless para processamento intermitente e um banco gerenciado para o operacional. Escolho a região por latência e compliance (LGPD), replico por zonas para HA, começo no free-tier e coloco tags/orçamentos/alertas de custo desde o dia 1. Prefiro gerenciado/serverless para gastar tempo com dados, não com servidores.
  :::
- **P:** "Onde a residência de dados entra numa decisão de nuvem?"
  :::{dropdown} Resposta modelo
  Na escolha da região. A LGPD/regulações podem exigir que dados pessoais fiquem em determinada geografia; então seleciono regiões compatíveis e evito replicar dados sensíveis para regiões não permitidas. É uma decisão de arquitetura tanto quanto de compliance (M14).
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (nuvem e custo como *undercurrents*).
- **Armbrust et al. — Lakehouse** (arquitetura de dados sobre object storage da nuvem).
- **Documentação AWS/GCP/Azure** — catálogo de serviços de dados e free-tier.

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — nuvem e FinOps. <!-- @reis2022 -->
- Armbrust, M. et al. *Lakehouse: A New Generation of Open Platforms* (2021) — dados na nuvem. <!-- @armbrust2020 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — implantação distribuída. <!-- @kleppmann2017 -->

*Acessado em: 2026-08-31.*

---
**Revisado em:** 2026-08-31
