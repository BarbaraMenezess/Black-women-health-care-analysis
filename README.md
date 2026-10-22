# 🌿 Territorial & Intersectional Health Disparities Dashboard

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-1F382B?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-D97757?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-1F382B?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-Visuals-8A9A86?style=for-the-badge&logo=python&logoColor=white)](https://seaborn.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## 🎯 Project Motivation & Scientific Context

This project was developed as an intersectional analytical tool to investigate public health disparities, social determinants of health (SDH), and structural inequalities. It bridges technical data science workflows with critical epidemiological research inspired by frameworks from **Cidacs/Fiocruz**.

The core objective is to analyze conditional probabilities of HIV vulnerability and severe health outcomes among women, comparing distinct geographical contexts (**Urban Centers, Peripheries, and Rural Areas**). 

### 📚 Scientific Foundation & Inspiration
The structure of this analysis is deeply anchored in public health insights regarding intersectionality (race, gender, education, and geography):
> *“Structural vulnerabilities—such as race, lower educational attainment, and income—drastically compound health risks, resulting in a disproportionate impact on marginalized populations.”* 
> 
> **Reference Study:** [Cidacs/Fiocruz — Mulheres negras com baixa escolaridade e menor renda têm risco sete vezes maior de morrer de Aids](https://cidacs.bahia.fiocruz.br/2026/10/mulheres-negras-com-baixa-escolaridade-e-menor-renda-tem-risco-sete-vezes-maior-de-morrer-de-aids/).

---

## 🛠️ Tech Stack & Libraries Used

The application is built using a classic aesthetic (off-white background and organic color palettes) mimicking academic epidemiological reports:

* **Language:** Python 3.10+
* **Web Framework:** [Streamlit](https://streamlit.io/) (for building the interactive web dashboard)
* **Data Manipulation & Triage:** [Pandas](https://pandas.pydata.org/) (for conditional filtering, data cleaning, and probability calculations)
* **Data Visualization:** [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) (for organic, publication-ready comparative charts)
* **Testing Framework:** [Pytest](https://docs.pytest.org/) (for unit and data integration testing)
* **Environment Control:** Git & GitHub

---

## 📂 Project Structure

```text
Health_analysis/
│
├── app.py                 # Main Streamlit interactive web dashboard script
├── requirements.txt       # Python dependencies configuration
├── README.md              # Project documentation and portfolio overview
└── tests/                 # Dedicated directory for test scripts
    └── test_app.py        # Automated unit tests for data integrity and filters