# 2. População e amostragem

## População-alvo

Profissionais que **criam ou mantêm produtos de dados ou automação** em empresas brasileiras (dashboards, relatórios, bases ou extrações, pipelines, segmentações de campanha, automações com RPA, low-code ou scripts), nas áreas de análise de dados/BI, CRM/marketing analytics, engenharia e ciência de dados e automação de processos. Não existe cadastro dessa população, então seu tamanho é desconhecido e tratado como infinito no cálculo da margem de erro.

A inclusão é verificada no formulário: consentimento (TC1), filtro de pertencimento (F1) e área de atuação (P1). As regras de descarte estão na seção 5.

**Colegas da turma** não contam na amostra, porque a população é de profissionais, e não de estudantes. Como a pergunta que os identificava saiu após o pré-teste (seção 4), a exclusão é feita na divulgação (seção 8). Estudantes de outras turmas que trabalham na área contam normalmente, porque o critério é o vínculo profissional.

## Origem dos contatos e estratégia de amostragem

Os contatos vêm de três fontes: (1) a rede direta dos integrantes, com colegas e ex-colegas de trabalho e contatos do LinkedIn da área; (2) comunidades abertas de dados, BI e automação no WhatsApp, Telegram, Discord e LinkedIn; (3) indicações dos próprios respondentes. Nenhuma lista comprada ou extraída sem consentimento é usada.

A amostragem é **não probabilística, por conveniência, combinada com bola de neve**. Uma amostra probabilística exigiria uma lista da população, que não existe, e o grupo não tem acesso a cadastros de empresas ou associações. A conveniência é a única opção viável em 11 dias de coleta e é a estratégia mais comum em surveys de Engenharia de Software (Kitchenham e Pfleeger, 2008). A bola de neve alcança profissionais fora da rede direta do grupo.

**Consequência:** os resultados descrevem a amostra e **não são generalizados** para todos os profissionais da área. A amostra tende a se concentrar em perfis parecidos com os dos integrantes e em pessoas mais interessadas em métricas. Para tornar esse viés visível, o dashboard mostra o perfil da amostra (P1–P6) e permite filtrar por segmento (seção 7).

## Tamanho de amostra e margem de erro

Margem de erro de uma proporção com 95% de confiança, no pior caso (p = 0,5): **e = 1,96 × √(p(1 − p) / n)**.

| n válidas | Cálculo | Margem |
|---|---|---|
| 50 (mínimo) | 1,96 × √(0,25 / 50) | ± 13,9 p.p. |
| **60 (meta)** | 1,96 × √(0,25 / 60) | **± 12,7 p.p.** |
| 70 | 1,96 × √(0,25 / 70) | ± 11,7 p.p. |

**Meta: 60 respostas válidas (± 12,7 p.p.).** Prevendo cerca de 15% de descarte, a meta é de **70 respostas brutas**; o mínimo aceitável é de 50 válidas. Com n = 60, uma métrica citada por 40% dos respondentes tem intervalo de cerca de 27% a 53%. Por isso, uma métrica só é dita "mais usada" que outra quando a diferença supera a margem; diferenças menores são relatadas como empate. Em subgrupos a margem é maior (n = 15 → ± 25 p.p.), e o dashboard mostra o n de cada segmento. A fórmula supõe amostragem aleatória simples, então a margem não inclui o viés de seleção, e a incerteza real é maior.
