from pathlib import Path
from html import escape
import time

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path(__file__).parent / "dados" / "simulacao_ciberseguranca_brasil.csv"
DATA_URL = (
    "https://github.com/AlexandreLouzada/Dados-Simulados-G2/blob/main/"
    "datasets_g2_30_temas/simulacao_ciberseguranca_brasil.csv"
)

MONTH_NAMES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}

FILTER_COLUMNS = {
    "Ano": "ano",
    "Mês": "mes",
    "Região": "regiao",
    "Estado (UF)": "uf",
    "Setor": "setor",
    "Tipo de ataque": "tipo_ataque",
    "Nível de criticidade": "nivel_criticidade",
}

COLOR_SEQUENCE = ["#0f766e", "#2563eb", "#dc2626", "#7c3aed", "#ca8a04", "#475569"]
DARK_COLOR_SEQUENCE = ["#2dd4bf", "#60a5fa", "#fb7185", "#c084fc", "#facc15", "#94a3b8"]


st.set_page_config(
    page_title="Análise de Segurança Cibernética",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["mes_nome"] = df["mes"].map(MONTH_NAMES)
    df["periodo"] = df["data"].dt.to_period("M").astype(str)
    return df


def format_integer(value: int | float) -> str:
    return f"{int(value):,}".replace(",", ".")


def format_currency(value: float) -> str:
    formatted = f"R$ {value:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def format_currency_markdown(value: float) -> str:
    return format_currency(value).replace("$", r"\$")


def format_hours(value: float) -> str:
    return f"{value:.1f} h".replace(".", ",")


def format_percent(value: float) -> str:
    return f"{value:.1f}%".replace(".", ",")


def unique_sorted(df: pd.DataFrame, column: str) -> list:
    return sorted(df[column].dropna().unique().tolist())


def sidebar_filters(df: pd.DataFrame) -> dict:
    st.sidebar.header("Filtros")
    st.sidebar.caption("Refine os dados para investigar cenários específicos.")

    selected = {}
    for label, column in FILTER_COLUMNS.items():
        values = unique_sorted(df, column)
        if column == "mes":
            selected[column] = st.sidebar.multiselect(
                label,
                values,
                default=values,
                format_func=lambda month: MONTH_NAMES.get(month, str(month)),
            )
        else:
            selected[column] = st.sidebar.multiselect(label, values, default=values)
    return selected


def configure_theme(dark_mode: bool) -> dict:
    if dark_mode:
        theme = {
            "plotly_template": "plotly_dark",
            "colors": DARK_COLOR_SEQUENCE,
            "plot_bg": "#111827",
            "paper_bg": "#111827",
            "font": "#e5e7eb",
            "grid": "#334155",
        }
        st.markdown(
            """
            <style>
            :root {
                color-scheme: dark;
            }

            .stApp {
                background: #0f172a;
                color: #e5e7eb;
            }

            [data-testid="stHeader"] {
                background: #0f172a;
                border-bottom: 1px solid #1e293b;
            }

            [data-testid="stHeader"]::before {
                background: transparent;
            }

            [data-testid="stToolbar"],
            [data-testid="stDecoration"],
            [data-testid="stStatusWidget"] {
                background: #0f172a;
                color: #cbd5e1;
            }

            [data-testid="stMainBlockContainer"] {
                padding-top: 4.5rem;
            }

            [data-testid="stSidebar"] {
                background: #020617;
                border-right: 1px solid #1e293b;
            }

            [data-testid="stSidebar"] > div {
                background: #020617;
            }

            [data-testid="stSidebar"] * {
                color: #e5e7eb;
            }

            [data-testid="stSidebarContent"] {
                background: #020617;
            }

            [data-testid="stSidebarCollapseButton"] {
                color: #e5e7eb;
            }

            [data-baseweb="select"] > div {
                background: #111827 !important;
                border-color: #334155 !important;
                box-shadow: none !important;
            }

            [data-baseweb="select"] > div:hover {
                border-color: #2dd4bf !important;
            }

            [data-baseweb="select"] input {
                color: #f8fafc !important;
            }

            [data-baseweb="select"] svg {
                color: #94a3b8 !important;
                fill: #94a3b8 !important;
            }

            [data-baseweb="tag"] {
                background: #0f766e !important;
                border: 1px solid #14b8a6 !important;
                color: #ffffff !important;
            }

            [data-baseweb="tag"] span {
                color: #ffffff !important;
            }

            [data-baseweb="popover"],
            [role="listbox"] {
                background: #111827 !important;
                border: 1px solid #334155 !important;
                color: #e5e7eb !important;
            }

            [role="option"] {
                background: #111827 !important;
                color: #e5e7eb !important;
            }

            [role="option"]:hover {
                background: #1f2937 !important;
            }

            [data-testid="stMetric"] {
                background: #111827;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 14px 16px;
            }

            [data-testid="stMetricLabel"],
            [data-testid="stMetricValue"] {
                color: #f8fafc;
            }

            div[data-testid="stMarkdownContainer"] p,
            div[data-testid="stMarkdownContainer"] li {
                color: #d1d5db;
            }

            .stTabs [data-baseweb="tab-list"] {
                border-bottom: 1px solid #334155;
            }

            .stTabs [data-baseweb="tab"] {
                color: #cbd5e1;
            }

            .stTabs [aria-selected="true"] {
                color: #2dd4bf;
            }

            [data-testid="stDataFrame"] {
                border: 1px solid #334155;
                border-radius: 8px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        return theme

    return {
        "plotly_template": "plotly_white",
        "colors": COLOR_SEQUENCE,
        "plot_bg": "#ffffff",
        "paper_bg": "#ffffff",
        "font": "#1f2937",
        "grid": "#e5e7eb",
    }


def apply_filters(df: pd.DataFrame, selected: dict) -> pd.DataFrame:
    mask = pd.Series(True, index=df.index)
    for column, values in selected.items():
        mask &= df[column].isin(values)
    return df.loc[mask].copy()


def top_by_incidents(df: pd.DataFrame, column: str) -> str:
    return df.groupby(column)["incidentes"].sum().idxmax()


def calculate_kpis(df: pd.DataFrame) -> dict:
    return {
        "total_incidentes": int(df["incidentes"].sum()),
        "ataque_predominante": top_by_incidents(df, "tipo_ataque"),
        "setor_mais_afetado": top_by_incidents(df, "setor"),
        "impacto_total": float(df["impacto_financeiro"].sum()),
        "tempo_medio": float(df["tempo_recuperacao"].mean()),
        "regiao_critica": top_by_incidents(df, "regiao"),
    }


def aggregate_incidents(df: pd.DataFrame, column: str, ascending: bool = False) -> pd.DataFrame:
    return (
        df.groupby(column, as_index=False)["incidentes"]
        .sum()
        .sort_values("incidentes", ascending=ascending)
    )


def apply_chart_layout(fig, theme: dict, height: int | None = None):
    fig.update_layout(
        template=theme["plotly_template"],
        colorway=theme["colors"],
        plot_bgcolor=theme["plot_bg"],
        paper_bgcolor=theme["paper_bg"],
        margin=dict(l=16, r=16, t=58, b=24),
        legend_title_text="",
        font=dict(family="Arial", size=13, color=theme["font"]),
        title=dict(font=dict(size=18, color=theme["font"])),
        xaxis=dict(gridcolor=theme["grid"], zerolinecolor=theme["grid"]),
        yaxis=dict(gridcolor=theme["grid"], zerolinecolor=theme["grid"]),
    )
    if height:
        fig.update_layout(height=height)
    return fig


def metric_card(container, label: str, value: str, help_text: str):
    container.metric(label, value, help=help_text)


def render_animated_kpis(kpis: dict, dark_mode: bool):
    duration_ms = 1600
    palette = {
        "bg": "#111827" if dark_mode else "#ffffff",
        "border": "#334155" if dark_mode else "#d8e0ea",
        "label": "#f8fafc" if dark_mode else "#111827",
        "value": "#f8fafc" if dark_mode else "#1f2937",
        "muted": "#94a3b8" if dark_mode else "#64748b",
        "accent": "#2dd4bf" if dark_mode else "#0f766e",
        "shadow": "rgba(0, 0, 0, 0.24)" if dark_mode else "rgba(15, 23, 42, 0.08)",
    }

    cards = [
        ("Total de incidentes", "integer", kpis["total_incidentes"], "Soma de incidentes no recorte filtrado."),
        ("Impacto financeiro total", "currency", kpis["impacto_total"], "Prejuízo estimado no recorte filtrado."),
        ("Tempo médio de recuperação", "hours", kpis["tempo_medio"], "Tempo médio necessário para recuperação dos incidentes."),
        ("Ataque predominante", "text", kpis["ataque_predominante"], "Tipo de ataque com maior volume de incidentes."),
        ("Setor mais afetado", "text", kpis["setor_mais_afetado"], "Setor com maior soma de incidentes."),
        ("Região mais crítica", "text", kpis["regiao_critica"], "Região com maior soma de incidentes."),
    ]

    def ease_out_cubic(progress: float) -> float:
        return 1 - (1 - progress) ** 3

    def format_card_value(kind: str, value):
        if kind == "currency":
            return format_currency(float(value))
        if kind == "hours":
            return format_hours(float(value))
        if kind == "integer":
            return format_integer(float(value))
        return str(value)

    def card_html(label: str, value: str, help_text: str, typing: bool) -> str:
        typing_class = " typing" if typing else ""
        return f"""
        <article class="animated-kpi-card">
          <div class="animated-kpi-label">
            <span>{escape(label)}</span>
            <span class="animated-kpi-help" title="{escape(help_text)}">?</span>
          </div>
          <div class="animated-kpi-value{typing_class}">{escape(value)}</div>
        </article>
        """

    def grid_html(values: list[tuple[str, str, str, bool]]) -> str:
        rendered_cards = "\n".join(
            card_html(label, value, help_text, typing)
            for label, value, help_text, typing in values
        )
        return f"""
        <style>
        .animated-kpi-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
            margin: 0.25rem 0 1.15rem;
        }}

        .animated-kpi-card {{
            min-height: 106px;
            background: {palette["bg"]};
            border: 1px solid {palette["border"]};
            border-radius: 8px;
            padding: 18px 18px 16px;
            box-shadow: 0 12px 28px {palette["shadow"]};
            position: relative;
            overflow: hidden;
        }}

        .animated-kpi-card::before {{
            content: "";
            position: absolute;
            inset: 0 0 auto 0;
            height: 3px;
            background: linear-gradient(90deg, {palette["accent"]}, transparent);
            opacity: 0.85;
        }}

        .animated-kpi-label {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: {palette["label"]};
            font-size: 0.86rem;
            line-height: 1.25;
            margin-bottom: 12px;
        }}

        .animated-kpi-help {{
            display: inline-grid;
            place-items: center;
            width: 17px;
            height: 17px;
            border: 1px solid {palette["muted"]};
            border-radius: 50%;
            color: {palette["muted"]};
            font-size: 11px;
        }}

        .animated-kpi-value {{
            color: {palette["value"]};
            font-size: clamp(1.9rem, 4vw, 2.35rem);
            line-height: 1.08;
            letter-spacing: 0;
            white-space: nowrap;
        }}

        .animated-kpi-value.typing::after {{
            content: "";
            display: inline-block;
            width: 2px;
            height: 0.9em;
            margin-left: 3px;
            background: {palette["accent"]};
            transform: translateY(3px);
            animation: animatedKpiBlink 0.75s step-end infinite;
        }}

        @keyframes animatedKpiBlink {{
            50% {{ opacity: 0; }}
        }}

        @media (max-width: 900px) {{
            .animated-kpi-grid {{
                grid-template-columns: 1fr;
            }}

            .animated-kpi-value {{
                white-space: normal;
            }}
        }}
        </style>
        <div class="animated-kpi-grid">{rendered_cards}</div>
        """

    placeholder = st.empty()
    frames = 32
    frame_delay = duration_ms / frames / 1000

    for frame in range(frames + 1):
        progress = frame / frames
        eased = ease_out_cubic(progress)
        rendered_values = []

        for label, kind, final_value, help_text in cards:
            if kind == "text":
                text = str(final_value)
                chars = max(1, round(len(text) * progress)) if progress else 0
                rendered_values.append((label, text[:chars], help_text, progress < 1))
            else:
                rendered_values.append(
                    (label, format_card_value(kind, float(final_value) * eased), help_text, False)
                )

        placeholder.markdown(grid_html(rendered_values), unsafe_allow_html=True)
        if frame < frames:
            time.sleep(frame_delay)


def render_landing_page_v2():
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
        }

        .stApp {
            background:
                radial-gradient(circle at 18% 22%, rgba(45, 212, 191, 0.13), transparent 28%),
                radial-gradient(circle at 84% 18%, rgba(96, 165, 250, 0.12), transparent 30%),
                #020617;
            color: #f8fafc;
        }

        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            background: transparent;
            color: #cbd5e1;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1040px;
            padding-top: 18vh;
        }

        .landing-shell {
            display: grid;
            gap: 26px;
            justify-items: center;
            text-align: center;
            padding: 12px 20px 44px;
        }

        .landing-kicker {
            color: #2dd4bf;
            font-size: clamp(1.2rem, 2vw, 1.65rem);
            font-weight: 700;
            letter-spacing: 0;
        }

        .landing-title {
            margin: 0;
            color: #f8fafc;
            font-size: clamp(3.2rem, 8vw, 6.6rem);
            line-height: 0.98;
            letter-spacing: 0;
        }

        .landing-subtitle {
            color: #cbd5e1;
            font-size: clamp(1.15rem, 2vw, 1.55rem);
            margin: 0;
        }

        .landing-meta {
            width: min(680px, 100%);
            display: grid;
            gap: 10px;
            padding: 24px;
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 8px;
            box-shadow: 0 22px 60px rgba(0, 0, 0, 0.24);
        }

        .landing-meta p {
            margin: 0;
            color: #e5e7eb;
            font-size: 1.03rem;
        }

        .landing-meta strong {
            color: #ffffff;
        }

        .landing-meta a {
            color: #ffffff;
            font-weight: 700;
            text-decoration: none;
            border-bottom: none;
        }

        .landing-meta a:hover {
            color: #5eead4;
            border-bottom: none;
        }

        .stButton {
            display: flex;
            justify-content: center;
        }

        .stButton > button {
            min-width: 220px;
            min-height: 48px;
            border-radius: 8px;
            border: 1px solid #2dd4bf;
            background: #0f766e;
            color: #ffffff;
            font-weight: 700;
            box-shadow: 0 16px 36px rgba(15, 118, 110, 0.28);
            transition: transform 160ms ease, background 160ms ease, border-color 160ms ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            background: #14b8a6;
            border-color: #5eead4;
            color: #02111b;
        }
        </style>

        <section class="landing-shell">
            <div class="landing-kicker">Linguagens de programação</div>
            <h1 class="landing-title">Projeto Final da Disciplina</h1>
            <p class="landing-subtitle">Análise de segurança cibernética e ataques digitais</p>
            <div class="landing-meta">
                <p><strong>Unilasalle - Sistemas de Informação</strong></p>
                <p>Professor orientador: <a href="https://github.com/AlexandreLouzada" target="_blank">Alexandre Neves Louzada</a></p>
                <p>Aluno: <a href="https://github.com/ruancorreia" target="_blank">Ruan da Silva Correia</a></p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 1, 1])
    with center:
        go_to_dashboard = st.button(
            "Ir para o dashboard",
            type="primary",
            use_container_width=True,
        )

    if go_to_dashboard:
        st.session_state["show_dashboard"] = True
        st.rerun()


if not st.session_state.get("show_dashboard", False):
    render_landing_page_v2()
    st.stop()


df = load_data()
dark_mode = st.sidebar.toggle("Modo escuro", value=True)
theme = configure_theme(dark_mode)
selected_filters = sidebar_filters(df)
filtered = apply_filters(df, selected_filters)

st.title("Análise de Segurança Cibernética e Ataques Digitais")
st.markdown(
    f"baseado no arquivo "
    f"[simulacao_ciberseguranca_brasil.csv]({DATA_URL})"
)

st.markdown(
    """
    Este painel investiga incidentes de segurança digital no Brasil entre 2015 e
    2024, com foco em tipos de ataque, setores afetados, impacto financeiro,
    vulnerabilidades, criticidade e tempo de recuperação.
    """
)

if filtered.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

kpis = calculate_kpis(filtered)

st.subheader("Visão geral")
render_animated_kpis(kpis, dark_mode)

tab_overview, tab_attacks, tab_regions, tab_risk, tab_data = st.tabs(
    ["Evolução", "Ataques", "Regiões e setores", "Risco", "Dados"]
)

with tab_overview:
    timeline = (
        filtered.groupby(["ano", "mes", "periodo"], as_index=False)["incidentes"].sum()
        .sort_values(["ano", "mes"])
    )
    fig_timeline = px.line(
        timeline,
        x="periodo",
        y="incidentes",
        markers=True,
        title="Evolução temporal dos incidentes",
        labels={"periodo": "Período", "incidentes": "Incidentes"},
        color_discrete_sequence=[theme["colors"][0]],
    )
    st.plotly_chart(apply_chart_layout(fig_timeline, theme, 420), width="stretch")

    periodo_critico = timeline.sort_values("incidentes", ascending=False).iloc[0]
    st.info(
        "Período crítico: "
        f"{periodo_critico['periodo']} registrou "
        f"{format_integer(periodo_critico['incidentes'])} incidentes no recorte selecionado."
    )

    heatmap = filtered.pivot_table(
        values="incidentes",
        index="ano",
        columns="mes",
        aggfunc="sum",
        fill_value=0,
    ).rename(columns=MONTH_NAMES)
    fig_heatmap = px.imshow(
        heatmap,
        aspect="auto",
        title="Heatmap mensal de incidentes",
        labels={"x": "Mês", "y": "Ano", "color": "Incidentes"},
        color_continuous_scale="Reds",
    )
    st.plotly_chart(apply_chart_layout(fig_heatmap, theme, 420), width="stretch")

with tab_attacks:
    col_left, col_right = st.columns(2)

    attacks_df = aggregate_incidents(filtered, "tipo_ataque", ascending=True)
    fig_attacks = px.bar(
        attacks_df,
        x="incidentes",
        y="tipo_ataque",
        orientation="h",
        title="Frequência por tipo de ataque",
        labels={"tipo_ataque": "Tipo de ataque", "incidentes": "Incidentes"},
        color="tipo_ataque",
        color_discrete_sequence=theme["colors"],
    )
    col_left.plotly_chart(apply_chart_layout(fig_attacks, theme, 380), width="stretch")

    vulnerability_df = aggregate_incidents(filtered, "vulnerabilidade", ascending=True)
    fig_vulnerabilities = px.bar(
        vulnerability_df,
        x="incidentes",
        y="vulnerabilidade",
        orientation="h",
        title="Ranking de vulnerabilidades",
        labels={"vulnerabilidade": "Vulnerabilidade", "incidentes": "Incidentes"},
        color="vulnerabilidade",
        color_discrete_sequence=theme["colors"],
    )
    col_right.plotly_chart(apply_chart_layout(fig_vulnerabilities, theme, 380), width="stretch")

    attack_sector = filtered.pivot_table(
        values="incidentes",
        index="setor",
        columns="tipo_ataque",
        aggfunc="sum",
        fill_value=0,
    )
    fig_attack_sector = px.imshow(
        attack_sector,
        aspect="auto",
        title="Mapa de ataques por setor",
        labels={"x": "Tipo de ataque", "y": "Setor", "color": "Incidentes"},
        color_continuous_scale="Teal",
    )
    st.plotly_chart(apply_chart_layout(fig_attack_sector, theme, 420), width="stretch")

with tab_regions:
    col_left, col_right = st.columns(2)

    sectors_df = aggregate_incidents(filtered, "setor", ascending=True)
    fig_sectors = px.bar(
        sectors_df,
        x="incidentes",
        y="setor",
        orientation="h",
        title="Comparação entre setores",
        labels={"setor": "Setor", "incidentes": "Incidentes"},
        color="setor",
        color_discrete_sequence=theme["colors"],
    )
    col_left.plotly_chart(apply_chart_layout(fig_sectors, theme, 380), width="stretch")

    regions_df = aggregate_incidents(filtered, "regiao")
    fig_regions = px.pie(
        regions_df,
        names="regiao",
        values="incidentes",
        title="Distribuição regional dos incidentes",
        color_discrete_sequence=theme["colors"],
    )
    fig_regions.update_traces(textposition="inside", textinfo="percent+label")
    col_right.plotly_chart(apply_chart_layout(fig_regions, theme, 380), width="stretch")

    uf_df = aggregate_incidents(filtered, "uf").head(10).sort_values("incidentes")
    fig_uf = px.bar(
        uf_df,
        x="incidentes",
        y="uf",
        orientation="h",
        title="Top 10 estados por incidentes",
        labels={"uf": "UF", "incidentes": "Incidentes"},
        color="incidentes",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(apply_chart_layout(fig_uf, theme, 420), width="stretch")

with tab_risk:
    col_left, col_right = st.columns(2)

    criticality_df = aggregate_incidents(filtered, "nivel_criticidade")
    fig_criticality = px.bar(
        criticality_df,
        x="nivel_criticidade",
        y="incidentes",
        title="Incidentes por nível de criticidade",
        labels={"nivel_criticidade": "Nível de criticidade", "incidentes": "Incidentes"},
        color="nivel_criticidade",
        color_discrete_sequence=theme["colors"],
    )
    col_left.plotly_chart(apply_chart_layout(fig_criticality, theme, 380), width="stretch")

    status_df = aggregate_incidents(filtered, "status_resposta")
    fig_status = px.pie(
        status_df,
        names="status_resposta",
        values="incidentes",
        title="Status de resposta dos incidentes",
        color_discrete_sequence=theme["colors"],
    )
    fig_status.update_traces(textposition="inside", textinfo="percent+label")
    col_right.plotly_chart(apply_chart_layout(fig_status, theme, 380), width="stretch")

    scatter_df = (
        filtered.groupby(["ano", "mes", "regiao", "setor", "tipo_ataque"], as_index=False)
        .agg(
            incidentes=("incidentes", "sum"),
            impacto_financeiro=("impacto_financeiro", "sum"),
            tempo_recuperacao=("tempo_recuperacao", "mean"),
        )
    )
    fig_scatter = px.scatter(
        scatter_df,
        x="incidentes",
        y="impacto_financeiro",
        color="tipo_ataque",
        size="tempo_recuperacao",
        hover_data=["ano", "mes", "regiao", "setor"],
        title="Impacto financeiro x incidentes",
        labels={
            "incidentes": "Incidentes",
            "impacto_financeiro": "Impacto financeiro",
            "tipo_ataque": "Tipo de ataque",
            "tempo_recuperacao": "Tempo médio de recuperação",
        },
        color_discrete_sequence=theme["colors"],
    )
    st.plotly_chart(apply_chart_layout(fig_scatter, theme, 470), width="stretch")

with tab_data:
    st.markdown(
        "Use a tabela dinâmica para comparar regiões, estados, setores e tipos de ataque."
    )
    pivot = pd.pivot_table(
        filtered,
        values=["incidentes", "impacto_financeiro", "tempo_recuperacao", "sistemas_afetados"],
        index=["regiao", "uf", "setor", "tipo_ataque"],
        aggfunc={
            "incidentes": "sum",
            "impacto_financeiro": "sum",
            "tempo_recuperacao": "mean",
            "sistemas_afetados": "sum",
        },
    ).reset_index()
    pivot = pivot.sort_values("incidentes", ascending=False)
    st.dataframe(
        pivot,
        width="stretch",
        hide_index=True,
        column_config={
            "regiao": "Região",
            "uf": "UF",
            "setor": "Setor",
            "tipo_ataque": "Tipo de ataque",
            "incidentes": st.column_config.NumberColumn("Incidentes", format="%d"),
            "impacto_financeiro": st.column_config.NumberColumn(
                "Impacto financeiro", format="R$ %.2f"
            ),
            "tempo_recuperacao": st.column_config.NumberColumn(
                "Tempo médio de recuperação", format="%.1f h"
            ),
            "sistemas_afetados": st.column_config.NumberColumn(
                "Sistemas afetados", format="%d"
            ),
        },
    )

st.subheader("Interpretação dos resultados")
timeline_summary = (
    filtered.groupby(["ano", "mes", "periodo"], as_index=False)["incidentes"].sum()
    .sort_values(["ano", "mes"])
)
critical_period = timeline_summary.sort_values("incidentes", ascending=False).iloc[0]
attack_summary = aggregate_incidents(filtered, "tipo_ataque")
sector_summary = aggregate_incidents(filtered, "setor")
region_summary = aggregate_incidents(filtered, "regiao")
vulnerability_summary = aggregate_incidents(filtered, "vulnerabilidade")
criticality_summary = aggregate_incidents(filtered, "nivel_criticidade")
status_summary = aggregate_incidents(filtered, "status_resposta")
year_summary = aggregate_incidents(filtered, "ano").sort_values("ano")

top_attack = attack_summary.iloc[0]
top_sector = sector_summary.iloc[0]
top_region = region_summary.iloc[0]
top_vulnerability = vulnerability_summary.iloc[0]
dominant_criticality = criticality_summary.iloc[0]
dominant_status = status_summary.iloc[0]
first_year = year_summary.iloc[0]
last_year = year_summary.iloc[-1]

attack_share = top_attack["incidentes"] / kpis["total_incidentes"] * 100
sector_share = top_sector["incidentes"] / kpis["total_incidentes"] * 100
region_share = top_region["incidentes"] / kpis["total_incidentes"] * 100
criticality_share = dominant_criticality["incidentes"] / kpis["total_incidentes"] * 100
status_share = dominant_status["incidentes"] / kpis["total_incidentes"] * 100
average_impact = kpis["impacto_total"] / kpis["total_incidentes"]
affected_systems = int(filtered["sistemas_afetados"].sum())
year_delta = int(last_year["incidentes"] - first_year["incidentes"])
year_delta_percent = year_delta / first_year["incidentes"] * 100 if first_year["incidentes"] else 0

st.markdown(
    f"""
    O recorte analisado reúne **{format_integer(kpis['total_incidentes'])} incidentes**
    e um impacto financeiro estimado de **{format_currency_markdown(kpis['impacto_total'])}**.
    Em média, cada incidente representa aproximadamente **{format_currency_markdown(average_impact)}**
    de prejuízo estimado, além de envolver **{format_integer(affected_systems)} sistemas
    afetados** no total. O tempo médio de recuperação ficou em
    **{format_hours(kpis['tempo_medio'])}**, o que indica uma janela relevante de
    indisponibilidade ou esforço operacional após os ataques.

    O tipo de ataque mais recorrente foi **{top_attack['tipo_ataque']}**, responsável
    por **{format_percent(attack_share)}** dos incidentes filtrados. O setor mais afetado foi
    **{top_sector['setor']}**, com **{format_percent(sector_share)}** do volume total, enquanto
    a região com maior concentração foi **{top_region['regiao']}**, com
    **{format_percent(region_share)}** dos registros. A vulnerabilidade mais associada aos
    incidentes foi **{top_vulnerability['vulnerabilidade']}**, sugerindo um ponto de
    atenção prioritário para ações de prevenção, treinamento, revisão de controles
    ou atualização de sistemas.

    Do ponto de vista temporal, o período mais crítico foi **{critical_period['periodo']}**,
    com **{format_integer(critical_period['incidentes'])} incidentes**. Comparando o
    primeiro e o último ano do recorte filtrado, houve uma variação de
    **{format_integer(year_delta)} incidentes** (**{format_percent(year_delta_percent)}**). Esse
    comportamento ajuda a avaliar se o cenário está se agravando, estabilizando ou
    reduzindo ao longo do tempo.

    Em criticidade, o nível mais frequente foi **{dominant_criticality['nivel_criticidade']}**,
    concentrando **{format_percent(criticality_share)}** dos incidentes. Já o status de resposta
    mais comum foi **{dominant_status['status_resposta']}**, representando
    **{format_percent(status_share)}** dos registros. Esses dois indicadores são importantes
    porque conectam volume de ataques com capacidade de resposta e priorização de
    risco.
    """
)

st.subheader("Conclusão executiva")
st.markdown(
    f"""
    A análise mostra que a estratégia de segurança deve priorizar três frentes:
    **redução da exposição**, **resposta mais rápida** e **monitoramento contínuo**.
    Como **{top_attack['tipo_ataque']}** aparece como a ameaça mais frequente, a
    organização deve direcionar controles, campanhas de conscientização, regras de
    detecção e planos de resposta para esse tipo de ataque. Ao mesmo tempo, a
    recorrência de **{top_vulnerability['vulnerabilidade']}** indica que a mitigação
    de vulnerabilidades não deve ser tratada apenas de forma reativa, mas como um
    processo contínuo de governança.

    O setor **{top_sector['setor']}** e a região **{top_region['regiao']}** devem
    receber atenção especial, pois concentram a maior parte dos incidentes no recorte
    selecionado. Isso pode envolver reforço de políticas de acesso, revisão de
    infraestrutura, priorização de auditorias, simulações de incidentes e melhoria
    dos procedimentos de recuperação. O impacto financeiro total de
    **{format_currency_markdown(kpis['impacto_total'])}** reforça que os ataques digitais têm
    efeito direto sobre custos, continuidade operacional e reputação.

    Como recomendação prática, o painel deve ser usado para acompanhar periodicamente
    os meses críticos, comparar setores e regiões, observar mudanças no perfil de
    ataques e medir se as ações de segurança reduzem o volume de incidentes, o tempo
    de recuperação e o impacto financeiro. Dessa forma, o dashboard deixa de ser
    apenas uma visualização descritiva e passa a apoiar decisões de priorização,
    prevenção e resposta a riscos cibernéticos.
    """
)
