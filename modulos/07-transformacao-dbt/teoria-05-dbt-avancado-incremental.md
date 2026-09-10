# dbt avançado: modelos incrementais, materializations e CI

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Seu model dbt `fct_eventos` reconstrói **do zero** uma tabela de 2 bilhões de linhas toda madrugada —
30 minutos e uma fatura alta, só para agregar os **poucos milhares** de eventos novos do dia. Isso não
escala. A resposta é o **modelo incremental**: processar **só o que mudou** e anexar/mesclar ao que já
existe. Dominar incremental, as **materializations** certas, e um **CI de dados** que testa só o que
foi tocado é o que separa "sei rodar `dbt build`" de "opero dbt em produção, em escala" — o nível que
a FIAP e vagas de pleno/sênior cobram. Você já viu sources, marts, testes e snapshots (teorias 01–04);
aqui está a camada de **performance e operação**.

## 💡 Conceito (o porquê)

### As materializations e o trade-off de cada uma
Cada model dbt é materializado de um jeito, e a escolha é de arquitetura:
- **view:** só uma view (nada é gravado); leve para o build, mas recomputa a cada consulta. Bom para
  staging leve.
- **table:** reconstrói a tabela inteira a cada `dbt run`. Simples e rápido de consultar, mas **caro**
  quando a fonte é enorme (reprocessa tudo sempre).
- **incremental:** grava numa tabela, mas em cada run processa **só as linhas novas/alteradas** e as
  anexa/mescla. É a resposta para tabelas grandes que crescem — troca simplicidade por escala.
- **ephemeral:** não vira objeto no banco; é "inlined" (CTE) em quem o referencia. Bom para lógica
  intermediária reutilizável sem materializar.

### Como o incremental funciona: is_incremental() + unique_key
O model incremental tem duas execuções:
- **Primeira vez (full refresh):** cria a tabela processando tudo.
- **Execuções seguintes:** roda um filtro que pega **só o novo**. O padrão:
```sql
select * from {{ source('app','eventos') }}
{% if is_incremental() %}
  where updated_at > (select max(updated_at) from {{ this }})   -- só o que chegou depois
{% endif %}
```
O `{{ this }}` é a própria tabela já materializada; o `is_incremental()` é verdadeiro só a partir da
2ª run. Isso é um **watermark**: você guarda até onde já processou e só pega o que passou disso.

### Estratégias de incremental (o que fazer com o "novo")
Achado o delta, como integrá-lo?
- **append:** só insere as linhas novas. Rápido, para dados **imutáveis** (logs, eventos) — nunca
  atualiza o passado.
- **merge (upsert):** insere novas e **atualiza** as existentes por `unique_key` (a chave do grão).
  Para dados que mudam (um pedido que muda de status). É o mais comum.
- **insert_overwrite:** **substitui partições inteiras** (ex.: reprocessa o dia todo). Ideal com
  particionamento — combina com a idempotência por partição (M08/M09).

A escolha depende de os dados serem imutáveis (append) ou mutáveis (merge), e de haver particionamento
(insert_overwrite).

### O problema dos dados atrasados (late-arriving)
`where updated_at > max(updated_at)` tem uma armadilha: um evento que **chega atrasado** com timestamp
antigo (rede, correção retroativa) fica **abaixo do watermark** e é perdido. Defesas: uma **janela de
segurança** (`> max - 3 dias`, reprocessando uma sobreposição), `insert_overwrite` das últimas
partições, ou full-refresh periódico. Pensar em late data é a marca de quem já apanhou em produção.

### Testes avançados e CI de dados
Além dos testes genéricos (unique/not_null/relationships, teoria 03):
- **Testes singulares:** um `.sql` em `tests/` que falha se retornar linhas (ex.: "receita negativa").
- **Pacotes:** `dbt_utils`, `dbt_expectations` trazem testes prontos (accepted_range, etc.).
- **Contratos e versões:** dbt pode **impor o schema** de um model (contract) e versioná-lo — o data
  contract (M12) dentro do dbt.
- **Slim CI:** no Pull Request, rodar `dbt build --select state:modified+` testa **só os models que
  mudaram** (e seus dependentes), usando o *manifest* de estado — rápido e barato. É o CI de dados
  (M13) aplicado ao dbt.

### Exposures e lineage até o consumo
`exposures` declaram **quem consome** os models (um dashboard, um ML), estendendo o lineage (M14) até
o destino final — então o impact analysis mostra "se eu mudar este model, este dashboard quebra".

## 🔎 Exemplo
`fct_eventos` (2 bi de linhas) vira **incremental** com estratégia **merge** por `evento_id`: cada run
processa só `where updated_at > max(updated_at) - interval 2 days` (janela de segurança para late
data) e faz upsert — de 30 min para 30 s. Staging vira **view** (leve), uma agregação intermediária
vira **ephemeral**. No Pull Request, o **Slim CI** roda `state:modified+` (só o que mudou) com testes
`unique`/`not_null` + um teste singular de "valor >= 0" do `dbt_utils`. Um **exposure** liga o mart ao
dashboard de vendas. Mesma transformação, agora **escalável, testada e barata** em produção.

