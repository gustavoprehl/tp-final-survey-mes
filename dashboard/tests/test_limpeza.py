"""Testes do pipeline de limpeza: regras de descarte da seção 5, codificação e sinalizações.

Cada caso parte de uma resposta válida dos dados sintéticos e altera só o que a regra testa.
"""
import numpy as np
import pandas as pd
import pytest

import dados

SINTETICOS = dados.PASTA_SINTETICOS / "respostas_sinteticas.csv"


@pytest.fixture(scope="module")
def base():
    """Uma resposta válida, já com os códigos da matriz."""
    df = dados.aplicar_descartes(dados.codificar(dados.carregar(SINTETICOS)))
    return df[df["motivo_descarte"].isna()].iloc[[0]].drop(columns="motivo_descarte")


def montar(base, *alteracoes):
    """Uma linha por alteração, com carimbos de data/hora distintos."""
    linhas = []
    for i, mudar in enumerate(alteracoes):
        linha = base.copy()
        for coluna, valor in mudar.items():
            linha[coluna] = valor
        linha["timestamp"] = pd.Timestamp("2026-11-13 10:00") + pd.Timedelta(minutes=i)
        linhas.append(linha)
    return pd.concat(linhas, ignore_index=True)


def motivos(df, fora=frozenset()):
    return dados.aplicar_descartes(df, fora)["motivo_descarte"].tolist()


def test_resposta_valida_nao_e_descartada(base):
    assert motivos(montar(base, {})) == [np.nan]


def test_regra_1_sem_consentimento(base):
    assert motivos(montar(base, {"TC1": "Não concordo"})) == [dados.SEM_CONSENTIMENTO]


def test_regra_2_fora_da_populacao_por_f1(base):
    assert motivos(montar(base, {"F1": "Não"})) == [dados.FORA_POPULACAO]


def test_regra_2_area_outra_so_sai_com_decisao_dos_dois(base):
    df = montar(base, {"P1": "Psicóloga"}, {"P1": "Psicóloga"})
    # o arquivo de decisões só lista a primeira (os dois marcaram "fora")
    assert motivos(df, {df.loc[0, "timestamp"]}) == [dados.FORA_POPULACAO, np.nan]


def test_regra_3_falha_na_atencao(base):
    assert motivos(montar(base, {"ATT": "Concordo"})) == [dados.FALHA_ATENCAO]


def test_regra_4_duplicada_mantem_a_primeira(base):
    assert motivos(montar(base, {}, {})) == [np.nan, dados.DUPLICADA]


def test_regra_4_compara_so_com_respostas_ainda_validas(base):
    # a cópia de uma resposta já descartada não vira "duplicada": é avaliada pelas próprias regras
    df = montar(base, {"ATT": "Neutro"}, {})
    assert motivos(df) == [dados.FALHA_ATENCAO, np.nan]


def test_regra_5_incompleta_cai_na_1_ou_na_2(base):
    # quem não aceita o termo ou não trabalha com dados vai direto ao envio (respostas vazias)
    vazia = {c: np.nan for c in dados.COLUNAS if c not in ("TC1", "F1")}
    df = montar(base, {**vazia, "TC1": "Não concordo", "F1": np.nan}, {**vazia, "F1": "Não"})
    assert motivos(df) == [dados.SEM_CONSENTIMENTO, dados.FORA_POPULACAO]


def test_primeira_regra_que_elimina_define_o_motivo(base):
    df = montar(base, {"TC1": "Não concordo", "F1": "Não", "ATT": "Neutro"}, {"F1": "Não", "ATT": "Neutro"})
    assert motivos(df) == [dados.SEM_CONSENTIMENTO, dados.FORA_POPULACAO]


def test_sinteticos_tem_todos_os_motivos():
    contagem = dados.processar(SINTETICOS)["motivo_descarte"].value_counts()
    for motivo in dados.MOTIVOS:
        assert contagem.get(motivo, 0) > 0, motivo


def test_likert_e_itens_reversos(base):
    df = dados.codificar(montar(base, {
        "UT1": "Discordo totalmente", "UT2": "Neutro", "UT3": "Concordo totalmente",
        "UT4": "Concordo totalmente", "MM4": "Discordo",
    }))
    assert df.loc[0, ["UT1_num", "UT2_num", "UT3_num"]].tolist() == [1, 3, 5]
    assert df.loc[0, "UT4_num"] == 1  # reverso: 6 - 5
    assert df.loc[0, "MM4_num"] == 4  # reverso: 6 - 2
    assert df.loc[0, "UT"] == pytest.approx((1 + 3 + 5 + 1) / 4)


def test_escalas_ordinais(base):
    df = dados.codificar(montar(base, {"P2": "10 anos ou mais", "P3": "Não sei", "M3": "Às vezes"}))
    assert df.loc[0, "P2_num"] == 5
    assert np.isnan(df.loc[0, "P3_num"])  # "Não sei" vira ausente
    assert df.loc[0, "M3_num"] == 3


def test_grade_igual_e_sinalizada_mas_nao_descartada(base):
    tudo_concordo = {i: "Concordo" for i in dados.ITENS_MM}
    tudo_discordo = {i: "Discordo totalmente" for i in dados.GRADES["UT"]}
    df = dados.marcar_grades_iguais(dados.aplicar_descartes(montar(base, tudo_concordo, tudo_discordo,
                                                                    {**tudo_concordo, **tudo_discordo})))
    assert df["grade_igual"].tolist()[:3] == ["MM", "UT", "UT e MM"]
    assert df["motivo_descarte"].isna().all()


def test_carregar_mantem_so_colunas_da_matriz():
    df = dados.carregar(SINTETICOS)
    assert list(df.columns) == ["id", "timestamp", *dados.COLUNAS]


def test_carregar_acusa_coluna_faltando(tmp_path):
    bruto = pd.read_csv(SINTETICOS, dtype=str).drop(columns=dados.COLUNAS["ATT"])
    bruto.to_csv(tmp_path / "faltando.csv", index=False)
    with pytest.raises(ValueError, match="ATT"):
        dados.carregar(tmp_path / "faltando.csv")
