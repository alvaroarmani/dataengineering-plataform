# Flashcards — Módulo 01

Revisão espaçada. Cubra a resposta, responda de memória, confira. Revise 1 dia, 1 semana e
1 mês depois de concluir o módulo.

- **P:** O que é Engenharia de Dados? / **R:** A disciplina que constrói e opera os sistemas que movem e preparam dados de forma confiável, repetível e em escala.
- **P:** Quais as etapas do ciclo de vida do dado? / **R:** Geração → Ingestão → Armazenamento → Transformação → Disponibilização (com governança, qualidade, segurança, orquestração e observabilidade permeando).
- **P:** OLTP vs OLAP? / **R:** OLTP = transacional (muitas escritas pequenas, orientado a linha); OLAP = analítico (leituras grandes e agregações, orientado a coluna).
- **P:** Por que não rodar análises no banco de produção? / **R:** Cargas analíticas pesadas degradam a operação transacional; por isso movemos dados para um ambiente analítico (DW).
- **P:** Batch vs streaming? / **R:** Batch processa em lotes periódicos (simples, barato, maioria dos casos); streaming processa evento a evento em tempo (quase) real (mais complexo).
- **P:** Data Warehouse vs Data Lake vs Lakehouse? / **R:** DW = estruturado/modelado p/ análise; Lake = dados brutos em qualquer formato, barato/flexível; Lakehouse = combina os dois com transações/schema (Delta/Iceberg).
- **P:** Por que armazenamento colunar em OLAP? / **R:** Análises leem muitas linhas mas poucas colunas e agregam; o formato colunar lê só as colunas necessárias (menos I/O) e comprime melhor (dados do mesmo tipo juntos).
- **P:** Quais são as "correntes de fundo" (undercurrents) do ciclo de vida? / **R:** Segurança, gestão/governança de dados, DataOps, arquitetura de dados, orquestração e engenharia de software — permeiam todas as etapas.
- **P:** ETL vs ELT? / **R:** ETL transforma antes de carregar (compute caro); ELT carrega o bruto e transforma depois, dentro do DW/lakehouse (habilitado por nuvem barata; padrão do Modern Data Stack e do dbt).
- **P:** CSV vs Parquet? / **R:** CSV = linha, texto, sem tipos, comprime mal; Parquet = colunar, binário, guarda schema/tipos, comprime bem e permite ler só as colunas necessárias.
- **P:** O que é idempotência e por que importa? / **R:** Executar N vezes = mesmo resultado que 1 vez. Importa porque pipelines falham e são reprocessados; sem ela, reprocessar duplica/corrompe dados.
- **P:** O que é um "data swamp"? / **R:** Um data lake sem governança: dados brutos acumulados que ninguém acha nem confia. Lakehouse (Delta/Iceberg) dá schema/ACID para evitar isso.
- **P:** Arquitetura medalhão (bronze/silver/gold)? / **R:** Camadas de refinamento: bronze = bruto, silver = limpo/conformado, gold = modelado para consumo.
- **P:** O que é Data Mesh? / **R:** Abordagem organizacional que descentraliza a responsabilidade pelos dados para os domínios de negócio, tratando dados como produto.
- **P:** Lambda vs Kappa? / **R:** Lambda = camada batch (precisa) + camada de velocidade (rápida) em paralelo; Kappa = tudo como stream, reprocessando do log de eventos.

---
**Revisado em:** 2026-08-20
