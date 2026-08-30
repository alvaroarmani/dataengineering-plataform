# Privacidade e compliance: LGPD e GDPR na prática

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Dados pessoais não são "só mais uma coluna". A **LGPD** (Lei Geral de Proteção de Dados, Brasil,
Lei 13.709/2018) e a **GDPR** (regulamento europeu equivalente) impõem regras sobre **coletar,
guardar, usar e apagar** dados de pessoas — com **multas pesadas** e obrigações concretas. Para
o engenheiro de dados, isso não é papo de advogado: vira **requisito técnico** do pipeline —
saber quais colunas são pessoais, restringir acesso, permitir apagar/exportar dados de uma pessoa
e não guardar o que não precisa. Ignorar isso é risco jurídico real para a empresa.

## 💡 Conceito (o porquê)

### Dado pessoal e dado sensível
- **Dado pessoal:** qualquer informação que identifica ou pode identificar uma pessoa — nome,
  CPF, email, telefone, endereço, IP, ID de dispositivo.
- **Dado pessoal sensível (categoria especial):** origem racial/étnica, saúde, orientação sexual,
  religião, opinião política, dado biométrico/genético. Recebe **proteção reforçada** — mais
  restrição de uso e acesso.

Saber classificar as colunas do warehouse nessas categorias é o primeiro passo prático.

### Bases legais e finalidade
Você só pode tratar dado pessoal com uma **base legal** (consentimento, cumprimento de contrato,
obrigação legal, legítimo interesse etc.) e para uma **finalidade específica e declarada**. Não
se coleta dado "porque um dia pode ser útil" — isso viola a **limitação de finalidade** e a
**minimização** (colete só o necessário).

### Direitos do titular (o que o pipeline precisa suportar)
A pessoa (titular) tem direitos que viram **funcionalidades** do seu sistema:
- **Acesso/portabilidade:** exportar os dados que você tem dela.
- **Correção:** corrigir dados errados.
- **Eliminação / "direito ao esquecimento":** apagar seus dados quando solicitado (respeitando
  retenções legais). Na prática, seu pipeline precisa **conseguir localizar e remover/anonimizar**
  todos os registros de uma pessoa — em todas as tabelas e backups. Se os dados estão espalhados
  sem lineage (U1), isso é quase impossível — por isso governança e privacidade andam juntas.

### Retenção e minimização
Guarde dado pessoal **só pelo tempo necessário** à finalidade; depois, **apague ou anonimize**.
Menos dado pessoal guardado = menos risco e menos trabalho de compliance. Anonimização (U2) é a
saída para **manter valor analítico sem manter dado pessoal**: dado verdadeiramente anônimo sai
do escopo da LGPD.

### Papéis e registro
A LGPD define **controlador** (decide o tratamento), **operador** (trata em nome do controlador)
e o **DPO/encarregado** (ponto de contato). Empresas mantêm um **registro de tratamento** (quais
dados, para quê, base legal) — e o **catálogo + lineage** (U1) são a matéria-prima técnica disso.

## 🔎 Exemplo
Um cliente pede exclusão dos dados (direito ao esquecimento). Com **catálogo + lineage**, você
localiza todas as tabelas com o `cliente_id` dele; onde a lei permite apagar, você remove; onde há
retenção obrigatória (ex.: fiscal), você **anonimiza** os campos pessoais mantendo o registro
contábil. As colunas `raca` e `saude` (sensíveis) já estavam com acesso restrito e mascaradas
para analytics (U2). Você guardou só o necessário (minimização) — então há menos lugares para
procurar. O pedido é atendido no prazo legal.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley tratam **privacidade e conformidade** (GDPR/CCPA e afins) como parte inseparável
da engenharia de dados moderna, ligando-a a governança, segurança e ao ciclo de vida do dado.
Kleppmann discute os desafios técnicos de apagar dados de forma abrangente em sistemas
distribuídos. — *Fundamentals of Data Engineering*; *Designing Data-Intensive Applications*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
O "direito ao esquecimento" é tecnicamente difícil: dados vazam para réplicas, data lakes,
backups e logs. Empresas maduras projetam o apagamento **desde o início** (chaves de titular
rastreáveis, tabelas de mapeamento, políticas de retenção) em vez de caçar dado depois. — Reis &
Housley; Kleppmann.
:::

