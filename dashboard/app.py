"""Dashboard do survey "Uso de métricas em produtos de dados e automação".

Executar na raiz do repositório:  streamlit run dashboard/app.py
"""
from pathlib import Path

import streamlit as st

import analises
import dados

st.set_page_config(page_title="Survey: métricas em produtos de dados", page_icon="📊", layout="wide")


@st.cache_data
def carregar(caminho, modificado_em, versao_pipeline, versao_decisoes):
    # os três últimos argumentos só renovam o cache quando o CSV, o pipeline (dados.py)
    # ou as decisões da regra 2 (descartes_fora_populacao.csv) mudam
    return dados.processar(caminho)


def modificado_em(arquivo):
    return Path(arquivo).stat().st_mtime if Path(arquivo).exists() else None


fonte, sintetico = dados.localizar_fonte()
respostas = carregar(fonte, modificado_em(fonte), modificado_em(dados.__file__),
                     modificado_em(dados.ARQUIVO_FORA_POPULACAO))
validas = respostas[respostas["motivo_descarte"].isna()]
# A regra de confiabilidade (seção 5) é decidida na amostra completa e vale para todas as páginas
construtos = analises.regra_cronbach(validas)
validas = analises.aplicar_escores(validas, construtos)

if sintetico:
    st.warning("**DADOS SINTÉTICOS.** Nenhum CSV em `dados/brutos/`: o dashboard está usando respostas "
               "geradas para desenvolvimento, que não fazem parte da análise.", icon="⚠️")

# Filtros por segmento: valem para todas as páginas
with st.sidebar:
    st.header("Filtros")
    filtros = {
        "P1_grupo": ("Área de atuação", dados.AREAS + [dados.OUTRA]),
        "P2": ("Tempo de experiência", dados.EXPERIENCIA),
        "P3": ("Porte da empresa", dados.PORTE + ["Não sei"]),
        "P4": ("Setor", sorted(validas["P4"].dropna().unique())),
    }
    filtradas = validas
    for coluna, (rotulo, opcoes) in filtros.items():
        escolha = st.multiselect(rotulo, opcoes, placeholder="Todos")
        if escolha:
            filtradas = filtradas[filtradas[coluna].isin(escolha)]
    st.caption(f"{len(filtradas)} de {len(validas)} respostas válidas no filtro")
    st.caption(f"Fonte: `{fonte.relative_to(dados.RAIZ).as_posix()}`")

st.session_state["respostas"] = respostas
st.session_state["validas"] = validas
st.session_state["construtos"] = construtos
st.session_state["filtradas"] = filtradas

pagina = st.navigation([
    st.Page("paginas/perfil.py", title="Perfil da amostra", icon="👥", default=True),
    st.Page("paginas/likert.py", title="Itens Likert", icon="📶"),
    st.Page("paginas/questoes.py", title="Questões de pesquisa", icon="🔬"),
    st.Page("paginas/confiabilidade.py", title="Confiabilidade", icon="🧮"),
    st.Page("paginas/metodologia.py", title="Metodologia e desvios", icon="📝"),
])
pagina.run()
