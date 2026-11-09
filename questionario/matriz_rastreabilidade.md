# Matriz de rastreabilidade do questionário

**Tema:** uso de métricas na avaliação de produtos de dados e automação (dashboards, relatórios, bases, pipelines e automações de processo) em empresas brasileiras.

**Objetivo (GQM):** analisar *o uso de métricas em produtos de dados e automação*, com o propósito de *caracterizá-lo*, com respeito a *quais métricas são usadas de fato e como sua utilidade é percebida*, do ponto de vista de *profissionais de dados, BI, CRM e automação*, no contexto de *empresas brasileiras*.

O formulário é gerado por [criar_formulario.gs](criar_formulario.gs). Ao alterar um item lá, altere aqui também e registre a mudança em [docs/DESVIOS.md](../docs/DESVIOS.md) se for depois da tag `protocolo-v1`.

## Questões de pesquisa

| QP | Pergunta | Hipóteses | Itens | Análise prevista |
|---|---|---|---|---|
| **QP1** | Quais métricas os profissionais de dados e automação usam de fato para avaliar suas entregas? | Descritiva, sem hipótese | M1, A1 | Proporção de cada métrica com margem de erro (IC 95%) |
| **QP2** | A utilidade percebida das métricas difere entre áreas de atuação? | H0: a distribuição de UT é igual entre áreas. H1: ao menos uma área difere | UT1–UT4, P1 | Kruskal-Wallis, ε², pós-teste de Dunn com Holm |
| **QP3** | Quem mede a qualidade dos dados de forma estruturada relata menos retrabalho? | H0: retrabalho igual entre os grupos. H1: menor no grupo que mede | M2, M3, M4 | Mann-Whitney, correlação rank-biserial *r* |
| **QP4** | A maturidade de medição do time está associada ao tempo de experiência do profissional? | H0: ρ = 0. H1: ρ ≠ 0 | MM1–MM4, P2 | Correlação de Spearman ρ |

Os testes inferenciais (QP2, QP3, QP4) recebem correção de Holm, com α = 0,05.

## Itens

Codificação Likert: Discordo totalmente = 1 … Concordo totalmente = 5. Itens marcados com **(R)** são reversos: valor = 6 − resposta.

