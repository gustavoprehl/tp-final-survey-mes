import streamlit as st

filtradas = st.session_state["filtradas"]

st.title("Questões de pesquisa")
st.caption(f"n = {len(filtradas)} respostas válidas no filtro atual")

QUESTOES = {
    "QP1": ("Quais métricas os profissionais de dados e automação usam de fato para avaliar suas entregas?",
            "Proporção de cada métrica (M1) com margem de erro de 95%; códigos das respostas abertas (A1)."),
    "QP2": ("A utilidade percebida das métricas difere entre áreas de atuação?",
            "Kruskal-Wallis do escore UT por área (P1), ε² e pós-teste de Dunn com Holm."),
    "QP3": ("Quem mede a qualidade dos dados de forma estruturada relata menos retrabalho?",
            "Mann-Whitney U unilateral de M3 entre \"mede\" e \"não mede\" (M2), r rank-biserial; M4 como secundária."),
    "QP4": ("A maturidade de medição do time está associada ao tempo de experiência do profissional?",
            "Correlação de Spearman entre o escore MM e a experiência (P2)."),
}

for aba, (codigo, (pergunta, analise)) in zip(st.tabs(list(QUESTOES)), QUESTOES.items()):
    with aba:
        st.subheader(f"{codigo}: {pergunta}")
        st.info(f"**Em construção (#18, #22):** {analise} Cada resultado mostra a estatística do teste, "
                "o p-valor bruto e ajustado (Holm), o tamanho de efeito e o n.")
