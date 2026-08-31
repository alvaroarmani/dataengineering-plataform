# Módulo 19 — Sistemas Distribuídos para Dados

> A engenharia por baixo de Spark, Kafka e Cassandra: particionamento, replicação, consistência,
> CAP e consenso — o que MIT e Harvard ensinam antes de qualquer framework.

## Identificação
- **Eixo:** 4 — Escala, Qualidade e Governança
- **Carga horária:** 25h
- **Pré-requisitos:** M11 (Spark), M17 (Kafka), M18 (NoSQL)
- **Onde roda:** 🟢 Conceitual + exercícios de lógica no browser

## Ementa
Fundamentos de sistemas distribuídos aplicados a dados. Por que distribuir: escala horizontal vs
vertical, particionamento (range/hash, hotspots, **consistent hashing**) e **falhas parciais**.
Replicação (líder/seguidores, síncrona/assíncrona, lag), consistência **forte vs eventual**,
**quóruns** (R+W>N), teorema **CAP** e **PACELC**. **Consenso** e tolerância a falhas: maioria,
**2f+1**, split-brain, panorama Raft/Paxos e coordenação (ZooKeeper/etcd). Como esses fundamentos
sustentam as ferramentas do curso.

## Competências e habilidades
- C17 — raciocinar sobre particionamento, replicação, consistência e consenso em sistemas de dados.

## Objetivos de aprendizagem
1. **Explicar** particionamento e replicação e seus trade-offs.
2. **Aplicar** a regra de quórum e distinguir consistência forte de eventual.
3. **Interpretar** corretamente o teorema CAP (e PACELC) numa decisão de projeto.
4. **Descrever** consenso, a regra 2f+1 e onde ela aparece na stack.

## Plano de aulas (unidades)

**Unidade 1 — Por que distribuir? Particionamento e falhas**
1. **Teoria:** [Por que distribuir? Particionamento e falhas parciais](teoria-01-por-que-distribuir-particionamento.md)
2. **Exercícios:** [Custo de replicação (🟢)](exercicio-01.md) · [Consistent hashing: nó do dado (🟢)](exercicio-02.md)

**Unidade 2 — Replicação, consistência e CAP**
1. **Teoria:** [Replicação, consistência e o teorema CAP](teoria-02-replicacao-consistencia-cap.md)
2. **Exercícios:** [Réplica atrasada / lag (🟢)](exercicio-05.md) · [Nó de menor carga (🟢)](exercicio-06.md)

**Unidade 3 — Consenso e tolerância a falhas**
1. **Teoria:** [Consenso e tolerância a falhas](teoria-03-consenso-tolerancia-falhas.md)
2. **Exercícios:** [Tolerância a falhas 2f+1 (🟢)](exercicio-03.md) · [Consenso por maioria (🟢)](exercicio-04.md)

> **Módulo completo.** A base teórica que explica *por que* Spark, Kafka, Cassandra e Kubernetes funcionam como funcionam.

## Metodologia e avaliação
**Maestria:** explicar particionamento/replicação/CAP e a regra 2f+1, e resolver os exercícios de
quórum, consistent hashing e consenso — conforme rubrica + quiz ≥ 80%.

## O que o mercado espera
Raciocinar sobre trade-offs distribuídos (consistência, disponibilidade, particionamento) é o que
separa quem "usa" de quem "entende" as ferramentas — e aparece direto no system design de pleno/sênior.

## Erros comuns
- Citar o CAP como "escolha 2 de 3".
- Número par de nós num cluster de consenso.
- Assumir rede confiável e relógio global.
- Exigir consistência forte onde a eventual bastava (ou o contrário).

## Recursos
Ver [`recursos.md`](recursos.md) (Kleppmann caps. 5/6/8/9; paper MapReduce; Raft/etcd).

---
**Revisado em:** 2026-08-31
