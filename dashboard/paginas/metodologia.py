import streamlit as st

import dados

st.title("Metodologia e desvios")

st.markdown(
    "O protocolo foi pré-registrado com a tag "
    "[`protocolo-v1`](https://github.com/gustavoprehl/tp-final-survey-mes/releases/tag/protocolo-v1) "
    "em 12/11/2026, antes da primeira resposta. A coleta foi de 12/11 a 22/11/2026, por amostragem "
    "por conveniência com bola de neve."
)

st.subheader("Desvios em relação ao protocolo")
st.markdown((dados.RAIZ / "docs" / "DESVIOS.md").read_text(encoding="utf-8").split("\n", 1)[1])

st.info("**Em construção (#23):** limitações (não resposta, autosseleção, desejabilidade social, "
        "amostra por conveniência) e taxa de resposta estimada por canal.")
