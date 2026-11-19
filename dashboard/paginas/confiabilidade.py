import streamlit as st

filtradas = st.session_state["filtradas"]

st.title("Confiabilidade dos construtos")
st.caption(f"n = {len(filtradas)} respostas válidas no filtro atual")

st.info("**Em construção (#21):** alfa de Cronbach, com IC de 95%, de UT (UT1–UT4) e MM (MM1–MM4), "
        "já com os itens reversos invertidos, e o alfa sem cada item. Limiares da seção 5 do protocolo: "
        "aceito com α ≥ 0,70; limitação declarada entre 0,60 e 0,70; abaixo de 0,60, regra de remoção de item.")
