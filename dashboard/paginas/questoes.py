import pandas as pd
import plotly.express as px
import streamlit as st

import analises
import componentes as ui
import dados
import estatistica as est

validas = st.session_state["validas"]
filtradas = st.session_state["filtradas"]
filtro_ativo = len(filtradas) < len(validas)

st.title("Questões de pesquisa")
ui.aviso_filtro(filtradas, validas)
ui.exigir_n_minimo(filtradas)

familia = analises.familia_principal(validas)

st.subheader("Família principal (amostra completa, α = 0,05, correção de Holm)")
st.dataframe(pd.DataFrame([{
    "QP": qp, "Teste": r["teste"], "Estatística": ui.num(r["estatistica"], 3), "n": r["n"],
    "p-valor": ui.p_valor(r["p"]), "p ajustado (Holm)": ui.p_valor(r["p_ajustado"]),
    "Tamanho de efeito": f"{ui.num(r['efeito'], 3)} ({est.magnitude(r['efeito'], r['limiares'])})",
    "Decisão": "Rejeita H0" if r["p_ajustado"] < est.ALFA else "Não rejeita H0",
} for qp, r in familia.items()]), hide_index=True, width="stretch")
st.caption(f"Margem de erro das proporções com n = {len(validas)}: ± {ui.num(100 * est.margem_erro(len(validas)), 1)} p.p. "
           "(pior caso, p = 0,5). Efeitos: ε² ≈ 0,01 / 0,06 / 0,14 e r, ρ ≈ 0,1 / 0,3 / 0,5 para pequeno / médio / grande.")


def exploratorio(funcao, rotulo_estatistica, rotulo_efeito):
    """Recalcula o teste no segmento filtrado, sem correção de Holm."""
    if not filtro_ativo:
        return
    with st.expander(f"Recalculado no filtro atual (exploratório, n = {len(filtradas)})"):
        try:
            r = funcao(filtradas)
            ui.cartao_teste("Segmento filtrado", r, rotulo_estatistica, rotulo_efeito, r["limiares"])
        except ValueError as erro:
            st.warning(f"Não é possível calcular o teste neste segmento: {erro}")


abas = st.tabs(["QP1 · Métricas usadas", "QP2 · Utilidade × área", "QP3 · Qualidade × retrabalho",
                "QP4 · Maturidade × experiência"])

with abas[0]:
    st.subheader("Quais métricas os profissionais de dados e automação usam de fato para avaliar suas entregas?")
    tabela, outros, conflitos = analises.qp1(filtradas)
    margem = est.margem_erro(len(filtradas))
    figura = px.bar(tabela.iloc[::-1], x="Proporção", y="Métrica", orientation="h",
                    error_x=tabela.iloc[::-1]["IC superior"] - tabela.iloc[::-1]["Proporção"],
                    error_x_minus=tabela.iloc[::-1]["Proporção"] - tabela.iloc[::-1]["IC inferior"],
                    text=tabela.iloc[::-1]["Proporção"].map(ui.pct), height=480)
    figura.update_traces(textposition="inside", insidetextanchor="start")
    figura.update_layout(xaxis={"tickformat": ".0%", "range": [0, 1]}, yaxis_title=None, margin={"t": 10})
    st.plotly_chart(figura, width="stretch")
    st.markdown(f"**Teste:** descritiva (sem hipótese). Proporção de cada métrica com IC de 95%, n = {len(filtradas)}, "
                f"margem máxima de ± {ui.num(100 * margem, 1)} p.p. Uma métrica só é dita mais usada que outra "
                "quando a diferença supera essa margem; diferenças menores são empate (seção 2).")
    lider = tabela.iloc[0]
    empatadas = tabela[lider["Proporção"] - tabela["Proporção"] <= margem]["Métrica"].tolist()
    st.info(f"**Leitura:** a métrica mais citada é *{lider['Métrica']}* ({ui.pct(lider['Proporção'])}, IC "
            f"{ui.pct(lider['IC inferior'])} a {ui.pct(lider['IC superior'])}). "
            + (f"Ela empata, dentro da margem de erro, com outras {len(empatadas) - 1} métrica(s)."
               if len(empatadas) > 1 else "Ela supera as demais além da margem de erro."))
    tabela_exibida = tabela.assign(**{c: tabela[c].map(ui.pct) for c in ["Proporção", "IC inferior", "IC superior"]})
    st.dataframe(tabela_exibida, hide_index=True, width="stretch")
    c1, c2 = st.columns(2)
    c1.caption(f"{len(outros)} resposta(s) com métrica em \"Outro\". {conflitos} resposta(s) marcaram "
               "\"Nenhuma\" junto com outras métricas; nesses casos valem as métricas marcadas.")
    a1 = filtradas["A1"].dropna()
    c2.caption(f"{len(a1)} resposta(s) na pergunta aberta A1 (métricas desejadas). Os códigos entram aqui "
               "depois da codificação pelos dois codificadores (#25).")

