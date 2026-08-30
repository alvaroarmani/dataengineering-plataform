# Introdução a Infraestrutura como Código (Terraform)

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Criar o banco, o bucket, o cluster **clicando no console da cloud** não escala nem se repete:
ninguém sabe o que existe, por que, nem como recriar. **Infraestrutura como Código (IaC)**
resolve — você **declara** a infra em arquivos versionados, e uma ferramenta (o **Terraform**)
a cria/atualiza de forma reprodutível. É o mesmo princípio do resto do curso (versionar,
reproduzir), aplicado à nuvem.

## 💡 Conceito (o porquê)

### IaC: declarar, não clicar
Em vez de passos manuais, você escreve **o estado desejado** ("quero um bucket X e um banco Y")
em código versionado. Vantagens: **reprodutível** (recria idêntico), **versionado** (histórico,
revisão, PR), **auditável** e **colaborativo**. Clicar no console é o "funciona na minha máquina"
da infraestrutura.

### Terraform: declarativo + estado
- Você escreve recursos em **HCL** (`.tf`):
  ```hcl
  resource "aws_s3_bucket" "dados" {
    bucket = "meu-datalake"
  }
  ```
- **Declarativo:** você diz **o que** quer, não os passos. O Terraform calcula o **diff** entre o
  **desejado** (código) e o **atual** (o que existe) e faz só a diferença.
- **Providers:** plugins para cada plataforma (AWS, GCP, Azure, Postgres, etc.).

### O ciclo: plan e apply
- **`terraform plan`:** mostra **o que vai mudar** — o que será **criado**, **atualizado** ou
  **destruído** — sem aplicar. Você revisa antes.
- **`terraform apply`:** executa o plano, deixando a infra igual ao código.
- **`terraform destroy`:** remove o que foi criado.

### Estado (state)
O Terraform guarda um **state** — o mapa entre o código e os recursos reais. É comparando o state
com o código que ele decide o diff. Em time, o state fica **remoto** (ex.: um bucket) e
**travado** para dois não aplicarem ao mesmo tempo. **Nunca** edite o state na mão nem o commite
com segredos.

### Idempotência
Rodar `apply` de novo sem mudar o código **não faz nada** (a infra já bate com o desejado) — é
**idempotente**, como as boas cargas de dados (M9). É isso que torna IaC seguro de reexecutar.

## 🔎 Exemplo
A infra do seu pipeline (bucket do data lake, dataset do BigQuery, service account) em `.tf`
versionados. Um PR muda o código para adicionar um novo dataset; o **`plan`** no CI mostra
"1 to add, 0 to change, 0 to destroy"; revisado e mergeado, o **`apply`** cria só o dataset novo.
Recriar tudo em outra conta = `apply` num diretório limpo. Sem clicar em nada.

:::{admonition} 📖 Da literatura
:class: seealso
Reis & Housley incluem **IaC** nas fundações do DataOps: infraestrutura versionada e reprodutível
(Terraform) elimina configuração manual não-rastreável e permite recriar/auditar ambientes — a
mesma disciplina de versionar e reproduzir aplicada à nuvem. — *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Times provisionam data lakes, warehouses e permissões via Terraform em repositório, com `plan` no
CI (revisar o diff no PR) e `apply` no merge. O **state** fica remoto e travado; segredos nunca
vão no código nem no state versionado. — Reis & Housley (IaC/DataOps).
:::

## ⚠️ Erros comuns
- **Clicar no console** e depois "esquecer" — a infra real diverge do código (drift).
- Editar o **state** na mão ou commitá-lo com segredos — corrompe/vaza.
- Rodar **`apply` sem revisar o `plan`** — pode destruir recurso sem querer.
- State **local** em time — dois `apply` simultâneos corrompem; use state remoto travado.
- Segredos hardcoded no `.tf` — use variáveis/secret manager.

## 💼 O que o mercado espera
Entender IaC (declarar vs clicar), o ciclo `plan/apply`, o papel do **state** e a idempotência é
esperado em níveis pleno — muitas vagas pedem "noções de Terraform". Saber ler um `plan` é o mínimo.

:::{admonition} ✨ Em resumo
:class: resumo
- **IaC** declara a infra em código versionado — reprodutível, auditável, colaborativo (vs clicar no console).
- **Terraform** é declarativo: calcula o **diff** entre desejado (código) e atual (**state**) e aplica só a diferença.
- Ciclo **`plan`** (revisar o que muda: criar/atualizar/destruir) → **`apply`**.
- `apply` é **idempotente**; state fica **remoto/travado**; **segredos nunca** no código/state.
:::

## 🧠 Quiz de recall
1. O que é IaC e por que usar?
   :::{dropdown} Resposta
   Declarar a infraestrutura em código versionado (em vez de clicar no console): reprodutível, versionado/auditável e colaborativo.
   :::
2. O que o Terraform faz de "declarativo"?
   :::{dropdown} Resposta
   Você declara o estado desejado; ele calcula o diff entre o desejado (código) e o atual (state) e aplica só a diferença.
   :::
3. Diferença entre `plan` e `apply`?
   :::{dropdown} Resposta
   plan mostra o que vai mudar (criar/atualizar/destruir) sem aplicar; apply executa o plano, deixando a infra igual ao código.
   :::
4. Para que serve o state?
   :::{dropdown} Resposta
   É o mapa entre o código e os recursos reais; comparando state e código, o Terraform decide o diff. Em time fica remoto e travado.
   :::
5. Por que `apply` é idempotente?
   :::{dropdown} Resposta
   Rodar de novo sem mudar o código não faz nada, pois a infra já bate com o desejado — seguro de reexecutar.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Por que Terraform em vez de criar recursos no console?"
  :::{dropdown} Resposta modelo
  Reprodutibilidade e rastreabilidade: a infra vira código versionado, revisável por PR e recriável em qualquer conta. Evita drift ("clicaram algo e ninguém sabe"), permite auditar mudanças e aplicar via CI com plan/apply. Clicar no console é o "funciona na minha máquina" da infra.
  :::
- **P:** "O que é o state do Terraform e qual cuidado?"
  :::{dropdown} Resposta modelo
  É o mapa entre o código e os recursos reais, usado para calcular o diff. Cuidados: mantê-lo remoto e travado (para dois apply não colidirem), nunca editá-lo na mão e nunca commitá-lo com segredos.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Terraform docs** — *plan/apply*, *state*, *providers*.
- **Reis & Housley — Fundamentals of Data Engineering** (IaC nas fundações do DataOps).

## 📚 Referências
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — IaC e DataOps. <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — reprodutibilidade e operação. <!-- @kleppmann2017 -->
- Beauchemin, M. *The Rise of the Data Engineer* (2017) — engenharia aplicada a dados. <!-- @beauchemin2017 -->

*Acessado em: 2026-08-29.*

---
**Revisado em:** 2026-08-29
