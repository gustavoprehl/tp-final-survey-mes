"""Aplica os testes da seção 5 às colunas do survey."""
import pandas as pd

import dados
import estatistica as est


def qp1(df):
    """Proporção de cada métrica de M1, com IC 95%, da mais para a menos citada."""
    marcadas, outro = dados.separar_multipla(df["M1"], dados.METRICAS)
    # "Nenhuma" marcada junto com outras métricas: valem as métricas marcadas
    conflito = (marcadas[dados.METRICAS[-1]] == 1) & (marcadas[dados.METRICAS[:-1]].sum(axis=1) > 0)
    marcadas.loc[conflito, dados.METRICAS[-1]] = 0
    n = len(df)
    linhas = []
    for metrica in dados.METRICAS:
        p, inf, sup = est.proporcao(marcadas[metrica].sum(), n)
        linhas.append({"Métrica": metrica, "Respondentes": int(marcadas[metrica].sum()),
                       "Proporção": p, "IC inferior": inf, "IC superior": sup})
    tabela = pd.DataFrame(linhas).sort_values("Proporção", ascending=False, ignore_index=True)
    return tabela, outro.dropna(), int(conflito.sum())


def grupos_qp2(df):
    return est.agrupar_areas(df["P1_grupo"])


def qp2(df):
    grupos = grupos_qp2(df)
    if grupos.nunique() < 2:
        raise ValueError("há só uma área no filtro, então não há grupos para comparar")
    if grupos.nunique() == 2:  # desvio previsto na seção 5
        a, b = sorted(grupos.unique())
        r = est.mann_whitney(df["UT"], grupos, a, b, alternativa="two-sided")
        return {**r, "teste": "Mann-Whitney U (só 2 grupos)", "limiares": est.LIMIARES_R}
    r = est.kruskal_wallis(df["UT"], grupos)
    return {**r, "teste": "Kruskal-Wallis", "limiares": est.LIMIARES_EPSILON2}


def qp3(df, variavel="M3_num"):
    r = est.mann_whitney(df[variavel], df["M2_grupo"], "Mede", "Não mede", alternativa="less")
    return {**r, "teste": "Mann-Whitney U unilateral", "limiares": est.LIMIARES_R}


def qp4(df):
    r = est.spearman(df["MM"], df["P2_num"])
    return {**r, "teste": "Correlação de Spearman", "limiares": est.LIMIARES_R}


def familia_principal(df):
    """QP2, QP3 (M3) e QP4 na amostra completa, com Holm entre os três testes."""
    resultados = {"QP2": qp2(df), "QP3": qp3(df), "QP4": qp4(df)}
    ajustados = est.holm([r["p"] for r in resultados.values()])
    for r, p_aj in zip(resultados.values(), ajustados):
        r["p_ajustado"] = p_aj
    return resultados
