# 8. Plano de divulgação

## Período de coleta

**09/11/2026 a 22/11/2026**, com 14 dias de coleta. O formulário só é aberto depois do commit com a tag `protocolo-v1` e do envio do protocolo na plataforma da disciplina. Às 23h59 de 22/11, o formulário deixa de aceitar respostas.

## Mensagem padrão

Todos os canais recebem a mesma mensagem-base, adaptada apenas no tamanho. Ela informa:

- quem somos (alunos de MES da PUC Minas) e para que serve a pesquisa;
- o público procurado: quem cria ou mantém dashboards, relatórios, bases, pipelines ou automações;
- o tempo estimado (10 a 15 minutos, medido no pré-teste) e o fato de a pesquisa ser anônima;
- o pedido para repassar o link a outras pessoas da área (bola de neve).

A mensagem não oferece recompensa, para não atrair respostas só pelo prêmio.

## Exclusão de colegas da turma

O formulário não tem pergunta para identificar colegas da disciplina (ela foi retirada após o pré-teste). Por isso, eles são excluídos aqui, na divulgação:

- o link **não** é publicado em grupos, fóruns ou canais da turma de MES nem na plataforma da disciplina;
- o link **não** é enviado diretamente a colegas de MES, mesmo os que trabalham com dados;
- a mensagem de divulgação pede: *"Se você cursa Medição e Experimentação de Software na PUC Minas neste semestre, por favor não responda."*

## Canais principais

| Canal | Ação | Responsável |
|---|---|---|
| LinkedIn (perfis pessoais) | Post de cada integrante, com a mensagem e o link | Todos |
| LinkedIn (mensagem direta) | Convite individual para contatos que atuam com dados, BI, CRM ou automação | Todos |
| Empresas dos integrantes | Envio a colegas de trabalho e ex-colegas da área, pelo canal interno de cada empresa (Teams, Slack, e-mail), com autorização do gestor quando a política interna exigir | Todos |
| Grupos de WhatsApp e Telegram | Grupos de dados, BI, Power BI e automação de que os integrantes já participam | Diogo |
| Comunidades no Discord | Servidores de dados e engenharia de dados, no canal de divulgação, respeitando as regras de cada servidor | Diogo |

## Canais reserva

São ativados se em **16/11** houver menos de **35 respostas brutas** (metade da meta de 70), conforme o ponto de controle do plano de ação.

| Canal reserva | Ação |
|---|---|
| Comunidades e grupos do LinkedIn | Post em grupos sobre dados, BI e RPA/low-code |
| Professores e coordenadores de cursos de dados | Pedido para repassar a ex-alunos que trabalham na área (sem incluir a turma atual de MES) |
| Reddit e fóruns brasileiros | r/brdev e fóruns de comunidades de dados, seguindo as regras de cada um |
| Segunda onda de mensagens diretas | Novo contato com quem visualizou e não respondeu, uma única vez |

Todo canal novo ou reserva usado é registrado em `docs/DESVIOS.md`.

## Calendário de divulgação e lembretes

Um novo post ou lembrete sai a cada 3 ou 4 dias. Cada pessoa ou grupo recebe no máximo 3 mensagens, para não se tornar spam.

| Data | Ação |
|---|---|
| **09/11 (seg)** | Abertura do formulário. Primeiros posts no LinkedIn, mensagens em grupos e envio nas empresas |
| 10/11 – 11/11 | Mensagens diretas no LinkedIn |
| **12/11 (qui)** | 1º lembrete nos grupos e repost no LinkedIn, com o número parcial de respostas |
| **16/11 (seg)** | Ponto de controle: se houver menos de 35 respostas brutas, ativar os canais reserva. 2º lembrete |
| **19/11 (qui)** | 3º lembrete: "últimos dias" |
| **22/11 (dom)** | Último aviso pela manhã e encerramento às 23h59 |

A contagem de respostas brutas é postada diariamente no grupo da equipe pelo integrante de plantão.

## Registro das evidências

Cada divulgação gera uma **captura de tela datada**, salva em `evidencias/divulgacao/` com o nome `AAAA-MM-DD_canal_descricao.png` (por exemplo, `2026-11-09_linkedin_post-diogo.png`).

- A captura deve mostrar a **data e a hora** da publicação (data visível na própria plataforma ou relógio do sistema na tela).
- Antes do commit, nomes, fotos e números de telefone de terceiros são **ocultados**, e só o texto da divulgação, o canal e a data ficam visíveis.
- O arquivo `evidencias/divulgacao/registro.md` lista cada divulgação com data, canal, responsável e arquivo correspondente.
- No encerramento, o painel do formulário (número de respostas por dia) também é capturado. A exportação bruta com data e hora de cada resposta é feita em 23/11 (Arthur).

Com esse registro, o dashboard pode cruzar os picos de respostas com as datas de divulgação.
