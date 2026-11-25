import pandas as pd
import streamlit as st

import componentes as ui
import dados
import estatistica as est

respostas = st.session_state["respostas"]
validas = st.session_state["validas"]

st.title("Metodologia e desvios")

st.subheader("Pré-registro")
inicio, fim = respostas["timestamp"].min(), respostas["timestamp"].max()
st.markdown(
    "O protocolo foi pré-registrado com a tag "
    "[`protocolo-v1`](https://github.com/gustavoprehl/tp-final-survey-mes/releases/tag/protocolo-v1) "
    "em **12/11/2026 às 19:23**, e enviado na plataforma da disciplina às 19:42. "
    f"A primeira resposta da base atual é de **{inicio:%d/%m/%Y %H:%M}** e a última, de **{fim:%d/%m/%Y %H:%M}**."
)
if inicio < pd.Timestamp("2026-11-12 19:23"):
    st.error("Há respostas anteriores à tag protocolo-v1. Verifique a base antes da apresentação.")

st.subheader("Desenho do estudo")
st.dataframe(pd.DataFrame([
    ("População", "Profissionais que criam ou mantêm produtos de dados ou automação em empresas brasileiras"),
    ("Amostragem", "Não probabilística, por conveniência, com bola de neve"),
    ("Período de coleta", "12/11 a 23/11/2026 (previsto até 22/11; ver desvios)"),
    ("Respostas", f"{len(respostas)} recebidas, {len(validas)} válidas, {len(respostas) - len(validas)} descartadas"),
    ("Margem de erro", f"± {ui.num(100 * est.margem_erro(len(validas)), 1)} p.p. (95%, p = 0,5, n = {len(validas)}); "
                       "não inclui o viés de seleção"),
    ("Instrumento", "Google Forms, 23 itens, 2 construtos de 4 itens (UT e MM), pergunta de atenção"),
    ("Análise", "Testes não paramétricos, α = 0,05, Holm na família principal: QP2, QP3 e QP4 item a item "
                "(MM1–MM4), 6 testes no total (ver desvios)"),
], columns=["Aspecto", "Descrição"]), hide_index=True, width="stretch")

st.subheader("Desvios em relação ao protocolo")
st.markdown((dados.RAIZ / "docs" / "DESVIOS.md").read_text(encoding="utf-8").split("\n", 1)[1])

st.subheader("Limitações")
n_validas = len(validas)
n_nao_mede = int((validas["M2_grupo"] == "Não mede").sum())
iguais = respostas["grade_igual"].notna()
iguais_validas = int((iguais & respostas["motivo_descarte"].isna()).sum())
if not iguais.any():
    texto_iguais = "Nenhuma resposta teve grades com todas as respostas iguais."
elif iguais_validas == 0:
    texto_iguais = ("A única resposta com grades iguais também falhou em outra regra e já estava descartada "
                    "(ver Perfil da amostra)." if iguais.sum() == 1 else
                    f"As {int(iguais.sum())} respostas com grades iguais também falharam em outra regra e já "
                    "estavam descartadas (ver Perfil da amostra).")
else:
    texto_iguais = (f"{iguais_validas} resposta(s) válida(s) têm grades iguais e seguem na análise, "
                    "apenas sinalizadas.")
st.markdown(f"""
**O que os resultados permitem afirmar.** O estudo seguiu o protocolo pré-registrado, com descartes, testes e
desvios documentados. Os resultados descrevem com segurança o perfil e as práticas das {n_validas} pessoas da
amostra, e os tamanhos de efeito indicam a direção e a força das relações observadas. As limitações abaixo,
cada uma com o que foi feito para lidar com ela, definem até onde essas conclusões podem ser estendidas.

- **Tamanho da amostra:** {n_validas} respostas válidas (meta de 60), com margem de erro de ± {ui.num(100 * est.margem_erro(n_validas), 1)} p.p. Diferenças pequenas podem não aparecer como significativas, por isso cada resultado é lido junto com o tamanho de efeito, que não depende do n.
- **Grupos pequenos:** na QP3, o grupo "não mede" ficou com {n_nao_mede} resposta(s). O teste é apresentado conforme o plano, e a comparação é tratada como indicativa. Na QP2, áreas com menos de 5 respostas são agrupadas em "Outras".
- **Confiabilidade dos construtos:** a regra pré-registrada (seção 5) foi aplicada como previsto: o escore UT usa os três itens consistentes entre si, e a maturidade (MM) é analisada item a item. Assim, cada conclusão se apoia em medidas com consistência verificada.
- **Amostra por conveniência e bola de neve:** as conclusões valem para a amostra, que foi diversificada com vários canais de divulgação; o perfil completo está na página Perfil da amostra.
- **Autosseleção:** a mensagem de divulgação foi neutra e sem recompensa, para não atrair só quem já se interessa por métricas.
- **Não resposta:** os lembretes foram espaçados e limitados. O alcance de cada divulgação e a taxa de resposta geral aparecem abaixo; a taxa por canal não é calculada porque o formulário não pergunta por onde a pessoa chegou.
- **Desejabilidade social:** reduzida pelo anonimato, pela redação neutra, pela opção "Não sei" e por um item reverso em cada construto.
- **Medidas autorrelatadas:** como em todo survey, as respostas refletem a percepção de quem responde; a M4 (número de falhas) complementa a percepção de retrabalho com um dado concreto.
- **Viés de memória:** a M4 usa uma janela curta (30 dias) e entra só como análise secundária.
- **Associação, não causa:** a QP3 mostra se as variáveis andam juntas; porte e setor ficam disponíveis nos filtros para exploração.
- **Colegas da turma:** excluídos na divulgação e avisados na mensagem; o repasse do link por terceiros é o risco que permanece.
- **Tempo de preenchimento:** o Google Forms registra só o horário de envio. Para identificar respostas descuidadas, há a pergunta de atenção (com descarte) e a sinalização de grades com todas as respostas iguais (sem descarte). {texto_iguais}
""")


def legenda(arquivo):
    """2026-11-12_linkedin-post_arthur.png -> "12/11/2026 · linkedin post · arthur"."""
    partes = arquivo.stem.split("_")
    data = pd.to_datetime(partes[0], format="%Y-%m-%d", errors="coerce")
    inicio = [f"{data:%d/%m/%Y}"] if not pd.isna(data) else [partes[0]]
    return " · ".join(inicio + [p.replace("-", " ") for p in partes[1:]])


st.subheader("Divulgação e taxa de resposta")
pasta_divulgacao = dados.RAIZ / "evidencias" / "divulgacao"
registro = pasta_divulgacao / "registro.md"
if registro.exists():
    st.markdown(registro.read_text(encoding="utf-8").split("\n", 1)[1])
else:
    st.info("O registro das divulgações (`evidencias/divulgacao/registro.md`, com data, canal, alcance e captura) "
            "ainda não foi criado. Quando existir, aparece aqui.")

capturas = sorted(p for p in pasta_divulgacao.glob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
with st.expander(f"Ver capturas da divulgação ({len(capturas)})"):
    if not capturas:
        st.caption("Nenhuma captura salva em evidencias/divulgacao/ ainda.")
    colunas = st.columns(2)
    for i, arquivo in enumerate(capturas):
        colunas[i % 2].image(str(arquivo), caption=legenda(arquivo), width="stretch")
