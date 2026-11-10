# 6. Ética e LGPD

## Enquadramento

O survey é uma pesquisa de opinião com participantes não identificados, aplicada a profissionais adultos, sem intervenção e sem dados sensíveis. Pela Resolução CNS nº 510/2016 (art. 1º, parágrafo único, I), esse tipo de pesquisa não é registrado nem avaliado pelo sistema CEP/Conep. Mesmo assim, seguimos os princípios da resolução e da LGPD (Lei nº 13.709/2018): consentimento livre e esclarecido, coleta mínima, anonimato e uso exclusivamente acadêmico.

## Termo de consentimento (TCLE)

A primeira página do formulário apresenta o TCLE (Apêndice A, `questionario/criar_formulario.gs`), com:

- quem são os pesquisadores, a disciplina e a instituição;
- o objetivo da pesquisa e o tempo estimado (10 a 15 min);
- participação voluntária, com possibilidade de desistir a qualquer momento antes do envio;
- os dados que **não** são coletados e o uso apenas agregado das respostas;
- o fato de que, por serem anônimas, as respostas não podem ser localizadas nem retiradas depois do envio;
- onde os dados ficam, por quanto tempo e um e-mail de contato.

O aceite (TC1) é obrigatório. Quem responde "Não concordo" é levado direto ao envio, e a resposta é descartada (regra 1 da seção 5).

## Anonimização

| Medida | Como é aplicada |
|---|---|
| Coleta mínima | O formulário não pede nome, e-mail, empresa nem cargo exato. A coleta de e-mail e o limite de uma resposta por usuário ficam desligados, porque exigiriam login. Não há sorteio |
| Perfil em faixas | Experiência, porte e setor são coletados em categorias amplas, o que dificulta identificar uma pessoa pela combinação de respostas |
| Respostas abertas | Antes de qualquer commit, A1 e A2 são revisadas, e nomes de pessoas, empresas ou sistemas internos são substituídos por `[removido]` |
| Exibição agregada | O dashboard só mostra resultados agregados. Filtros que deixam menos de 5 respostas exibem o aviso de n pequeno e não mostram a distribuição |

O carimbo de data/hora é o único metadado mantido, porque é a evidência de que a coleta começou depois do pré-registro.

## Armazenamento e acesso

| Local | Conteúdo | Acesso | Prazo |
|---|---|---|---|
| Planilha de respostas do Google Forms | Export original | Apenas os três pesquisadores | Apagada ao fim do semestre letivo (dezembro/2026) |
| Repositório GitHub (`dados/brutos/`, `evidencias/`) | CSV anonimizado, com as respostas abertas revisadas | Grupo e professor | Mantido como evidência do trabalho |

O `.gitignore` bloqueia arquivos com "identificad", "contatos" ou "emails" no nome. As capturas de tela da divulgação mostram só a postagem e a data, sem nomes ou fotos de quem interagiu.
