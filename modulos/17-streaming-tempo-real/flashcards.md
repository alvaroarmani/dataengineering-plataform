# Flashcards — Módulo 17

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** Batch vs streaming? / **R:** Batch processa lotes finitos em intervalos; streaming processa um fluxo ilimitado de eventos em tempo quase real. A latência exigida decide.
- **P:** O que é um evento? / **R:** Um fato imutável que ocorreu num instante (registro do que aconteceu) — não um comando.
- **P:** O que a arquitetura orientada a eventos desacopla? / **R:** Produtor de consumidor: quem gera publica, quem se interessa reage; muitos consomem o mesmo evento.
- **P:** O que é CDC? / **R:** Change Data Capture — lê o log de transações do banco e emite cada mudança como evento (ponte OLTP → plataforma de dados).
- **P:** Kafka é fila ou log? / **R:** Log distribuído durável: ler não apaga; vários consumidores releem os mesmos eventos no seu próprio offset.
- **P:** Tópico, partição, offset? / **R:** Tópico = fluxo nomeado; partição = log independente (unidade de paralelismo e ordem); offset = posição sequencial dentro da partição.
- **P:** Em que nível o Kafka garante ordem? / **R:** Por partição — não há ordem global entre partições de um tópico.
- **P:** Para que serve a chave da mensagem? / **R:** Define a partição (hash da chave); a mesma chave vai sempre para a mesma partição → ordem por entidade sem perder paralelismo.
- **P:** O que é um consumer group? / **R:** Consumidores com o mesmo group id que dividem as partições (1 partição → 1 membro); grupos diferentes recebem todos os eventos.
- **P:** Tempo de evento vs de processamento? / **R:** Evento = quando o fato ocorreu; processamento = quando o sistema o viu. Agregações temporais usam tempo de evento.
- **P:** Tipos de janela? / **R:** Tumbling (fixa), sliding (deslizante, sobrepõe), session (agrupa por atividade separada por inatividade).
- **P:** O que é um watermark? / **R:** A decisão de "já vi eventos até T; fecho as janelas até T" — equilíbrio entre esperar atrasados e emitir o resultado.
- **P:** As três semânticas de entrega? / **R:** At-most-once (pode perder), at-least-once (pode duplicar), exactly-once (nem perde nem duplica).
- **P:** Como obter exactly-once na prática? / **R:** At-least-once + idempotência (chave/upsert/dedup): reprocessar não corrompe o resultado.

---
**Revisado em:** 2026-08-31
