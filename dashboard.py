  from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# Page configuration and paths
# ---------------------------------------------------------
st.set_page_config(
    page_title="Black Women's Health Analysis",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

RACE_FILE = RESULTS_DIR / "female_mortality_by_race_2023_2025.csv"
SUMMARY_FILE = RESULTS_DIR / "female_mortality_summary_2023_2025.csv"

NAVY = "#243746"
TERRACOTTA = "#B07D62"
SAGE = "#7D9B8A"
GOLD = "#D6B779"
LILAC = "#9A8FBF"
ROSE = "#C98282"
INK = "#29343B"
MUTED = "#6B7280"
PAPER = "#FDFBF7"
SIDEBAR = "#F5F1E9"
BORDER = "#E8E3DA"

RACE_COLORS = {
    "White": NAVY,
    "Black (Preta)": TERRACOTTA,
    "Brown (Parda)": SAGE,
    "Asian (Amarela)": GOLD,
    "Indigenous": LILAC,
    "Ignored": ROSE,
    "Missing": "#9CA3AF",
    "Unspecified/other code": "#B8A99A",
}


# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background: {PAPER};
        color: {INK};
    }}
    [data-testid="stSidebar"] {{
        background: {SIDEBAR};
        border-right: 1px solid {BORDER};
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 1.5rem;
    }}
    h1, h2, h3 {{
        color: {NAVY};
        letter-spacing: -0.025em;
    }}
    h1 {{
        font-weight: 700;
    }}
    [data-testid="stMetric"] {{
        background: #FFFFFF;
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(36, 55, 70, 0.035);
    }}
    [data-testid="stMetricLabel"] {{
        color: {MUTED};
        font-size: 0.83rem;
    }}
    [data-testid="stMetricValue"] {{
        color: {NAVY};
        font-weight: 700;
    }}
    div[data-testid="stExpander"] {{
        background: #FFFFFF;
        border: 1px solid {BORDER};
        border-radius: 12px;
    }}
    div.stButton > button {{
        border-radius: 9px;
        border: 1px solid {BORDER};
    }}
    .eyebrow {{
        color: {TERRACOTTA};
        text-transform: uppercase;
        letter-spacing: 0.16em;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }}
    .subtitle {{
        color: {MUTED};
        font-size: 1rem;
        line-height: 1.65;
        max-width: 900px;
    }}
    .year-card {{
        background: #FFFFFF;
        border: 1px solid {BORDER};
        border-radius: 13px;
        padding: 13px 16px;
        min-height: 74px;
    }}
    .year-label {{
        color: {MUTED};
        text-transform: uppercase;
        letter-spacing: 0.11em;
        font-size: 0.68rem;
        font-weight: 700;
    }}
    .year-value {{
        color: {NAVY};
        font-size: 1.55rem;
        font-weight: 700;
        line-height: 1.3;
    }}
    .small-note {{
        color: {MUTED};
        font-size: 0.82rem;
        line-height: 1.5;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Load and validate datasets
# ---------------------------------------------------------
@st.cache_data
def load_data(race_path: str, summary_path: str):
    race_data = pd.read_csv(race_path)
    summary_data = pd.read_csv(summary_path)

    race_data["Year"] = pd.to_numeric(
        race_data["Year"], errors="coerce"
    ).astype("Int64")
    summary_data["Year"] = pd.to_numeric(
        summary_data["Year"], errors="coerce"
    ).astype("Int64")

    race_data["Deaths"] = pd.to_numeric(
        race_data["Deaths"], errors="coerce"
    ).fillna(0)
    race_data["Percentage"] = pd.to_numeric(
        race_data["Percentage"], errors="coerce"
    ).fillna(0)

    numeric_summary_columns = [
        "RecordsInPeriod",
        "FemaleDeaths",
        "BlackWomenDeaths",
        "BlackWomenPercentage",
    ]
    for column in numeric_summary_columns:
        if column in summary_data.columns:
            summary_data[column] = pd.to_numeric(
                summary_data[column], errors="coerce"
            ).fillna(0)

    return race_data, summary_data


if not RACE_FILE.exists() or not SUMMARY_FILE.exists():
    st.error(
        "The analysis files were not found. Please check that these files "
        "exist inside the `results` folder:\n\n"
        "- `female_mortality_by_race_2023_2025.csv`\n"
        "- `female_mortality_summary_2023_2025.csv`"
    )
    st.stop()

try:
    race_df, summary_df = load_data(str(RACE_FILE), str(SUMMARY_FILE))
except Exception as error:
    st.error(f"Unable to read the analysis files: {error}")
    st.stop()

required_race_columns = {"Year", "Race", "Deaths", "Percentage"}
required_summary_columns = {
    "Year", "FemaleDeaths", "BlackWomenDeaths", "BlackWomenPercentage"
}

if not required_race_columns.issubset(race_df.columns):
    st.error(
        "The race/color CSV is missing required columns. Expected: "
        + ", ".join(sorted(required_race_columns))
    )
    st.stop()

if not required_summary_columns.issubset(summary_df.columns):
    st.error(
        "The summary CSV is missing required columns. Expected: "
        + ", ".join(sorted(required_summary_columns))
    )
    st.stop()

available_years = sorted(
    set(race_df["Year"].dropna().astype(int))
    & set(summary_df["Year"].dropna().astype(int))
)

if not available_years:
    st.error("No matching years were found in the two datasets.")
    st.stop()


# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        f"""
        <div style="color:{NAVY};font-size:1.2rem;font-weight:750;">
            Research filters
        </div>
        <div class="small-note" style="margin-top:5px;margin-bottom:20px;">
            Choose the years and race/color groups to explore.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="eyebrow" style="color:{MUTED};">Comparison years</div>',
        unsafe_allow_html=True,
    )

    default_years = [
        year for year in [2023, 2025] if year in available_years
    ] or available_years

    # The bordered year cards make the filter area feel more deliberate;
    # the multiselect keeps the selection fully accessible and interactive.
    year_columns = st.columns(2)
    for index, year in enumerate(available_years):
        with year_columns[index % 2]:
            st.markdown(
                f"""
                <div class="year-card">
                    <div class="year-label">Year</div>
                    <div class="year-value">{year}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    selected_years = st.multiselect(
        "Select years",
        options=available_years,
        default=default_years,
        format_func=lambda year: str(year),
        help="Select one or both years. The dashboard updates automatically.",
    )

    st.markdown("---")
    st.markdown(
        '<div class="eyebrow" style="color:#6B7280;">Race / color</div>',
        unsafe_allow_html=True,
    )

    available_races = sorted(race_df["Race"].dropna().astype(str).unique())
    selected_races = st.multiselect(
        "Select race/color groups",
        options=available_races,
        default=available_races,
    )

    st.markdown("---")
    st.caption("Period covered: January–July")
    st.caption("Source: Brazilian Mortality Information System (SIM)")


if not selected_years:
    st.info("Select at least one year in the sidebar to display the analysis.")
    st.stop()

if not selected_races:
    st.info("Select at least one race/color group in the sidebar.")
    st.stop()


# ---------------------------------------------------------
# Filter datasets
# ---------------------------------------------------------
filtered_race = race_df[
    race_df["Year"].isin(selected_years)
    & race_df["Race"].isin(selected_races)
].copy()

filtered_summary = summary_df[
    summary_df["Year"].isin(selected_years)
].copy()

all_race_for_selected_years = race_df[
    race_df["Year"].isin(selected_years)
].copy()


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown(
    '<div class="eyebrow">Public health · Brazil · Descriptive analysis</div>',
    unsafe_allow_html=True,
)
st.title("Black Women's Health Analysis")
st.markdown(
    """
    <div class="subtitle">
        A descriptive comparison of recorded female deaths by race/color
        in Brazil, comparing January–July 2023 and January–July 2025.
        The analysis highlights records for Black women, defined here as
        women classified as <em>Preta</em> or <em>Parda</em>.
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")


# ---------------------------------------------------------
# KPI cards
# ---------------------------------------------------------
total_female_deaths = int(filtered_summary["FemaleDeaths"].sum())
total_black_women_deaths = int(filtered_summary["BlackWomenDeaths"].sum())

overall_black_percentage = (
    total_black_women_deaths / total_female_deaths * 100
    if total_female_deaths
    else 0
)

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(
    "Recorded female deaths",
    f"{total_female_deaths:,}",
    help="Total female deaths recorded in the selected years, January–July.",
)
kpi2.metric(
    "Deaths among Black women",
    f"{total_black_women_deaths:,}",
    help="Records classified as Preta or Parda in the selected years.",
)
kpi3.metric(
    "Black women's share",
    f"{overall_black_percentage:.2f}%",
    help="Share of recorded female deaths, not a population mortality rate.",
)

st.caption(
    "Counts and percentages describe recorded deaths only; they do not "
    "measure an individual's mortality risk."
)
st.divider()


# ---------------------------------------------------------
# Elegant year comparison cards
# ---------------------------------------------------------
st.subheader("Selected comparison period")
year_card_columns = st.columns(max(1, len(selected_years)))
for column, year in zip(year_card_columns, selected_years):
    year_row = summary_df[summary_df["Year"] == year]
    if year_row.empty:
        continue

    row = year_row.iloc[0]
    with column:
        st.markdown(
            f"""
            <div class="year-card" style="padding:18px 20px;">
                <div class="year-label">January–July</div>
                <div class="year-value">{year}</div>
                <div style="color:{MUTED};font-size:0.86rem;margin-top:7px;">
                    {int(row["FemaleDeaths"]):,} recorded female deaths
                </div>
                <div style="color:{TERRACOTTA};font-size:0.9rem;
                            font-weight:650;margin-top:3px;">
                    {float(row["BlackWomenPercentage"]):.2f}% Black women
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")


# ---------------------------------------------------------
# Chart 1: recorded deaths by race/color and year
# ---------------------------------------------------------
st.subheader("Recorded female deaths by race/color")

yearly_deaths = (
    filtered_race.groupby(["Year", "Race"], as_index=False)["Deaths"]
    .sum()
)
yearly_deaths["Year"] = yearly_deaths["Year"].astype(str)

if yearly_deaths.empty:
    st.warning("No records match the selected filters.")
else:
    fig_deaths = px.bar(
        yearly_deaths,
        x="Race",
        y="Deaths",
        color="Race",
        facet_col="Year" if len(selected_years) > 1 else None,
        title=None,
        labels={
            "Race": "Race/color",
            "Deaths": "Recorded deaths",
            "Year": "Year",
        },
        color_discrete_map=RACE_COLORS,
        text_auto=".2s",
    )
    fig_deaths.update_layout(
        paper_bgcolor=PAPER,
        plot_bgcolor="#FFFFFF",
        font=dict(color=INK, family="Arial, sans-serif"),
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False,
        xaxis_title="Race/color",
        yaxis_title="Recorded deaths",
        bargap=0.32,
    )
    fig_deaths.update_xaxes(
        showgrid=False,
        tickangle=-25,
        linecolor=BORDER,
    )
    fig_deaths.update_yaxes(
        gridcolor="#EEEAE3",
        zeroline=False,
    )
    st.plotly_chart(fig_deaths, use_container_width=True)


# ---------------------------------------------------------
# Chart 2: share of recorded female deaths
# ---------------------------------------------------------
chart_left, chart_right = st.columns([1.15, 0.85])

with chart_left:
    st.subheader("Share of recorded deaths")
    share_df = filtered_race.copy()
    share_df["Year"] = share_df["Year"].astype(str)

    if share_df.empty:
        st.info("No percentage data are available for these filters.")
    else:
        fig_share = px.bar(
            share_df,
            x="Race",
            y="Percentage",
            color="Race",
            facet_col="Year" if len(selected_years) > 1 else None,
            labels={
                "Race": "Race/color",
                "Percentage": "Share of recorded female deaths (%)",
                "Year": "Year",
            },
            color_discrete_map=RACE_COLORS,
            text=share_df["Percentage"].map(lambda value: f"{value:.1f}%"),
        )
        fig_share.update_layout(
            paper_bgcolor=PAPER,
            plot_bgcolor="#FFFFFF",
            font=dict(color=INK, family="Arial, sans-serif"),
            margin=dict(l=8, r=8, t=15, b=10),
            showlegend=False,
            bargap=0.32,
        )
        fig_share.update_xaxes(
            showgrid=False,
            tickangle=-25,
            linecolor=BORDER,
        )
        fig_share.update_yaxes(
            title="Percentage (%)",
            gridcolor="#EEEAE3",
            rangemode="tozero",
        )
        st.plotly_chart(fig_share, use_container_width=True)

with chart_right:
    st.subheader("Black women's share by year")
    black_share_df = filtered_summary[
        ["Year", "BlackWomenPercentage"]
    ].copy()
    black_share_df["Year"] = black_share_df["Year"].astype(str)
    black_share_df = black_share_df.rename(
        columns={"BlackWomenPercentage": "Percentage"}
    )

    fig_black = px.bar(
        black_share_df,
        x="Year",
        y="Percentage",
        text=black_share_df["Percentage"].map(lambda value: f"{value:.2f}%"),
        labels={
            "Year": "Year",
            "Percentage": "Share (%)",
        },
        color="Year",
        color_discrete_sequence=[NAVY, TERRACOTTA],
    )
    fig_black.update_layout(
        paper_bgcolor=PAPER,
        plot_bgcolor="#FFFFFF",
        font=dict(color=INK, family="Arial, sans-serif"),
        margin=dict(l=8, r=8, t=15, b=10),
        showlegend=False,
    )
    fig_black.update_xaxes(showgrid=False, linecolor=BORDER)
    fig_black.update_yaxes(
        gridcolor="#EEEAE3",
        rangemode="tozero",
        ticksuffix="%",
    )
    st.plotly_chart(fig_black, use_container_width=True)


# ---------------------------------------------------------
# Data table
# ---------------------------------------------------------
st.divider()
st.subheader("Data table")
st.markdown(
    "Counts and percentages for the selected years and race/color groups."
)

table_df = filtered_race.sort_values(
    ["Year", "Deaths"], ascending=[True, False]
).copy()
table_df["Percentage"] = table_df["Percentage"].map(
    lambda value: f"{value:.2f}%"
)
table_df["Deaths"] = table_df["Deaths"].map(lambda value: f"{int(value):,}")
st.dataframe(
    table_df[["Year", "Race", "Deaths", "Percentage"]],
    use_container_width=True,
    hide_index=True,
)

with st.expander("View summary totals by year"):
    summary_view = filtered_summary[
        [
            "Year",
            "FemaleDeaths",
            "BlackWomenDeaths",
            "BlackWomenPercentage",
        ]
    ].copy()
    summary_view = summary_view.rename(
        columns={
            "FemaleDeaths": "Recorded female deaths",
            "BlackWomenDeaths": "Deaths among Black women",
            "BlackWomenPercentage": "Black women's share (%)",
        }
    )
    st.dataframe(summary_view, use_container_width=True, hide_index=True)


# ---------------------------------------------------------
# Research conclusion and scientific evidence
# ---------------------------------------------------------
st.divider()
st.subheader("Research conclusion & scientific evidence")

st.markdown(
    """
    ### Key findings

    This descriptive analysis examines recorded female deaths in Brazil
    by race/color, focusing on Black women classified as **Preta** or
    **Parda**.

    The dashboard compares January–July 2023 with January–July 2025.
    The results describe the distribution of recorded deaths across
    race/color groups and the share represented by Black women.

    These percentages are **not population mortality rates** and should
    not be interpreted as direct measures of individual mortality risk.

    ### Scientific context

    Research from Cidacs/Fiocruz Bahia highlights how race, education,
    and socioeconomic conditions can intersect and contribute to
    inequalities in health outcomes.

    A study involving 28.3 million Brazilians reported substantially
    higher AIDS-related mortality among Black women with lower
    educational attainment and income compared with more advantaged
    White women. This study provides relevant context, but its
    disease-specific findings cannot be directly generalized to
    all-cause female mortality in this dashboard.
    """
)

st.markdown(
    """
    **Reference 1 — Cidacs/Fiocruz Bahia**

    [Black women with lower education and income face a sevenfold
    higher risk of AIDS-related death](https://cidacs.bahia.fiocruz.br/2026/10/mulheres-negras-com-baixa-escolaridade-e-menor-renda-tem-risco-sete-vezes-maior-de-morrer-de-aids/)
    """
)

st.markdown(
    """
    **Reference 2 — Radis / Fiocruz**

    [The health of Black people remains neglected](https://radis.ensp.fiocruz.br/reportagem/equidade/saude-das-pessoas-negras-ainda-e-negligenciada/)

    This report discusses racial health inequalities and the
    implementation of Brazil's National Policy for Comprehensive
    Health of the Black Population.
    """
)

st.markdown(
    """
    **Additional research resource**

    [Observatory of Black Population Health — Fiocruz](https://observatoriospn.ensp.fiocruz.br/)
    """
)

st.info(
    "These references provide scientific context for understanding racial "
    "inequalities in health. They do not establish that race alone causes "
    "the patterns observed in this dataset."
)


# ---------------------------------------------------------
# Final report
# ---------------------------------------------------------
st.divider()
st.subheader("Final report")

with st.expander("Executive summary", expanded=True):
    st.markdown(
        f"""
        This project describes female mortality records by race/color
        in Brazil, comparing January–July 2023 and January–July 2025.

        - **Female deaths recorded in the selected years:** {total_female_deaths:,}
        - **Deaths recorded among Black women (Preta + Parda):** {total_black_women_deaths:,}
        - **Black women's share of recorded female deaths:** {overall_black_percentage:.2f}%

        These totals reflect the years selected in the sidebar. They
        represent counts and proportions of recorded deaths, not
        population mortality rates.
        """
    )

with st.expander("Methodology"):
    st.markdown(
        """
        1. Read the supplied Brazilian Mortality Information System (SIM)
           summary files for 2023 and 2025.
        2. Restrict both datasets to January through July, as prepared
           in the source analysis.
        3. Include records with the female sex code.
        4. Group records by the available race/color classification.
        5. Define Black women for this analysis as Preta (code 2) plus
           Parda (code 4).
        6. Calculate counts and each group's percentage of recorded
           female deaths.
        """
    )

with st.expander("Limitations and interpretation"):
    st.markdown(
        """
        - The analysis is descriptive and does not establish causation.
        - Percentages use recorded female deaths as the denominator,
          not the total female population.
        - Population size and age structure are not controlled.
        - Missing, ignored, or inconsistently recorded race/color
          information may affect the distribution.
        - Data completeness and reporting practices may differ.
        - Findings from studies focused on AIDS or another specific
          cause of death should not be generalized directly to
          all-cause mortality.
        - Population denominators and age-standardized mortality rates
          would be needed to compare mortality risks.
        """
    )

st.caption(
    "Black Women's Health Analysis | Descriptive research dashboard | "
    "Sources: Brazilian SIM records and linked Fiocruz resources."
)
