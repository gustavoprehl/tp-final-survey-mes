# 5. Plano de análise

A análise é feita em Python (pandas, SciPy, pingouin, scikit-posthocs) e roda dentro do dashboard Streamlit, que lê o CSV bruto exportado do formulário. O código fica versionado no repositório.

## Preparação e critérios de descarte

As regras são aplicadas nesta ordem. Cada resposta descartada recebe o motivo da primeira regra que a eliminou, e o dashboard mostra a contagem por motivo.

1. **Sem consentimento:** TC1 = "Não concordo".
2. **Fora da população:** F1 = "Não".
3. **Falha de atenção:** ATT diferente de "Discordo totalmente".
4. **Duplicada:** todas as colunas idênticas a outra resposta, exceto o carimbo de data/hora. A primeira é mantida.
5. **Incompleta:** todos os itens obrigatórios são exigidos pelo formulário, então uma resposta só fica incompleta se encerrar em TC1 ou F1, casos já cobertos pelas regras 1 e 2.

Colegas da turma não são descartados na análise, porque o formulário não os identifica: eles são excluídos na divulgação (seções 2 e 8). Valores ausentes por opção do respondente ("Não sei" em P3 e M2) **não** levam ao descarte. A resposta só sai da análise em que a variável é usada.

Antes da análise, os itens reversos (UT4, MM4) são invertidos com 6 − resposta, e os escores UT e MM são calculados como a média dos quatro itens.

## Estatística descritiva por tipo de escala

| Escala | Itens | O que é relatado |
|---|---|---|
| Nominal | P1, P4, P6, M1, M2 | Frequência e %; nas proporções da QP1, IC 95% pela margem de erro da seção 2 |
| Ordinal | P2, P3, M3, UT1–UT4, MM1–MM4 | Frequência por categoria, **mediana** e intervalo interquartil (IIQ); itens Likert em gráfico de barras divergentes |
| Razão | P5, M4 | Mediana, IIQ, mínimo e máximo (a média aparece só como complemento, por causa da assimetria esperada) |
| Escores UT e MM | Média de 4 itens | Mediana e IIQ, tratados como ordinais nos testes |

**Nunca calculamos a média de um item Likert isolado.** Um item de 5 pontos é ordinal: a distância entre "Discordo" e "Neutro" não é necessariamente igual à distância entre "Neutro" e "Concordo". O escore do construto usa a média de 4 itens, prática comum em escalas somadas, que só é aceita se a consistência interna for adequada (alfa ≥ 0,70). Mesmo assim, o escore é analisado com testes não paramétricos, que usam apenas a ordem dos valores.

## Confiabilidade dos construtos

O alfa de Cronbach é calculado para UT (UT1–UT4) e MM (MM1–MM4), já com os itens reversos invertidos, junto com o intervalo de confiança de 95%.

- **α ≥ 0,70:** construto aceito, e o escore é usado na QP correspondente.
- **0,60 ≤ α < 0,70:** o escore é usado, mas como limitação declarada. Relatamos também o alfa sem cada item.
- **α < 0,60:** se a remoção de um item levar o alfa a 0,70 ou mais, o escore passa a ser calculado sem esse item, e a mudança é registrada em `docs/DESVIOS.md`. Caso contrário, a QP é analisada item a item (um teste por item, todos dentro da correção de Holm) e o resultado é apresentado como exploratório.

## Testes por questão de pesquisa

Todas as variáveis dependentes são ordinais ou de razão com distribuição assimétrica, e as amostras são pequenas. Por isso, todos os testes são **não paramétricos**: não pressupõem normalidade nem intervalos iguais entre as categorias.

| QP | Variáveis | Teste | Por que este teste | Tamanho de efeito | Correção |
|---|---|---|---|---|---|
| **QP1** | M1 (nominal, múltipla) | Descritiva: proporção de cada métrica com IC 95% | Questão descritiva, sem hipótese | Própria proporção ± margem de erro | — |
| **QP2** | UT (ordinal) × P1 (nominal, k grupos) | **Kruskal-Wallis**; se significativo, pós-teste de **Dunn** | Compara a distribuição de uma variável ordinal entre 3 ou mais grupos independentes | **ε²** = H / (n − 1) | Holm na família principal; Holm também entre os pares do Dunn |
| **QP3** | M3 (ordinal) × M2 (Sim/Não) | **Mann-Whitney U**, unilateral (H1: menor retrabalho em quem mede) | Compara uma variável ordinal entre 2 grupos independentes; H1 é direcional | **r rank-biserial** | Holm na família principal |
| QP3 (sec.) | M4 (razão) × M2 | Mann-Whitney U, unilateral | Contagem assimétrica, com muitos zeros esperados | r rank-biserial | Relatado à parte, como secundário |
| **QP4** | MM (ordinal) × P2 (ordinal) | **Correlação de Spearman** | Associação entre duas variáveis ordinais, sem supor relação linear | **ρ** (o próprio coeficiente) | Holm na família principal |

**Grupos.** Na QP2, áreas com menos de 5 respostas são agrupadas em "Outras". Se restarem só 2 grupos, o teste passa a ser Mann-Whitney com r rank-biserial (desvio a registrar). Na QP3, as duas respostas "Sim" de M2 (automatizada e manual) formam o grupo "mede", "Não" forma o grupo "não mede", e "Não sei" fica fora.

**Interpretação dos efeitos.** Usamos os limiares de Cohen para pequeno, médio e grande: ε² ≈ 0,01 / 0,06 / 0,14; r e ρ ≈ 0,1 / 0,3 / 0,5. Todo resultado é relatado com estatística do teste, p-valor bruto, p-valor ajustado, tamanho de efeito e n.

## Nível de significância e múltiplas comparações

- **α = 0,05.**
- **Família principal:** QP2, QP3 (M3) e QP4, com três testes. Os p-valores são ajustados pelo método de **Holm**: ordenados do menor para o maior, o i-ésimo é comparado com α / (3 − i + 1). Holm controla a taxa de erro da família como Bonferroni, mas perde menos poder.
- Os pós-testes de Dunn da QP2 e a análise secundária de M4 têm correção de Holm própria e são apresentados como complementares.
- Uma diferença sem significância **não** é interpretada como prova de igualdade: relatamos que a amostra não tem evidência suficiente, e o tamanho de efeito mostra a magnitude observada.

## Análise por segmento

O dashboard permite filtrar os resultados por tempo de experiência (P2), porte (P3) e setor (P4). Os testes da tabela acima usam a amostra completa. Os resultados filtrados são **exploratórios**, mostram o n do segmento e não entram na correção de Holm.

## Respostas abertas

A1 (métricas desejadas e barreiras) complementa a QP1. O processo de codificação é este:

1. **Codificação aberta:** dois codificadores (Arthur e Gustavo) leem as respostas de forma independente e propõem códigos.
2. **Livro de códigos:** os códigos são comparados e unificados em um livro de códigos, com definição e exemplo de cada um.
3. **Codificação final:** os dois codificadores aplicam o livro de códigos a todas as respostas, de forma independente. A concordância é medida pelo **kappa de Cohen** (κ ≥ 0,60 é considerado aceitável), e as divergências são resolvidas por consenso, com Diogo como desempate.
4. **Relato:** frequência de cada código, com trechos ilustrativos anonimizados.

A2 (comentários) é lida para registrar críticas ao instrumento e não entra nos testes.
