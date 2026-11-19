"""Formatação e blocos de interface usados por várias páginas."""
import numpy as np
import streamlit as st

import estatistica as est

N_MIN_EXIBICAO = 5  # seção 6: filtros com menos respostas não mostram distribuições


def num(valor, casas=2):
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(valor, casas=1):
    return f"{num(100 * valor, casas)}%"


def p_valor(p):
    return "p < 0,001" if p < 0.001 else f"p = {num(p, 3)}"


def exigir_n_minimo(df):
    """Interrompe a página se o filtro deixar poucas respostas (anonimização)."""
    if len(df) < N_MIN_EXIBICAO:
        st.warning(f"O filtro atual deixa {len(df)} resposta(s). Com menos de {N_MIN_EXIBICAO}, "
                   "as distribuições não são exibidas, para proteger o anonimato (seção 6).")
        st.stop()


def aviso_filtro(filtradas, validas):
    if len(filtradas) < len(validas):
        st.info(f"**Filtro ativo ({len(filtradas)} de {len(validas)} respostas).** Os resultados abaixo "
                "são exploratórios: os testes confirmatórios usam a amostra completa e ficam fora da "
                "correção de Holm quando recalculados por segmento (seção 5).")


def cartao_teste(nome, resultado, rotulo_estatistica, rotulo_efeito, limiares, p_ajustado=None):
    """Mostra estatística, p-valores, tamanho de efeito e n de um teste."""
    colunas = st.columns(5)
    colunas[0].metric(rotulo_estatistica, num(resultado["estatistica"], 2))
    colunas[1].metric("p-valor", p_valor(resultado["p"]).removeprefix("p = "))
    colunas[2].metric("p ajustado (Holm)", "—" if p_ajustado is None else p_valor(p_ajustado).removeprefix("p = "))
    colunas[3].metric(rotulo_efeito, num(resultado["efeito"], 3),
                      est.magnitude(resultado["efeito"], limiares), delta_color="off")
    colunas[4].metric("n", resultado["n"])
    referencia = resultado["p"] if p_ajustado is None else p_ajustado
    if referencia < est.ALFA:
        st.success(f"**{nome}:** rejeita H0 com α = 0,05"
                   + (" após a correção de Holm." if p_ajustado is not None else "."))
    else:
        st.warning(f"**{nome}:** não rejeita H0 com α = 0,05. Isso não prova igualdade: a amostra não "
                   "traz evidência suficiente, e o tamanho de efeito mostra a magnitude observada.")
