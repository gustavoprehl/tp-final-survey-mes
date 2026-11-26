"""Visão geral: o resumo do survey numa tela (KPIs, perfil, Likert, QP1 e achados)."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import analises
import componentes as ui
import dados
import estatistica as est
import tema

respostas = st.session_state["respostas"]
validas = st.session_state["validas"]
filtradas = st.session_state["filtradas"]
construtos = st.session_state["construtos"]
filtro_ativo = len(filtradas) < len(validas)

topo_esq, topo_dir = st.columns([3, 1], vertical_alignment="bottom")
topo_esq.title("Uso de métricas em produtos de dados e automação")
topo_dir.markdown(f'<div style="text-align:right"><span class="chip">'
                  f'{"Filtro: " if filtro_ativo else ""}n = {len(filtradas)} de {len(validas)}</span></div>',
                  unsafe_allow_html=True)

# ---- KPIs (amostra completa) --------------------------------------------------
descartadas = len(respostas) - len(validas)
k = st.columns(6)
tema.kpi(k[0], "Recebidas", len(respostas), "respostas no formulário")
tema.kpi(k[1], "Válidas", len(validas), "após as regras da seção 5")
tema.kpi(k[2], "Descarte", ui.pct(descartadas / len(respostas) if len(respostas) else 0, 0),
         f"{descartadas} resposta(s)")
tema.kpi(k[3], "Margem de erro", f"±{ui.num(100 * est.margem_erro(len(validas)), 1)} p.p.", "95%, pior caso")
for coluna, nome, titulo in [(k[4], "UT", "α Utilidade"), (k[5], "MM", "α Maturidade")]:
    d = construtos[nome]
    nota = ("item a item" if d["item_a_item"] else f"sem {d['removido']}" if d["removido"] else "4 itens") \
        + (" · ok" if d["alfa_final"] >= 0.60 and not d["item_a_item"] else "")
    tema.kpi(coluna, titulo, ui.num(d["alfa_final"], 2), nota)

st.write("")

# ---- Achados das questões de pesquisa -----------------------------------------
st.subheader("Principais achados")
familia = analises.familia_principal(validas, construtos)
tabela_qp1, _, _ = analises.qp1(validas)
lider = tabela_qp1.iloc[0]

cartoes = st.columns(4)
tema.achado(cartoes[0], "QP1 · Métricas usadas", "descritiva",
            f"A mais citada é <b>{lider['Métrica']}</b>, usada por {ui.pct(lider['Proporção'], 0)} dos respondentes.",
            f"IC 95%: {ui.pct(lider['IC inferior'], 0)} a {ui.pct(lider['IC superior'], 0)}", "desc")
TITULOS = {"QP2": "QP2 · Utilidade × área", "QP3": "QP3 · Qualidade × retrabalho",
           "QP4": "QP4 · Maturidade × experiência"}
for coluna, qp in zip(cartoes[1:], TITULOS):
    itens = {chave: r for chave, r in familia.items() if chave.split(" ·")[0] == qp}
    if qp in itens:  # escore do construto
        r = itens[qp]
        rejeita = r["p_ajustado"] < est.ALFA
        texto = analises.conclusao(qp, r, r["p_ajustado"]).split(". ")[0] + "."
        numeros = (f"{r['teste']} · p Holm {ui.p_valor(r['p_ajustado']).removeprefix('p ')} · "
                   f"efeito {est.magnitude(r['efeito'], r['limiares'])} · n = {r['n']}")
    else:  # regra de confiabilidade mandou analisar item a item
        rejeita = any(r["p_ajustado"] < est.ALFA for r in itens.values())
        significativos = [c.split("· ")[1] for c, r in itens.items() if r["p_ajustado"] < est.ALFA]
        texto = ("Analisada item a item (α baixo). "
                 + (f"Diferença em {', '.join(significativos)}." if significativos else "Nenhum item significativo."))
        numeros = "exploratória · ver Questões de pesquisa"
    tema.achado(coluna, TITULOS[qp], "rejeita H0" if rejeita else "não rejeita H0", texto, numeros,
                "sim" if rejeita else "")
st.caption("Testes na amostra completa, α = 0,05 com correção de Holm. Detalhes, pós-testes e tabelas na página "
           "*Questões de pesquisa*.")

st.divider()

# ---- Distribuições (seguem o filtro) -------------------------------------------
ui.exigir_n_minimo(filtradas)


def barras_h(contagem, altura=None, formato_pct=True):
    tabela = contagem.rename_axis("Categoria").reset_index(name="Valor")
    texto = tabela["Valor"].map(lambda v: ui.pct(v, 0)) if formato_pct else tabela["Valor"]
    figura = px.bar(tabela, x="Valor", y="Categoria", orientation="h", text=texto,
                    height=altura or 50 + 30 * len(tabela))
    figura.update_traces(marker_color=tema.PRIMARIA, textposition="outside", cliponaxis=False)
    figura.update_layout(yaxis={"categoryorder": "array", "categoryarray": tabela["Categoria"][::-1], "title": None},
                         xaxis={"visible": False, "range": [0, tabela["Valor"].max() * 1.2]})
    return figura


def proporcao(coluna, ordem):
    contagem = filtradas[coluna].value_counts(normalize=True)
    return contagem.reindex([o for o in ordem if o in contagem.index] +
                            [o for o in contagem.index if o not in ordem])


esq, dir_ = st.columns(2, gap="large")
with esq:
    with st.container(border=True):
        st.markdown("**Quais métricas os times usam (QP1)**")
        tabela = analises.qp1(filtradas)[0].head(7).set_index("Métrica")["Proporção"]
        st.plotly_chart(barras_h(tabela), width="stretch", config={"displayModeBar": False})
with dir_:
    with st.container(border=True):
        st.markdown("**Concordância nos itens Likert**")
        curtos = {"UT1": "UT1 Ajudam a decidir", "UT2": "UT2 Refletem valor", "UT3": "UT3 Baseiam decisões",
                  "UT4": "UT4 (R) Tomam tempo", "MM1": "MM1 Metas definidas", "MM2": "MM2 Revisão periódica",
                  "MM3": "MM3 Coleta automática", "MM4": "MM4 (R) Cada um mede"}
        prop = pd.DataFrame({i: filtradas[i].value_counts(normalize=True).reindex(dados.LIKERT, fill_value=0)
                             for i in dados.ITENS_LIKERT}).T.iloc[::-1]
        y = [curtos[i] for i in prop.index]
        figura = go.Figure()
        for categoria, fator, legenda in [("Neutro", -0.5, False), ("Discordo", -1, True),
                                          ("Discordo totalmente", -1, True), ("Neutro", 0.5, True),
                                          ("Concordo", 1, True), ("Concordo totalmente", 1, True)]:
            figura.add_bar(y=y, x=prop[categoria] * fator, name=categoria, orientation="h", showlegend=legenda,
                           marker_color=tema.LIKERT[dados.LIKERT.index(categoria)],
                           customdata=[ui.pct(v) for v in prop[categoria]],
                           hovertemplate=f"{categoria}: %{{customdata}}<extra></extra>")
        figura.update_layout(barmode="relative", height=340, legend={"y": -0.12, "traceorder": "normal"},
                             xaxis={"range": [-1, 1], "tickvals": [-1, -0.5, 0, 0.5, 1],
                                    "ticktext": ["100%", "50%", "0", "50%", "100%"],
                                    "zeroline": True, "zerolinecolor": tema.TEXTO_SUAVE})
        st.plotly_chart(figura, width="stretch", config={"displayModeBar": False})

c = st.columns(3, gap="large")
with c[0]:
    with st.container(border=True):
        st.markdown("**Área de atuação**")
        st.plotly_chart(barras_h(proporcao("P1_grupo", dados.AREAS + [dados.OUTRA])), width="stretch",
                        config={"displayModeBar": False})
with c[1]:
    with st.container(border=True):
        st.markdown("**Tempo de experiência**")
        st.plotly_chart(barras_h(proporcao("P2", dados.EXPERIENCIA)), width="stretch",
                        config={"displayModeBar": False})
with c[2]:
    with st.container(border=True):
        st.markdown("**Porte da empresa**")
        st.plotly_chart(barras_h(proporcao("P3", dados.PORTE + ["Não sei"])), width="stretch",
                        config={"displayModeBar": False})

with st.container(border=True):
    st.markdown("**Respostas por dia**")
    por_dia = (respostas.assign(Situação=respostas["motivo_descarte"].isna().map({True: "Válida", False: "Descartada"}),
                                Dia=respostas["timestamp"].dt.date)
               .groupby(["Dia", "Situação"]).size().reset_index(name="Respostas"))
    st.plotly_chart(px.bar(por_dia, x="Dia", y="Respostas", color="Situação", height=220,
                           color_discrete_map={"Válida": tema.PRIMARIA, "Descartada": tema.NEUTRA})
                    .update_layout(xaxis_title=None, legend={"y": 1.15, "x": 1, "xanchor": "right"}),
                    width="stretch", config={"displayModeBar": False})
    st.caption("Mostra todas as respostas recebidas, independente do filtro.")
