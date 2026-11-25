"""Testes, tamanhos de efeito e confiabilidade definidos na seção 5 do protocolo."""
from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats

ALFA = 0.05
Z95 = 1.96
N_MIN_GRUPO = 5  # áreas com menos respostas são agrupadas em "Outras" (QP2)


def margem_erro(n, p=0.5):
    """Margem de erro de uma proporção com 95% de confiança (seção 2)."""
    return Z95 * np.sqrt(p * (1 - p) / n) if n else np.nan


def proporcao(sucessos, n):
    """Proporção com IC 95% pela mesma fórmula da margem de erro."""
    p = sucessos / n
    e = margem_erro(n, p)
    return p, max(p - e, 0), min(p + e, 1)


def holm(p_valores):
    """P-valores ajustados por Holm, na ordem original."""
    p = np.asarray(p_valores, dtype=float)
    ordem = np.argsort(p)
    m = len(p)
    ajustados = np.empty(m)
    acumulado = 0.0
    for posicao, i in enumerate(ordem):
        acumulado = max(acumulado, min(1.0, (m - posicao) * p[i]))
        ajustados[i] = acumulado
    return ajustados


def magnitude(valor, limiares):
    """Classifica |valor| pelos limiares de Cohen (pequeno, médio, grande)."""
    v = abs(valor)
    if np.isnan(v):
        return "—"
    if v < limiares[0]:
        return "desprezível"
    if v < limiares[1]:
        return "pequeno"
    if v < limiares[2]:
        return "médio"
    return "grande"


LIMIARES_EPSILON2 = (0.01, 0.06, 0.14)
LIMIARES_R = (0.1, 0.3, 0.5)


def agrupar_areas(areas):
    """Junta em "Outras" as áreas com menos de N_MIN_GRUPO respostas."""
    contagem = areas.value_counts()
    pequenas = contagem[contagem < N_MIN_GRUPO].index
    return areas.where(~areas.isin(pequenas), "Outras")


def kruskal_wallis(valores, grupos):
    """Kruskal-Wallis com ε² = H / (n − 1)."""
    dados = pd.DataFrame({"v": valores, "g": grupos}).dropna()
    amostras = [g["v"].to_numpy() for _, g in dados.groupby("g")]
    h, p = stats.kruskal(*amostras)
    n = len(dados)
    return {"estatistica": h, "p": p, "efeito": h / (n - 1), "n": n, "k": len(amostras),
            "n_min": min(len(a) for a in amostras)}


def dunn(valores, grupos):
    """Pós-teste de Dunn (bicaudal, com correção de empates) e Holm entre os pares."""
    dados = pd.DataFrame({"v": valores, "g": grupos}).dropna()
    dados["posto"] = stats.rankdata(dados["v"])
    n = len(dados)
    empates = dados["v"].value_counts()
    correcao = (empates ** 3 - empates).sum() / (12 * (n - 1))
    resumo = dados.groupby("g")["posto"].agg(["mean", "size"])
    linhas = []
    for a, b in combinations(resumo.index, 2):
        erro = np.sqrt((n * (n + 1) / 12 - correcao) * (1 / resumo.at[a, "size"] + 1 / resumo.at[b, "size"]))
        z = (resumo.at[a, "mean"] - resumo.at[b, "mean"]) / erro
        linhas.append({"Grupo A": a, "Grupo B": b, "z": z, "p": 2 * stats.norm.sf(abs(z))})
    tabela = pd.DataFrame(linhas)
    if not tabela.empty:
        tabela["p ajustado (Holm)"] = holm(tabela["p"])
    return tabela


