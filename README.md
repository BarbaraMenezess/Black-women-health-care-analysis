# 🌿 Black Women's Health Analysis Dashboard

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-1F382B?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive_App-D97757?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-1F382B?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Data_Visualization-8A9A86?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## 🎯 Project Motivation & Scientific Context

**Black Women's Health Analysis** is a public health data analysis project designed to explore racial disparities in recorded female mortality in Brazil, with a particular focus on Black women.

The project uses real-world mortality records from Brazil's **Mortality Information System (Sistema de Informações sobre Mortalidade — SIM)**, maintained by the Brazilian Ministry of Health.

The analysis compares records from January through July 2023 and January through July 2025, examining the distribution of recorded female deaths by race/color and highlighting deaths among women classified as **Preta (Black) or Parda (Brown)**.

The project combines data processing, descriptive statistics, interactive visualizations, and scientific references to support a more informed discussion of racial inequalities in health.

### 📚 Scientific Foundation & Inspiration

This project is informed by research on racial health inequalities, social determinants of health, and structural barriers to equitable healthcare.

- **Cidacs/Fiocruz Bahia:** Research on the intersection of race, education, income, and AIDS-related mortality among Black women.
- **Radis/Fiocruz:** Reporting and analysis on inequalities in healthcare and the implementation of Brazil's National Policy for Comprehensive Health of the Black Population.
- **Observatory of Black Population Health — Fiocruz:** A research resource for investigating racial inequalities in health.

