import pandas as pd
import streamlit as st

import componentes as ui
import dados
import estatistica as est

validas = st.session_state["validas"]
filtradas = st.session_state["filtradas"]
filtro_ativo = len(filtradas) < len(validas)

st.title("Confiabilidade dos construtos")
ui.exigir_n_minimo(validas)
st.caption("Alfa de Cronbach com IC de 95% (método de Feldt), calculado com os itens reversos (UT4, MM4) já "
           "invertidos. Regras da seção 5: aceito com α ≥ 0,70; limitação declarada entre 0,60 e 0,70; abaixo de "
           "0,60, o escore só é recalculado sem um item se isso levar a α ≥ 0,70, e a mudança vira desvio. "
           "A decisão é tomada uma única vez, na amostra completa de respostas válidas, e não muda com os filtros.")

CONSTRUTOS = {
    "UT · Utilidade percebida (QP2)": dados.ITENS_UT,
    "MM · Maturidade de medição (QP4)": dados.ITENS_MM,
}


def colunas_num(itens):
    return [f"{i}_num" for i in itens]


def linha_resumo(nome, itens, df, com_decisao):
    r = est.cronbach(df[colunas_num(itens)])
    linha = {"Construto": nome, "Itens": ", ".join(itens), "n": r["n"], "α": ui.num(r["alfa"], 3),
             "IC 95%": f"{ui.num(r['ic_inf'], 2)} a {ui.num(r['ic_sup'], 2)}"}
    if com_decisao:
        linha["Decisão"] = est.decisao_cronbach(r["alfa"])
    return linha


st.subheader("Amostra completa (decisão)")
st.dataframe(pd.DataFrame([linha_resumo(nome, itens, validas, True) for nome, itens in CONSTRUTOS.items()]),
             hide_index=True, width="stretch")

for coluna, (nome, itens) in zip(st.columns(2), CONSTRUTOS.items()):
    with coluna:
        st.markdown(f"**{nome}**")
        tabela = est.alfa_sem_item(validas[colunas_num(itens)])
        tabela["Item"] = tabela["Item"].str.removesuffix("_num").map(lambda i: f"{i} (R)" if i in dados.REVERSOS else i)
        st.dataframe(tabela.round(3), hide_index=True, width="stretch")
        alfa = est.cronbach(validas[colunas_num(itens)])["alfa"]
        melhor = tabela.loc[tabela["Alfa sem o item"].idxmax()]
        if alfa < 0.60 and melhor["Alfa sem o item"] >= 0.70:
            st.warning(f"Pela regra da seção 5, o escore passa a ser calculado sem {melhor['Item']} "
                       f"(α = {ui.num(melhor['Alfa sem o item'], 3)}). Registrar em docs/DESVIOS.md.")
        elif alfa < 0.60:
            st.error("Nenhuma remoção de item leva a α ≥ 0,70: pela seção 5, a QP deste construto é analisada "
                     "item a item, como exploratória. Registrar em docs/DESVIOS.md.")
        elif alfa < 0.70:
            st.info("0,60 ≤ α < 0,70: o escore é usado, e o alfa abaixo de 0,70 entra nas limitações.")
        if alfa >= 0.60 and melhor["Alfa sem o item"] > alfa:
            st.caption(f"Sem {melhor['Item']}, o alfa subiria para {ui.num(melhor['Alfa sem o item'], 3)}. "
                       "Informativo: a regra de remoção só se aplica com α < 0,60.")

st.caption("Correlação item-total corrigida: correlação de cada item com a soma dos demais. Valores baixos ou "
           "negativos indicam item que mede outra coisa ou reverso não invertido.")

if filtro_ativo:
    st.subheader(f"Segmento filtrado (exploratório, n = {len(filtradas)})")
    if len(filtradas) < ui.N_MIN_EXIBICAO:
        st.warning(f"O filtro deixa {len(filtradas)} resposta(s); com menos de {ui.N_MIN_EXIBICAO}, o alfa "
                   "do segmento não é exibido (seção 6).")
    else:
        st.dataframe(pd.DataFrame([linha_resumo(nome, itens, filtradas, False)
                                   for nome, itens in CONSTRUTOS.items()]), hide_index=True, width="stretch")
        st.caption("Apenas descritivo: com poucas respostas o alfa é instável (veja a largura do IC) e não altera "
                   "a decisão tomada na amostra completa.")
