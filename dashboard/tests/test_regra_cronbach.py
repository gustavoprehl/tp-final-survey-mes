"""Regra de confiabilidade da seção 5 aplicada aos construtos UT e MM."""
import numpy as np
import pandas as pd

import analises
import dados


def construto(itens, ruido, rng, n=60, item_ruim=None):
    """Itens Likert 1–5 de um fator latente; item_ruim recebe só ruído."""
    latente = rng.normal(3, 1, n)
    colunas = {}
    for item in itens:
        base = rng.normal(3, 1, n) if item == item_ruim else latente + rng.normal(0, ruido, n)
        colunas[f"{item}_num"] = np.clip(np.rint(base), 1, 5)
    return pd.DataFrame(colunas)


def base(ut, mm):
    return pd.concat([ut, mm], axis=1)


def test_alfa_alto_mantem_os_quatro_itens():
    rng = np.random.default_rng(1)
    df = base(construto(dados.ITENS_UT, 0.4, rng), construto(dados.ITENS_MM, 0.4, rng))
    decisoes = analises.regra_cronbach(df)
    for nome, itens in analises.CONSTRUTOS.items():
        assert decisoes[nome]["itens"] == itens
        assert not decisoes[nome]["item_a_item"]


def test_remove_item_que_leva_alfa_acima_de_070():
    rng = np.random.default_rng(2)
    ut = construto(dados.ITENS_UT, 0.5, rng, item_ruim="UT4")
    ut["UT4_num"] = 6 - ut["UT1_num"]  # reverso "esquecido": derruba o alfa
    df = base(ut, construto(dados.ITENS_MM, 0.4, rng))
    decisao = analises.regra_cronbach(df)["UT"]
    assert decisao["alfa"] < 0.60
    assert decisao["removido"] == "UT4"
    assert decisao["alfa_final"] >= 0.70
    escores = analises.aplicar_escores(df, {"UT": decisao})
    assert np.allclose(escores["UT"], df[["UT1_num", "UT2_num", "UT3_num"]].mean(axis=1))


def test_sem_remocao_suficiente_vira_item_a_item():
    rng = np.random.default_rng(3)
    mm = pd.DataFrame({f"{i}_num": rng.integers(1, 6, 60).astype(float) for i in dados.ITENS_MM})
    df = base(construto(dados.ITENS_UT, 0.4, rng), mm)
    decisao = analises.regra_cronbach(df)["MM"]
    assert decisao["item_a_item"]
    assert decisao["removido"] is None


def test_familia_item_a_item_tem_um_teste_por_item_e_holm_conjunto(validas_sinteticas):
    decisoes = analises.regra_cronbach(validas_sinteticas)
    decisoes["MM"] = {**decisoes["MM"], "item_a_item": True}
    familia = analises.familia_principal(validas_sinteticas, decisoes)
    assert list(familia) == ["QP2", "QP3", *[f"QP4 · {i}" for i in dados.ITENS_MM]]
    assert all(familia[f"QP4 · {i}"]["exploratoria"] for i in dados.ITENS_MM)
    p_brutos = sorted(r["p"] for r in familia.values())
    assert min(r["p_ajustado"] for r in familia.values()) == min(1, len(familia) * p_brutos[0])
