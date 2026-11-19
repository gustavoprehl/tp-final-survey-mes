"""Dashboard do survey "Uso de métricas em produtos de dados e automação".

Executar na raiz do repositório:  streamlit run dashboard/app.py
"""
import streamlit as st

import dados

st.set_page_config(page_title="Survey: métricas em produtos de dados", page_icon="📊", layout="wide")


@st.cache_data
def carregar(caminho, _modificado_em):
    return dados.processar(caminho)


fonte, sintetico = dados.localizar_fonte()
respostas = carregar(fonte, fonte.stat().st_mtime)
validas = respostas[respostas["motivo_descarte"].isna()]

if sintetico:
    st.warning("**DADOS SINTÉTICOS.** Nenhum CSV em `dados/brutos/`: o dashboard está usando respostas "
               "geradas para desenvolvimento, que não fazem parte da análise.", icon="⚠️")

# Filtros por segmento: valem para todas as páginas
with st.sidebar:
    st.header("Filtros")
    filtros = {
        "P1_grupo": ("Área de atuação", dados.AREAS + ["Outra"]),
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
st.session_state["filtradas"] = filtradas

pagina = st.navigation([
    st.Page("paginas/perfil.py", title="Perfil da amostra", icon="👥", default=True),
    st.Page("paginas/likert.py", title="Itens Likert", icon="📶"),
    st.Page("paginas/questoes.py", title="Questões de pesquisa", icon="🔬"),
    st.Page("paginas/confiabilidade.py", title="Confiabilidade", icon="🧮"),
    st.Page("paginas/metodologia.py", title="Metodologia e desvios", icon="📝"),
])
pagina.run()
