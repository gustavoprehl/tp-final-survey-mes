"""Testes do módulo estatístico (seção 5 do protocolo).

Os valores de referência foram obtidos com pingouin 0.5 e scikit-posthocs 0.11
sobre os mesmos dados, para conferir as implementações próprias.
Executar na raiz do repositório: python -m pytest dashboard/tests
"""
import numpy as np
import pandas as pd
import pytest

import analises
import dados
import estatistica as est

# três grupos de 10 respostas (escala 1 a 5)
VALORES = np.array([1, 2, 2, 3, 3, 3, 4, 4, 5, 5,
                    2, 3, 3, 4, 4, 4, 5, 5, 5, 5,
                    1, 1, 2, 2, 2, 3, 3, 3, 4, 4])
GRUPOS = np.array(["A"] * 10 + ["B"] * 10 + ["C"] * 10)


def test_margem_erro_pior_caso():
    assert est.margem_erro(68) == pytest.approx(1.96 * np.sqrt(0.25 / 68))
    assert np.isnan(est.margem_erro(0))


def test_proporcao_limita_ic_entre_0_e_1():
    p, inferior, superior = est.proporcao(1, 10)
    assert p == pytest.approx(0.1)
    assert inferior == 0
    assert superior < 1


def test_holm_exemplo_manual():
    # ordenados: 0,01·3 = 0,03; 0,03·2 = 0,06; 0,04·1 = 0,04 → monotonia leva a 0,06
    assert est.holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
    assert est.holm([0.5, 0.9]).max() <= 1


def test_kruskal_wallis_e_epsilon2():
    r = est.kruskal_wallis(VALORES, GRUPOS)
    assert r["estatistica"] == pytest.approx(6.85473, abs=1e-5)   # pingouin.kruskal
    assert r["p"] == pytest.approx(0.032472, abs=1e-6)
    assert r["efeito"] == pytest.approx(r["estatistica"] / 29)
    assert (r["n"], r["k"], r["n_min"]) == (30, 3, 10)


def test_dunn_igual_scikit_posthocs():
    tabela = est.dunn(VALORES, GRUPOS).set_index(["Grupo A", "Grupo B"])
    ajustado = tabela["p ajustado (Holm)"]
    assert ajustado[("A", "B")] == pytest.approx(0.319766, abs=1e-6)  # posthoc_dunn(p_adjust="holm")
    assert ajustado[("A", "C")] == pytest.approx(0.319766, abs=1e-6)
    assert ajustado[("B", "C")] == pytest.approx(0.026711, abs=1e-6)


def test_mann_whitney_unilateral_e_rank_biserial():
    valores = [1, 1, 2, 2, 3, 3, 4, 2, 3, 3, 4, 4, 5, 5, 5]
    grupos = ["Mede"] * 7 + ["Não mede"] * 8
    r = est.mann_whitney(valores, grupos, "Mede", "Não mede", alternativa="less")
    assert r["estatistica"] == pytest.approx(9.0)                   # pingouin.mwu
    assert r["p"] == pytest.approx(0.014396, abs=1e-6)
    assert r["efeito"] == pytest.approx(-0.678571, abs=1e-6)        # RBC: negativo = "Mede" menor
    assert (r["n_a"], r["n_b"], r["n_min"]) == (7, 8, 7)


def test_mann_whitney_grupo_vazio():
    with pytest.raises(ValueError):
        est.mann_whitney([1, 2, 3], ["Mede"] * 3, "Mede", "Não mede")


def test_spearman_ignora_ausentes():
    r = est.spearman([1, 2, 3, 4, np.nan], [2, 4, 6, 8, 10])
    assert r["estatistica"] == pytest.approx(1.0)
    assert r["n"] == 4