def mann_whitney(valores, grupos, grupo_a, grupo_b, alternativa="less"):
    """Mann-Whitney U de A contra B, com r rank-biserial = 2·U_A / (n_A·n_B) − 1.

    Com alternativa "less", H1 é: valores de A tendem a ser menores que os de B.
    r negativo indica A com valores menores.
    """
    a = pd.Series(valores)[pd.Series(grupos) == grupo_a].dropna().to_numpy()
    b = pd.Series(valores)[pd.Series(grupos) == grupo_b].dropna().to_numpy()
    if len(a) == 0 or len(b) == 0:
        raise ValueError(f"o grupo \"{grupo_a if len(a) == 0 else grupo_b}\" não tem respostas")
    u, p = stats.mannwhitneyu(a, b, alternative=alternativa)
    return {"estatistica": u, "p": p, "efeito": 2 * u / (len(a) * len(b)) - 1,
            "n": len(a) + len(b), "n_a": len(a), "n_b": len(b), "n_min": min(len(a), len(b))}


def spearman(x, y):
    """Correlação de Spearman; o próprio ρ é o tamanho de efeito."""
    dados = pd.DataFrame({"x": x, "y": y}).dropna()
    rho, p = stats.spearmanr(dados["x"], dados["y"])
    return {"estatistica": rho, "p": p, "efeito": rho, "n": len(dados), "n_min": len(dados)}


LIMIARES_KAPPA = [(0.20, "fraca"), (0.40, "razoável"), (0.60, "moderada"), (0.80, "substancial")]
KAPPA_MINIMO = 0.60  # seção 5


def kappa_cohen(a, b):
    """Kappa de Cohen entre dois codificadores (mesmos itens, na mesma ordem)."""
    a, b = np.asarray(a), np.asarray(b)
    categorias = np.union1d(a, b)
    observada = np.mean(a == b)
    esperada = sum(np.mean(a == c) * np.mean(b == c) for c in categorias)
    if esperada == 1:  # os dois usaram uma única categoria: kappa indefinido
        return np.nan
    return (observada - esperada) / (1 - esperada)


def interpretar_kappa(kappa):
    """Faixas de Landis e Koch (1977)."""
    if np.isnan(kappa):
        return "—"
    for limite, rotulo in LIMIARES_KAPPA:
        if kappa < limite:
            return rotulo
    return "quase perfeita"


def cronbach(itens):
    """Alfa de Cronbach com IC 95% de Feldt."""
    itens = itens.dropna()
    n, k = itens.shape
    variancia_total = itens.sum(axis=1).var(ddof=1)
    if n < 2 or not variancia_total > 0:  # todos responderam igual: alfa indefinido
        return {"alfa": np.nan, "ic_inf": np.nan, "ic_sup": np.nan, "n": n, "k": k}
    alfa = k / (k - 1) * (1 - itens.var(ddof=1).sum() / variancia_total)
    gl1, gl2 = n - 1, (n - 1) * (k - 1)
    inferior = 1 - (1 - alfa) * stats.f.ppf(0.975, gl1, gl2)
    superior = 1 - (1 - alfa) * stats.f.ppf(0.025, gl1, gl2)
    return {"alfa": alfa, "ic_inf": inferior, "ic_sup": superior, "n": n, "k": k}


def alfa_sem_item(itens):
    """Alfa recalculado sem cada item e correlação item-total corrigida."""
    itens = itens.dropna()
    linhas = []
    for coluna in itens.columns:
        resto = itens.drop(columns=coluna)
        linhas.append({
            "Item": coluna,
            "Correlação item-total": itens[coluna].corr(resto.sum(axis=1)),
            "Alfa sem o item": cronbach(resto)["alfa"] if resto.shape[1] > 1 else np.nan,
        })
    return pd.DataFrame(linhas)


def decisao_cronbach(alfa):
    """Regra da seção 5 do protocolo."""
    if alfa >= 0.70:
        return "Aceito (α ≥ 0,70)"
    if alfa >= 0.60:
        return "Usado com limitação declarada (0,60 ≤ α < 0,70)"
    return "Abaixo de 0,60: aplicar a regra de remoção de item ou analisar item a item"
