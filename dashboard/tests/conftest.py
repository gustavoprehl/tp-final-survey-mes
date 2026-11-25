import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402

import dados  # noqa: E402


@pytest.fixture(scope="session")
def validas_sinteticas():
    df = dados.processar(dados.PASTA_SINTETICOS / "respostas_sinteticas.csv")
    return df[df["motivo_descarte"].isna()]
