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


CONSTRUTOS = {"UT": dados.ITENS_UT, "MM": dados.ITENS_MM}


def regra_cronbach(validas):
    """Aplica a regra de confiabilidade da seção 5, uma única vez, na amostra completa.

    α ≥ 0,60: o escore usa os quatro itens. α < 0,60: se tirar um item leva a α ≥ 0,70,
    o escore é calculado sem ele; senão, a QP do construto é analisada item a item.
    """
    decisoes = {}
    for nome, itens in CONSTRUTOS.items():
        colunas = [f"{i}_num" for i in itens]
        alfa = est.cronbach(validas[colunas])["alfa"]
        decisao = {"alfa": alfa, "itens": itens, "removido": None, "alfa_final": alfa, "item_a_item": False}
        if alfa < 0.60:
            tabela = est.alfa_sem_item(validas[colunas])
            melhor = tabela.loc[tabela["Alfa sem o item"].idxmax()]
            if melhor["Alfa sem o item"] >= 0.70:
                removido = melhor["Item"].removesuffix("_num")
                decisao.update(itens=[i for i in itens if i != removido], removido=removido,
                               alfa_final=melhor["Alfa sem o item"])
            else:
                decisao["item_a_item"] = True
        decisoes[nome] = decisao
    return decisoes


def aplicar_escores(df, decisoes):
    """Recalcula os escores UT e MM só com os itens mantidos pela regra de confiabilidade."""
    df = df.copy()
    for nome, decisao in decisoes.items():
        df[nome] = df[[f"{i}_num" for i in decisao["itens"]]].mean(axis=1, skipna=False)
    return df


def grupos_qp2(df):
    return est.agrupar_areas(df["P1_grupo"])


def qp2(df, variavel="UT"):
    grupos = grupos_qp2(df)
    if grupos.nunique() < 2:
        raise ValueError("há só uma área no filtro, então não há grupos para comparar")
    if grupos.nunique() == 2:  # desvio previsto na seção 5
        a, b = sorted(grupos.unique())
        r = est.mann_whitney(df[variavel], grupos, a, b, alternativa="two-sided")
        return {**r, "teste": "Mann-Whitney U (só 2 grupos)", "limiares": est.LIMIARES_R}
    r = est.kruskal_wallis(df[variavel], grupos)
    return {**r, "teste": "Kruskal-Wallis", "limiares": est.LIMIARES_EPSILON2}


def qp3(df, variavel="M3_num"):
    r = est.mann_whitney(df[variavel], df["M2_grupo"], "Mede", "Não mede", alternativa="less")
    return {**r, "teste": "Mann-Whitney U unilateral", "limiares": est.LIMIARES_R}


def qp4(df, variavel="MM"):
    r = est.spearman(df[variavel], df["P2_num"])
    return {**r, "teste": "Correlação de Spearman", "limiares": est.LIMIARES_R}


def familia_principal(df, decisoes=None):
    """QP2, QP3 (M3) e QP4 na amostra completa, com Holm entre todos os testes da família.

    Se a regra de confiabilidade mandar analisar um construto item a item, a QP
    correspondente vira um teste por item ("QP4 · MM1"…), marcado como exploratório.
    """
    decisoes = decisoes or {}

    def por_construto(qp, funcao, construto):
        if not decisoes.get(construto, {}).get("item_a_item"):
            return {qp: funcao(df, construto)}
        return {f"{qp} · {item}": {**funcao(df, f"{item}_num"), "exploratoria": True}
                for item in CONSTRUTOS[construto]}

    resultados = {**por_construto("QP2", qp2, "UT"), "QP3": qp3(df), **por_construto("QP4", qp4, "MM")}
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


def _separar_codigos(serie):
    """"USUARIO;NEGOCIO" -> {"USUARIO", "NEGOCIO"}; vazio -> conjunto vazio."""
    return serie.map(lambda t: {c.strip() for c in t.split(";") if c.strip()} if isinstance(t, str) else set())


def concordancia_a1(cod, dimensao):
    """Concordância entre os dois codificadores da A1 em uma dimensão (seção 5).

    Como uma resposta pode ter mais de um código, o kappa é calculado sobre as
    decisões código a código (presente ou ausente em cada resposta). A
    concordância simples é a fração de respostas com exatamente os mesmos códigos.
    Devolve None enquanto o segundo codificador não terminou.
    """
    a = _separar_codigos(cod[f"{dimensao}_arthur"])
    b = _separar_codigos(cod[f"{dimensao}_gustavo"])
    if b.map(len).eq(0).any():
        return None
    codigos = dados.CODIGOS_A1[dimensao]
    decisoes_a = [c in s for s in a for c in codigos]
    decisoes_b = [c in s for s in b for c in codigos]
    kappa = est.kappa_cohen(decisoes_a, decisoes_b)
    return {"kappa": kappa, "interpretacao": est.interpretar_kappa(kappa),
            "concordancia": (a == b).mean(), "n": len(cod), "divergencias": cod.loc[a != b, "timestamp"]}


def frequencia_codigos_a1(cod, df, dimensao):
    """Respostas de df (válidas, com filtro) em cada código da A1.

    Usa os códigos finais (consenso); enquanto não existem, os do codificador
    principal, e o retorno indica que o resultado é provisório.
    """
    final = cod[f"{dimensao}_final"]
    provisorio = final.isna().any()
    coluna = cod[f"{dimensao}_arthur"] if provisorio else final
    codigos = _separar_codigos(coluna)[cod["timestamp"].isin(df["timestamp"]).values]
    n = len(codigos)
    linhas = [{"Código": rotulo, "Respostas": int(sum(c in s for s in codigos)),
               "Proporção": sum(c in s for s in codigos) / n if n else 0}
              for c, rotulo in dados.CODIGOS_A1[dimensao].items()]
    tabela = pd.DataFrame(linhas).sort_values("Respostas", ascending=False, ignore_index=True)
    return tabela, n, provisorio
