# Flashcards — Módulo 19

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** Escala vertical vs horizontal? / **R:** Vertical = máquina maior (teto físico, ponto único de falha); horizontal = mais máquinas dividindo o trabalho (escala sem teto, tolera falhas).
- **P:** O que é particionar (shard)? / **R:** Dividir os dados por nós (por intervalo ou por hash) para nenhuma máquina guardar tudo; alvo = balancear e evitar hotspots.
- **P:** O que o consistent hashing resolve? / **R:** Adicionar/remover nós movendo só as chaves vizinhas, em vez de remapear tudo como no hash % N.
- **P:** Por que replicar? / **R:** Manter cópias em vários nós para tolerar falhas — se o nó de uma partição cai, outra réplica assume.
- **P:** O que é falha parcial? / **R:** Parte do sistema funciona e parte não (nó lento ≡ morto, rede perde mensagens, sem relógio global) — a regra em distribuídos.
- **P:** Replicação síncrona vs assíncrona? / **R:** Síncrona espera a réplica confirmar (segura, lenta); assíncrona confirma na hora e propaga depois (rápida, cria lag).
- **P:** Consistência forte vs eventual? / **R:** Forte: toda leitura vê a última escrita. Eventual: réplicas convergem depois; leituras podem divergir temporariamente.
- **P:** O que garante R + W > N? / **R:** Que os conjuntos lido e escrito se sobreponham → a leitura sempre alcança o valor mais recente (quórum).
- **P:** O que o CAP afirma? / **R:** Sob partição de rede, escolha C (consistência) ou A (disponibilidade); sem partição, tem as duas.
- **P:** O que o PACELC acrescenta? / **R:** Mesmo sem partição (Else), há trade-off Latência vs Consistência — consistência forte custa latência sempre.
- **P:** Por que N = 2f + 1? / **R:** Para tolerar f falhas, a maioria (f+1) precisa sobreviver; por isso clusters de consenso têm nº ímpar de nós.
- **P:** O que Raft faz? / **R:** Consenso por eleição de líder (maioria) + log replicado; nova eleição se o líder cai, evitando split-brain.
- **P:** Onde consenso aparece na stack? / **R:** Líder de partição no Kafka, coordenação via ZooKeeper/etcd, estado do Kubernetes (etcd), transações de NewSQL.
- **P:** Quando usar consenso? / **R:** Só para acordo forte (quem é líder, ordem do log); é caro. No resto, replicação + idempotência.

---
**Revisado em:** 2026-08-31
