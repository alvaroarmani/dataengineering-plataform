# Método de Aprendizado

Ter bom material não basta — a maioria desiste ou esquece. Este método é desenhado para
você **concluir** e **reter**, terminando **empregável**. Leia antes de começar.

## O ciclo de cada unidade

```{mermaid}
flowchart LR
    P[Problema motivador] --> T[Teoria: o porquê]
    T --> L[Lab guiado]
    L --> E[Exercício: faça o pytest passar]
    E --> S[Solução comentada]
    S --> R[Reflexão Feynman]
    R -->|revisão espaçada| P
```

1. **Problema motivador** — primeiro a dor, depois a ferramenta. Você entende *por que* aquilo existe.
2. **Teoria (o porquê)** — conceito + fonte primária. Não decoreba de API.
3. **Lab guiado** — código que roda, passo a passo.
4. **Exercício autocorrigível** — "faça o `pytest` passar". Feedback objetivo.
5. **Solução comentada** — liberada **após** você passar; compare seu raciocínio.
6. **Reflexão (Feynman)** — escreva no [diário](diario.md): "o que eu ensinaria disso?". Se não consegue explicar, não entendeu ainda.

## Retenção: revisão espaçada + interleaving

Você **vai** esquecer se só seguir em frente. Por isso:

- **Flashcards** por módulo (`flashcards.md`) — revise nos **dias de revisão** do [plano de estudos](plano-de-estudos.md).
- **Checkpoints cumulativos** por eixo misturam conteúdo antigo com novo (*interleaving*).
- Regra prática: revise um tópico **1 dia**, **1 semana** e **1 mês** depois.

## Progressão por maestria (não por tempo)

Só avance quando **dominar**. Cada módulo tem um critério objetivo:

- `pytest` verde nos exercícios · Quiz de recall ≥ 80% · Projeto conforme rubrica.

Se você **já sabe** um tema, faça o **diagnóstico** ("testar para pular") e siga em frente.

## Quando travar (feedback estando sozinho)

Travar faz parte — saber destravar é *skill de DE*:

1. **Leia o erro de verdade** (traceback: última linha primeiro, depois de baixo para cima).
2. **Reproduza mínimo** (isole o menor caso que falha).
3. **Consulte a doc oficial** (não o primeiro blog aleatório).
4. **Use as dicas progressivas** do exercício (hint ladder) antes da solução.
5. **IA como tutor Socrático:** peça para te *guiar com perguntas*, não para entregar a resposta. Ex.: "não me dê o código; me faça perguntas para eu achar o bug".

## Anti-desistência

- **Diário** (`diario.md`): registre o que aprendeu e as dúvidas — metacognição.
- **Build-in-public:** publique cada projeto no GitHub com README. Progresso visível motiva.
- **Hábito diário** e **dashboard** (streak, mapa vivo) — ver [Dashboard](dashboard.md).

---
**Revisado em:** 2026-08-20
