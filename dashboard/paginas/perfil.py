import plotly.express as px
import streamlit as st

import dados

respostas = st.session_state["respostas"]
validas = st.session_state["validas"]
filtradas = st.session_state["filtradas"]

st.title("Perfil da amostra")

col1, col2, col3 = st.columns(3)
col1.metric("Respostas recebidas", len(respostas))
col2.metric("Válidas", len(validas))
col3.metric("Descartadas", len(respostas) - len(validas))

st.subheader("Descartes por motivo")
contagem = (respostas["motivo_descarte"].value_counts()
            .reindex(dados.MOTIVOS, fill_value=0).rename_axis("Motivo").reset_index(name="Respostas"))
st.dataframe(contagem, hide_index=True, width="content")

st.subheader("Respostas por dia")
por_dia = respostas.groupby(respostas["timestamp"].dt.date).size().rename_axis("Dia").reset_index(name="Respostas")
st.plotly_chart(px.bar(por_dia, x="Dia", y="Respostas"), width="stretch")

st.info("**Em construção (#19):** distribuição de área, experiência, porte, setor, tamanho do time e "
        f"ferramentas, sobre as {len(filtradas)} respostas válidas do filtro atual.")
