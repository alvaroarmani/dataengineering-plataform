# Flashcards — Módulo 23

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** REST: recursos e verbos? / **R:** Recursos no endereço (/pedidos/42) + verbos HTTP (GET ler, POST criar, PUT/PATCH atualizar, DELETE remover); resposta traz JSON + status.
- **P:** 4xx vs 5xx? / **R:** 4xx = erro do cliente (corrija, não repita); 5xx = erro do servidor (retry faz sentido).
- **P:** Por que paginar ao ingerir de API? / **R:** A API devolve em blocos; sem percorrer as páginas você pega só a primeira (dados incompletos) ou estoura limites.
- **P:** Onde vão credenciais de API? / **R:** Header de auth, valor vindo de secret/env — nunca na URL nem no código.
- **P:** Microserviços vs monólito? / **R:** Serviços pequenos e independentes por domínio (cada um dono do seu dado) vs um sistema único; para dados, cada serviço é uma fonte.
- **P:** Síncrono vs assíncrono? / **R:** Síncrono (REST/RPC) espera a resposta e acopla — use quando precisa agora; assíncrono (eventos) desacopla e resiste a picos.
- **P:** RabbitMQ vs Kafka? / **R:** RabbitMQ = fila de tarefas (mensagem consumida some); Kafka = log de eventos (fica, muitos consumidores releem).
- **P:** Por que event-driven desacopla? / **R:** O produtor publica sem saber quem consome; novos consumidores entram sem mexer no produtor.
- **P:** O que é idempotência e por que importa na integração? / **R:** N execuções = 1; como a entrega é at-least-once (repete após falha), torna retry/reentrega seguros.
- **P:** Como uma Idempotency-Key evita cobrança dupla? / **R:** O servidor guarda a chave; ao vê-la de novo, retorna o resultado anterior em vez de reprocessar.
- **P:** Retry com backoff exponencial? / **R:** Esperar mais a cada tentativa (1s,2s,4s…) + jitter, só no retriável (5xx/timeout), nunca no 4xx.
- **P:** O que faz um circuit breaker? / **R:** Após N falhas, para de chamar o serviço caído por um tempo, evitando o efeito dominó.
- **P:** O que é o padrão Saga? / **R:** Transação entre serviços = passos locais + compensações; se um falha, desfaz os concluídos na ordem inversa (não há COMMIT distribuído).
- **P:** O que é o contrato de uma API? / **R:** Campos obrigatórios, tipos e formato esperados; validar na borda impede lixo entrar no pipeline.

---
**Revisado em:** 2026-09-09
