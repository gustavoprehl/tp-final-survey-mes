# Questionário

- [matriz_rastreabilidade.md](matriz_rastreabilidade.md): questões de pesquisa, itens, métricas, escalas, construtos e regras de descarte
- [criar_formulario.gs](criar_formulario.gs): Google Apps Script que gera o Google Forms e a planilha de respostas

## Gerar o formulário

1. Acesse https://script.google.com, crie um projeto e cole o conteúdo de `criar_formulario.gs`.
2. Preencha `CONFIG.contato` com o e-mail de contato do grupo (aparece no TCLE).
3. Execute `criarFormulario` e autorize o acesso. Os links de edição, de resposta e da planilha aparecem no registro de execução.

**Pré-teste:** rode com `CONFIG.preTeste = true`. O script cria uma cópia separada, já aberta, com "[PRÉ-TESTE]" no título. Essas respostas não entram na amostra.

**Formulário oficial:** é criado **fechado para respostas**. Só abra (aba Respostas → "Aceitando respostas") depois do commit com a tag `protocolo-v1`.

Depois do pré-teste, aplique as mudanças no script e na matriz, e gere o formulário oficial de novo.
