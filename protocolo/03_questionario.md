# 3. Questionário com rastreabilidade

O questionário tem 23 itens em seis páginas do Google Forms, gerado por um script versionado no repositório (`questionario/criar_formulario.gs`). O tempo estimado é de 10 a 15 minutos, medido no pré-teste. Nome, e-mail e empresa não são coletados.

| Página | Conteúdo | Itens | Escala |
|---|---|---|---|
| 1 | Termo de consentimento; "Não concordo" leva direto ao envio | TC1 | Nominal |
| 2 | Filtro da população; "Não" leva direto ao envio | F1 | Nominal |
| 3 | Perfil: área, experiência, porte, setor, tamanho do time, ferramentas | P1–P6 | P1, P4, P6 nominais; P2, P3 ordinais; P5 razão |
| 4 | Métricas acompanhadas, medição de qualidade, retrabalho e falhas | M1–M4 | M1, M2 nominais; M3 ordinal; M4 razão |
| 5 | Dois construtos em grade Likert de 5 pontos e a pergunta de atenção | UT1–UT4, ATT, MM1–MM4 | Ordinal (1 = Discordo totalmente … 5 = Concordo totalmente) |
| 6 | Perguntas abertas, opcionais | A1, A2 | Aberta |

## Construtos medidos por mais de um item

| Construto | Itens | QP |
|---|---|---|
| **Utilidade percebida (UT)** | UT1: as métricas ajudam a decidir o que melhorar · UT2: refletem o valor das entregas · UT3: decisões sobre o trabalho se baseiam nelas · UT4 (R): acompanhar métricas toma tempo sem benefício real | QP2 |
| **Maturidade de medição (MM)** | MM1: o time define metas ou limites · MM2: as métricas são revisadas periodicamente · MM3: a coleta é automática · MM4 (R): cada pessoa mede do seu jeito, sem padrão | QP4 |

Os itens reversos (R) são invertidos (6 − resposta). O escore de cada construto é a média dos quatro itens, e sua confiabilidade é verificada pelo alfa de Cronbach (seção 5).

**Pergunta de atenção (ATT):** na grade de utilidade, entre UT3 e UT4, a linha *"Para mostrar que você está lendo com atenção, marque 'Discordo totalmente' nesta linha"*. Qualquer outra resposta leva ao descarte.

## Rastreabilidade

| QP | Itens | Variáveis de apoio |
|---|---|---|
| QP1 | M1, A1 | P1–P4 (segmentos) |
| QP2 | UT1–UT4 | P1 (grupos) |
| QP3 | M2 (grupo), M3 (principal), M4 (secundária) | — |
| QP4 | MM1–MM4 | P2 |
| Controle | TC1, F1, ATT | Regras de descarte (seção 5) |

O Apêndice A traz a matriz completa, com o texto de cada item, a métrica, a escala e a codificação.