with abas[1]:
    st.subheader("A utilidade percebida das métricas difere entre áreas de atuação?")
    grupos = analises.grupos_qp2(filtradas)
    dados_qp2 = filtradas.assign(Área=grupos)
    figura = px.box(dados_qp2, x="UT", y="Área", points="all", orientation="h", height=380)
    figura.update_layout(xaxis={"range": [0.8, 5.2], "title": "Escore UT (1 a 5)"}, yaxis_title=None, margin={"t": 10})
    st.plotly_chart(figura, width="stretch")
    resumo = dados_qp2.groupby("Área")["UT"].agg(n="size", Mediana="median",
                                                 Q1=lambda s: s.quantile(.25), Q3=lambda s: s.quantile(.75))
    st.dataframe(resumo.round(2), width="stretch")
    st.caption("Áreas com menos de 5 respostas são agrupadas em \"Outras\". H0: a distribuição de UT é igual "
               "entre as áreas. H1: ao menos uma área difere.")
    r = familia["QP2"]
    ui.cartao_teste(f"QP2 ({r['teste']})", r, "H de Kruskal-Wallis" if r["teste"] == "Kruskal-Wallis" else "U",
                    "ε²" if r["teste"] == "Kruskal-Wallis" else "r rank-biserial", r["limiares"], r["p_ajustado"])
    if r["teste"] == "Kruskal-Wallis" and r["p_ajustado"] < est.ALFA:
        st.markdown("**Pós-teste de Dunn (bicaudal, Holm entre os pares, amostra completa)**")
        tabela_dunn = est.dunn(validas["UT"], analises.grupos_qp2(validas))
        tabela_dunn["Diferença"] = tabela_dunn["p ajustado (Holm)"] < est.ALFA
        st.dataframe(tabela_dunn.assign(z=tabela_dunn["z"].round(2), p=tabela_dunn["p"].map(ui.p_valor),
                                        **{"p ajustado (Holm)": tabela_dunn["p ajustado (Holm)"].map(ui.p_valor)}),
                     hide_index=True, width="stretch")
    exploratorio(analises.qp2, "Estatística", "Efeito")

with abas[2]:
    st.subheader("Quem mede a qualidade dos dados de forma estruturada relata menos retrabalho?")
    dados_qp3 = filtradas.dropna(subset=["M2_grupo"])
    distribuicao = (dados_qp3.groupby("M2_grupo")["M3"].value_counts(normalize=True)
                    .rename("Proporção").reset_index())
    figura = px.bar(distribuicao, x="Proporção", y="M2_grupo", color="M3", orientation="h", height=260,
                    category_orders={"M3": dados.RETRABALHO},
                    color_discrete_sequence=["#2166ac", "#67a9cf", "#c8c8c8", "#ef8a62", "#b2182b"],
                    labels={"M2_grupo": "", "M3": "Retrabalho (3 meses)"})
    figura.update_layout(xaxis_tickformat=".0%", margin={"t": 10}, legend={"orientation": "h", "y": -0.3})
    st.plotly_chart(figura, width="stretch")
    nao_sei = (filtradas["M2"] == "Não sei").sum()
    st.caption(f"\"Mede\" = Sim, automatizada ou manual; \"Não mede\" = Não. {nao_sei} resposta(s) \"Não sei\" ficam "
               "fora. H0: retrabalho igual nos dois grupos. H1 (unilateral): menor em quem mede. "
               "r negativo indica menos retrabalho no grupo \"Mede\".")
    r = familia["QP3"]
    ui.cartao_teste("QP3 (Mann-Whitney U unilateral, M3)", r, "U", "r rank-biserial", r["limiares"], r["p_ajustado"])
    st.markdown("**Análise secundária: nº de falhas nos últimos 30 dias (M4), fora da família principal**")
    secundaria = analises.qp3(validas, "M4_num")
    medianas = validas.groupby("M2_grupo")["M4_num"].median()
    st.caption(f"Mediana de falhas: Mede = {ui.num(medianas.get('Mede'), 1)}, "
               f"Não mede = {ui.num(medianas.get('Não mede'), 1)}.")
    ui.cartao_teste("M4 (secundária)", secundaria, "U", "r rank-biserial", secundaria["limiares"])
    st.caption("A QP3 é uma associação, não uma relação de causa: porte, setor e tipo de entrega podem influenciar "
               "os dois lados (seção 7).")
    exploratorio(analises.qp3, "U", "r rank-biserial")

with abas[3]:
    st.subheader("A maturidade de medição do time está associada ao tempo de experiência do profissional?")
    figura = px.box(filtradas, x="P2", y="MM", points="all", height=380,
                    category_orders={"P2": dados.EXPERIENCIA},
                    labels={"P2": "Tempo de experiência", "MM": "Escore MM (1 a 5)"})
    figura.update_layout(yaxis_range=[0.8, 5.2], margin={"t": 10})
    st.plotly_chart(figura, width="stretch")
    st.caption("H0: não há correlação entre MM e o tempo de experiência (ρ = 0). H1: ρ ≠ 0. A experiência é ordinal "
               "(1 = menos de 1 ano … 5 = 10 anos ou mais).")
    r = familia["QP4"]
    ui.cartao_teste("QP4 (Spearman)", r, "ρ de Spearman", "ρ", r["limiares"], r["p_ajustado"])
    exploratorio(analises.qp4, "ρ", "ρ")
