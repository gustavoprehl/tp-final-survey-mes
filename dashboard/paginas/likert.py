import streamlit as st

filtradas = st.session_state["filtradas"]

st.title("Itens Likert")
st.caption(f"n = {len(filtradas)} respostas válidas no filtro atual")

st.info("**Em construção (#20):** gráfico de barras divergentes, centrado em \"Neutro\", para os itens "
        "UT1–UT4 (utilidade percebida) e MM1–MM4 (maturidade de medição). Os itens reversos (UT4, MM4) "
        "aparecem com a resposta original e são sinalizados.")
