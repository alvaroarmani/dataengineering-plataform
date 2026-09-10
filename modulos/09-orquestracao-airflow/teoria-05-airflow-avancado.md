# Airflow avançado: dynamic mapping, deferrable, datasets e executores

<!-- tipo: conceitual -->

## 🎯 O problema (motivação)

Sua DAG precisa processar **N arquivos** que só existem em runtime (às vezes 3, às vezes 300) — mas você
não sabe N ao escrever o código. Outra DAG tem 500 **sensores** esperando arquivos chegarem, e cada um
**ocupa um worker** parado, entupindo o cluster. E o pipeline de marketing só deveria rodar **quando** o
de vendas termina de atualizar a tabela — mas está preso a um horário fixo que às vezes dispara cedo
demais. Estes são os limites do Airflow "básico" (teorias 01–04), e resolvê-los — **dynamic task
mapping**, **deferrable operators**, **data-aware scheduling** e a escolha do **executor** — é o que a
FIAP e vagas de pleno esperam de quem opera orquestração em escala.

## 💡 Conceito (o porquê)

### O modelo mental: DAG = grafo de dependências
Antes do avançado, fixe o núcleo: uma DAG é um **grafo dirigido acíclico** de tasks. O scheduler
resolve a **ordem topológica** (uma task só roda depois de todas as suas *upstream*) e, a cada momento,
a **fronteira** de tasks "prontas" é aquela cujas dependências **já concluíram**. Todo o avançado abaixo
é sobre **como** essa fronteira é construída, disparada e escalada.

### Dynamic Task Mapping: paralelismo que não se conhece em tempo de escrita
Quando o número de tarefas **depende dos dados** (N arquivos, N partições descobertas em runtime), você
não escreve N tasks à mão. O **dynamic task mapping** (`.expand()`) cria as instâncias **em tempo de
execução**, uma por item de uma lista produzida por uma task anterior:
```python
arquivos = listar_arquivos()          # retorna, em runtime, ["a.csv", "b.csv", ...]
processar.expand(caminho=arquivos)    # cria 1 task por arquivo, dinamicamente
```
É o padrão fan-out/fan-in nativo — a DAG se adapta ao volume de dados de cada execução.

### Deferrable operators: esperar sem ocupar worker
Um sensor "clássico" que espera um arquivo fica **em poll**, ocupando um slot de worker o tempo todo —
500 sensores = 500 workers presos. Os **deferrable operators** (triggers, sobre asyncio) resolvem: a
task **se suspende** e devolve o worker, e um processo leve (o *triggerer*) a **reativa** quando a
condição ocorre. Milhares de "esperas" concorrentes sem consumir o cluster — é a concorrência I/O-bound
(M03) aplicada à orquestração.

### Data-aware scheduling: disparar por dado, não por relógio
Em vez de agendar a DAG de marketing para "07h e torça para vendas já ter terminado", o Airflow moderno
agenda **por Dataset**: a DAG de vendas **produz** um dataset; a de marketing **é disparada** quando
esse dataset é atualizado. É **orquestração orientada a dados** — elimina o acoplamento frágil por
horário e cria um lineage de execução entre DAGs.

### TaskGroups, pools, prioridade e trigger rules
Ferramentas de controle em DAGs grandes:
- **TaskGroups:** agrupam tasks visual e logicamente (organização, não isolamento).
- **Pools:** limitam a concorrência de um recurso escasso (ex.: no máximo 5 tasks batendo no mesmo
  banco ao mesmo tempo), evitando sobrecarga. **priority_weight** decide quem roda primeiro na fila.
- **Trigger rules:** por padrão uma task roda se todas as upstream tiveram sucesso (`all_success`); mas
  há `all_done`, `one_failed`, `none_failed_min_one_success` — para tasks de limpeza/alerta que devem
  rodar mesmo se algo falhou, ou branches condicionais.

### Executores: onde as tasks realmente rodam
O **executor** define o modelo de execução, e a escolha é de arquitetura:
- **SequentialExecutor:** uma task por vez (só dev/teste).
- **LocalExecutor:** paralelismo numa máquina (bom para começar; é o da bancada).
- **CeleryExecutor:** fila de workers distribuídos (escala horizontal em várias máquinas).
- **KubernetesExecutor:** cada task vira um **pod** efêmero (isolamento e elasticidade — M20); sobe para
  a task e some ao terminar.

Escala e isolamento sobem de Sequential → Local → Celery/Kubernetes.

### SLAs e o que não deixar quebrar em silêncio
Um **SLA** define "esta task deveria terminar até X"; se estourar, o Airflow **alerta** — a diferença
entre descobrir o atraso no dashboard quebrado e ser avisado a tempo. Combina com a observabilidade
(teoria 04) para operar com confiança.

## 🔎 Exemplo
Uma DAG ingere um número **variável** de arquivos por dia: uma task lista os arquivos e
`processar.expand()` cria dinamicamente uma instância por arquivo (dynamic mapping). Ela espera os
arquivos chegarem com um **deferrable sensor** (não ocupa worker enquanto aguarda). Um **pool** limita a
5 as gravações simultâneas no warehouse. Ao concluir, a DAG **produz um Dataset**; a DAG de relatórios é
disparada **por esse Dataset** (data-aware), não por horário. Tudo roda no **KubernetesExecutor** (cada
task num pod efêmero) com **SLAs** que alertam se a carga passar de 06h. Orquestração que se adapta ao
dado, escala e avisa quando algo foge do esperado.

