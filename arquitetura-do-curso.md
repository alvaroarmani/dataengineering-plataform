# Arquitetura do Curso (big picture)

Este é o **quebra-cabeça completo** que você monta ao longo do curso. Cada eixo constrói
uma peça desta máquina — da ingestão ao Data Warehouse consumível — culminando no **TCC**.
Volte a esta página ao terminar cada eixo: você vai reconhecer cada vez mais partes.

## O sistema completo (alvo do TCC)

```{mermaid}
flowchart LR
    subgraph FONTES[Fontes de dados]
        API[APIs públicas]
        CSV[Arquivos / OLTP]
    end

    subgraph ING[Ingestão · Eixo 3]
        I[Ingestão batch/incremental<br/>Python + Airflow]
    end

    subgraph LAKE[Armazenamento · Eixo 4]
        B[(bronze / raw<br/>Parquet em MinIO)]
    end

    subgraph TRANS[Transformação · Eixo 2]
        S[(silver<br/>limpo/conformado)]
        G[(gold · star schema<br/>dbt sobre BigQuery)]
    end

    subgraph CONS[Consumo]
        BI[Analytics / BI / SQL]
    end

    API --> I
    CSV --> I
    I --> B --> S --> G --> BI

    ORQ[Orquestração · Airflow<br/>idempotente, agendada]:::cross -.coordena.-> I
    QA[Qualidade & Observabilidade · Eixo 4]:::cross -.valida.-> S
    GOV[Governança / LGPD · Eixo 4]:::cross -.protege.-> LAKE
    DOCK[Docker / DataOps · Eixo 3-4]:::cross -.empacota.-> ING

    classDef cross fill:#ffe9b3,stroke:#5a4300,color:#5a4300;
```

## Qual eixo constrói qual peça

| Peça da arquitetura | Onde você aprende |
|---|---|
| Fundamentos (Python, SQL, Git, Docker) | **Eixo 1** |
| Modelagem dimensional + DW + dbt (silver/gold) | **Eixo 2** |
| Ingestão + orquestração (Airflow) + containers | **Eixo 3** |
| Escala (Spark), lake/lakehouse, qualidade, governança | **Eixo 4** |
| Integração de tudo em um DW completo | **TCC** |

## Como ler este mapa ao longo do curso

- **Terminou o Eixo 1?** Você já entende os blocos e sabe programar/consultar cada um.
- **Eixo 2?** As caixas *silver/gold* e o *star schema* deixam de ser abstração.
- **Eixo 3?** A *ingestão* e a *orquestração* (setas tracejadas) passam a fazer sentido.
- **Eixo 4?** As *correntes de fundo* (qualidade, governança, DataOps) se encaixam.
- **TCC?** Você constrói a máquina inteira, ponta a ponta.

Veja o detalhamento do alvo final em [Especificação do TCC](tcc/especificacao-dw.md).

---
**Revisado em:** 2026-08-20