:::{admonition} 📖 Da literatura
:class: seealso
Beauchemin, em *Functional Data Engineering*, defende pipelines **idempotentes e particionados** —
exatamente a base do incremental (insert_overwrite/merge determinísticos). Reis & Housley tratam
transformação incremental e testes como práticas centrais do estágio de transformação. — *Functional
Data Engineering*; *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Quase todo model dbt "pesado" em produção é incremental — reconstruir tudo não escala nem no custo. E
o erro mais comum é o watermark ingênuo que perde dados atrasados; times maduros usam janela de
segurança ou insert_overwrite de partições. O Slim CI (`state:modified+`) é padrão para PRs de dbt
não levarem 40 minutos. — Beauchemin; prática de mercado.
:::

## ⚠️ Erros comuns
- **`table` para uma fonte gigante que só cresce** — reprocessa tudo sempre; use `incremental`.
- **Watermark ingênuo** (`> max`) — perde eventos atrasados; use janela de segurança/insert_overwrite.
- **merge sem `unique_key`** (ou chave errada) — duplica em vez de atualizar.
- **append em dado mutável** — nunca reflete atualizações do passado; use merge.
- **CI que roda tudo** em cada PR — lento e caro; use `state:modified+` (Slim CI).

## 💼 O que o mercado espera
Escolher a materialization certa, implementar modelos **incrementais** (is_incremental, unique_key,
estratégia append/merge/insert_overwrite), tratar **late-arriving data**, e montar **testes avançados +
Slim CI**. É o núcleo de operar dbt em escala — assunto certo em entrevistas de Analytics/Data
Engineering.

:::{admonition} ✨ Em resumo
:class: resumo
- **Materializations**: view (leve), table (reconstrói tudo), **incremental** (só o delta), ephemeral (CTE inline).
- **Incremental**: `is_incremental()` + watermark (`updated_at > max`) + `unique_key`; estratégias **append** (imutável), **merge/upsert** (mutável), **insert_overwrite** (partições).
- **Late-arriving data**: watermark ingênuo perde atrasados; use **janela de segurança** ou insert_overwrite.
- **Operação**: testes singulares/pacotes/contratos + **Slim CI** (`state:modified+`) + exposures (lineage até o consumo).
:::

## 🧠 Quiz de recall
1. Quando usar materialization incremental em vez de table?
   :::{dropdown} Resposta
   Quando a fonte é grande e cresce, e reconstruir tudo a cada run é caro/lento; o incremental processa só as linhas novas/alteradas e as anexa/mescla.
   :::
2. Como um model incremental sabe o que é "novo"?
   :::{dropdown} Resposta
   Com `is_incremental()` (verdadeiro a partir da 2ª run) e um filtro de watermark, tipo `where updated_at > (select max(updated_at) from {{ this }})`.
   :::
3. Diferencie append, merge e insert_overwrite.
   :::{dropdown} Resposta
   Append só insere (dados imutáveis); merge faz upsert por unique_key (dados que mudam); insert_overwrite substitui partições inteiras (reprocessa períodos, combina com particionamento).
   :::
4. Qual a armadilha dos dados atrasados no incremental?
   :::{dropdown} Resposta
   Um evento que chega atrasado com timestamp antigo fica abaixo do watermark (`> max`) e é perdido; a defesa é uma janela de segurança (`> max - N dias`) ou insert_overwrite das últimas partições.
   :::
5. O que é Slim CI no dbt?
   :::{dropdown} Resposta
   Rodar no PR só os models que mudaram e seus dependentes (`dbt build --select state:modified+`), usando o manifest de estado — muito mais rápido/barato que rodar tudo.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Um model dbt reconstrói uma tabela enorme toda noite e está caro. Como você resolve?"
  :::{dropdown} Resposta modelo
  Converto para materialization incremental: na 2ª run em diante, filtro só o delta com um watermark (`updated_at > max(updated_at)`), com `unique_key` para fazer merge/upsert dos registros que mudam (ou append se forem imutáveis, ou insert_overwrite por partição). Adiciono uma janela de segurança para não perder dados atrasados. Isso troca "reprocessar tudo" por "processar o delta", derrubando tempo e custo — e mantenho um full-refresh periódico por garantia.
  :::
- **P:** "Como você deixaria o CI do projeto dbt rápido num PR?"
  :::{dropdown} Resposta modelo
  Slim CI: em vez de `dbt build` completo, rodo `dbt build --select state:modified+`, que testa só os models alterados e seus dependentes, comparando com o manifest da produção. Assim o PR valida o que importa em segundos/minutos, não a árvore inteira. Combino com testes genéricos (unique/not_null/relationships), singulares e de pacotes (dbt_utils), rodando em GitHub Actions (M13).
  :::

## 🚀 Para ir além (leitura dirigida)
- **Beauchemin — Functional Data Engineering** (idempotência e particionamento, base do incremental).
- **Documentação do dbt** — incremental models, materializations, `state:` selection, contracts.
- **Reis & Housley — Fundamentals of Data Engineering** (transformação incremental e testes).

## 📚 Referências
- Beauchemin, M. *Functional Data Engineering* (2018) — pipelines idempotentes/particionados. <!-- @beauchemin2018 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — transformação e testes. <!-- @reis2022 -->
- Kimball, R.; Ross, M. *The Data Warehouse Toolkit* (2013) — cargas incrementais no DW. <!-- @kimball2013 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
