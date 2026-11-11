# 8. Plano de divulgação

**Período de coleta: 12/11/2026 a 22/11/2026 (11 dias).** O formulário só é aberto depois do commit com a tag `protocolo-v1` e do envio do protocolo na plataforma da disciplina, e deixa de aceitar respostas às 23h59 de 22/11. Se a tag atrasar, a abertura passa para o dia seguinte à tag, o encerramento é mantido e a mudança é registrada em `docs/DESVIOS.md`.

**Mensagem padrão.** Todos os canais usam a mesma mensagem, adaptada só no tamanho. Ela diz quem somos e para que serve a pesquisa, qual é o público procurado, o tempo estimado (10 a 15 min), que as respostas são anônimas, e pede que o link seja repassado a outras pessoas da área. Não há recompensa, para não atrair respostas só pelo prêmio.

**Exclusão de colegas da turma.** O link não é publicado em grupos, fóruns ou na plataforma da turma de MES, nem enviado diretamente a colegas da disciplina. A mensagem também pede: *"Se você cursa Medição e Experimentação de Software na PUC Minas neste semestre, por favor não responda."*

| Canal | Ação | Responsável |
|---|---|---|
| LinkedIn | Post no perfil de cada integrante e convites por mensagem direta a contatos da área | Todos |
| Empresas dos integrantes | Envio a colegas da área pelo canal interno (Teams, Slack, e-mail), com autorização do gestor quando necessário | Todos |
| WhatsApp, Telegram e Discord | Grupos e servidores de dados, BI e automação de que os integrantes já participam, respeitando as regras de cada um | Diogo |
| **Reserva** | Grupos do LinkedIn sobre dados e RPA; professores de cursos de dados (repasse a ex-alunos, sem a turma de MES); r/brdev e fóruns de dados; segunda e última mensagem direta a quem não respondeu | Todos |

Os canais reserva são ativados se, em **17/11**, houver menos de **35 respostas brutas**. Todo canal novo é registrado em `docs/DESVIOS.md`.

| Data | Ação |
|---|---|
| **12/11 (qui)** | Abertura: posts no LinkedIn, mensagens em grupos e envio nas empresas |
| 13/11 – 14/11 | Mensagens diretas no LinkedIn |
| **16/11 (seg)** | 1º lembrete, com o número parcial de respostas |
| **17/11 (ter)** | Ponto de controle dos canais reserva |
| **19/11 (qui)** | 2º lembrete: "últimos dias" |
| **22/11 (dom)** | Último aviso e encerramento às 23h59 |

Cada pessoa ou grupo recebe no máximo 3 mensagens, e a contagem diária de respostas é postada no grupo da equipe.

**Evidências.** Cada divulgação gera uma captura de tela com data e hora visíveis, salva em `evidencias/divulgacao/` como `AAAA-MM-DD_canal_descricao.png` e listada em `evidencias/divulgacao/registro.md`. Nomes, fotos e telefones de terceiros são ocultados antes do commit. No encerramento, o painel de respostas do formulário também é capturado, e a exportação bruta com data e hora de cada resposta é feita em 23/11.
