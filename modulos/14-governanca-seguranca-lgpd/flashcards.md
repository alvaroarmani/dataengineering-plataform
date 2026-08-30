# Flashcards — Módulo 14

Revisão espaçada. Cubra a resposta, responda de memória, confira.

- **P:** Para que serve um catálogo de dados? / **R:** Índice dos datasets (o que existe, o que significa, como achar); combate o conhecimento tribal.
- **P:** O que é lineage e para que serve? / **R:** Mapa origem→destino do dado; habilita impact analysis e root cause.
- **P:** Por que ownership importa? / **R:** Sem dono, dado quebrado é problema de ninguém; o dono responde por qualidade/SLAs/mudanças.
- **P:** Princípio do menor privilégio? / **R:** Cada pessoa/serviço só o acesso necessário — limita o estrago de uma conta comprometida.
- **P:** O que é RBAC? / **R:** Acesso por papel: permissões vão a papéis, pessoas a papéis; fácil auditar e revogar.
- **P:** Criptografia em trânsito vs em repouso? / **R:** Em trânsito protege na rede (TLS); em repouso protege no disco/storage.
- **P:** Mascaramento vs anonimização vs pseudonimização? / **R:** Mascaramento = exibição parcial; anonimização = irreversível; pseudonimização = reversível só com chave separada.
- **P:** Onde ficam senhas/chaves? / **R:** Em gestor de segredos (env/Secrets/Vault), fora do código/Git, e rotacionadas.
- **P:** Dado pessoal vs sensível (LGPD)? / **R:** Pessoal identifica alguém (nome/CPF/email); sensível é categoria especial (saúde/raça/religião/biometria) com proteção reforçada.
- **P:** O que é minimização de dados? / **R:** Coletar/guardar só o necessário à finalidade, pelo tempo necessário.
- **P:** O que o direito ao esquecimento exige do pipeline? / **R:** Localizar e apagar/anonimizar todos os registros da pessoa em todas as tabelas — depende de catálogo/lineage.
- **P:** Controlador, operador e encarregado (DPO)? / **R:** Controlador decide o tratamento; operador trata em nome dele; encarregado é o ponto de contato.

---
**Revisado em:** 2026-08-29
