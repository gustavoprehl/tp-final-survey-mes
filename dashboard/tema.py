"""Identidade visual do dashboard: paleta, template Plotly e CSS dos cartões.

Chame `aplicar()` uma vez no app.py: todas as figuras `px.*` e `go.Figure` passam
a usar o template "survey" sem precisar repetir layout em cada página.
"""
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

PRIMARIA = "#2563eb"
NEUTRA = "#94a3b8"
TEXTO = "#0f172a"
TEXTO_SUAVE = "#64748b"
GRADE = "#e2e8f0"
POSITIVO = "#16a34a"
NEGATIVO = "#dc2626"

# Categórica: ordem pensada para as primeiras cores serem as mais distintas
CATEGORICA = ["#2563eb", "#f59e0b", "#10b981", "#8b5cf6", "#ef4444", "#06b6d4", "#84cc16", "#ec4899"]
# Likert: discorda (vermelho) → neutro (cinza) → concorda (azul)
LIKERT = ["#b91c1c", "#f87171", "#cbd5e1", "#60a5fa", "#1d4ed8"]

_CSS = f"""
<style>
.block-container {{ padding-top: 2rem; }}
.kpi {{ background: var(--secondary-background-color, #f8fafc); border: 1px solid {GRADE};
       border-radius: 12px; padding: 14px 16px; height: 100%; }}
.kpi .rotulo {{ font-size: .78rem; color: {TEXTO_SUAVE}; text-transform: uppercase; letter-spacing: .04em; }}
.kpi .valor {{ font-size: 1.7rem; font-weight: 700; line-height: 1.2; margin-top: 2px; }}
.kpi .nota {{ font-size: .78rem; color: {TEXTO_SUAVE}; margin-top: 2px; }}
.achado {{ border: 1px solid {GRADE}; border-left: 5px solid {NEUTRA}; border-radius: 10px;
          padding: 12px 14px; height: 100%; background: var(--background-color, #fff); }}
.achado.sim {{ border-left-color: {POSITIVO}; }}
.achado.desc {{ border-left-color: {PRIMARIA}; }}
.achado .qp {{ font-weight: 700; font-size: .9rem; }}
.selo {{ display: inline-block; font-size: .7rem; font-weight: 600; padding: 2px 8px; border-radius: 999px;
        margin-left: 6px; background: #f1f5f9; color: {TEXTO_SUAVE}; }}
.achado.sim .selo {{ background: #dcfce7; color: #166534; }}
.achado.desc .selo {{ background: #dbeafe; color: #1e40af; }}
.achado .texto {{ font-size: .85rem; margin-top: 6px; }}
.achado .numeros {{ font-size: .75rem; color: {TEXTO_SUAVE}; margin-top: 8px; font-variant-numeric: tabular-nums; }}
.chip {{ display: inline-block; background: #eff6ff; color: #1e40af; border-radius: 999px;
        padding: 3px 10px; font-size: .8rem; font-weight: 600; }}
</style>
"""


def aplicar():
    template = go.layout.Template(pio.templates["plotly_white"])
    template.layout.update(
        font={"family": "Inter, Segoe UI, sans-serif", "size": 12, "color": TEXTO},
        colorway=CATEGORICA,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 0, "r": 10, "t": 10, "b": 0},
        xaxis={"gridcolor": GRADE, "zerolinecolor": GRADE, "title": {"font": {"color": TEXTO_SUAVE}}},
        yaxis={"gridcolor": GRADE, "zerolinecolor": GRADE, "title": {"font": {"color": TEXTO_SUAVE}}},
        legend={"orientation": "h", "y": -0.15, "title": {"text": ""}},
        hoverlabel={"font": {"family": "Inter, Segoe UI, sans-serif"}},
    )
    pio.templates["survey"] = template
    pio.templates.default = "survey"
    st.markdown(_CSS, unsafe_allow_html=True)


def kpi(coluna, rotulo, valor, nota=""):
    coluna.markdown(f'<div class="kpi"><div class="rotulo">{rotulo}</div><div class="valor">{valor}</div>'
                    f'<div class="nota">{nota}</div></div>', unsafe_allow_html=True)


def achado(coluna, qp, selo, texto, numeros="", estado=""):
    """estado: "sim" (rejeita H0), "desc" (descritiva) ou "" (não rejeita)."""
    coluna.markdown(f'<div class="achado {estado}"><span class="qp">{qp}</span><span class="selo">{selo}</span>'
                    f'<div class="texto">{texto}</div><div class="numeros">{numeros}</div></div>',
                    unsafe_allow_html=True)