| Código | Item (texto no formulário) | QP | Métrica | Escala | Codificação / uso |
|---|---|---|---|---|---|
| TC1 | Você leu o termo acima e concorda em participar da pesquisa? | — | Consentimento | Nominal | "Não concordo" → descarte |
| F1 | No seu trabalho atual, você cria ou mantém produtos de dados ou automação? | — | Pertencimento à população | Nominal | "Não" → descarte |
| P1 | Qual é a sua área de atuação principal? | QP2 | Área de atuação | Nominal | Grupo da QP2; segmento do dashboard. Áreas com n < 5 são agrupadas em "Outras" |
| P2 | Há quanto tempo você trabalha com dados ou automação? | QP4 | Tempo de experiência | Ordinal | 1 (< 1 ano) … 5 (> 10 anos); segmento |
| P3 | Qual é o porte da empresa em que você trabalha? | — | Porte da empresa | Ordinal | 1 … 4; "Não sei" = ausente; segmento |
| P4 | Qual é o setor da empresa? | — | Setor | Nominal | Segmento; descritivo |
| P5 | Quantas pessoas fazem parte do seu time direto (incluindo você)? | — | Tamanho do time | Razão | Descritivo (mediana, IIQ) |
| P6 | Quais ferramentas você usa com frequência no trabalho? | — | Ferramentas | Nominal (múltipla) | Uma variável 0/1 por opção; descritivo |
| M1 | Quais indicadores o seu time acompanha regularmente para saber se as entregas (dashboards, relatórios, bases, automações) estão funcionando bem? | QP1 | Métricas adotadas | Nominal (múltipla) | Uma variável 0/1 por métrica; % de adoção ± margem de erro |
| M2 | O seu time mede a qualidade dos dados de forma estruturada? | QP3 | Medição formal de qualidade | Nominal | Sim (automatizada ou manual) = 1; Não = 0; "Não sei" fica fora da QP3 |
| M3 | Nos últimos 3 meses, com que frequência você precisou refazer ou corrigir uma entrega por causa de problemas nos dados? | QP3 | Frequência de retrabalho | Ordinal | Nunca = 1 … Sempre = 5; variável dependente principal da QP3 |
| M4 | Nos últimos 30 dias, quantas vezes uma entrega sob sua responsabilidade falhou ou exibiu dados incorretos? | QP3 | Nº de falhas | Razão | Variável dependente secundária da QP3 |
| UT1 | As métricas que acompanhamos ajudam a decidir o que melhorar nas entregas. | QP2 | Utilidade percebida | Ordinal (Likert 5) | Construto UT |
| UT2 | As métricas refletem bem o valor que as minhas entregas geram para a empresa. | QP2 | Utilidade percebida | Ordinal (Likert 5) | Construto UT |
| UT3 | Decisões sobre o meu trabalho são tomadas com base nessas métricas. | QP2 | Utilidade percebida | Ordinal (Likert 5) | Construto UT |
| ATT | Para mostrar que você está lendo com atenção, marque "Discordo totalmente" nesta linha. | — | Atenção | Nominal | Qualquer resposta ≠ "Discordo totalmente" → descarte |
| UT4 (R) | Acompanhar métricas toma tempo sem trazer benefício real. | QP2 | Utilidade percebida | Ordinal (Likert 5) | Construto UT, reverso |
| MM1 | O meu time define metas ou limites aceitáveis para as métricas que acompanha. | QP4 | Maturidade de medição | Ordinal (Likert 5) | Construto MM |
| MM2 | As métricas são revisadas periodicamente pelo time ou pela gestão. | QP4 | Maturidade de medição | Ordinal (Likert 5) | Construto MM |
| MM3 | Os dados das métricas são coletados automaticamente, sem preenchimento manual. | QP4 | Maturidade de medição | Ordinal (Likert 5) | Construto MM |
| MM4 (R) | No meu time, cada pessoa mede as entregas do seu jeito, sem um padrão. | QP4 | Maturidade de medição | Ordinal (Likert 5) | Construto MM, reverso |
| A1 | Que métrica você gostaria de acompanhar nas suas entregas, mas hoje não consegue? Por quê? | QP1 | Métricas desejadas e barreiras | Aberta | Codificação aberta por dois codificadores |
| A2 | Algum comentário sobre o tema ou sobre esta pesquisa? | — | — | Aberta | Leitura qualitativa; não entra nos testes |

## Construtos

| Construto | Itens | Escore | Confiabilidade |
|---|---|---|---|
| **UT**: utilidade percebida das métricas | UT1, UT2, UT3, UT4 (R) | Média dos 4 itens, tratada como ordinal nos testes | Alfa de Cronbach ≥ 0,70; se ficar abaixo, informar o alfa sem o item mais fraco |
| **MM**: maturidade de medição do time | MM1, MM2, MM3, MM4 (R) | Média dos 4 itens, tratada como ordinal nos testes | Alfa de Cronbach ≥ 0,70 |

## Regras de descarte (ordem de aplicação)

1. Sem consentimento (TC1)
2. Fora da população: F1 = "Não", **ou** P1 = "Outra" com uma área sem relação com dados ou automação (ex.: "Psicóloga"). Este segundo caso é decidido por dois pesquisadores de forma independente; em caso de divergência, a resposta é mantida
3. Falhou na pergunta de atenção (ATT)
4. Respostas duplicadas (todas as colunas idênticas, exceto o carimbo de data/hora)

Cada resposta descartada recebe o motivo da primeira regra que a eliminou. O dashboard mostra a contagem por motivo.

> **Colegas da turma:** a pergunta que identificava alunos da disciplina foi retirada após o pré-teste. A exclusão de colegas passa a ser feita na divulgação: o link não é enviado nos canais da turma nem a colegas da disciplina (ver seções 7 e 8 do protocolo).

> **Limitação:** o Google Forms registra apenas a hora de envio, não a de início. Por isso, o tempo de preenchimento não pode ser usado como critério de descarte.