## ⚠️ Erros comuns
- **Não saber onde estão os dados pessoais** — sem catálogo/lineage, atender direitos é inviável.
- **Coletar "por precaução"** — viola minimização e finalidade.
- **Guardar para sempre** — ignora retenção; aumenta risco.
- **Achar que mascarar = anonimizar** — se dá para reverter, ainda é dado pessoal (U2).
- **Tratar LGPD como "problema do jurídico"** — os controles são técnicos e ficam no pipeline.

## 💼 O que o mercado espera
Reconhecer dado pessoal/sensível, entender minimização, finalidade, retenção e os direitos do
titular — e saber que o pipeline precisa **suportar exclusão/exportação**. Não se espera que você
seja advogado, mas que **projete o sistema para conformidade**. Pergunta comum: "como você
atenderia um pedido de exclusão de dados?".

:::{admonition} ✨ Em resumo
:class: resumo
- **LGPD/GDPR** transformam privacidade em **requisito técnico** do pipeline.
- **Classifique**: dado pessoal vs sensível (proteção reforçada).
- **Minimização + finalidade + retenção**: colete só o necessário, para um fim declarado, pelo tempo necessário.
- **Direitos do titular** viram features: acesso/exportação, correção e **eliminação** — que dependem de catálogo/lineage (U1) e anonimização (U2).
:::

## 🧠 Quiz de recall
1. Qual a diferença entre dado pessoal e dado pessoal sensível?
   :::{dropdown} Resposta
   Pessoal identifica alguém (nome, CPF, email); sensível é uma categoria especial (saúde, raça, religião, orientação sexual, biometria) com proteção reforçada.
   :::
2. O que é minimização de dados?
   :::{dropdown} Resposta
   Coletar e guardar apenas os dados pessoais estritamente necessários à finalidade — nada "por precaução".
   :::
3. O que o "direito ao esquecimento" exige do pipeline?
   :::{dropdown} Resposta
   Conseguir localizar e apagar (ou anonimizar, quando há retenção legal) todos os registros de uma pessoa em todas as tabelas — o que depende de catálogo/lineage.
   :::
4. Por que governança (U1) é pré-requisito para compliance?
   :::{dropdown} Resposta
   Sem catálogo/lineage você não sabe onde estão os dados pessoais, tornando impossível atender direitos como exclusão e exportação.
   :::
5. Como manter valor analítico sem manter dado pessoal?
   :::{dropdown} Resposta
   Anonimizando de forma irreversível: dado verdadeiramente anônimo sai do escopo da LGPD, mas ainda serve para análises agregadas.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Chega um pedido de exclusão de dados de um cliente (LGPD). Como você atende, tecnicamente?"
  :::{dropdown} Resposta modelo
  Uso o catálogo/lineage para achar todas as tabelas com o identificador do titular. Onde a lei permite, apago os registros; onde há retenção obrigatória (fiscal, por exemplo), anonimizo os campos pessoais mantendo o que a lei exige. Confirmo réplicas/backups e registro o atendimento. Se o sistema foi projetado com chaves de titular rastreáveis e minimização, isso é viável no prazo.
  :::
- **P:** "Como você decide quais colunas do warehouse merecem proteção extra?"
  :::{dropdown} Resposta modelo
  Classifico as colunas: comuns, pessoais (nome/CPF/email) e sensíveis (saúde/raça/religião/biometria). As sensíveis recebem acesso mais restrito e mascaramento; as pessoais entram nas rotinas de direitos do titular e retenção. Essa classificação vira metadado no catálogo e orienta acesso, mascaramento e políticas de retenção.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Reis & Housley — Fundamentals of Data Engineering** (privacidade, conformidade, ciclo de vida).
- **Kleppmann — Designing Data-Intensive Applications** (apagar dados, integridade em escala).
- **Texto da LGPD (Lei 13.709/2018)** e materiais da ANPD — fontes primárias.

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — privacidade e conformidade. <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — apagamento e integridade. <!-- @kleppmann2017 -->
- Dehghani, Z. *Data Mesh Principles and Logical Architecture* (2020) — governança e privacidade na plataforma. <!-- @dehghani2020 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
