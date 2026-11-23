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


def _fmt(valor, casas=2):
    return f"{valor:.{casas}f}".replace(".", ",")


def conclusao(qp, r, p_ref=None, pares_dunn=None):
    """Conclusão em linguagem simples para QP2, QP3 e QP4.

    p_ref é o p-valor usado na decisão (o ajustado por Holm na família principal;
    o bruto no recálculo exploratório). pares_dunn lista os pares de áreas com
    diferença após o Dunn.
    """
    p_ref = r["p"] if p_ref is None else p_ref
    significativo = p_ref < est.ALFA
    forca = est.magnitude(r["efeito"], r["limiares"])
    simbolo = "ε²" if r["teste"] == "Kruskal-Wallis" else "ρ" if qp == "QP4" else "r"
    efeito = f"efeito {forca}, {simbolo} = {_fmt(r['efeito'])}"
    ressalva = " Com efeito desprezível, a diferença tem pouca relevância prática." if forca == "desprezível" else ""

    if qp == "QP2":
        if not significativo:
            return (f"Não há evidência de que a utilidade percebida das métricas mude entre as áreas ({efeito}). "
                    "Isso não prova que as áreas sejam iguais, só que a amostra não mostrou diferença.")
        texto = f"A utilidade percebida das métricas difere entre as áreas de atuação ({efeito}).{ressalva}"
        if pares_dunn:
            texto += " Pelo pós-teste de Dunn, a diferença aparece entre " + "; ".join(
                f"{a} e {b}" for a, b in pares_dunn) + "."
        elif pares_dunn is not None:
            texto += " Nenhum par de áreas se separa após a correção de Holm no Dunn: a diferença é difusa."
        return texto

    if qp == "QP3":
        if significativo and r["efeito"] < 0:
            return (f"Quem mede a qualidade dos dados de forma estruturada relata menos retrabalho ({efeito}).{ressalva} "
                    "É uma associação, não prova que medir reduza o retrabalho.")
        return (f"Não há evidência de que quem mede a qualidade dos dados relate menos retrabalho ({efeito}). "
                "Isso não prova que os grupos sejam iguais.")

    if qp == "QP4":
        if not significativo:
            return (f"Não há evidência de associação entre a maturidade de medição do time e a experiência do "
                    f"profissional ({efeito}). Isso não prova que a associação seja nula.")
        sentido = "maior" if r["efeito"] > 0 else "menor"
        return (f"Quanto mais experiente o profissional, {sentido} tende a ser a maturidade de medição do time "
                f"({efeito}).{ressalva} É uma associação, não uma relação de causa.")

    raise ValueError(f"QP desconhecida: {qp}")
