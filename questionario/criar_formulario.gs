/**
 * Cria o Google Forms do survey "Uso de métricas em produtos de dados e automação".
 *
 * Como usar:
 *   1. Acesse https://script.google.com, crie um projeto e cole este arquivo.
 *   2. Preencha CONFIG.contato abaixo.
 *   3. Execute a função criarFormulario e autorize o acesso ao Forms/Sheets.
 *   4. Os links aparecem em "Registro de execução".
 *
 * O formulário é criado FECHADO para respostas (pré-registro): só abra depois
 * do commit com a tag protocolo-v1. Para o pré-teste, rode com CONFIG.preTeste = true,
 * que cria uma cópia separada, aberta, cujas respostas não entram na amostra.
 *
 * Os códigos dos itens (UT1, MM2…) estão em questionario/matriz_rastreabilidade.md.
 */

const CONFIG = {
  contato: 'PREENCHER',  // e-mail de contato do grupo exibido no TCLE
  preTeste: false,  // true = cópia de pré-teste, aberta; false = formulário oficial, fechado
};

const LIKERT = ['Discordo totalmente', 'Discordo', 'Neutro', 'Concordo', 'Concordo totalmente'];

function criarFormulario() {
  if (CONFIG.contato === 'PREENCHER') {
    throw new Error('Preencha CONFIG.contato antes de executar.');
  }

  const titulo = 'Pesquisa: uso de métricas em produtos de dados e automação'
    + (CONFIG.preTeste ? ' [PRÉ-TESTE]' : '');
  const form = FormApp.create(titulo);
  form.setDescription(
    'Pesquisa acadêmica sobre como profissionais que entregam dashboards, relatórios, bases de dados, '
    + 'pipelines e automações de processo medem a qualidade e o uso dessas entregas. '
    + 'Tempo estimado: 7 a 9 minutos. Respostas anônimas.');
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false);  // exigiria login, o que identifica o respondente
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage('Obrigado pela participação! Se puder, compartilhe a pesquisa com colegas da área.');

  secaoConsentimento(form);
  secaoFiltroEPerfil(form);
  secaoMetricas(form);
  secaoPercepcoes(form);
  secaoAbertas(form);

  const planilha = SpreadsheetApp.create(titulo + ' (respostas)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, planilha.getId());
  form.setAcceptingResponses(CONFIG.preTeste);

  Logger.log('Editar:     ' + form.getEditUrl());
  Logger.log('Responder:  ' + form.getPublishedUrl());
  Logger.log('Planilha:   ' + planilha.getUrl());
  Logger.log('Aceitando respostas: ' + CONFIG.preTeste);
}

// Página 1 — TCLE
function secaoConsentimento(form) {
  form.addSectionHeaderItem()
    .setTitle('Termo de Consentimento Livre e Esclarecido')
    .setHelpText(
      'Esta pesquisa faz parte do trabalho final da disciplina de Medição e Experimentação de Software '
      + 'da PUC Minas, realizado pelos alunos Arthur Panzera, Diogo Brunoro e Gustavo Prehl.\n\n'
      + 'Objetivo: entender quais métricas os profissionais de dados, BI, CRM e automação usam para avaliar '
      + 'suas entregas e como percebem a utilidade dessas métricas.\n\n'
      + '• A participação é voluntária, e você pode desistir a qualquer momento antes de enviar.\n'
      + '• Não coletamos nome, e-mail, empresa ou qualquer dado que identifique você.\n'
      + '• As respostas serão usadas apenas para fins acadêmicos e divulgadas somente de forma agregada.\n'
      + '• Os dados ficam armazenados com acesso restrito aos pesquisadores, conforme a LGPD (Lei 13.709/2018).\n'
      + '• Não há riscos previstos além do tempo de preenchimento.\n\n'
      + 'Dúvidas: ' + CONFIG.contato);

  const consentimento = form.addMultipleChoiceItem();
  consentimento
    .setTitle('Você leu o termo acima e concorda em participar da pesquisa?')
    .setChoices([
      consentimento.createChoice('Sim, concordo em participar', FormApp.PageNavigationType.CONTINUE),
      consentimento.createChoice('Não concordo', FormApp.PageNavigationType.SUBMIT),
    ])
    .setRequired(true);
}

