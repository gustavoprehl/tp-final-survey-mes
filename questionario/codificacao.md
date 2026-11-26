# Codificação das respostas abertas (A1)

A1: *"Que métrica você gostaria de acompanhar nas suas entregas, mas hoje não consegue? Por quê?"*

A codificação segue a seção 5 do protocolo: dois codificadores independentes (Arthur e Gustavo), livro de códigos unificado, kappa de Cohen (κ ≥ 0,60 aceitável) e consenso nas divergências, com Diogo como desempate (não foi necessário).

## Procedimento

1. As respostas foram revisadas antes da codificação. Nenhuma cita nome de pessoa ou empresa, então nada foi substituído por `[removido]` (seção 6).
2. **Codificação aberta independente.** Arthur e Gustavo codificaram as 17 respostas da A1 (15 válidas e 2 descartadas), cada um com o próprio livro de códigos, sem ver a codificação do outro. A de Gustavo está em `dados/codificacao_A1_gustavo_original.csv` e `questionario/livro_codigos_A1_gustavo.md`; a de Arthur, na coluna `*_arthur` de `dados/codificacao_A1.csv`.
3. **Livro unificado.** Os dois livros tinham categorias quase equivalentes. Foram unidos no livro abaixo, que mantém todas as categorias de ambos: as que Gustavo detalhou mais (por exemplo, desempenho, entregabilidade e testes) foram agrupadas, e duas categorias que só ele usou (prazo das entregas e métrica genérica) foram incorporadas.
4. **Concordância.** A codificação de cada um foi expressa no livro unificado pela tabela de correspondência, sem mudar nenhuma classificação, e o kappa foi calculado a partir daí. Como uma resposta pode ter mais de um código, o kappa usa as decisões código a código (cada código presente ou ausente em cada resposta). A concordância simples é a fração de respostas com exatamente os mesmos códigos.
5. **Consenso.** As divergências foram decididas em conjunto pelos dois codificadores, e o resultado está nas colunas `metrica_final` e `barreira_final`.
6. O dashboard mostra a frequência dos códigos finais **só nas respostas válidas** (aba QP1).

## Livro de códigos unificado

Cada resposta recebe códigos em duas dimensões. Uma resposta pode ter **mais de um código** na mesma dimensão, separados por `;`.

### Dimensão 1: métrica desejada

| Código | Definição | Exemplo | Arthur | Gustavo |
|---|---|---|---|---|
| `NEGOCIO` | Resultado ou meta de negócio que a entrega deveria apoiar: conversão, receita, OKR, retorno | "KPIs de conversão das campanhas" | NEGOCIO | IMP |
| `ENTREGA` | Prazo, SLA ou aderência ao planejado nas entregas | "SLA… o prazo de um chamado simples é o mesmo de um projeto longo" | — | ENT |
| `OPERACAO` | Funcionamento técnico da entrega ou do produto: desempenho, escala, entregabilidade, testes | "Métricas de escala do produto" | OPERACAO | DES, ENV, TES |
| `QUALIDADE` | Qualidade, completude ou disponibilidade dos próprios dados | "Qualidade dos dados hoje não é possível de medir" | QUALIDADE | QLD |
| `USUARIO` | Uso, adoção, usabilidade ou satisfação de quem consome a entrega | "NPS dos usuários internos" | USUARIO | USO, SAT |
| `INDIVIDUAL` | Desempenho, resultado ou valor da própria pessoa que respondeu | "Meu resultado" | INDIVIDUAL | IND |
| `GENERICA` | Métrica citada de forma genérica, sem objeto definido | "Métricas de desempenho" | — | GEN |
| `SEM_CONTEUDO` | A resposta não indica nenhuma métrica | ".", "n/a" | SEM_CONTEUDO | SEM |

### Dimensão 2: por que não consegue medir

| Código | Definição | Exemplo | Arthur | Gustavo |
|---|---|---|---|---|
| `FERRAMENTA` | Falta de ferramenta ou limitação técnica para coletar ou calcular | "não consigo por limitações técnicas" | FERRAMENTA | FER |
| `SISTEMA` | O dado não está disponível, não é registrado ou não é separado nos sistemas | "Ainda em processo de sanitização da base" | SISTEMA | DAD |
| `ADESAO` | Depende do processo ou da adesão de outras pessoas | "atualmente nem todos respondem" | ADESAO | PRO |
| `NAO_INFORMADA` | A resposta não explica o motivo | "Métricas de desempenho" | NAO_INFORMADA | NI |

## Resultado

| Dimensão | Concordância simples | Kappa de Cohen | Interpretação (Landis e Koch) |
|---|---|---|---|
| Métrica desejada | 14 de 17 (82%) | 0,81 | quase perfeita |
| Barreira | 16 de 17 (94%) | 0,92 | quase perfeita |

As duas dimensões passam do mínimo de 0,60 definido na seção 5.

### Divergências e decisão de consenso

| Resposta (timestamp) | Dimensão | Arthur | Gustavo | Decisão final | Justificativa |
|---|---|---|---|---|---|
| 14/11/2026 20:43:59 ("SLA… chamado simples e projeto longo") | Métrica | OPERACAO | ENTREGA | `ENTREGA` | SLA é prazo de entrega, que tem categoria própria no livro unificado |
| 14/11/2026 20:43:59 ("seria interessante ter essa separação nos sistemas") | Barreira | SISTEMA | FERRAMENTA | `SISTEMA` | O problema é o sistema não separar os tipos de chamado, e não a falta de ferramenta |
| 15/11/2026 17:14:50 ("NPS… / aderência ao planejado mensal") | Métrica | USUARIO; NEGOCIO | USUARIO; ENTREGA | `USUARIO; ENTREGA` | "Aderência ao planejado" é cumprimento de plano, e não resultado de negócio |
| 15/11/2026 21:13:46 ("Métricas de desempenho") | Métrica | OPERACAO | GENERICA | `GENERICA` | A resposta não diz de que é o desempenho |

### Frequência dos códigos finais (15 respostas válidas)

| Métrica desejada | Respostas | | Barreira | Respostas |
|---|---|---|---|---|
| Funcionamento técnico da entrega | 3 | | Motivo não informado | 9 |
| Resultado de negócio | 2 | | Falta de ferramenta / limitação técnica | 3 |
| Prazo e cumprimento das entregas | 2 | | Dado indisponível ou não registrado | 2 |
| Qualidade dos dados | 2 | | Processo ou adesão das pessoas | 1 |
| Uso e satisfação do usuário | 2 | | | |
| Desempenho individual | 2 | | | |
| Sem conteúdo | 2 | | | |
| Métrica genérica | 1 | | | |

Uma resposta tem dois códigos de métrica, então a coluna soma 16. A resposta de 17/11/2026 23:04:39 foi codificada, mas saiu das válidas pela regra 2 (área "Outra" julgada fora da população pelos dois pesquisadores).
