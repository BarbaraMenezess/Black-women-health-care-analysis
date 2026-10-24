
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# Configure project paths
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

RACE_FILE = RESULTS_DIR / "female_mortality_by_race_2023_2025.csv"
SUMMARY_FILE = RESULTS_DIR / "female_mortality_summary_2023_2025.csv"


# Configure the dashboard page
st.set_page_config(
    page_title="Black Women's Health Analysis",
    page_icon="📊",
    layout="wide",
)


# Apply a clean visual style
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FDFBF7;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E8E3DA;
        padding: 18px;
        border-radius: 12px;
    }

    h1, h2, h3 {
        color: #243746;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    """Load the aggregated CSV files."""

    race_df = pd.read_csv(RACE_FILE)
    summary_df = pd.read_csv(SUMMARY_FILE)

    race_df["Year"] = race_df["Year"].astype(int)
    summary_df["Year"] = summary_df["Year"].astype(int)

    return race_df, summary_df


# Check whether the result files exist
if not RACE_FILE.exists() or not SUMMARY_FILE.exists():
    st.error(
        "Result files were not found. Run `python app.py` first."
    )
    st.stop()


race_df, summary_df = load_data()


# Dashboard heading
st.title("Black Women's Health Analysis")

st.markdown(
    """
    ### Female mortality in Brazil

    Exploring recorded female deaths by race/color, with a focus on
    Black women (Preta + Parda).
    """
)

st.caption(
    "Comparison period: January–July 2023 and January–July 2025."
)


# Sidebar filters
st.sidebar.header("Filters")

available_years = sorted(
    summary_df["Year"].unique().tolist()
)

selected_years = st.sidebar.multiselect(
    "Select years",
    options=available_years,
    default=available_years,
)

available_races = sorted(race_df["Race"].dropna().unique())

selected_races = st.sidebar.multiselect(
    "Select race/color groups",
    options=available_races,
    default=available_races,
)


# Apply filters
filtered_summary = summary_df[
    summary_df["Year"].isin(selected_years)
].copy()

filtered_race = race_df[
    race_df["Year"].isin(selected_years)
    & race_df["Race"].isin(selected_races)
].copy()


if filtered_summary.empty:
    st.warning("Select at least one year to display the indicators.")
    st.stop()


# Calculate dashboard indicators
total_female_deaths = int(filtered_summary["FemaleDeaths"].sum())

total_black_women_deaths = int(
    filtered_summary["BlackWomenDeaths"].sum()
)

overall_black_percentage = (
    total_black_women_deaths / total_female_deaths * 100
    if total_female_deaths
    else 0
)


# KPI cards
st.subheader("Key indicators")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Recorded female deaths",
    f"{total_female_deaths:,}",
)

col2.metric(
    "Deaths among Black women",
    f"{total_black_women_deaths:,}",
)

col3.metric(
    "Black women's share",
    f"{overall_black_percentage:.2f}%",
)


# Charts
st.divider()
st.subheader("Mortality by race/color")

if filtered_race.empty:
    st.info("Select at least one race/color group.")
else:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        percentage_chart = px.bar(
            filtered_race,
            x="Race",
            y="Percentage",
            color="Year",
            barmode="group",
            text="Percentage",
            title="Share of Female Deaths by Race/Color",
            labels={
                "Race": "Race/Color",
                "Percentage": "Percentage (%)",
                "Year": "Year",
            },
        )

        percentage_chart.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
        )

        percentage_chart.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FDFBF7",
            yaxis_title="Percentage (%)",
            xaxis_title="",
            legend_title="Year",
        )

        st.plotly_chart(
            percentage_chart,
            use_container_width=True,
        )

    with chart_col2:
        count_chart = px.bar(
            filtered_race,
            x="Race",
            y="Deaths",
            color="Year",
            barmode="group",
            title="Recorded Female Deaths by Race/Color",
            labels={
                "Race": "Race/Color",
                "Deaths": "Number of deaths",
                "Year": "Year",
            },
        )

        count_chart.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FDFBF7",
            xaxis_title="",
            yaxis_title="Number of deaths",
            legend_title="Year",
        )

        st.plotly_chart(
            count_chart,
            use_container_width=True,
        )


# Black women's comparison
st.divider()
st.subheader("Focus: Black women (Preta + Parda)")

black_col1, black_col2 = st.columns(2)

with black_col1:
    black_count_chart = px.bar(
        filtered_summary,
        x="Year",
        y="BlackWomenDeaths",
        text="BlackWomenDeaths",
        title="Recorded Deaths Among Black Women",
        labels={
            "Year": "Year",
            "BlackWomenDeaths": "Number of deaths",
        },
    )

    black_count_chart.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FDFBF7",
        xaxis_title="",
        yaxis_title="Number of deaths",
    )

    st.plotly_chart(
        black_count_chart,
        use_container_width=True,
    )

with black_col2:
    black_share_chart = px.bar(
        filtered_summary,
        x="Year",
        y="BlackWomenPercentage",
        text="BlackWomenPercentage",
        title="Black Women's Share of Female Deaths",
        labels={
            "Year": "Year",
            "BlackWomenPercentage": "Percentage (%)",
        },
    )

    black_share_chart.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )

    black_share_chart.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FDFBF7",
        xaxis_title="",
        yaxis_title="Percentage (%)",
    )

    st.plotly_chart(
        black_share_chart,
        use_container_width=True,
    )


# Display the underlying data
with st.expander("View data tables"):
    st.markdown("**Summary by year**")
    st.dataframe(filtered_summary, use_container_width=True)

    st.markdown("**Distribution by race/color**")
    st.dataframe(filtered_race, use_container_width=True)


# Methodology and limitations
st.divider()
st.subheader("Methodology and limitations")

st.markdown(
    """
    - The analysis uses recorded deaths from the Brazilian Mortality
      Information System (SIM) files supplied for this project.
    - Only records with the female sex code are included.
    - Black women are defined here as records classified as
      **Preta (code 2) or Parda (code 4)**.
    - Both years are restricted to January through July to align the
      comparison periods.
    - Percentages represent each race/color group's share of recorded
      female deaths, not population mortality rates.
    - Differences in population size, age structure, data completeness,
      and reporting may affect comparisons.
    """
)

st.caption(
    "Research dashboard for descriptive analysis. "
    "Interpret findings in light of the data's limitations."
)