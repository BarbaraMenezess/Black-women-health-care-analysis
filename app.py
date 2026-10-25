
from pathlib import Path

import pandas as pd


# Define project paths
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

FILE_2023 = BASE_DIR / "Mortalidade_Geral_2023.csv"
FILE_2025 = BASE_DIR / "Mortalidade_Geral_2025.csv"

CHUNK_SIZE = 100_000

# Compare the same months in both years
START_MONTH = 1
END_MONTH = 7

# Brazilian SIM race/color codes
RACE_LABELS = {
    "1": "White",
    "2": "Black (Preta)",
    "3": "Asian (Amarela)",
    "4": "Brown (Parda)",
    "5": "Indigenous",
    "9": "Ignored",
    "0": "Unspecified/other code",
}


def read_deaths(file_path, year):
    """Read mortality records in chunks using the correct file format."""

    if year == 2023:
        # The 2023 file has no header.
        # Read only the columns needed for this analysis.
        column_positions = [3, 9, 10]

        reader = pd.read_csv(
            file_path,
            sep=";",
            header=None,
            usecols=column_positions,
            dtype=str,
            chunksize=CHUNK_SIZE,
            encoding="utf-8",
            on_bad_lines="error",
        )

        column_names = ["DTOBITO", "SEXO", "RACACOR"]

        date_format = "%d-%m-%Y"

    elif year == 2025:
        # The 2025 file includes column names.
        reader = pd.read_csv(
            file_path,
            sep=";",
            dtype=str,
            chunksize=CHUNK_SIZE,
            encoding="utf-8",
            on_bad_lines="error",
        )

        column_names = ["DTOBITO", "SEXO", "RACACOR"]

        date_format = "%d%m%Y"

    else:
        raise ValueError(f"Unsupported year: {year}")

    for chunk in reader:
        if year == 2023:
            # Rename the selected columns by their position.
            chunk.columns = column_names

        else:
            # Keep only the required columns from the 2025 file.
            required_columns = ["DTOBITO", "SEXO", "RACACOR"]

            missing_columns = [
                column
                for column in required_columns
                if column not in chunk.columns
            ]

            if missing_columns:
                raise ValueError(
                    f"Missing columns in the {year} file: "
                    f"{missing_columns}"
                )

            chunk = chunk[required_columns].copy()

        # Parse death dates using the correct format for each year.
        chunk["DTOBITO"] = pd.to_datetime(
            chunk["DTOBITO"].str.strip(),
            format=date_format,
            errors="coerce",
        )

        # Keep January through July for a fair comparison.
        chunk = chunk[
            chunk["DTOBITO"].dt.month.between(
                START_MONTH, END_MONTH
            )
        ].copy()

        # Normalize race/color codes.
        chunk["RACACOR"] = (
            chunk["RACACOR"]
            .fillna("")
            .str.strip()
        )

        # Yield only records from the selected period.
        yield chunk


def analyze_file(file_path, year):
    """Calculate female mortality counts by race/color."""

    print(f"\nAnalyzing {year}...")

    race_counts = {}
    total_female_deaths = 0
    total_black_female_deaths = 0
    total_records = 0

    for chunk in read_deaths(file_path, year):
        total_records += len(chunk)

        # In the SIM dataset, code 2 represents female.
        female = chunk[chunk["SEXO"].str.strip() == "2"]

        total_female_deaths += len(female)

        # Count records by race/color among women.
        counts = female["RACACOR"].value_counts(dropna=False)

        for race_code, count in counts.items():
            race_code = str(race_code).strip()

            if race_code == "":
                race_code = "Missing"

            race_counts[race_code] = (
                race_counts.get(race_code, 0) + int(count)
            )

        # Black women = women recorded as Preta or Parda.
        black_women = female[
            female["RACACOR"].isin(["2", "4"])
        ]

        total_black_female_deaths += len(black_women)

    # Build the race/color results table.
    results = []

    for race_code, count in race_counts.items():
        if race_code == "Missing":
            race_label = "Missing"
        else:
            race_label = RACE_LABELS.get(
                race_code,
                f"Other/unknown code ({race_code})",
            )

        percentage = (
            count / total_female_deaths * 100
            if total_female_deaths
            else 0
        )

        results.append(
            {
                "Year": year,
                "RaceCode": race_code,
                "Race": race_label,
                "Deaths": count,
                "Percentage": round(percentage, 2),
            }
        )

    race_df = pd.DataFrame(results)

    if not race_df.empty:
        race_df = race_df.sort_values(
            by="Deaths",
            ascending=False,
        )

    black_percentage = (
        total_black_female_deaths / total_female_deaths * 100
        if total_female_deaths
        else 0
    )

    summary = {
        "Year": year,
        "Period": f"January-{END_MONTH:02d}",
        "RecordsInPeriod": total_records,
        "FemaleDeaths": total_female_deaths,
        "BlackWomenDeaths": total_black_female_deaths,
        "BlackWomenPercentage": round(black_percentage, 2),
    }

    print(f"Records in selected period: {total_records:,}")
    print(f"Female deaths: {total_female_deaths:,}")
    print(
        f"Black women deaths (Preta + Parda): "
        f"{total_black_female_deaths:,}"
    )
    print(f"Percentage among female deaths: {black_percentage:.2f}%")

    return race_df, summary