def test_cronbach_e_ic_feldt():
    itens = pd.DataFrame({"i1": [1, 2, 3, 4, 5, 3, 4, 2, 5, 4], "i2": [2, 2, 3, 5, 4, 3, 4, 1, 5, 5],
                          "i3": [1, 3, 3, 4, 5, 2, 5, 2, 4, 4], "i4": [2, 1, 4, 4, 5, 3, 3, 2, 5, 3]})
    r = est.cronbach(itens)
    assert r["alfa"] == pytest.approx(0.931390, abs=1e-6)           # pingouin.cronbach_alpha
    assert r["ic_inf"] == pytest.approx(0.819, abs=1e-3)
    assert r["ic_sup"] == pytest.approx(0.981, abs=1e-3)
    tabela = est.alfa_sem_item(itens)
    assert list(tabela["Item"]) == ["i1", "i2", "i3", "i4"]
    assert tabela["Alfa sem o item"].notna().all()


def test_cronbach_sem_variancia_devolve_nan():
    itens = pd.DataFrame({"i1": [3, 3, 3], "i2": [3, 3, 3]})
    assert np.isnan(est.cronbach(itens)["alfa"])


@pytest.mark.parametrize("alfa, inicio", [(0.75, "Aceito"), (0.65, "Usado com limitação"), (0.5, "Abaixo")])
def test_decisao_cronbach(alfa, inicio):
    assert est.decisao_cronbach(alfa).startswith(inicio)


@pytest.mark.parametrize("valor, esperado", [(0.005, "desprezível"), (0.03, "pequeno"),
                                             (0.1, "médio"), (0.2, "grande")])
def test_magnitude_epsilon2(valor, esperado):
    assert est.magnitude(valor, est.LIMIARES_EPSILON2) == esperado


def test_magnitude_usa_valor_absoluto():
    assert est.magnitude(-0.4, est.LIMIARES_R) == "médio"


def test_agrupar_areas_junta_pequenas_em_outras():
    areas = pd.Series(["BI"] * 5 + ["CRM"] * 4 + ["Eng"] * 1)
    assert set(est.agrupar_areas(areas)) == {"BI", "Outras"}


def test_familia_principal_nos_sinteticos(validas_sinteticas):
    familia = analises.familia_principal(validas_sinteticas)
    assert list(familia) == ["QP2", "QP3", "QP4"]
    for r in familia.values():
        assert r["p"] <= r["p_ajustado"] <= 1
    assert familia["QP3"]["n"] == validas_sinteticas["M2_grupo"].notna().sum()


def test_qp2_com_duas_areas_vira_mann_whitney(validas_sinteticas):
    duas = validas_sinteticas[validas_sinteticas["P1_grupo"].isin(dados.AREAS[:2])]
    assert analises.qp2(duas)["teste"].startswith("Mann-Whitney")


def test_qp1_proporcoes_entre_0_e_1(validas_sinteticas):
    tabela, _, _ = analises.qp1(validas_sinteticas)
    assert tabela["Proporção"].between(0, 1).all()
    assert (tabela["IC inferior"] <= tabela["Proporção"]).all()


def test_conclusao_qp3_significativa_e_nao():
    r = {"teste": "Mann-Whitney U unilateral", "p": 0.01, "efeito": -0.4, "limiares": est.LIMIARES_R}
    assert analises.conclusao("QP3", r).startswith("Quem mede")
    assert analises.conclusao("QP3", r, p_ref=0.2).startswith("Não há evidência")


def test_conclusao_qp4_indica_sentido():
    r = {"teste": "Correlação de Spearman", "p": 0.001, "efeito": -0.35, "limiares": est.LIMIARES_R}
    assert "menor" in analises.conclusao("QP4", r)


def test_conclusao_qp2_cita_pares_dunn():
    r = {"teste": "Kruskal-Wallis", "p": 0.001, "efeito": 0.2, "limiares": est.LIMIARES_EPSILON2}
    assert "BI e CRM" in analises.conclusao("QP2", r, pares_dunn=[("BI", "CRM")])
    assert "difusa" in analises.conclusao("QP2", r, pares_dunn=[])
