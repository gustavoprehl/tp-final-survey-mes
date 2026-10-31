Survey Pré-Registrado

Enunciado do Trabalho Final: planejamento, execução e análise de um survey em Engenharia de Software

Grupos: Arhur Panzera,Diogo Brunoro e Gustavo Prehl
Entregas: 2 partes
Vale: 10 pts

01. Objetivo
O survey é uma das principais estratégias empíricas da Engenharia de Software: permite levantar práticas, percepções e características de uma população a partir de uma amostra. Neste trabalho, o grupo vai planejar, executar e analisar um survey real, aplicando os conceitos da disciplina: objetivos e métricas pelo GQM, escalas de medição, validação de medidas, amostragem, testes estatísticos e ameaças à validade.

O planejamento deve ser registrado antes da coleta, como se faz em pesquisas com pré-registro. Assim, o que foi planejado pode ser comparado com o que foi de fato executado.

02. Visão Geral das Entregas
Parte 1 · 2 pts
Planejamento
Protocolo do survey, entregue antes de qualquer coleta, com data comprovada.

Parte 2 · 8 pts
Dashboard e evidências
Dashboard com os dados coletados, evidências da coleta e defesa ao vivo.

03. Parte 1: Planejamento
O protocolo (até 6 páginas, em PDF) deve conter as oito seções abaixo. A data de entrega precisa ser comprovada, por exemplo por um commit em um repositório GitHub do grupo ou pelo envio na plataforma da disciplina, e deve ser anterior à primeira resposta coletada.

    1. Objetivo e questões de pesquisa: objetivo no template GQM e de 2 a 4 questões de pesquisa.
    2. População e amostragem: população-alvo, origem dos contatos, estratégia de amostragem (probabilística, por conveniência ou bola de neve), tamanho de amostra pretendido e a margem de erro correspondente.
    3. Questionário com rastreabilidade: cada item ligado a uma questão de pesquisa e a uma métrica, com a escala declarada (nominal, ordinal, intervalar ou razão). Construtos medidos por mais de um item. Inclua uma pergunta de atenção para identificar respostas descuidadas ou automáticas.
    4. Pré-teste: aplicação do questionário a 3 a 5 pessoas e as mudanças feitas a partir dele.
    5. Plano de análise: estatística descritiva, testes coerentes com as escalas (por exemplo χ², Mann-Whitney, Kruskal-Wallis, correlação de Spearman), tamanho de efeito, correção para múltiplas comparações e forma de codificação das respostas abertas.
    6. Ética e LGPD: termo de consentimento, anonimização e forma de armazenamento dos dados.
    7. Ameaças à validade: ameaças típicas de survey (não resposta, autosseleção, desejabilidade social, entre outras) e como serão mitigadas.
    8. Plano de divulgação: canais que serão usados e período de coleta.

Margem de erro de uma proporção (nível de confiança de 95%): e = 1,96 × √( p(1 − p) / n ). No pior caso (p = 0,5), com n = 50 respostas, a margem é de aproximadamente ±14 pontos percentuais.

04. Parte 2: Dashboard e evidências
Dashboard
A ferramenta é livre (Power BI, Looker Studio, Streamlit, Excel ou outra), mas o dashboard deve ler os dados brutos coletados, e não apenas exibir imagens prontas. Ele deve mostrar:

- Perfil da amostra: número de respostas recebidas, respostas descartadas e o motivo de cada descarte;
- Itens em escala Likert em gráfico de barras divergentes;
- Resposta a cada questão de pesquisa, com o teste estatístico usado, o p-valor, o tamanho de efeito e a margem de erro;
- Filtros por segmento (por exemplo, tempo de experiência ou tipo de empresa);
- Confiabilidade dos construtos medidos por mais de um item (alfa de Cronbach);
- Página de metodologia e desvios: o que mudou em relação ao protocolo da Parte 1 e por quê.

Evidências da coleta
Apresentem pelo menos uma das evidências abaixo:

- Carta de anuência assinada pela empresa ou organização em que o survey foi aplicado, autorizando a aplicação;
- Registros digitais: exportação bruta do formulário com data e hora de cada resposta, capturas datadas dos canais de divulgação e acesso ao painel do formulário durante a apresentação.

Nenhuma evidência pode expor dados pessoais dos respondentes.

Apresentação e defesa
- Demonstração ao vivo do dashboard, com 10 minutos por grupo;
- Mudança de cenário: o professor proporá uma alteração no estudo, e o grupo deverá explicar o que mudaria no planejamento ou na análise;
- Arguição individual: cada integrante responde a uma pergunta sobre o trabalho. Todos devem dominar o estudo inteiro, não apenas a parte que apresentaram.

05. Regras da Coleta
- Mínimo de 50 respostas válidas, ou de 30 quando o survey for aplicado em uma única organização com carta de anuência.
- Colegas da turma não contam como amostra, exceto quando a população-alvo forem estudantes e isso estiver justificado no protocolo.
- Os dados devem corresponder ao protocolo da Parte 1. Desvios são aceitos, desde que declarados e justificados.
- A margem de erro deve ser relatada junto com os resultados, e as conclusões devem respeitar esse limite.
- Sigam as orientações da instituição sobre pesquisas com pessoas.

Atenção: indícios de respostas fabricadas ou de dados manipulados serão tratados conforme as normas acadêmicas da instituição. A coleta leva tempo: iniciem a divulgação assim que a Parte 1 for entregue.

06. Temas Sugeridos
Tema | Exemplo de questão de pesquisa
Assistentes de IA | A produtividade percebida com assistentes de IA varia com o tempo de experiência do desenvolvedor?
Uso de métricas | Quais métricas as empresas usam de fato e como os times percebem o uso delas?
Testes e revisão de código | Times que fazem revisão de código obrigatória relatam menos defeitos em produção?
Dívida técnica | Como a dívida técnica é percebida e gerenciada em empresas de portes diferentes?
Plantão e bem-estar | A participação em plantões (on-call) está associada à carga de trabalho percebida?

07. Critérios de avaliação
Parte | Critério | Pontos
Planejamento | Objetivo GQM, questões de pesquisa e rastreabilidade do questionário | 0,75 pt
Planejamento | Amostragem, tamanho de amostra e margem de erro | 05, pt
Planejamento | Plano de análise coerente com as escalas; ética e LGPD | 0,5 pt
Planejamento | Pré-teste e ameaças à validade | 0,25 pt
Dashboard | Evidências da coleta e consistência dos dados com o protocolo | 2,0 pt
Dashboard | Qualidade dos dados: limpeza, descartes justificados e confiabilidade dos construtos | 1,5 pt
Dashboard | Questões de pesquisa respondidas com testes, tamanhos de efeito e visualizações corretos | 2,0 pt
Dashboard | Desvios em relação ao protocolo e limitações (não resposta, vieses) | 0,5 pt
Dashboard | Defesa ao vivo: mudança de cenário e arguição individual | 2,0 pt

Total = 10 pt

Referências
KITCHENHAM, B.; PFLEEGER, S. L. Personal opinion surveys. In: SHULL, F.; SINGER, J.; SJØBERG, D. (ed.). Guide to Advanced Empirical Software Engineering. London: Springer, 2008.
WOHLIN, C. et al. Experimentation in Software Engineering. Berlin: Springer, 2012.
