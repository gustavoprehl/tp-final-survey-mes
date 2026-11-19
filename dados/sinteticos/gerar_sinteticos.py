"""Gera respostas SINTÉTICAS no mesmo formato do CSV exportado da planilha do Forms.

Servem só para desenvolver e testar o dashboard antes do fim da coleta.
Nunca entram na análise: o dashboard mostra um aviso sempre que estão em uso.

Uso (na raiz do repositório):  python dados/sinteticos/gerar_sinteticos.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "dashboard"))
import dados as d  # noqa: E402

N = 80
SAIDA = Path(__file__).resolve().parent / "respostas_sinteticas.csv"
rng = np.random.default_rng(2026)


def likert(latente, reverso=False):
    valor = np.clip(np.rint(latente + rng.normal(0, 0.8)), 1, 5).astype(int)
    return d.LIKERT[(6 - valor if reverso else valor) - 1]


def multipla(opcoes, p):
    escolhidas = [o for o in opcoes if rng.random() < p]
    return ", ".join(escolhidas or [opcoes[0]])


def resposta():
    area = rng.choice(d.AREAS, p=[0.4, 0.2, 0.15, 0.1, 0.15])
    exp = rng.choice(len(d.EXPERIENCIA), p=[0.1, 0.35, 0.25, 0.2, 0.1])
    mede = rng.random() < 0.6
    # utilidade um pouco maior em CRM e maturidade crescendo com a experiência
    ut = 3.2 + (0.5 if area == d.AREAS[1] else 0) + rng.normal(0, 0.6)
    mm = 2.4 + 0.3 * exp + (0.4 if mede else 0) + rng.normal(0, 0.6)
    retrabalho = int(np.clip(np.rint(3.2 - (0.8 if mede else 0) + rng.normal(0, 0.9)), 1, 5))
    metricas = [m for m in d.METRICAS[:-1] if rng.random() < 0.35]

    return {
        d.TIMESTAMP: None,
        "TC1": "Sim, concordo em participar",
        "F1": "Sim",
        "P1": area,
        "P2": d.EXPERIENCIA[exp],
        "P3": rng.choice(d.PORTE + ["Não sei"], p=[0.15, 0.2, 0.2, 0.4, 0.05]),
        "P4": rng.choice(d.SETORES),
        "P5": str(int(rng.integers(2, 25))),
        "P6": multipla(d.FERRAMENTAS, 0.35),
        "M1": ", ".join(metricas) if metricas else d.METRICAS[-1],
        "M2": rng.choice(d.QUALIDADE[:2]) if mede else rng.choice(["Não", "Não sei"], p=[0.85, 0.15]),
        "M3": d.RETRABALHO[retrabalho - 1],
        "M4": str(int(rng.poisson(retrabalho - 0.5))),
        "UT1": likert(ut), "UT2": likert(ut), "UT3": likert(ut),
        "ATT": "Discordo totalmente",
        "UT4": likert(ut, reverso=True),
        "MM1": likert(mm), "MM2": likert(mm), "MM3": likert(mm),
        "MM4": likert(mm, reverso=True),
        "A1": rng.choice(["", "", "Tempo médio de entrega das demandas.",
                          "Uso real dos dashboards, porque não temos log de acesso."]),
        "A2": "",
    }


linhas = [resposta() for _ in range(N)]

# Casos de descarte, para exercitar todas as regras da seção 5
for i in range(3):
    linhas[i] = {"TC1": "Não concordo"}
for i in range(3, 7):
    linhas[i] = {"TC1": "Sim, concordo em participar", "F1": "Não"}
for i in range(7, 12):
    linhas[i]["ATT"] = rng.choice(["Concordo", "Neutro"])
linhas[12].update(P1="Psicóloga", P4="Saúde")
linhas.append(dict(linhas[20]))  # duplicada

inicio = pd.Timestamp("2026-11-12 20:00")
segundos = np.sort(rng.integers(0, 10 * 24 * 3600, len(linhas)))
df = pd.DataFrame(linhas).reindex(columns=[d.TIMESTAMP, *d.COLUNAS])
df[d.TIMESTAMP] = [(inicio + pd.Timedelta(seconds=int(s))).strftime("%d/%m/%Y %H:%M:%S") for s in segundos]
df = df.rename(columns=d.COLUNAS)
df.to_csv(SAIDA, index=False, encoding="utf-8")
print(f"{len(df)} respostas sintéticas em {SAIDA}")