**Selected reference:** [Cidacs/Fiocruz Bahia — Black women with lower education and income face a sevenfold higher risk of AIDS-related death](https://cidacs.bahia.fiocruz.br/2026/10/mulheres-negras-com-baixa-escolaridade-e-menor-renda-tem-risco-sete-vezes-maior-de-morrer-de-aids/).

These studies provide scientific context for understanding racial health inequalities. Findings focused on a specific disease, such as AIDS, should not be generalized directly to all-cause mortality.

---

## 🗄️ Data Sources

The primary data source is the Brazilian Ministry of Health's **Sistema de Informações sobre Mortalidade (SIM)**.

### Official databases

- **[SIM — Open Data SUS](https://dadosabertos.saude.gov.br/dataset/sim):** Official dataset catalog containing mortality data and downloadable resources.
- **[General Mortality Records — 2023](https://dadosabertos.saude.gov.br/dataset/sim/resource/2a7269c5-91b2-4569-8b36-3ab775328555):** Official 2023 general mortality dataset.
- **[Brazilian Ministry of Health — Mortality Data](https://www.gov.br/saude/pt-br/acesso-a-informacao/sic/dados-em-transparencia-ativa/svsa/mortalidade):** Information about mortality data, access methods, and data availability.
- **[Cidacs/Fiocruz Bahia](https://cidacs.bahia.fiocruz.br/2026/10/mulheres-negras-com-baixa-escolaridade-e-menor-renda-tem-risco-sete-vezes-maior-de-morrer-de-aids/):** Scientific context on racial and socioeconomic inequalities in health.

The analysis uses the local mortality data files `Mortalidade_Geral_2023.csv` and `Mortalidade_Geral_2025.csv`. The 2025 data are preliminary and may be revised by the Ministry of Health.

The files are processed locally to generate aggregated analytical outputs for the dashboard.

---

## 📊 Analytical Scope & Key Indicators

The dashboard focuses on descriptive analysis of recorded female mortality.

### Main indicators

- **Recorded female deaths:** Total records classified as female within the selected comparison period.
- **Deaths among Black women:** Records classified as Preta or Parda.
- **Black women's share of recorded female deaths:** The proportion of recorded female deaths classified as Preta or Parda.
- **Distribution by race/color:** Counts and percentages for the available race/color categories.
- **Year comparison:** Comparison between January–July 2023 and January–July 2025.

### Race/color classification

The analysis uses the race/color codes provided in the mortality records:

| Code | Category |
|---|---|
| 1 | White (Branca) |
| 2 | Black (Preta) |
| 3 | Asian (Amarela) |
| 4 | Brown (Parda) |
| 5 | Indigenous (Indígena) |
| 9 | Ignored (Ignorado) |
| 0 | Other or unspecified code |

For the purposes of this project, **Black women are defined as records classified as Preta (code 2) or Parda (code 4)**.

### Important interpretation note

The percentages shown in this dashboard represent each group's share of recorded female deaths. They are **not population-based mortality rates** and should not be interpreted as individual mortality risks.

A more comprehensive mortality-rate analysis would require appropriate population denominators and additional adjustments, including age standardization where relevant.

---

## 🛠️ Tech Stack & Libraries Used

The application uses a classic visual style, with an off-white background and muted, organic colors inspired by academic research reports.

- **Language:** Python
- **Web framework:** [Streamlit](https://streamlit.io/) — interactive dashboard development.
- **Data manipulation:** [Pandas](https://pandas.pydata.org/) — data loading, cleaning, filtering, aggregation, and calculations.
- **Data visualization:** [Plotly Express](https://plotly.com/python/plotly-express/) — interactive comparative charts.
- **Testing framework:** [Pytest](https://docs.pytest.org/) — automated testing.
- **Version control:** Git and GitHub.
- **Deployment:** [Streamlit Community Cloud](https://share.streamlit.io/).

---

## 📈 Dashboard Features

- Interactive year filters.
- Race/color category filters.
- Key performance indicators for recorded female deaths.
- Comparative bar charts showing counts and percentages by race/color.
- Dedicated visualizations for recorded deaths among Black women.
- Data tables for reviewing aggregated results.
- Scientific references and research context.
- Methodology, limitations, and interpretation notes.
- An executive summary based on the selected years.

The dashboard is intended to make descriptive public health data more accessible while maintaining transparency about the scope and limitations of the analysis.

---

## 📂 Project Structure

```text
Black Womens Health_analysis/
│
├── app.py
├── dashboard.py
├── health_bias_analysis.py
├── requirements.txt
├── README.md
├── test_app.py
│
└── results/
    ├── female_mortality_by_race_2023_2025.csv
    └── female_mortality_summary_2023_2025.csv
```

- `app.py` — application entry point; its role depends on the current project configuration.
- `dashboard.py` — interactive dashboard interface, charts, filters, and research sections.
- `health_bias_analysis.py` — mortality data processing and analytical calculations.
- `test_app.py` — automated tests.
- `requirements.txt` — Python dependencies.
- `results/` — aggregated CSV outputs used by the dashboard.

The dashboard requires the aggregated output files to be available in the `results/` directory.

---

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/BarbaraMenezess/Black-women-health-care-analysis.git
cd Black-women-health-care-analysis
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the data

Obtain the mortality files from the official SIM data catalog and place the required files in the project directory according to the paths configured in the analysis script.

Run the processing script to generate the aggregated results. The exact command depends on the current implementation of `health_bias_analysis.py` and `app.py`.

### 5. Launch the dashboard

Run Streamlit using the entry-point file configured for the dashboard:

```bash
streamlit run dashboard.py
```

If the deployed application uses `app.py` as its main file, make sure the entry point and the local execution command are consistent before deployment.

---

## 🔬 Methodology

1. Load the available Brazilian SIM mortality records.
2. Parse the death-date fields and standardize the relevant variables.
3. Restrict both comparison periods to January through July.
4. Select records classified as female.
5. Group the records by the available race/color categories.
6. Define Black women as the combined Preta and Parda categories.
7. Calculate death counts and the percentage distribution by race/color.
8. Generate aggregated CSV files for use in the dashboard.
9. Present the results through interactive charts, indicators, and summary tables.

---

## ⚠️ Limitations & Responsible Interpretation

- The analysis is descriptive and does not establish causation.
- The number of recorded deaths is not equivalent to a population-based mortality rate.
- Population size and age structure are not controlled in the current analysis.
- Race/color information may be missing, ignored, or inconsistently recorded.
- The 2025 records are preliminary and may change as the database is updated.
- Differences in data completeness and reporting may affect comparisons.
- Results from disease-specific studies should not be directly generalized to all-cause mortality.
- The analysis should not be interpreted as evidence that race alone causes a particular health outcome.

Future improvements could include population denominators, age-standardized mortality rates, analysis by cause of death, and additional geographic and socioeconomic variables where suitable data are available.

---

## 📄 Research Conclusion

This project demonstrates how official public health records can be used to examine the distribution of recorded female deaths across race/color groups in Brazil.

By focusing on women classified as Preta or Parda, the dashboard highlights an important dimension of racial health equity while providing transparent calculations and methodological caveats.

The project is an exploratory analytical resource rather than a causal epidemiological study. Its findings should be interpreted alongside official documentation, population-based indicators, and peer-reviewed research.

---

## 📚 Additional References

- [Brazilian Ministry of Health — Mortality Data](https://www.gov.br/saude/pt-br/acesso-a-informacao/sic/dados-em-transparencia-ativa/svsa/mortalidade)
- [Open Data SUS — Mortality Information System (SIM)](https://dadosabertos.saude.gov.br/dataset/sim)
- [Cidacs/Fiocruz Bahia — Research on AIDS-related mortality among Black women](https://cidacs.bahia.fiocruz.br/2026/10/mulheres-negras-com-baixa-escolaridade-e-menor-renda-tem-risco-sete-vezes-maior-de-morrer-de-aids/)
- [Radis/Fiocruz — Health inequalities affecting Black people](https://radis.ensp.fiocruz.br/reportagem/equidade/saude-das-pessoas-negras-ainda-e-negligenciada/)
- [Observatory of Black Population Health — Fiocruz](https://observatoriospn.ensp.fiocruz.br/)

---

<div align="center">

**Black Women's Health Analysis**  
*Data science, public health, and racial health equity.*

</div>