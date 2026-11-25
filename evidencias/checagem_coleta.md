# Checagem da coleta

Evidências de que a coleta seguiu o protocolo pré-registrado (seções 6 e 8).

## Pré-registro antes da primeira resposta

| Evento | Data e hora | Evidência |
|---|---|---|
| Commit do protocolo | 12/11/2026 19:23 | commit `08da3fb` |
| Tag `protocolo-v1` | 12/11/2026 19:31 | [release `protocolo-v1`](https://github.com/gustavoprehl/tp-final-survey-mes/releases/tag/protocolo-v1) |
| Envio do protocolo na plataforma da disciplina | 12/11/2026 19:42 | `evidencias/2026-11-12_envio-protocolo-plataforma.png` |
| **Primeira resposta** | **13/11/2026 16:12** | carimbo de data/hora no CSV exportado |
| Última resposta analisada | 23/11/2026 13:38 | carimbo de data/hora no CSV exportado |
| Resposta fora do período (não analisada) | 25/11/2026 10:21 | linha 32 da planilha do Forms; ver `docs/DESVIOS.md` |

**Resultado:** nenhuma resposta é anterior à tag. A primeira chegou cerca de 20h40 depois do pré-registro. A página "Metodologia e desvios" do dashboard refaz essa conferência a cada carga e mostra um alerta se alguma resposta for anterior à tag.

## Exportação bruta

| Item | Situação |
|---|---|
| Arquivo | `dados/brutos/respostas_2026-11-23.csv`, exportado da planilha do Google Forms em 23/11/2026 e commitado em 25/11/2026 (`84d7ece`) |
| Conteúdo | 30 respostas, com o carimbo de data/hora de cada uma e as 23 perguntas do formulário |
| Dados identificáveis | Nenhum: a coleta de e-mail estava desligada e o formulário não pergunta nome, e-mail, telefone ou empresa (seção 6) |
| Respostas abertas | Revisadas antes do commit; nenhuma citava nome de pessoa ou empresa, então nada foi substituído por `[removido]` |
| Encerramento | Previsto para 22/11. A exportação foi feita em 23/11, mas o formulário só foi fechado em 25/11, e 1 resposta chegou nesse intervalo (25/11 às 10:21). Ela não entra na análise, que usa as 30 respostas da exportação. Os dois desvios estão em `docs/DESVIOS.md` |

## Encerramento do formulário

O formulário foi fechado em 25/11/2026. Capturas:

- `evidencias/2026-11-25_forms-painel-encerrado.png`: painel do Google Forms com 31 respostas e o aviso "Este formulário não está aceitando respostas". As 31 são as 30 da exportação analisada mais a resposta de 25/11, que fica fora da análise.
- `evidencias/2026-11-25_forms-link-encerrado.png`: o link público do formulário informando que ele não aceita mais respostas.

## Carta de anuência

Não se aplica. A pesquisa não é feita dentro de uma organização específica nem usa dados de empresas: os participantes respondem individualmente e de forma anônima, e o formulário não identifica a empresa de quem responde. A divulgação em grupos de trabalho foi feita pelas redes pessoais dos integrantes.