// Página 2 — filtro da população
// Página 3 — perfil (variáveis de segmento do dashboard)
function secaoFiltroEPerfil(form) {
  form.addPageBreakItem().setTitle('Sobre o seu trabalho');

  const populacao = form.addMultipleChoiceItem();
  populacao
    .setTitle('No seu trabalho atual, você cria ou mantém produtos de dados ou automação?')
    .setHelpText('Exemplos: dashboards, relatórios, bases ou extrações para outras áreas, pipelines de dados, '
      + 'segmentações de campanha, automações de processos (RPA, low-code, scripts, workflows).')
    .setChoices([
      populacao.createChoice('Sim', FormApp.PageNavigationType.CONTINUE),
      populacao.createChoice('Não', FormApp.PageNavigationType.SUBMIT),
    ])
    .setRequired(true);

  form.addPageBreakItem().setTitle('Perfil');

  form.addMultipleChoiceItem()
    .setTitle('Qual é a sua área de atuação principal?')
    .setChoiceValues([
      'Análise de dados / BI',
      'CRM / marketing analytics',
      'Engenharia de dados',
      'Ciência de dados',
      'Desenvolvimento de sistemas / automação de processos',
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Há quanto tempo você trabalha com dados ou automação?')
    .setChoiceValues(['Menos de 1 ano', '1 a 3 anos', '3 a 5 anos', '5 a 10 anos', 'Mais de 10 anos'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Qual é o porte da empresa em que você trabalha?')
    .setChoiceValues([
      'Até 49 funcionários',
      '50 a 249 funcionários',
      '250 a 999 funcionários',
      '1.000 funcionários ou mais',
      'Não sei',
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Qual é o setor da empresa?')
    .setChoiceValues([
      'Indústria (inclui automotivo)',
      'Varejo / e-commerce',
      'Financeiro / seguros',
      'Tecnologia / software',
      'Consultoria / serviços',
      'Saúde',
      'Educação',
      'Setor público',
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addTextItem()
    .setTitle('Quantas pessoas fazem parte do seu time direto (incluindo você)?')
    .setValidation(FormApp.createTextValidation()
      .requireWholeNumber()
      .setHelpText('Informe um número inteiro.')
      .build())
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('Quais ferramentas você usa com frequência no trabalho?')
    .setChoiceValues([
      'Excel / Google Sheets',
      'Power BI',
      'Tableau',
      'Looker Studio',
      'Dataiku',
      'SQL (qualquer banco)',
      'Python ou R',
      'Sydle',
      'Salesforce / Marketing Cloud',
      'Power Automate / RPA',
    ])
    .showOtherOption(true)
    .setRequired(true);
}

// Página 4 — métricas usadas (QP1) e qualidade/retrabalho (QP3)
function secaoMetricas(form) {
  form.addPageBreakItem()
    .setTitle('Métricas que você usa')
    .setHelpText('Considere as entregas do seu time: dashboards, bases, pipelines, automações etc.');

  form.addCheckboxItem()
    .setTitle('Quais indicadores o seu time acompanha regularmente para saber se as entregas '
      + '(dashboards, relatórios, bases, automações) estão funcionando bem?')
    .setHelpText('Considere apenas indicadores medidos com frequência definida, como toda semana ou todo mês. '
      + 'Marque todos os que se aplicam.')
    .setChoiceValues([
      'Uso ou adoção (acessos, usuários ativos, consultas)',
      'Qualidade dos dados (completude, erros, duplicidade)',
      'Atualização no prazo / latência dos dados',
      'Falhas ou incidentes em pipelines e automações',
      'Retrabalho ou correções solicitadas',
      'Tempo de entrega das demandas',
      'Tempo ou custo economizado pela automação',
      'Impacto no negócio (conversão, receita, retorno de campanha)',
      'Satisfação de quem usa ou solicita a entrega',
      'Nenhuma métrica é acompanhada com regularidade',
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('O seu time mede a qualidade dos dados de forma estruturada?')
    .setHelpText('Por exemplo: regras de validação, testes automáticos, checklists ou indicadores de qualidade.')
    .setChoiceValues(['Sim, de forma automatizada', 'Sim, de forma manual', 'Não', 'Não sei'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Nos últimos 3 meses, com que frequência você precisou refazer ou corrigir uma entrega por causa de problemas nos dados?')
    .setChoiceValues(['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('Nos últimos 30 dias, quantas vezes uma entrega sob sua responsabilidade falhou ou exibiu dados incorretos?')
    .setHelpText('Estimativa aproximada. Se não aconteceu, informe 0.')
    .setValidation(FormApp.createTextValidation()
      .requireWholeNumber()
      .setHelpText('Informe um número inteiro.')
      .build())
    .setRequired(true);
}

// Página 5 — construtos multi-item (QP2 e QP4) e pergunta de atenção
function secaoPercepcoes(form) {
  form.addPageBreakItem()
    .setTitle('Sua percepção')
    .setHelpText('Indique o quanto você concorda com cada afirmação. Se o seu time não usa métricas formais, '
      + 'considere as formas informais de avaliar as entregas.');

  form.addGridItem()
    .setTitle('Sobre a utilidade das métricas no seu trabalho')
    .setRows([
      'As métricas que acompanhamos ajudam a decidir o que melhorar nas entregas.',
      'As métricas refletem bem o valor que as minhas entregas geram para a empresa.',
      'Decisões sobre o meu trabalho são tomadas com base nessas métricas.',
      'Para mostrar que você está lendo com atenção, marque "Discordo totalmente" nesta linha.',
      'Acompanhar métricas toma tempo sem trazer benefício real.',
    ])
    .setColumns(LIKERT)
    .setRequired(true);

  form.addGridItem()
    .setTitle('Sobre a forma como o seu time mede as entregas')
    .setRows([
      'O meu time define metas ou limites aceitáveis para as métricas que acompanha.',
      'As métricas são revisadas periodicamente pelo time ou pela gestão.',
      'Os dados das métricas são coletados automaticamente, sem preenchimento manual.',
      'No meu time, cada pessoa mede as entregas do seu jeito, sem um padrão.',
    ])
    .setColumns(LIKERT)
    .setRequired(true);
}

// Página 6 — respostas abertas (opcionais)
function secaoAbertas(form) {
  form.addPageBreakItem().setTitle('Para terminar');

  form.addParagraphTextItem()
    .setTitle('Que métrica você gostaria de acompanhar nas suas entregas, mas hoje não consegue? Por quê?')
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('Algum comentário sobre o tema ou sobre esta pesquisa?')
    .setHelpText('Não inclua nomes de pessoas ou empresas.')
    .setRequired(false);
}
