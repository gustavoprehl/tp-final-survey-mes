# Dashboard

App Streamlit que lê o CSV bruto exportado do formulário, aplica as regras de descarte da seção 5 do protocolo e mostra os resultados.

## Executar

Na raiz do repositório (Windows):

```
py -m venv .venv
.venv\Scripts\activate
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
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
| `paginas/perfil.py` | Respostas recebidas, válidas e descartadas por motivo; perfil da amostra (#19) |
| `paginas/likert.py` | Barras divergentes dos itens Likert (#20) |
| `paginas/questoes.py` | QP1–QP4 com teste, p-valor, tamanho de efeito e margem de erro (#18, #22) |
| `paginas/confiabilidade.py` | Alfa de Cronbach (#21) |
| `paginas/metodologia.py` | Pré-registro, desvios (`docs/DESVIOS.md`) e limitações (#23) |

As páginas leem de `st.session_state` três tabelas: `respostas` (todas, com `motivo_descarte`), `validas` e `filtradas` (válidas com os filtros da barra lateral aplicados).
