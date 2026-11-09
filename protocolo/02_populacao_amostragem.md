# 2. População e amostragem

## População-alvo

Profissionais que **criam ou mantêm produtos de dados ou automação** em empresas brasileiras: dashboards, relatórios, bases ou extrações para outras áreas, pipelines de dados, segmentações de campanha e automações de processo (RPA, low-code, scripts, workflows). Isso inclui as áreas de análise de dados/BI, CRM/marketing analytics, engenharia de dados, ciência de dados e automação de processos.

A população não tem cadastro (lista completa de membros), então o tamanho dela é desconhecido e tratado como infinito no cálculo da margem de erro.

## Critérios de inclusão e exclusão

Os critérios são aplicados por perguntas filtro no próprio formulário. Isso permite contar no dashboard quantas respostas foram descartadas por cada motivo.

| Critério | Item | Regra |
|---|---|---|
| Consentimento | TC1 | "Não concordo" → encerra o formulário; resposta descartada |
| Pertencer à população | F1 | "Não" (não cria nem mantém produtos de dados ou automação) → encerra o formulário; resposta descartada |
| Atenção | ATT | Valor diferente de "Discordo totalmente" → descartada |

**Colegas da turma.** O enunciado não permite que colegas da turma contem na amostra, a menos que a população-alvo seja de estudantes. Nossa população é de **profissionais**, então essa exceção não se aplica. A pergunta que identificava colegas da disciplina foi retirada após o pré-teste (ver seção 4). Agora a exclusão acontece **na divulgação**: o link não é enviado nos canais da turma (grupos e fóruns da disciplina) nem diretamente a colegas de MES (ver seção 8). Por isso, a exclusão depende do controle dos canais, e o risco de um colega receber o link por repasse é tratado como ameaça na seção 7. Estudantes de outras turmas ou cursos que já trabalham na área contam normalmente, porque o critério é o vínculo profissional (F1).

## Origem dos contatos

1. **Rede direta dos integrantes:** colegas de trabalho e ex-colegas nas empresas onde os integrantes trabalham ou estagiaram, e contatos do LinkedIn que atuam com dados, BI, CRM ou automação.
2. **Comunidades abertas:** grupos de WhatsApp, Telegram e Discord, além de comunidades do LinkedIn sobre dados, BI, Power BI, engenharia de dados e automação/RPA.
3. **Indicação (bola de neve):** a mensagem de divulgação pede que cada respondente repasse o link a outras pessoas da área.

Nenhum contato é feito a partir de listas compradas ou extraídas sem consentimento. O formulário não pede nome, e-mail nem empresa (ver seção 6).

## Estratégia de amostragem

A amostragem é **não probabilística, por conveniência, combinada com bola de neve**.

**Por que não probabilística.** Uma amostra probabilística exige uma lista da população em que cada pessoa tem uma chance conhecida de ser sorteada. Não existe essa lista para profissionais de dados e automação no Brasil, e o grupo não tem acesso a cadastros de empresas ou associações. Com duas semanas de coleta e sem recursos, a conveniência é a única opção viável. Ela é também a estratégia mais comum em surveys de Engenharia de Software (Kitchenham e Pfleeger, 2008).

**Por que bola de neve.** É uma população especializada, espalhada por áreas e empresas diferentes. A indicação entre pares alcança pessoas que não estão na rede direta dos integrantes nem nas comunidades abertas.

**Consequências.** Os resultados descrevem a amostra obtida e **não podem ser generalizados** para todos os profissionais da área no Brasil. A amostra tende a concentrar pessoas parecidas com os integrantes (região, setor, porte da empresa) e pessoas mais interessadas em métricas (autosseleção). Para tornar esse viés visível, o perfil da amostra (P1–P6) aparece no dashboard e a análise pode ser filtrada por segmento. Essas ameaças e suas mitigações estão na seção 7.

## Tamanho de amostra e margem de erro

A margem de erro de uma proporção, com 95% de confiança, é:

$$e = 1{,}96 \times \sqrt{\frac{p(1-p)}{n}}$$

Usamos o pior caso, p = 0,5, porque ele dá a maior margem possível e não depende de nenhum resultado prévio.

| n válidas | Cálculo (p = 0,5) | Margem de erro |
|---|---|---|
| 50 (mínimo do enunciado) | 1,96 × √(0,25 / 50) = 1,96 × 0,0707 | **± 13,9 p.p.** |
| **60 (meta)** | 1,96 × √(0,25 / 60) = 1,96 × 0,0645 | **± 12,7 p.p.** |
| 70 | 1,96 × √(0,25 / 70) = 1,96 × 0,0598 | ± 11,7 p.p. |
| 100 | 1,96 × √(0,25 / 100) = 1,96 × 0,0500 | ± 9,8 p.p. |

**Meta.** Queremos **60 respostas válidas**, com margem de erro de **± 12,7 p.p.** Prevendo cerca de 15% de descarte (fora da população, falha na pergunta de atenção, duplicadas), a meta de respostas brutas é de **70**. O mínimo aceitável é de 50 válidas (± 13,9 p.p.).

**Interpretação.** Com n = 60, se 40% dos respondentes disserem que acompanham uma métrica (QP1), o intervalo de confiança vai aproximadamente de 27% a 53%. Por isso, só vamos afirmar que uma métrica é "mais usada" que outra quando a diferença for maior que a margem de erro. Diferenças menores serão apresentadas como empate.

**Subgrupos.** A margem vale para a amostra inteira. Em subgrupos ela é maior: uma área com n = 15 tem margem de ± 25 p.p. Por isso, nas comparações entre áreas (QP2), as áreas com menos de 5 respostas são agrupadas em "Outras", e o dashboard mostra o n de cada segmento filtrado.

**Ressalva.** A fórmula assume amostragem aleatória simples. Como a nossa amostra é por conveniência, a margem de erro mede apenas o erro de amostragem aleatória. Ela não inclui o viés de seleção, então a incerteza real é maior que a margem calculada.
