# Segurança de dados: acesso, criptografia e mascaramento

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Um data warehouse concentra o que a empresa tem de mais sensível: dados de clientes, valores,
salários. Um vazamento aqui é catastrófico — multas, perda de confiança, manchete. E a maioria
dos incidentes não vem de "hackers geniais": vem de **acesso amplo demais** (todo mundo é admin),
**dados trafegando/armazenados sem criptografia** e **credencial no código**. Segurança de dados
é o conjunto de controles que reduz essa superfície de ataque — e boa parte é **higiene básica**
que todo engenheiro de dados precisa aplicar.

## 💡 Conceito (o porquê)

### Princípio do menor privilégio (least privilege)
Cada pessoa ou serviço recebe **só o acesso de que precisa**, e nada além. O analista de
marketing não precisa da tabela de salários; o job de ETL precisa escrever em `staging`, não
`DROP DATABASE`. Menor privilégio **limita o estrago** quando uma conta é comprometida. Na
prática: papéis (roles) com permissões específicas, concedidos por necessidade — não "admin
para todos porque é mais fácil".

### RBAC (controle de acesso por papel)
Em vez de dar permissão a cada pessoa individualmente, você define **papéis** (`analista`,
`engenheiro`, `admin`) com um conjunto de permissões, e associa pessoas aos papéis. Facilita
auditar ("quem pode ver isto?") e revogar (tira do papel). É o modelo de `GRANT`/`REVOKE` do
Postgres (M4) e o padrão em warehouses.

### Criptografia: em repouso e em trânsito
- **Em trânsito (in transit):** dados criptografados ao trafegar pela rede (TLS/HTTPS). Impede
  que alguém "escutando" a rede leia o conteúdo. Sempre ligado em conexões de banco/APIs.
- **Em repouso (at rest):** dados criptografados no disco/storage. Se roubarem o disco ou o
  bucket, o conteúdo é ilegível sem a chave. Hoje é padrão nos storages de nuvem (muitas vezes
  transparente).

### Mascaramento e anonimização
Nem todo mundo que usa a tabela precisa ver o dado **cru**. **Mascaramento** mostra uma versão
parcial (`a***@email.com`, CPF `***.***.***-12`) — útil para suporte/analytics sem expor o valor
completo. **Anonimização** remove/substitui identificadores de forma que **não dá para voltar**
à pessoa (importante para LGPD, U3). **Pseudonimização** troca o identificador por um token
reversível só com uma chave separada — reduz risco mantendo a capacidade de re-ligar quando
autorizado.

### Gestão de segredos (secrets)
Senha de banco, chave de API, token **nunca** vão no código ou no Git (M13). Ficam em um **gestor
de segredos** (variáveis de ambiente, GitHub Secrets, Vault, Secret Manager da nuvem) e são
**rotacionados** periodicamente. Segredo vazado = rotacione imediatamente.

## 🔎 Exemplo
A tabela `clientes` tem nome, email e CPF. Você cria o papel `analytics` com `SELECT` só numa
**view** que expõe email/CPF **mascarados**; o time de dados tem `SELECT` na tabela crua via
papel `engenharia`. A conexão usa TLS (em trânsito); o storage é criptografado (em repouso). A
senha do banco vem de uma variável de ambiente, não do código. Resultado: o analista faz seu
trabalho sem nunca ver um CPF completo, e um vazamento de credencial do analytics não expõe
dados crus.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley colocam **segurança** como responsabilidade transversal do engenheiro de dados —
com destaque para **menor privilégio**, criptografia e gestão de segredos como práticas de base.
Kleppmann discute criptografia e controle de acesso como parte da confiabilidade de sistemas de
dados. — *Fundamentals of Data Engineering*; *Designing Data-Intensive Applications*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
A causa recorrente de vazamentos é banal: bucket de storage público por engano, credencial
commitada no Git, acesso amplo demais. Por isso "menor privilégio + segredos fora do código +
criptografia ligada" pega a maior parte do risco com pouco esforço. — Reis & Housley.
:::

## ⚠️ Erros comuns
- **Admin para todos** — viola menor privilégio; um vazamento compromete tudo.
- **Credencial no código/Git** — o vazamento mais comum e evitável.
- **Sem TLS** — dados trafegando em texto claro.
- **Confundir mascaramento com anonimização** — mascarar na exibição não torna o dado anônimo se o cru continua acessível.
- **Nunca rotacionar segredos** — uma chave antiga vazada continua válida para sempre.

## 💼 O que o mercado espera
Aplicar **menor privilégio**, entender criptografia em repouso/trânsito, saber que segredos ficam
fora do código e distinguir mascaramento/anonimização/pseudonimização. "Como você protegeria uma
tabela com dados sensíveis?" é pergunta clássica de entrevista.

:::{admonition} ✨ Em resumo
:class: resumo
- **Menor privilégio + RBAC**: cada um só o acesso necessário, via papéis — limita o estrago.
- **Criptografia**: em trânsito (TLS) e em repouso (disco/storage).
- **Mascaramento** (exibição parcial) ≠ **anonimização** (irreversível) ≠ **pseudonimização** (reversível com chave).
- **Segredos** fora do código, em um gestor, e **rotacionados**.
:::

## 🧠 Quiz de recall
1. O que é o princípio do menor privilégio?
   :::{dropdown} Resposta
   Conceder a cada pessoa/serviço só o acesso estritamente necessário, para limitar o estrago quando uma conta é comprometida.
   :::
2. Qual a diferença entre criptografia em trânsito e em repouso?
   :::{dropdown} Resposta
   Em trânsito protege os dados na rede (TLS); em repouso protege os dados gravados no disco/storage.
   :::
3. Mascaramento é o mesmo que anonimização?
   :::{dropdown} Resposta
   Não. Mascaramento mostra uma versão parcial na exibição; anonimização remove/substitui identificadores de forma irreversível. Se o dado cru continua acessível, mascarar não anonimiza.
   :::
4. Onde devem ficar senhas e chaves de API?
   :::{dropdown} Resposta
   Em um gestor de segredos (variáveis de ambiente, Secrets, Vault) — nunca no código ou no Git — e devem ser rotacionadas.
   :::
5. O que é RBAC?
   :::{dropdown} Resposta
   Controle de acesso por papel: permissões são atribuídas a papéis, e pessoas são associadas a papéis, facilitando auditar e revogar.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Como você daria acesso a uma tabela com CPF a um time de analytics sem expor os CPFs?"
  :::{dropdown} Resposta modelo
  Não daria acesso à tabela crua. Criaria uma view com o CPF mascarado (ou anonimizado) e concederia SELECT nela ao papel de analytics (menor privilégio + RBAC). O acesso ao dado cru fica restrito a quem realmente precisa. Somaria criptografia em repouso/trânsito e auditoria de acessos.
  :::
- **P:** "Você achou uma senha de banco commitada no repositório. O que faz?"
  :::{dropdown} Resposta modelo
  Rotaciono a credencial imediatamente (a do Git deve ser considerada comprometida), removo-a do código movendo para um gestor de segredos/variável de ambiente, e — como ela fica no histórico do Git — trato o segredo como vazado de vez. Depois reviso por que passou (hook/scan de segredos no CI).
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (segurança, menor privilégio, segredos).
- **Kleppmann — Designing Data-Intensive Applications** (criptografia, controle de acesso).
- **Documentação do Postgres — GRANT/REVOKE e roles**.

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — segurança de dados. <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — criptografia e acesso. <!-- @kleppmann2017 -->
- Dehghani, Z. *Data Mesh Principles and Logical Architecture* (2020) — segurança na plataforma. <!-- @dehghani2020 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
