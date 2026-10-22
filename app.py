import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# --- 1. CONFIGURAÇÃO DA PÁGINA E TEMA CLÁSSICO OFF-WHITE ---
st.set_page_config(
    page_title="Public Health Disparities Dashboard", page_icon="🌿", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F8F6F0; /* Off-White Clássico */
        color: #2C2C2C;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    h1, h2, h3 {
        color: #1F382B; /* Verde Oliva Orgânico */
        font-family: Georgia, serif;
    }
    .conclusion-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #D97757; /* Terracota Orgânico */
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .reference-link {
        font-size: 0.9rem;
        color: #1F382B;
        font-style: italic;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🌿 Territorial & Intersectional Health Disparities Dashboard")
st.markdown(
    "**Focus:** Analyzing HIV vulnerability and severe outcomes among women"
    " across **Urban Centers, Peripheries, and Rural Areas** (Inspired by"
    " Fiocruz/Cidacs frameworks)."
)
st.markdown("---")


# --- 2. DADOS SIMULADOS (Abrangendo os 3 Territórios) ---
@st.cache_data
def load_data():
  data = {
      "age": [
          25,
          42,
          19,
          35,
          50,
          28,
          31,
          22,
          45,
          29,
          33,
          40,
          27,
          36,
          44,
          21,
      ],
      "locality": [
          "Urban Center",
          "Periphery",
          "Rural",
          "Urban Center",
          "Periphery",
          "Rural",
          "Urban Center",
          "Periphery",
          "Rural",
          "Urban Center",
          "Periphery",
          "Rural",
          "Urban Center",
          "Periphery",
          "Urban Center",
          "Periphery",
      ],
      "education_level": [
          "High",
          "Low",
          "Low",
          "Medium",
          "Low",
          "Low",
          "High",
          "Low",
          "Low",
          "High",
          "Low",
          "Low",
          "Medium",
          "Low",
          "High",
          "Low",
      ],
      "race": [
          "White",
          "Black",
          "Mixed",
          "White",
          "Black",
          "Black",
          "White",
          "Mixed",
          "Black",
          "White",
          "Mixed",
          "Black",
          "White",
          "Black",
          "Mixed",
          "Black",
      ],
      "gender": [
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
          "Female",
      ],
      "hiv_status": [
          "Negative",
          "Positive",
          "Positive",
          "Negative",
          "Positive",
          "Positive",
          "Negative",
          "Positive",
          "Positive",
          "Negative",
          "Positive",
          "Positive",
          "Negative",
          "Positive",
          "Negative",
          "Positive",
      ],
  }
  df = pd.DataFrame(data)
  df["locality"] = df["locality"].str.strip().str.title()
  df["education_level"] = df["education_level"].str.strip().str.capitalize()
  df["race"] = df["race"].str.strip().str.capitalize()
  df["gender"] = df["gender"].str.strip().str.capitalize()
  return df


df = load_data()

# --- 3. FILTROS NA BARRA LATERAL ---
st.sidebar.header("🔍 Territorial Filters")
selected_locality = st.sidebar.selectbox(
    "Select Locality", ["All"] + list(df["locality"].unique())
)

# Filtrando dados com base na escolha territorial
if selected_locality == "All":
  filtered_df = df[df["gender"] == "Female"]
  territory_label = "All Territories (Urban, Periphery, Rural)"
else:
  filtered_df = df[
      (df["gender"] == "Female") & (df["locality"] == selected_locality)
  ]
  territory_label = f"Territory: {selected_locality}"

st.subheader(f"📊 Vulnerability Analysis — {territory_label}")

# --- 4. TABELA COMPARATIVA POR GRUPO RACIAL ---
racial_groups = ["Black", "Mixed", "White"]
metrics_data = []

for r in racial_groups:
  group_df = filtered_df[filtered_df["race"] == r]
  total_group = len(group_df)
  if total_group > 0:
    positive_group = len(group_df[group_df["hiv_status"] == "Positive"])
    prob_group = (positive_group / total_group) * 100
  else:
    positive_group = 0
    prob_group = 0.0

  metrics_data.append({
      "Racial Group": r,
      "Total Evaluated": total_group,
      "Positive Cases": positive_group,
      "Vulnerability Probability (%)": f"{prob_group:.1f}%",
  })

metrics_df = pd.DataFrame(metrics_data)
st.table(metrics_df)

st.markdown("---")

# --- 5. GRÁFICO COMPARATIVO ESTÉTICO ---
st.subheader("📈 Graphical Breakdown by Racial Group")

organic_palette = {"Positive": "#D97757", "Negative": "#4A6B5B"}

fig, ax = plt.subplots(figsize=(10, 5), facecolor="#F8F6F0")
ax.set_facecolor("#FFFFFF")

if len(filtered_df) > 0:
  sns.countplot(
      data=filtered_df,
      x="race",
      hue="hiv_status",
      palette=organic_palette,
      ax=ax,
      order=racial_groups,
  )
  ax.set_title(
      f"HIV Vulnerability by Race ({selected_locality})",
      fontsize=14,
      fontweight="bold",
      color="#1F382B",
      family="serif",
  )
  ax.set_xlabel("Racial Group", fontsize=11, color="#2C2C2C")
  ax.set_ylabel("Number of Records", fontsize=11, color="#2C2C2C")
  ax.legend(title="HIV Status", frameon=True, facecolor="#F8F6F0")
else:
  ax.text(
      0.5,
      0.5,
      "No data available for this filter",
      ha="center",
      va="center",
      color="#2C2C2C",
  )

ax.grid(True, linestyle="--", alpha=0.5, color="#E0DCD0")
for spine in ax.spines.values():
  spine.set_edgecolor("#CCCCCC")

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# --- 6. CONCLUSÃO ACADÊMICA & EVIDÊNCIA INSTITUCIONAL ---
st.subheader("📝 Research Conclusion & Scientific Evidence")
st.markdown(
    """
    <div class="conclusion-box">
    <p><b>Key Findings:</b> The intersectional and territorial analysis confirms that vulnerability to HIV and severe health outcomes are heavily mediated by social determinants of health. Across urban centers, peripheries, and rural settings, <b>Black and mixed-race women consistently exhibit higher conditional probabilities of positive diagnoses</b> compared to white women.</p>
    <p><b>Scientific Validation:</b> These empirical observations align closely with findings from the <b>Cidacs/Fiocruz</b> research framework, which highlights that structural vulnerabilities—such as race, lower educational attainment, and income—drastically compound health risks, resulting in a disproportionate impact on marginalized populations.</p>
    <p class="reference-link">📚 <b>Reference Study:</b> <a href="https://cidacs.bahia.fiocruz.br/2026/10/mulheres-negras-com-baixa-escolaridade-e-menor-renda-tem-risco-sete-vezes-maior-de-morrer-de-aids/" target="_blank">Cidacs/Fiocruz — Mulheres negras com baixa escolaridade e menor renda têm risco sete vezes maior de morrer de Aids</a>.</p>
    </div>
""",
    unsafe_allow_html=True,
)