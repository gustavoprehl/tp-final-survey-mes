# Plano de Ação — TP Final: Survey Pré-Registrado

**Integrantes:** Arthur Panzera · Diogo Brunoro · Gustavo Prehl
**Entregas:** Parte 1 (Planejamento, 2 pts) em **12/11/2026** · Parte 2 (Dashboard e evidências, 8 pts) em **26/11/2026**
**Ferramenta do dashboard:** Streamlit (Python), lendo o CSV bruto exportado do formulário
**Tema:** uso de métricas na avaliação de produtos de dados e automação (dashboards, bases, pipelines e automações de processo). Ver [matriz de rastreabilidade](../questionario/matriz_rastreabilidade.md)

O acompanhamento das tarefas é feito no [GitHub Projects](https://github.com/users/gustavoprehl/projects/7). Cada tarefa é uma issue com responsável, início, prazo e critério de pronto.

---

## 1. Estratégia geral

O prazo entre as entregas é de apenas duas semanas, e a coleta só pode começar **depois** do commit do protocolo. Por isso:

1. **Antecipar a Parte 1.** Meta interna: protocolo commitado e com tag `protocolo-v1` até **11/11**, um dia antes do prazo. Isso dá 11 dias de coleta (12/11 a 22/11).
2. **Construir o dashboard em paralelo à coleta.** Durante o desenvolvimento, o dashboard usa o CSV do pré-teste ou dados sintéticos, guardados em `dados/sinteticos/` e identificados como tal. Esses dados **nunca** entram na análise final, já que o enunciado trata dados fabricados como fraude acadêmica.
3. **Meta de coleta com folga.** O mínimo são 50 respostas válidas. A meta é de **70 respostas brutas**, porque parte delas será descartada (pergunta de atenção, respostas incompletas, pessoas fora da população).
4. **Todos dominam tudo.** A arguição é individual e cobre o estudo inteiro. Toda seção escrita por alguém é revisada por outro integrante, e o ensaio final inclui perguntas cruzadas.

## 2. Divisão de responsabilidades

| Integrante | Frente principal | Parte 1 (protocolo) | Parte 2 (dashboard e evidências) |
|---|---|---|---|
| **Gustavo** | Instrumento e dashboard | §1 GQM e QPs · §3 Questionário e rastreabilidade · Google Forms · Consolidação do PDF e commit | Esqueleto Streamlit · Perfil da amostra · Likert divergente · Filtros por segmento · 2º codificador das respostas abertas |
| **Diogo** | Amostragem e estatística | §2 População e amostragem · §5 Plano de análise · §8 Plano de divulgação | Execução da divulgação e capturas datadas · Testes por QP, tamanho de efeito, correção de Holm e margem de erro · Alfa de Cronbach · Página de resultados por QP |
| **Arthur** | Qualidade dos dados, ética e validade | §4 Pré-teste · §6 Ética e LGPD · §7 Ameaças à validade | Pipeline de limpeza e descartes · Exportação bruta e evidências · Codificação das respostas abertas · Página de metodologia, desvios e limitações |
| **Todos** | — | Kickoff e tema · Revisão cruzada | Divulgação nas próprias redes · Análise final · Ensaio da defesa |

### Correspondência com os critérios de avaliação

| Critério | Pts | Responsável principal |
|---|---|---|
| Objetivo GQM, QPs e rastreabilidade do questionário | 0,75 | Gustavo |
| Amostragem, tamanho de amostra e margem de erro | 0,5 | Diogo |
| Plano de análise coerente com as escalas; ética e LGPD | 0,5 | Diogo (análise) · Arthur (ética) |
| Pré-teste e ameaças à validade | 0,25 | Arthur |
| Evidências da coleta e consistência com o protocolo | 2,0 | Arthur · Diogo |
| Qualidade dos dados: limpeza, descartes e confiabilidade | 1,5 | Arthur · Diogo |
| QPs respondidas com testes, efeitos e visualizações | 2,0 | Diogo · Gustavo |
| Desvios em relação ao protocolo e limitações | 0,5 | Arthur |
| Defesa ao vivo | 2,0 | Todos |

## 3. Cronograma

### Parte 1 — Planejamento (30/10 a 11/11; prazo oficial 12/11)

| Período | Tarefa | Responsável |
|---|---|---|
| 31/10 – 01/11 | Kickoff: escolher o tema e rascunhar o objetivo GQM | Todos |
| até 02/11 | §1 Objetivo GQM e 2 a 4 questões de pesquisa, com hipóteses | Gustavo |
| 02/11 – 04/11 | §2 População, amostragem, tamanho de amostra e margem de erro | Diogo |
| 02/11 – 04/11 | §3 Questionário e matriz de rastreabilidade | Gustavo |
| 02/11 – 04/11 | §6 Ética e LGPD (TCLE, anonimização, armazenamento) | Arthur |
| 04/11 – 05/11 | Montar o Google Forms com o TCLE na primeira página | Gustavo |
| 04/11 – 06/11 | §5 Plano de análise | Diogo |
| 04/11 – 06/11 | §8 Plano de divulgação | Diogo |
| 04/11 – 06/11 | §7 Ameaças à validade | Arthur |
| 05/11 – 07/11 | §4 Pré-teste com 3 a 5 pessoas e registro das mudanças | Arthur |
| 07/11 – 08/11 | Consolidar o PDF (até 6 páginas) | Gustavo |
| 08/11 | Revisão cruzada do protocolo | Todos |
| **11/11** | **Commit, tag `protocolo-v1` e envio na plataforma. Só depois disso o formulário é aberto.** | Gustavo |

### Parte 2 — Coleta, dashboard e defesa (12/11 a 26/11)

| Período | Tarefa | Responsável |
|---|---|---|
| 12/11 – 22/11 | Divulgação nos canais planejados, com capturas de tela datadas | Diogo |
| 12/11 – 22/11 | Divulgação nas redes de cada integrante e acompanhamento diário da contagem | Todos |
| 10/11 – 14/11 | Esqueleto do dashboard Streamlit lendo o CSV bruto | Gustavo |
| 12/11 – 17/11 | Pipeline de limpeza e descartes, com o motivo de cada um | Arthur |
| 12/11 – 19/11 | Módulo estatístico: testes, p-valor, tamanho de efeito, Holm e margem de erro | Diogo |
| 15/11 – 20/11 | Página de perfil da amostra e descartes | Gustavo |
| 15/11 – 21/11 | Gráficos Likert divergentes e filtros por segmento | Gustavo |
| 17/11 – 19/11 | Confiabilidade dos construtos (alfa de Cronbach) | Diogo |
| 20/11 – 23/11 | Página de resultados por QP | Diogo |
| 20/11 – 24/11 | Página de metodologia, desvios e limitações | Arthur |
| **22/11** | **Encerramento da coleta** | — |
| 23/11 | Exportação bruta datada e pacote de evidências, sem dados pessoais | Arthur |
| 23/11 – 24/11 | Codificação das respostas abertas, com dois codificadores | Arthur · Gustavo |
| 23/11 – 24/11 | Análise final e conclusões dentro da margem de erro | Todos |
| 25/11 | Ensaio: demo de 10 min, simulação de mudança de cenário e arguição cruzada | Todos |
| **26/11** | **Apresentação e defesa** | Todos |

## 4. Pontos de controle

- **Contagem de respostas:** quem estiver de plantão na semana posta diariamente no grupo o número de respostas brutas. Se em 17/11 houver menos de 35, o grupo ativa os canais reserva previstos no §8.
- **Desvios:** toda mudança em relação ao protocolo (pergunta alterada, canal novo, teste trocado) é registrada **no mesmo dia** em `docs/DESVIOS.md`, com data, o que mudou e por quê. Esse arquivo alimenta a página de metodologia do dashboard.
- **Dados pessoais:** o repositório guarda apenas dados anonimizados. Se o formulário coletar e-mail (para sorteio, por exemplo), esse campo fica fora do repositório, em uma pasta restrita do Drive, e é removido antes de qualquer export.

## 5. Estrutura do repositório

```
├── Enunciado.md
├── docs/
│   ├── PLANO_DE_ACAO.md     ← este arquivo
│   └── DESVIOS.md           ← registro de desvios em relação ao protocolo
├── protocolo/               ← fonte e PDF do protocolo (Parte 1)
├── questionario/            ← matriz de rastreabilidade, TCLE, registro do pré-teste
├── dados/
│   ├── brutos/              ← export anonimizado do formulário (lido pelo dashboard)
│   └── sinteticos/          ← dados de desenvolvimento, nunca usados na análise
├── dashboard/               ← app Streamlit
└── evidencias/              ← capturas datadas e export bruto, sem dados pessoais
```
