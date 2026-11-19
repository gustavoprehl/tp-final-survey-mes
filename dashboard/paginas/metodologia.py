import pandas as pd
import streamlit as st

import componentes as ui
import dados
import estatistica as est

respostas = st.session_state["respostas"]
validas = st.session_state["validas"]

st.title("Metodologia e desvios")

st.subheader("Pré-registro")
inicio, fim = respostas["timestamp"].min(), respostas["timestamp"].max()
st.markdown(
    "O protocolo foi pré-registrado com a tag "
    "[`protocolo-v1`](https://github.com/gustavoprehl/tp-final-survey-mes/releases/tag/protocolo-v1) "
    "em **12/11/2026 às 19:23**, e enviado na plataforma da disciplina às 19:42. "
    f"A primeira resposta da base atual é de **{inicio:%d/%m/%Y %H:%M}** e a última, de **{fim:%d/%m/%Y %H:%M}**."
)
if inicio < pd.Timestamp("2026-11-12 19:23"):
    st.error("Há respostas anteriores à tag protocolo-v1. Verifique a base antes da apresentação.")

st.subheader("Desenho do estudo")
st.dataframe(pd.DataFrame([
    ("População", "Profissionais que criam ou mantêm produtos de dados ou automação em empresas brasileiras"),
    ("Amostragem", "Não probabilística, por conveniência, com bola de neve"),
    ("Período de coleta", "12/11 a 22/11/2026"),
    ("Respostas", f"{len(respostas)} recebidas, {len(validas)} válidas, {len(respostas) - len(validas)} descartadas"),
    ("Margem de erro", f"± {ui.num(100 * est.margem_erro(len(validas)), 1)} p.p. (95%, p = 0,5, n = {len(validas)}); "
                       "não inclui o viés de seleção"),
    ("Instrumento", "Google Forms, 23 itens, 2 construtos de 4 itens (UT e MM), pergunta de atenção"),
    ("Análise", "Testes não paramétricos, α = 0,05, Holm na família principal (QP2, QP3, QP4)"),
], columns=["Aspecto", "Descrição"]), hide_index=True, width="stretch")

st.subheader("Desvios em relação ao protocolo")
st.markdown((dados.RAIZ / "docs" / "DESVIOS.md").read_text(encoding="utf-8").split("\n", 1)[1])

st.subheader("Limitações")
st.markdown("""
- **Amostra por conveniência e bola de neve:** os resultados descrevem a amostra e não são generalizados para todos os profissionais da área. A amostra tende a se parecer com as redes dos integrantes.
- **Autosseleção:** pessoas mais interessadas em métricas tendem a responder mais.
- **Não resposta:** quem não respondeu pode ser diferente de quem respondeu. A taxa de resposta por canal aparece abaixo, quando o alcance é conhecido.
- **Desejabilidade social:** respondentes podem declarar mais medição ou utilidade do que existe, apesar do anonimato e dos itens reversos.
- **Viés de método único:** todas as medidas são autorrelatadas.
- **Associação, não causa:** a QP3 não controla porte, setor ou tipo de entrega.
- **Colegas da turma:** a exclusão foi feita na divulgação; o repasse do link por terceiros não pode ser controlado.
- **Tempo de preenchimento:** o Google Forms não registra o início, então respostas muito rápidas não podem ser detectadas.
""")

st.subheader("Divulgação e taxa de resposta por canal")
registro = dados.RAIZ / "evidencias" / "divulgacao" / "registro.md"
if registro.exists():
    st.markdown(registro.read_text(encoding="utf-8").split("\n", 1)[1])
else:
    st.info("O registro das divulgações (`evidencias/divulgacao/registro.md`, com data, canal, alcance e captura) "
            "ainda não foi criado. Quando existir, aparece aqui.")