def main():
    """Run the analysis and save the results."""

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Check that both source files exist.
    for file_path in [FILE_2023, FILE_2025]:
        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

    all_race_results = []
    all_summaries = []

    # Analyze both years using the same January-July period.
    for year, file_path in [
        (2023, FILE_2023),
        (2025, FILE_2025),
    ]:
        race_df, summary = analyze_file(file_path, year)

        all_race_results.append(race_df)
        all_summaries.append(summary)

    # Combine the results from both years.
    combined_race_results = pd.concat(
        all_race_results,
        ignore_index=True,
    )

    summary_df = pd.DataFrame(all_summaries)

    # Save the results as CSV files.
    race_output = (
        RESULTS_DIR
        / "female_mortality_by_race_2023_2025.csv"
    )

    summary_output = (
        RESULTS_DIR
        / "female_mortality_summary_2023_2025.csv"
    )

    combined_race_results.to_csv(
        race_output,
        index=False,
        encoding="utf-8-sig",
    )

    summary_df.to_csv(
        summary_output,
        index=False,
        encoding="utf-8-sig",
    )

    print("\nAnalysis completed successfully.")
    print(f"Race results saved to: {race_output}")
    print(f"Summary saved to: {summary_output}")

    print("\nSummary comparison:")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
    # Research conclusion and scientific evidence
st.divider()
st.subheader("📝 Research Conclusion & Scientific Evidence")

st.markdown(
    """
    ### Key Findings

    This descriptive analysis examines recorded female deaths in Brazil
    by race/color, focusing on Black women classified as Preta or Parda.

    The dashboard compares January–July 2023 with January–July 2025.
    The results describe the distribution of recorded deaths across
    race/color groups and the share represented by Black women.

    These percentages are not population mortality rates and should not
    be interpreted as direct measures of individual mortality risk.

    ### Scientific Context

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
    **📚 Reference 1 — Cidacs/Fiocruz Bahia**

    [Black women with lower education and income face a sevenfold
    higher risk of AIDS-related death](https://cidacs.bahia.fiocruz.br/2026/10/mulheres-negras-com-baixa-escolaridade-e-menor-renda-tem-risco-sete-vezes-maior-de-morrer-de-aids/)
    """
)

st.markdown(
    """
    **📚 Reference 2 — Radis / Fiocruz**

    [The health of Black people remains neglected](https://radis.ensp.fiocruz.br/reportagem/equidade/saude-das-pessoas-negras-ainda-e-negligenciada/)

    This report discusses racial health inequalities and the
    implementation of Brazil's National Policy for Comprehensive
    Health of the Black Population.
    """
)

st.markdown(
    """
    **📊 Additional research resource**

    [Observatory of Black Population Health — Fiocruz](https://observatoriospn.ensp.fiocruz.br/)
    """
)

st.info(
    "Interpretation: These references provide scientific context for "
    "understanding racial inequalities in health. They do not establish "
    "that race alone causes the patterns observed in this dataset."
)


# Final report
st.divider()
st.subheader("📄 Final Report")

with st.expander("Executive summary", expanded=True):
    st.markdown(
        f"""
        This project describes female mortality records by race/color
        in Brazil, comparing January–July 2023 and January–July 2025.

        - **Female deaths recorded in the selected years:** 
          {total_female_deaths:,}
        - **Deaths recorded among Black women (Preta + Parda):**
          {total_black_women_deaths:,}
        - **Black women's share of recorded female deaths:**
          {overall_black_percentage:.2f}%

        These totals reflect the years selected in the sidebar.
        They represent counts and proportions of recorded deaths,
        not population mortality rates.
        """
    )

with st.expander("Methodology"):
    st.markdown(
        """
        1. Read the supplied Brazilian Mortality Information System
           (SIM) records for 2023 and 2025.
        2. Restrict both datasets to January through July.
        3. Include records with the female sex code.
        4. Group records by the available race/color classification.
        5. Define Black women for this analysis as Preta (code 2)
           plus Parda (code 4).
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
        - Additional population denominators and age-standardized
          mortality rates would be needed to compare mortality risks.
        """
    )

st.caption(
    "Black Women's Health Analysis | Descriptive research dashboard "
    "| Sources: Brazilian SIM records and the linked Fiocruz resources."
)