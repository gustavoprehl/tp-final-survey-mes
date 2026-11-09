# 3. Questionário com rastreabilidade

## Estrutura

O questionário é aplicado pelo Google Forms, gerado por script versionado no repositório (`questionario/criar_formulario.gs`). Tem 23 itens em seis páginas, com tempo estimado de 10 a 15 minutos (medido no pré-teste). Não coleta nome, e-mail nem empresa.

| Página | Conteúdo | Itens |
|---|---|---|
| 1 | Termo de consentimento; quem não concorda vai direto ao envio | TC1 |
| 2 | Filtro da população; quem não trabalha com produtos de dados ou automação vai direto ao envio | F1 |
| 3 | Perfil, usado como segmento nas análises | P1–P6 |
| 4 | Métricas usadas, qualidade dos dados e retrabalho | M1–M4 |
| 5 | Percepções: dois construtos em grade Likert de 5 pontos e a pergunta de atenção | UT1–UT4, ATT, MM1–MM4 |
| 6 | Perguntas abertas, opcionais | A1, A2 |

## Escalas

| Escala | Itens |
|---|---|
| Nominal | TC1, F1, P1, P4, P6 (múltipla), M1 (múltipla), M2, ATT |
| Ordinal | P2, P3, M3, UT1–UT4, MM1–MM4 (Likert: Discordo totalmente = 1 … Concordo totalmente = 5) |
| Razão | P5 (pessoas no time), M4 (nº de falhas em 30 dias) |
| Aberta | A1, A2 |

## Construtos medidos por mais de um item

| Construto | Itens | QP |
|---|---|---|
| **Utilidade percebida das métricas (UT)** | UT1: as métricas ajudam a decidir o que melhorar · UT2: as métricas refletem o valor das entregas · UT3: decisões sobre o trabalho se baseiam nas métricas · UT4 (R): acompanhar métricas toma tempo sem benefício real | QP2 |
| **Maturidade de medição do time (MM)** | MM1: o time define metas ou limites para as métricas · MM2: as métricas são revisadas periodicamente · MM3: a coleta é automática · MM4 (R): cada pessoa mede do seu jeito, sem padrão | QP4 |

Cada construto tem um item reverso (R), que é invertido (6 − resposta) antes do cálculo. O escore é a média dos quatro itens. A confiabilidade é verificada pelo alfa de Cronbach, com limiar de 0,70.

## Pergunta de atenção

Na grade de utilidade, entre UT3 e UT4, há a linha *"Para mostrar que você está lendo com atenção, marque 'Discordo totalmente' nesta linha"* (ATT). Respostas com outro valor são descartadas como descuidadas ou automáticas.

## Rastreabilidade

| QP | Itens que a respondem | Variáveis de apoio |
|---|---|---|
| QP1 | M1, A1 | P1–P4 (segmentos) |
| QP2 | UT1–UT4 | P1 (grupos) |
| QP3 | M2 (grupo), M3 (principal), M4 (secundária) | — |
| QP4 | MM1–MM4 | P2 |
| Controle | TC1, F1, ATT | Regras de descarte (seção 5) |

A matriz completa, com o texto de cada item, a métrica, a escala e a codificação, está no Apêndice A (`questionario/matriz_rastreabilidade.md`).
