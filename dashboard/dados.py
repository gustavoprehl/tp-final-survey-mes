"""Leitura, codificação e limpeza das respostas do formulário.

Os cabeçalhos são os textos do formulário oficial publicado em 12/11/2026, que é o
que a planilha do Google Forms usa ao exportar o CSV. Os códigos (TC1, P2, UT1…)
seguem questionario/matriz_rastreabilidade.md, e as regras de descarte seguem a
seção 5 do protocolo.
"""
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
PASTA_BRUTOS = RAIZ / "dados" / "brutos"
PASTA_SINTETICOS = RAIZ / "dados" / "sinteticos"
ARQUIVO_FORA_POPULACAO = RAIZ / "dados" / "descartes_fora_populacao.csv"

TIMESTAMP = "Carimbo de data/hora"
GRADE_UT = "Sobre a utilidade das métricas no seu trabalho"
GRADE_MM = "Sobre a forma como o seu time mede as entregas"

# código -> cabeçalho exato da planilha (grades: "título [linha]")
COLUNAS = {
    "TC1": "Você leu o termo acima e concorda em participar da pesquisa?",
    "F1": "No seu trabalho atual, você cria ou mantém produtos de dados ou automação?",
    "P1": "Qual é a sua área de atuação principal?",
    "P2": "Há quanto tempo você trabalha com dados ou automação?",
    "P3": "Qual é o porte da empresa em que você trabalha?",
    "P4": "Qual é o setor da empresa?",
    "P5": "Quantas pessoas fazem parte do seu time direto (incluindo você)?",
    "P6": "Quais ferramentas você usa com frequência no trabalho?",
    "M1": "Quais indicadores o seu time acompanha regularmente para saber se as entregas "
          "(dashboards, relatórios, bases, automações) estão funcionando bem?",
    "M2": "O seu time mede a qualidade dos dados de forma estruturada?",
    "M3": "Nos últimos 3 meses, com que frequência você precisou refazer ou corrigir uma entrega "
          "por causa de problemas nos dados?",
    "M4": "Nos últimos 30 dias, quantas vezes uma entrega sob sua responsabilidade falhou ou "
          "exibiu dados incorretos?",
    "UT1": f"{GRADE_UT} [As métricas que acompanhamos ajudam a decidir o que melhorar nas entregas.]",
    "UT2": f"{GRADE_UT} [As métricas refletem bem o valor que as minhas entregas geram para a empresa.]",
    "UT3": f"{GRADE_UT} [Decisões sobre o meu trabalho são tomadas com base nessas métricas.]",
    "ATT": f'{GRADE_UT} [Para mostrar que você está lendo com atenção, marque "Discordo totalmente" nesta linha.]',
    "UT4": f"{GRADE_UT} [Acompanhar métricas toma tempo sem trazer benefício real.]",
    "MM1": f"{GRADE_MM} [O meu time define metas ou limites aceitáveis para as métricas que acompanha.]",
    "MM2": f"{GRADE_MM} [As métricas são revisadas periodicamente pelo time ou pela gestão.]",
    "MM3": f"{GRADE_MM} [Os dados das métricas são coletados automaticamente, sem preenchimento manual.]",
    "MM4": f"{GRADE_MM} [No meu time, cada pessoa mede as entregas do seu jeito, sem um padrão.]",
    "A1": "Que métrica você gostaria de acompanhar nas suas entregas, mas hoje não consegue? Por quê?",
    "A2": "Algum comentário sobre o tema ou sobre esta pesquisa?",
}

# Escalas e opções, na ordem do formulário
LIKERT = ["Discordo totalmente", "Discordo", "Neutro", "Concordo", "Concordo totalmente"]
AREAS = [
    "Análise de dados / BI",
    "CRM / marketing analytics",
    "Engenharia de dados",
    "Ciência de dados",
    "Desenvolvimento de sistemas / automação de processos",
]
EXPERIENCIA = ["Menos de 1 ano", "1 a menos de 3 anos", "3 a menos de 5 anos",
               "5 a menos de 10 anos", "10 anos ou mais"]
