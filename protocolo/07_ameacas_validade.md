# 7. Ameaças à validade

As ameaças seguem a classificação de Wohlin et al. (2012). Para cada uma, indicamos a mitigação e a seção em que ela é aplicada. As ameaças que não podem ser eliminadas são declaradas como limitações na página de metodologia do dashboard.

## Validade de construto

| Ameaça | Mitigação |
|---|---|
| Um único item não mede bem um conceito abstrato | Utilidade (UT) e maturidade (MM) são medidas por 4 itens cada, com um item reverso. A consistência é verificada pelo alfa de Cronbach, com regras definidas antes da coleta (seção 5) |
| O respondente entende os termos de forma diferente da pretendida | Definições e exemplos no enunciado dos itens ("regularmente", tipos de entrega). Itens confusos foram reescritos após o pré-teste (seção 4) |
| **Desejabilidade social:** declarar mais medição ou utilidade do que existe | Anonimato total e garantido no TCLE (seção 6), redação neutra, opção "Não sei" em M2 e P3, e um item reverso em cada construto |
| Viés de método único: todas as medidas são autorrelatadas | Não há como mitigar com um survey. A ameaça é declarada como limitação, e M4 (nº de falhas) é usado como medida mais concreta, ao lado da percepção de retrabalho (M3) |

## Validade interna

| Ameaça | Mitigação |
|---|---|
| **Respostas descuidadas ou automáticas** | Pergunta de atenção (ATT) com descarte (seção 5). O Google Forms registra só a hora do envio, não o tempo de preenchimento, por isso o tempo não é usado como critério. Grades com todas as respostas iguais são sinalizadas no dashboard, mas não descartadas |
| Mesma pessoa responder mais de uma vez | Sem login, isso não pode ser impedido. Respostas idênticas são descartadas (regra 4), e a mensagem pede uma única resposta |
| Colega da turma receber o link por repasse | Exclusão na divulgação e aviso explícito na mensagem (seção 8). O risco residual é declarado como limitação |
| Fatores de confusão na QP3 (porte, setor, tipo de entrega) | A QP3 é tratada como associação, não como causa. A análise por porte e setor fica disponível nos filtros, como exploratória |
| Viés de memória em M4 (falhas nos últimos 30 dias) | Janela curta e definida. M4 é análise secundária (seção 5) |

## Validade externa

| Ameaça | Mitigação |
|---|---|
| **Amostra por conveniência e bola de neve** concentrada em pessoas parecidas com os integrantes | Vários canais e comunidades diferentes (seção 8). O perfil da amostra (P1–P6) fica visível no dashboard, e as conclusões valem só para a amostra, sem generalização (seção 2) |
| **Autosseleção:** pessoas mais interessadas em métricas respondem mais | Mensagem neutra, sem recompensa, voltada a quem trabalha com dados, e não a quem "gosta de métricas". Declarada como limitação |
| **Não resposta:** quem não responde pode ser diferente de quem responde | Lembretes espaçados e limite de 3 mensagens por pessoa (seção 8). A taxa de resposta é estimada por canal quando o alcance é conhecido (mensagens diretas e grupos com nº de membros) |

## Validade de conclusão

| Ameaça | Mitigação |
|---|---|
| Baixo poder estatístico (n ≈ 60, subgrupos menores) | Relato do tamanho de efeito junto do p-valor. Ausência de significância não é tratada como igualdade. Áreas com menos de 5 respostas são agrupadas (seção 5) |
| Múltiplas comparações inflam o erro tipo I | Correção de Holm na família principal e nos pós-testes. Filtros por segmento são exploratórios (seção 5) |
| Tratar Likert como intervalar | Apenas testes não paramétricos. Nenhuma média de item isolado (seção 5) |
| Subjetividade na codificação das respostas abertas | Dois codificadores independentes, livro de códigos e kappa de Cohen (seção 5) |
| Ajustar a análise depois de ver os dados | Pré-registro com a tag `protocolo-v1`. Toda mudança é registrada em `docs/DESVIOS.md` e aparece no dashboard |
