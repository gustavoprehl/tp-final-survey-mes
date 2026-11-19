import pandas as pd
import streamlit as st

import componentes as ui
import dados
import estatistica as est

validas = st.session_state["validas"]
filtradas = st.session_state["filtradas"]

st.title("Confiabilidade dos construtos")
ui.aviso_filtro(filtradas, validas)
ui.exigir_n_minimo(filtradas)
st.caption("Alfa de Cronbach com IC de 95% (método de Feldt), calculado com os itens reversos (UT4, MM4) já "
           "invertidos. Regras da seção 5: aceito com α ≥ 0,70; limitação declarada entre 0,60 e 0,70; abaixo de "
           "0,60, o escore só é recalculado sem um item se isso levar a α ≥ 0,70, e a mudança vira desvio.")

CONSTRUTOS = {
    "UT · Utilidade percebida (QP2)": dados.ITENS_UT,
    "MM · Maturidade de medição (QP4)": dados.ITENS_MM,
}

resumo = []
for nome, itens in CONSTRUTOS.items():
    r = est.cronbach(filtradas[[f"{i}_num" for i in itens]])
    resumo.append({"Construto": nome, "Itens": ", ".join(itens), "n": r["n"], "α": ui.num(r["alfa"], 3),
                   "IC 95%": f"{ui.num(r['ic_inf'], 2)} a {ui.num(r['ic_sup'], 2)}",
                   "Decisão": est.decisao_cronbach(r["alfa"])})
st.dataframe(pd.DataFrame(resumo), hide_index=True, width="stretch")

for coluna, (nome, itens) in zip(st.columns(2), CONSTRUTOS.items()):
    with coluna:
        st.markdown(f"**{nome}**")
        tabela = est.alfa_sem_item(filtradas[[f"{i}_num" for i in itens]])
        tabela["Item"] = tabela["Item"].str.removesuffix("_num").map(lambda i: f"{i} (R)" if i in dados.REVERSOS else i)
        st.dataframe(tabela.round(3), hide_index=True, width="stretch")
        alfa = est.cronbach(filtradas[[f"{i}_num" for i in itens]])["alfa"]
        melhor = tabela.loc[tabela["Alfa sem o item"].idxmax()]
        if alfa < 0.60 and melhor["Alfa sem o item"] >= 0.70:
            st.warning(f"Pela regra da seção 5, o escore passaria a ser calculado sem {melhor['Item']} "
                       f"(α = {ui.num(melhor['Alfa sem o item'], 3)}). Registrar em docs/DESVIOS.md.")
        elif melhor["Alfa sem o item"] > alfa:
            st.caption(f"Sem {melhor['Item']}, o alfa subiria para {ui.num(melhor['Alfa sem o item'], 3)}. "
                       "Informativo: a regra de remoção só se aplica com α < 0,60.")

st.caption("Correlação item-total corrigida: correlação de cada item com a soma dos demais. Valores baixos ou "
           "negativos indicam item que mede outra coisa ou reverso não invertido.")