PORTE = ["Até 49 funcionários", "50 a 249 funcionários", "250 a 999 funcionários",
         "1.000 funcionários ou mais"]  # "Não sei" vira ausente
SETORES = [
    "Indústria (inclui automotivo)", "Varejo / e-commerce", "Financeiro / seguros",
    "Tecnologia / software", "Consultoria / serviços", "Saúde", "Educação", "Setor público",
]
FERRAMENTAS = [
    "Excel / Google Sheets", "Power BI", "Tableau", "Looker Studio", "Dataiku",
    "SQL (qualquer banco)", "Python ou R", "Sydle", "Salesforce / Marketing Cloud",
    "Power Automate / RPA",
]
METRICAS = [
    "Uso ou adoção (acessos, usuários ativos, consultas)",
    "Qualidade dos dados (completude, erros, duplicidade)",
    "Atualização no prazo / latência dos dados",
    "Falhas ou incidentes em pipelines e automações",
    "Retrabalho ou correções solicitadas",
    "Tempo de entrega das demandas",
    "Tempo ou custo economizado pela automação",
    "Impacto no negócio (conversão, receita, retorno de campanha)",
    "Satisfação de quem usa ou solicita a entrega",
    "Nenhuma métrica é acompanhada com regularidade",
]
QUALIDADE = ["Sim, de forma automatizada", "Sim, de forma manual", "Não", "Não sei"]
RETRABALHO = ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]

ITENS_UT = ["UT1", "UT2", "UT3", "UT4"]
ITENS_MM = ["MM1", "MM2", "MM3", "MM4"]
REVERSOS = {"UT4", "MM4"}
ITENS_LIKERT = ITENS_UT + ITENS_MM

# Motivos de descarte, na ordem de aplicação (seção 5 do protocolo)
SEM_CONSENTIMENTO = "1. Sem consentimento"
FORA_POPULACAO = "2. Fora da população"
FALHA_ATENCAO = "3. Falha na pergunta de atenção"
DUPLICADA = "4. Resposta duplicada"
MOTIVOS = [SEM_CONSENTIMENTO, FORA_POPULACAO, FALHA_ATENCAO, DUPLICADA]


def _normalizar(texto):
    return " ".join(str(texto).split())


def carregar(caminho):
    """Lê o CSV exportado da planilha e troca os cabeçalhos pelos códigos da matriz."""
    bruto = pd.read_csv(caminho, dtype=str, keep_default_na=False)
    por_texto = {_normalizar(c): c for c in bruto.columns}
    renomear, faltando = {}, []
    for codigo, cabecalho in {"timestamp": TIMESTAMP, **COLUNAS}.items():
        original = por_texto.get(_normalizar(cabecalho))
        if original is None:
            faltando.append(codigo)
        else:
            renomear[original] = codigo
    if faltando:
        raise ValueError(f"Colunas não encontradas no CSV: {', '.join(faltando)}")

    df = bruto.rename(columns=renomear)[["timestamp", *COLUNAS]].replace("", np.nan)
    df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=True)
    df.insert(0, "id", [f"R{i:03d}" for i in range(1, len(df) + 1)])
    return df


def separar_multipla(serie, opcoes):
    """Transforma uma pergunta de caixas de seleção em colunas 0/1, uma por opção.

    As opções têm vírgulas no texto, então a célula não pode ser separada por ", ".
    Cada opção conhecida é procurada na célula; o que sobra é a resposta "Outro".
    """
    marcadas = pd.DataFrame(0, index=serie.index, columns=opcoes)
    outro = pd.Series(np.nan, index=serie.index, dtype=object)
    for idx, celula in serie.dropna().items():
        resto = celula
        for opcao in sorted(opcoes, key=len, reverse=True):
            if opcao in resto:
                marcadas.at[idx, opcao] = 1
                resto = resto.replace(opcao, "")
        resto = resto.strip(" ,")
        if resto:
            outro[idx] = resto
    return marcadas, outro


