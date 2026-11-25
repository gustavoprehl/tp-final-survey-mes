# Roteiro da defesa (26/11/2026)

Dashboard: **https://tp-final-survey-mes.streamlit.app/** (privado: entrar com a conta convidada). Plano B: rodar local com `.venv\Scripts\streamlit run dashboard/app.py`. Plano C: capturas de cada página.

## Resultados em uma frase cada

| | Resultado (n = 27 válidas, margem ± 18,9 p.p.) |
|---|---|
| Amostra | 30 respostas brutas, 27 válidas: 2 falharam na pergunta de atenção, 1 estava fora da população. Abaixo do mínimo de 50 (desvio declarado) |
| QP1 | Qualidade dos dados e tempo de entrega são as mais citadas (63,0% cada), mas **empatam** com outras 4 métricas dentro da margem de erro. Atualização no prazo é a menos citada (25,9%) |
| QP2 | Sem evidência de diferença de utilidade percebida entre as áreas (Kruskal-Wallis, p ajustado = 1,0, ε² = 0,05, pequeno). UT calculado sem UT4 |
| QP3 | Sem evidência de menos retrabalho em quem mede a qualidade (Mann-Whitney unilateral, p ajustado = 1,0). O efeito observado foi até no sentido oposto (r = +0,23), e o grupo "não mede" tem só 2 pessoas |
| QP4 | MM não foi confiável (α = 0,42): análise item a item. Nenhum item se associa à experiência (\|ρ\| ≤ 0,19, p ajustado = 1,0) |
| Confiabilidade | UT: α = 0,44 → 0,72 sem o reverso UT4. MM: α = 0,42, nenhuma remoção chega a 0,70 |

## Demo de 10 minutos

| Tempo | Página | Quem | O que mostrar |
|---|---|---|---|
| 0–1 | — | Gustavo | Tema, objetivo GQM e as 4 QPs |
| 1–3 | Perfil da amostra | Gustavo | Recebidas × válidas × descartes por motivo; respostas por dia; perfil |
| 3–4 | Itens Likert | Gustavo | Barras divergentes; aplicar um filtro ao vivo |
| 4–7 | Questões de pesquisa | Diogo | Tabela da família principal (Holm); uma aba por QP com teste, p, efeito e margem |
| 7–8 | Confiabilidade | Diogo | Alfa, regra da seção 5 e por que UT perdeu UT4 e MM virou item a item |
| 8–10 | Metodologia e desvios | Arthur | Pré-registro (tag antes da 1ª resposta), desvios, limitações, evidências da coleta |

## Prováveis mudanças de cenário

| Se o professor propuser… | O que mudaria |
|---|---|
| Aplicar só em uma empresa, com carta de anuência | População finita e conhecida: mínimo de 30, margem com correção para população finita, possibilidade de sorteio a partir da lista de funcionários. Conclusões valem só para a empresa. Cresce o risco de desejabilidade social (medo de identificação), então reforçar anonimato e agregação mínima |
| Amostragem probabilística | Precisa de um cadastro (lista de membros de uma comunidade ou associação) e sorteio aleatório simples ou estratificado por área. Só então a margem de erro mede de fato o erro amostral |
| n = 200 | Margem de ± 6,9 p.p.; mais poder; os subgrupos da QP2 deixariam de ser agrupados em "Outras"; o Dunn ficaria mais informativo |
| QP3 com 3 grupos (automatizada, manual, não mede) | Kruskal-Wallis com ε² e pós-teste de Dunn com Holm, no lugar do Mann-Whitney |
| Nova QP relacionando duas variáveis nominais (ex.: M2 × setor) | Qui-quadrado de independência com V de Cramér; Fisher exato se frequências esperadas < 5 |
| Medir retrabalho em horas (razão) | Descritiva com média e desvio-padrão; teste t ou Welch se a distribuição permitir, senão Mann-Whitney; Pearson só com relação linear e normalidade |
| Medir antes e depois de adotar métricas | Desenho pareado: Wilcoxon de postos sinalizados (ordinal) ou t pareado (razão normal) |
| Alfa ≥ 0,70 nos dois construtos | Escores com 4 itens e QP4 com um único Spearman: família principal de 3 testes |

## Arguição: todos precisam saber explicar

- Por que GQM e como cada QP chega a itens e métricas (matriz de rastreabilidade)
- A fórmula da margem de erro, por que p = 0,5 e por que ela não cobre o viés de seleção
- Por que testes não paramétricos (Likert é ordinal; amostra pequena) e por que nunca a média de um item isolado
- Holm: o que controla, como funciona e por que é menos conservador que Bonferroni
- A regra do alfa de Cronbach e o que aconteceu com UT4 e MM
- Por que "não rejeitar H0" não prova igualdade, e o papel do tamanho de efeito
- Cada desvio de `docs/DESVIOS.md` e por que foi aceito
- Como o pré-registro foi comprovado (tag `protocolo-v1` antes da 1ª resposta)
