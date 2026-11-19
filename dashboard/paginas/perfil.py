import plotly.express as px
import streamlit as st

import componentes as ui
import dados
import estatistica as est

respostas = st.session_state["respostas"]
validas = st.session_state["validas"]
filtradas = st.session_state["filtradas"]

st.title("Perfil da amostra")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Respostas recebidas", len(respostas))
col2.metric("Válidas", len(validas))
col3.metric("Descartadas", len(respostas) - len(validas))
col4.metric("Margem de erro (n válido)", f"± {ui.num(100 * est.margem_erro(len(validas)), 1)} p.p.",
            help="Pior caso (p = 0,5), 95% de confiança: 1,96 × √(0,25 / n).")

esquerda, direita = st.columns([2, 3])
with esquerda:
    st.subheader("Descartes por motivo")
    contagem = (respostas["motivo_descarte"].value_counts()
                .reindex(dados.MOTIVOS, fill_value=0).rename_axis("Motivo").reset_index(name="Respostas"))
    st.dataframe(contagem, hide_index=True, width="stretch")
    st.caption("Cada resposta recebe o motivo da primeira regra que a elimina (seção 5 do protocolo).")
with direita:
    st.subheader("Respostas por dia")
    por_dia = (respostas.assign(Situação=respostas["motivo_descarte"].isna().map({True: "Válida", False: "Descartada"}),
                                Dia=respostas["timestamp"].dt.date)
               .groupby(["Dia", "Situação"]).size().reset_index(name="Respostas"))
    st.plotly_chart(px.bar(por_dia, x="Dia", y="Respostas", color="Situação", height=280,
                           color_discrete_map={"Válida": "#2166ac", "Descartada": "#bbbbbb"}), width="stretch")

st.divider()
ui.exigir_n_minimo(filtradas)
st.subheader(f"Perfil das respostas válidas (n = {len(filtradas)})")


def barras(coluna, titulo, ordem=None):
    contagem = filtradas[coluna].value_counts()
    if ordem:
        contagem = contagem.reindex([o for o in ordem if o in contagem.index] +
                                    [o for o in contagem.index if o not in ordem])
    tabela = contagem.rename_axis(titulo).reset_index(name="Respostas")
    tabela["%"] = tabela["Respostas"] / len(filtradas)
    figura = px.bar(tabela, x="Respostas", y=titulo, orientation="h", text=tabela["%"].map(ui.pct),
                    height=60 + 32 * len(tabela))
    figura.update_layout(yaxis={"categoryorder": "array", "categoryarray": tabela[titulo][::-1]},
                         margin={"l": 0, "r": 10, "t": 10, "b": 0}, yaxis_title=None)
    st.markdown(f"**{titulo}**")
    st.plotly_chart(figura, width="stretch")


c1, c2 = st.columns(2)
with c1:
    barras("P1_grupo", "Área de atuação", dados.AREAS + ["Outra"])
    barras("P3", "Porte da empresa", dados.PORTE + ["Não sei"])
with c2:
    barras("P2", "Tempo de experiência", dados.EXPERIENCIA)
    barras("P4", "Setor")

c1, c2 = st.columns(2)
with c1:
    st.markdown("**Tamanho do time direto (P5)**")
    p5 = filtradas["P5_num"].dropna()
    st.dataframe({"Mediana": [p5.median()], "IIQ": [f"{ui.num(p5.quantile(.25), 0)} a {ui.num(p5.quantile(.75), 0)}"],
                  "Mínimo": [p5.min()], "Máximo": [p5.max()]}, hide_index=True)
    st.plotly_chart(px.histogram(p5, nbins=15, height=230, labels={"value": "Pessoas no time"})
                    .update_layout(showlegend=False, margin={"t": 10, "b": 0}, yaxis_title="Respostas"),
                    width="stretch")
with c2:
    st.markdown("**Ferramentas usadas com frequência (P6, múltipla escolha)**")
    marcadas, _ = dados.separar_multipla(filtradas["P6"], dados.FERRAMENTAS)
    uso = marcadas.mean().sort_values().rename_axis("Ferramenta").reset_index(name="Proporção")
    st.plotly_chart(px.bar(uso, x="Proporção", y="Ferramenta", orientation="h", text=uso["Proporção"].map(ui.pct),
                           height=360).update_layout(xaxis_tickformat=".0%", yaxis_title=None,
                                                     margin={"t": 10, "b": 0}), width="stretch")