def codificar(df):
    """Acrescenta as versões numéricas das escalas e os escores dos construtos."""
    df = df.copy()
    df["P1_grupo"] = df["P1"].where(df["P1"].isin(AREAS) | df["P1"].isna(), "Outra")
    df["P2_num"] = df["P2"].map({t: i for i, t in enumerate(EXPERIENCIA, 1)})
    df["P3_num"] = df["P3"].map({t: i for i, t in enumerate(PORTE, 1)})
    df["M3_num"] = df["M3"].map({t: i for i, t in enumerate(RETRABALHO, 1)})
    df["M2_grupo"] = df["M2"].map({"Sim, de forma automatizada": "Mede", "Sim, de forma manual": "Mede",
                                   "Não": "Não mede"})
    df["P5_num"] = pd.to_numeric(df["P5"], errors="coerce")
    df["M4_num"] = pd.to_numeric(df["M4"], errors="coerce")

    escala = {t: i for i, t in enumerate(LIKERT, 1)}
    for item in ITENS_LIKERT:
        valor = df[item].map(escala)
        df[f"{item}_num"] = 6 - valor if item in REVERSOS else valor
    df["UT"] = df[[f"{i}_num" for i in ITENS_UT]].mean(axis=1, skipna=False)
    df["MM"] = df[[f"{i}_num" for i in ITENS_MM]].mean(axis=1, skipna=False)
    return df


def ids_fora_populacao():
    """Respostas com P1 = "Outra" julgadas fora da população por dois pesquisadores.

    Arquivo opcional dados/descartes_fora_populacao.csv com as colunas
    timestamp (como na planilha), decisao_1 e decisao_2 ("fora" ou "dentro").
    Só sai a resposta em que os dois decidiram "fora" (seção 5, regra 2).
    """
    if not ARQUIVO_FORA_POPULACAO.exists():
        return set()
    decisoes = pd.read_csv(ARQUIVO_FORA_POPULACAO, dtype=str)
    fora = decisoes[(decisoes["decisao_1"] == "fora") & (decisoes["decisao_2"] == "fora")]
    return set(pd.to_datetime(fora["timestamp"], dayfirst=True))


def aplicar_descartes(df, fora_populacao_manual=frozenset()):
    """Marca o motivo de descarte de cada resposta (vazio = válida).

    Cada resposta recebe o motivo da primeira regra que a elimina.
    """
    df = df.copy()
    motivo = pd.Series(np.nan, index=df.index, dtype=object)

    motivo[df["TC1"] != "Sim, concordo em participar"] = SEM_CONSENTIMENTO
    fora = (df["F1"] != "Sim") | df["timestamp"].isin(fora_populacao_manual)
    motivo[motivo.isna() & fora] = FORA_POPULACAO
    motivo[motivo.isna() & (df["ATT"] != "Discordo totalmente")] = FALHA_ATENCAO
    restantes = motivo.isna()
    duplicadas = df.loc[restantes, list(COLUNAS)].duplicated(keep="first")
    motivo[duplicadas[duplicadas].index] = DUPLICADA

    df["motivo_descarte"] = motivo
    return df


def processar(caminho):
    """Carrega, codifica e marca os descartes. Devolve todas as respostas."""
    return aplicar_descartes(codificar(carregar(caminho)), ids_fora_populacao())


def localizar_fonte():
    """Usa o CSV mais recente de dados/brutos; sem ele, os dados sintéticos."""
    brutos = sorted(PASTA_BRUTOS.glob("*.csv"), key=lambda p: p.stat().st_mtime)
    if brutos:
        return brutos[-1], False
    return PASTA_SINTETICOS / "respostas_sinteticas.csv", True
