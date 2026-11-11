# 5. Plano de análise

A análise é feita em Python (pandas, SciPy, pingouin, scikit-posthocs) dentro do dashboard Streamlit, que lê o CSV bruto exportado do formulário. O código fica versionado no repositório.

## Preparação e descartes

As regras são aplicadas nesta ordem, e cada descarte recebe o motivo da primeira regra que o eliminou (o dashboard mostra a contagem por motivo): (1) **sem consentimento** (TC1 = "Não concordo"); (2) **fora da população**: F1 = "Não", ou P1 = "Outra" com área sem relação com dados ou automação, decidido por dois pesquisadores de forma independente e mantido se houver divergência; (3) **falha de atenção** (ATT ≠ "Discordo totalmente"); (4) **duplicada**: todas as colunas iguais a outra resposta, exceto o carimbo de data/hora, mantendo a primeira. Os itens são obrigatórios, então não há respostas incompletas além das encerradas em TC1 ou F1. "Não sei" em P3 e M2 não leva ao descarte: a resposta só sai da análise que usa essa variável. Antes da análise, UT4 e MM4 são invertidos (6 − resposta), e os escores UT e MM são calculados como a média dos quatro itens.

## Estatística descritiva

| Escala | Itens | O que é relatado |
|---|---|---|
| Nominal | P1, P4, P6, M1, M2 | Frequência e %; na QP1, proporção com IC 95% (seção 2) |
| Ordinal | P2, P3, M3, UT1–UT4, MM1–MM4 | Frequência por categoria, mediana e intervalo interquartil (IIQ); itens Likert em barras divergentes |
| Razão | P5, M4 | Mediana, IIQ, mínimo e máximo |
| Escores UT e MM | Média de 4 itens | Mediana e IIQ, tratados como ordinais nos testes |

Um item Likert isolado é ordinal, então **nunca é resumido pela média**. O escore do construto (média de 4 itens) só é usado se a consistência interna for adequada e, mesmo assim, entra apenas em testes não paramétricos.

## Confiabilidade dos construtos

O alfa de Cronbach de UT e MM é calculado já com os itens reversos invertidos, junto com o IC 95%. Com **α ≥ 0,70**, o construto é aceito. Com **0,60 ≤ α < 0,70**, o escore é usado, mas declarado como limitação, e relatamos o alfa sem cada item. Com **α < 0,60**, se a remoção de um item levar a α ≥ 0,70, o escore passa a ser calculado sem esse item (registrado como desvio); caso contrário, a QP é analisada item a item, como exploratória.

## Testes por questão de pesquisa

As variáveis dependentes são ordinais ou contagens assimétricas, e as amostras são pequenas. Por isso, todos os testes são **não paramétricos**.

| QP | Variáveis | Teste | Tamanho de efeito |
|---|---|---|---|
| **QP1** | M1 (nominal, múltipla) | Descritiva: proporção de cada métrica ± margem de erro | — |
| **QP2** | UT (ordinal) × P1 (k grupos) | **Kruskal-Wallis**; se significativo, pós-teste de **Dunn** com Holm | **ε²** = H / (n − 1) |
| **QP3** | M3 (ordinal) × M2 (mede / não mede) | **Mann-Whitney U** unilateral (H1 direcional) | **r rank-biserial** |
| QP3 (sec.) | M4 (contagem) × M2 | Mann-Whitney U unilateral, relatado à parte | r rank-biserial |
| **QP4** | MM (ordinal) × P2 (ordinal) | **Correlação de Spearman** | **ρ** |

Na QP2, áreas com menos de 5 respostas são agrupadas em "Outras"; se restarem só 2 grupos, o teste passa a ser Mann-Whitney (desvio registrado). Na QP3, "Sim, automatizada" e "Sim, manual" formam o grupo "mede", "Não" forma o grupo "não mede", e "Não sei" fica de fora. Os efeitos são interpretados pelos limiares de Cohen: ε² ≈ 0,01 / 0,06 / 0,14 e r, ρ ≈ 0,1 / 0,3 / 0,5 para pequeno, médio e grande. Cada resultado é relatado com a estatística do teste, o p-valor bruto, o p-valor ajustado, o tamanho de efeito e o n.

## Significância e múltiplas comparações

Usamos **α = 0,05**. A família principal (QP2, QP3 com M3 e QP4, três testes) é ajustada por **Holm**: os p-valores são ordenados, e o i-ésimo é comparado com α / (3 − i + 1). Os pós-testes de Dunn e a análise de M4 têm correção própria e são complementares. Um resultado não significativo não é tratado como prova de igualdade. Os filtros por segmento (P2, P3, P4) no dashboard são **exploratórios**, mostram o n e ficam fora da correção.

## Respostas abertas

A1 complementa a QP1. Dois codificadores (Arthur e Gustavo) fazem a codificação aberta de forma independente e unificam os códigos em um livro de códigos, com definição e exemplo. Em seguida, os dois reaplicam o livro a todas as respostas. A concordância é medida pelo **kappa de Cohen** (κ ≥ 0,60 aceitável), e as divergências são resolvidas por consenso, com Diogo como desempate. O relato traz a frequência dos códigos e trechos anonimizados. A2 serve só para registrar críticas ao instrumento.