:::{admonition} 📖 Da literatura
:class: seealso
Beauchemin — criador do Airflow — enquadra a orquestração como **pipelines como código** e DAGs
versionadas, com o scheduler resolvendo dependências. Reis & Housley tratam orquestração, agendamento
orientado a eventos/dados e escala de execução como pilares do estágio de transformação/serving. — *The
Rise of the Data Engineer*; *Fundamentals of Data Engineering*.
:::

:::{admonition} 🏭 Do mundo real
:class: important
Dois erros caros em produção: (1) criar tasks fixas para um volume variável — o certo é dynamic mapping;
(2) 500 sensores clássicos entupindo os workers — o certo é deferrable. E o agendamento por horário
("roda 07h e torce") é frágil; times maduros migram para data-aware scheduling (Datasets) para disparar
pela dependência real de dados. — Beauchemin; prática de mercado.
:::

## ⚠️ Erros comuns
- **Tasks fixas para volume variável** — use dynamic task mapping (`.expand`).
- **Sensores clássicos em massa** ocupando workers — use deferrable operators.
- **Agendar por horário e torcer** — acople por dado (Datasets/data-aware), não por relógio.
- **Sem pools** — muitas tasks batendo no mesmo recurso o derrubam; limite a concorrência.
- **Executor errado** — Sequential/Local não escalam para produção pesada; use Celery/Kubernetes.

## 💼 O que o mercado espera
Aplicar dynamic task mapping, deferrable operators, data-aware scheduling (Datasets), pools/trigger
rules e escolher o executor certo (Local/Celery/Kubernetes), além de SLAs. É o que distingue "escrevo
DAGs" de "opero Airflow em escala" — assunto de entrevista de pleno/sênior.

:::{admonition} ✨ Em resumo
:class: resumo
- DAG = grafo; o scheduler roda em **ordem topológica** e dispara a **fronteira** de tasks com dependências concluídas.
- **Dynamic task mapping** (`.expand`) cria tasks em runtime conforme o volume; **deferrable operators** esperam sem ocupar worker.
- **Data-aware scheduling (Datasets)** dispara por dado atualizado, não por relógio; **pools/trigger rules/TaskGroups** controlam concorrência e fluxo.
- **Executor** = escala/isolamento: Sequential → Local → Celery → **Kubernetes** (pod por task); **SLAs** alertam atrasos.
:::

## 🧠 Quiz de recall
1. Como o scheduler decide o que rodar a cada momento?
   :::{dropdown} Resposta
   Resolve a ordem topológica do DAG e dispara a "fronteira" de tasks cujas dependências (upstream) já concluíram; uma task só roda depois de todas as suas upstream.
   :::
2. Quando usar dynamic task mapping?
   :::{dropdown} Resposta
   Quando o número de tarefas depende dos dados e só é conhecido em runtime (N arquivos/partições); `.expand()` cria uma instância por item de uma lista produzida por uma task anterior.
   :::
3. Que problema os deferrable operators resolvem?
   :::{dropdown} Resposta
   Sensores clássicos ocupam um worker enquanto esperam; os deferrable suspendem a task e devolvem o worker, sendo reativados por um triggerer quando a condição ocorre — milhares de esperas sem consumir o cluster.
   :::
4. O que é data-aware scheduling?
   :::{dropdown} Resposta
   Agendar DAGs por atualização de Dataset em vez de horário: uma DAG produz um dataset e outra é disparada quando ele muda, eliminando o acoplamento frágil por relógio.
   :::
5. Diferencie LocalExecutor de KubernetesExecutor.
   :::{dropdown} Resposta
   LocalExecutor paraleliza tasks numa máquina; KubernetesExecutor roda cada task num pod efêmero (isolamento e elasticidade, escala horizontal), que sobe para a task e some ao terminar.
   :::

## 🎤 Q&A estilo entrevista
- **P:** "Sua DAG precisa processar um número variável de arquivos por dia. Como modela?"
  :::{dropdown} Resposta modelo
  Com dynamic task mapping: uma task lista os arquivos em runtime e `processar.expand(caminho=arquivos)` cria uma instância por arquivo, adaptando o paralelismo ao volume do dia. Se preciso esperar os arquivos chegarem, uso um deferrable sensor (não ocupa worker), limito a concorrência de escrita com um pool, e rodo no KubernetesExecutor para isolamento/elasticidade. Assim a DAG escala com o dado sem eu fixar N no código.
  :::
- **P:** "A DAG B só deveria rodar quando a A termina de atualizar uma tabela. Como fazer sem depender de horário?"
  :::{dropdown} Resposta modelo
  Data-aware scheduling: a DAG A declara que produz um Dataset (a tabela); a DAG B é agendada por esse Dataset, disparando quando ele é atualizado. Isso remove o "roda 07h e torce" e cria uma dependência de dados explícita entre DAGs. Alternativamente, um sensor deferrable, mas Datasets é a forma nativa e mais limpa no Airflow moderno.
  :::

## 🚀 Para ir além (leitura dirigida)
- **Documentação do Airflow** — dynamic task mapping, deferrable operators, Datasets, executors, pools.
- **Beauchemin — The Rise of the Data Engineer** (orquestração como pipelines-como-código).
- **Reis & Housley — Fundamentals of Data Engineering** (orquestração e agendamento).

## 📚 Referências
- Beauchemin, M. *The Rise of the Data Engineer* (2017) — orquestração e DAGs (criador do Airflow). <!-- @beauchemin2017 -->
- Reis, J.; Housley, M. *Fundamentals of Data Engineering* (2022) — orquestração e escala. <!-- @reis2022 -->
- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — fluxos de trabalho e dataflow. <!-- @kleppmann2017 -->

*Acessado em: 2026-09-09.*

---
**Revisado em:** 2026-09-09
