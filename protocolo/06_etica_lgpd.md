# 6. Ética e LGPD

O survey é uma pesquisa de opinião com adultos não identificados, sem intervenção e sem dados sensíveis. Pela Resolução CNS nº 510/2016 (art. 1º, parágrafo único, I), não exige registro no sistema CEP/Conep. Mesmo assim, seguimos seus princípios e a LGPD (Lei nº 13.709/2018): consentimento livre e esclarecido, coleta mínima, anonimato e uso exclusivamente acadêmico.

**Termo de consentimento (TCLE).** Fica na primeira página do formulário (texto em `questionario/criar_formulario.gs`) e informa: os pesquisadores, a disciplina e a instituição; o objetivo e o tempo estimado; que a participação é voluntária e pode ser interrompida antes do envio; quais dados não são coletados e que o uso é só agregado; que, por serem anônimas, as respostas não podem ser localizadas nem retiradas após o envio; onde os dados ficam, por quanto tempo e um e-mail de contato. O aceite (TC1) é obrigatório, e quem não concorda vai direto ao envio.

| Medida de anonimização | Como é aplicada |
|---|---|
| Coleta mínima | Sem nome, e-mail, empresa ou cargo exato; coleta de e-mail e limite por usuário desligados, porque exigiriam login; sem sorteio |
| Perfil em faixas | Experiência, porte e setor em categorias amplas, para dificultar a identificação pela combinação de respostas |
| Respostas abertas | Antes de qualquer commit, nomes de pessoas, empresas ou sistemas internos em A1 e A2 são substituídos por `[removido]` |
| Exibição agregada | O dashboard só mostra agregados; filtros com menos de 5 respostas exibem aviso e não mostram a distribuição |

O único metadado mantido é o carimbo de data/hora, que comprova que a coleta começou depois do pré-registro.

| Armazenamento | Conteúdo | Acesso | Prazo |
|---|---|---|---|
| Planilha do Google Forms | Export original | Só os três pesquisadores | Apagada em dezembro/2026 |
| Repositório GitHub (`dados/brutos/`, `evidencias/`) | CSV anonimizado, abertas revisadas | Grupo e professor | Mantido como evidência |

O `.gitignore` bloqueia arquivos de identificação ou contatos, e as capturas da divulgação mostram só a postagem e a data.
