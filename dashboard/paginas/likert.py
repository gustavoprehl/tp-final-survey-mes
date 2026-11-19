import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import componentes as ui
import dados

validas = st.session_state["validas"]
filtradas = st.session_state["filtradas"]

st.title("Itens Likert")
ui.aviso_filtro(filtradas, validas)
ui.exigir_n_minimo(filtradas)
st.caption(f"n = {len(filtradas)} respostas válidas. Barras centradas em \"Neutro\", que é dividido "
           "ao meio entre os dois lados. Itens marcados com (R) são reversos e aparecem com a resposta original.")

ROTULOS = {
    "UT1": "UT1 · Ajudam a decidir o que melhorar",
    "UT2": "UT2 · Refletem o valor das entregas",
    "UT3": "UT3 · Decisões se baseiam nelas",
    "UT4": "UT4 (R) · Tomam tempo sem benefício",
    "MM1": "MM1 · Time define metas ou limites",
    "MM2": "MM2 · Revisadas periodicamente",
    "MM3": "MM3 · Coleta automática",
    "MM4": "MM4 (R) · Cada um mede do seu jeito",
}
CORES = ["#b2182b", "#ef8a62", "#c8c8c8", "#67a9cf", "#2166ac"]


def proporcoes(itens):
    return pd.DataFrame({item: filtradas[item].value_counts(normalize=True).reindex(dados.LIKERT, fill_value=0)
                         for item in itens}).T


def divergente(itens, titulo):
    prop = proporcoes(itens).iloc[::-1]  # primeiro item no topo
    rotulos = [ROTULOS[i] for i in prop.index]
    figura = go.Figure()
    lados = [("Neutro", -0.5, False), ("Discordo", -1, True), ("Discordo totalmente", -1, True),
             ("Neutro", 0.5, True), ("Concordo", 1, True), ("Concordo totalmente", 1, True)]
    for categoria, fator, legenda in lados:
        valores = prop[categoria] * fator
        # o rótulo do "Neutro" fica só no hover, porque ele aparece dividido nos dois lados
        texto = [ui.pct(v, 0) if v >= 0.06 and categoria != "Neutro" else "" for v in prop[categoria]]
        figura.add_bar(y=rotulos, x=valores, name=categoria, orientation="h", showlegend=legenda,
                       marker_color=CORES[dados.LIKERT.index(categoria)], text=texto, textposition="inside",
                       hovertemplate=f"{categoria}: %{{customdata}}<extra></extra>",
                       customdata=[ui.pct(v) for v in prop[categoria]])
    figura.update_layout(barmode="relative", height=90 + 48 * len(itens), title=titulo,
                         xaxis={"tickformat": ".0%", "range": [-1, 1], "zeroline": True, "zerolinecolor": "#555"},
                         legend={"orientation": "h", "y": -0.15, "traceorder": "normal"},
                         margin={"l": 0, "r": 10, "t": 40, "b": 10})
    figura.update_xaxes(tickvals=[-1, -0.5, 0, 0.5, 1], ticktext=["100%", "50%", "0", "50%", "100%"])
    st.plotly_chart(figura, width="stretch")


divergente(dados.ITENS_UT, "Utilidade percebida das métricas (UT, QP2)")
divergente(dados.ITENS_MM, "Maturidade de medição do time (MM, QP4)")

st.subheader("Resumo por item")
linhas = []
for item in dados.ITENS_LIKERT:
    original = filtradas[item].map({t: i for i, t in enumerate(dados.LIKERT, 1)})
    prop = filtradas[item].value_counts(normalize=True)
    linhas.append({
        "Item": ROTULOS[item],
        "Mediana (1–5)": original.median(),
        "IIQ": f"{ui.num(original.quantile(.25), 1)} a {ui.num(original.quantile(.75), 1)}",
        "Concorda (4–5)": ui.pct(prop.get("Concordo", 0) + prop.get("Concordo totalmente", 0)),
        "Discorda (1–2)": ui.pct(prop.get("Discordo", 0) + prop.get("Discordo totalmente", 0)),
    })
st.dataframe(pd.DataFrame(linhas), hide_index=True, width="stretch")
st.caption("Itens Likert isolados são ordinais: são resumidos por mediana e IIQ, nunca pela média (seção 5).")
