"""Testes da codificação das respostas abertas (A1) e do kappa de Cohen."""
import numpy as np
import pandas as pd
import pytest

import analises
import dados
import estatistica as est


def test_kappa_exemplo_classico():
    # 50 itens: 20 sim/sim, 5 sim/não, 10 não/sim, 15 não/não -> po = 0,70, pe = 0,50, κ = 0,40
    a = ["sim"] * 25 + ["não"] * 25
    b = ["sim"] * 20 + ["não"] * 5 + ["sim"] * 10 + ["não"] * 15
    assert est.kappa_cohen(a, b) == pytest.approx(0.4)


def test_kappa_concordancia_perfeita_e_indefinido():
    assert est.kappa_cohen(["A", "B", "C"], ["A", "B", "C"]) == pytest.approx(1)
    assert np.isnan(est.kappa_cohen(["A", "A"], ["A", "A"]))


def test_interpretacao_kappa():
    assert est.interpretar_kappa(0.55) == "moderada"
    assert est.interpretar_kappa(0.85) == "quase perfeita"


def _planilha(gustavo):
    return pd.DataFrame({
        "timestamp": pd.to_datetime(["2026-11-13 10:00", "2026-11-13 11:00", "2026-11-13 12:00"]),
        "metrica_arthur": ["NEGOCIO", "USUARIO;NEGOCIO", "SEM_CONTEUDO"],
        "metrica_gustavo": gustavo,
        "metrica_final": [np.nan] * 3,
    })


def test_concordancia_espera_o_segundo_codificador():
    assert analises.concordancia_a1(_planilha([np.nan] * 3), "metrica") is None


def test_concordancia_codigo_a_codigo():
    r = analises.concordancia_a1(_planilha(["NEGOCIO", "USUARIO", "SEM_CONTEUDO"]), "metrica")
    assert r["concordancia"] == pytest.approx(2 / 3)
    assert len(r["divergencias"]) == 1
    # uma decisão por código em cada resposta; a única divergência é NEGOCIO na 2ª resposta
    codigos = list(dados.CODIGOS_A1["metrica"])
    arthur = [{"NEGOCIO"}, {"USUARIO", "NEGOCIO"}, {"SEM_CONTEUDO"}]
    gustavo = [{"NEGOCIO"}, {"USUARIO"}, {"SEM_CONTEUDO"}]
    a = [c in s for s in arthur for c in codigos]
    b = [c in s for s in gustavo for c in codigos]
    assert sum(x != y for x, y in zip(a, b)) == 1
    assert r["kappa"] == pytest.approx(est.kappa_cohen(a, b))


def test_frequencia_so_conta_respostas_do_recorte():
    cod = _planilha([np.nan] * 3)
    validas = pd.DataFrame({"timestamp": cod["timestamp"].iloc[:2]})
    tabela, n, provisorio = analises.frequencia_codigos_a1(cod, validas, "metrica")
    assert n == 2 and provisorio
    contagem = dict(zip(tabela["Código"], tabela["Respostas"]))
    assert contagem[dados.CODIGOS_A1["metrica"]["NEGOCIO"]] == 2
    assert contagem[dados.CODIGOS_A1["metrica"]["SEM_CONTEUDO"]] == 0


def test_planilha_real_cobre_todas_as_respostas_a1():
    cod = dados.carregar_codificacao()
    if cod is None:
        pytest.skip("planilha de codificação ainda não existe")
    respostas = dados.processar(dados.localizar_fonte()[0])
    com_a1 = respostas.loc[respostas["A1"].notna(), "timestamp"]
    assert set(cod["timestamp"]) == set(com_a1)
    for dimensao, codigos in dados.CODIGOS_A1.items():
        for coluna in ["arthur", "gustavo", "final"]:
            usados = set().union(*analises._separar_codigos(cod[f"{dimensao}_{coluna}"]))
            assert usados <= set(codigos), f"código fora do livro em {dimensao}_{coluna}"
