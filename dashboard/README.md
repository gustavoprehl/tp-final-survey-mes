# Dashboard

App Streamlit que lê o CSV bruto exportado do formulário, aplica as regras de descarte da seção 5 do protocolo e mostra os resultados.

## Executar

Na raiz do repositório (Windows):

```
py -m venv .venv
.venv\Scripts\python -m pip install -r dashboard/requirements.txt
.venv\Scripts\streamlit run dashboard/app.py
```

Os comandos chamam o Python e o Streamlit direto do `.venv`, sem `activate`. No PowerShell, o `activate` costuma ser bloqueado pela política de execução de scripts.

## Testes

O módulo estatístico é conferido contra valores de referência do pingouin e do scikit-posthocs e com os dados sintéticos:

```
.venv\Scripts\python -m pip install -r dashboard/requirements-dev.txt
.venv\Scripts\python -m pytest dashboard/tests
```

## Dados

- **Reais:** exporte a planilha de respostas (Arquivo → Fazer download → CSV) e salve em `dados/brutos/`, já anonimizada (seção 6). O dashboard usa o CSV mais recente dessa pasta.
- **Sintéticos:** sem CSV em `dados/brutos/`, o dashboard usa `dados/sinteticos/respostas_sinteticas.csv` e mostra um aviso. Para gerar de novo: `python dados/sinteticos/gerar_sinteticos.py`.
- **Fora da população (regra 2):** respostas com área "Outra" julgadas fora da população vão em `dados/descartes_fora_populacao.csv`, com as colunas `timestamp`, `decisao_1` e `decisao_2` (`fora` ou `dentro`). Só sai a resposta que os dois pesquisadores marcaram como `fora`.

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `app.py` | Entrada: fonte de dados, filtros por segmento (barra lateral) e navegação |
| `dados.py` | Leitura do CSV, códigos da matriz, codificação das escalas, escores UT/MM e descartes |
| `estatistica.py` | Margem de erro, Holm, Kruskal-Wallis + ε², Dunn, Mann-Whitney + r rank-biserial, Spearman, alfa de Cronbach (IC de Feldt) |
| `analises.py` | Aplica os testes às QPs; família principal (QP2, QP3, QP4) com Holm na amostra completa |
| `componentes.py` | Formatação em português, cartão de resultado de teste (com aviso quando o menor grupo tem n < 5) e bloqueio de filtros com n < 5 |
| `tests/` | Testes do módulo estatístico (pytest) |
| `paginas/perfil.py` | Recebidas, válidas e descartes por motivo; respostas por dia; perfil (P1–P6) |
| `paginas/likert.py` | Barras divergentes de UT e MM, mediana e IIQ por item |
| `paginas/questoes.py` | QP1–QP4: visualização, teste, p-valor bruto e ajustado, tamanho de efeito, n e margem de erro |
| `paginas/confiabilidade.py` | Alfa de Cronbach com IC 95%, decisão pela regra da seção 5, alfa sem cada item |
| `paginas/metodologia.py` | Pré-registro, desenho do estudo, desvios (`docs/DESVIOS.md`), limitações e divulgação |

Com filtro ativo, os testes da família principal continuam calculados na amostra completa; o recálculo no segmento aparece à parte, como exploratório e sem Holm (seção 5).

As páginas leem de `st.session_state` três tabelas: `respostas` (todas, com `motivo_descarte`), `validas` e `filtradas` (válidas com os filtros da barra lateral aplicados).

## Testes

```
.venv\Scripts\python -m pip install -r dashboard/requirements-dev.txt
.venv\Scripts\python -m pytest dashboard/tests
```

## Deploy (Streamlit Community Cloud)

O repositório já está pronto: `dashboard/requirements.txt` fica ao lado do `app.py` (é onde o Cloud procura) e `.streamlit/config.toml` fica na raiz.

1. Acesse https://share.streamlit.io e entre com a conta do GitHub dona do repositório. Autorize o acesso a repositórios privados.
2. **Create app** → *Deploy a public app from GitHub* (o app herda a privacidade do repositório):
   - Repository: `gustavoprehl/tp-final-survey-mes`
   - Branch: `main`
   - Main file path: `dashboard/app.py`
3. Em **Advanced settings**, escolha **Python 3.13** e clique em **Deploy**.
4. Como o repositório é privado, o app também é: em **Settings → Sharing**, adicione os e-mails de quem pode ver (professor e integrantes).

O app lê o CSV de `dados/brutos/` direto do repositório. Para atualizar os dados, faça commit de um novo `respostas_AAAA-MM-DD.csv` (o dashboard usa o de nome mais recente); o Cloud reinstala e recarrega sozinho a cada push na `main`.
