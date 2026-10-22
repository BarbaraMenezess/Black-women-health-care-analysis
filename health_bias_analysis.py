import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 1. DATASET SIMULATING PUBLIC HEALTH RECORDS (SUS / Determinants of Health)
data = {
    "age": [25, 42, 19, 35, 50, 28, 31, 22, 45, 29, 33, 40],
    "locality": [
        "Periphery",
        "Periphery",
        "Periphery",
        "Urban Center",
        "Rural",
        "Periphery",
        "Urban Center",
        "Periphery",
        "Periphery",
        "Urban Center",
        "Periphery",
        "Rural",
    ],
    "education_level": [
        "Low",
        "Low",
        "Low",
        "High",
        "Low",
        "Low",
        "High",
        "Low",
        "Low",
        "High",
        "Low",
        "Low",
    ],
    "race": [
        "Black",
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
    ],
    "gender": [
        "Female",
        "Female",
        "Female",
        "Female",
        "Male",
        "Female",
        "Female",
        "Female",
        "Female",
        "Female",
        "Female",
        "Female",
    ],
    "hiv_status": [
        "Positive",
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
    ],
}

df = pd.DataFrame(data)

# 2. DATA CLEANING & TEXT STANDARDIZATION
df["locality"] = df["locality"].str.strip().str.title()
df["education_level"] = df["education_level"].str.strip().str.capitalize()
df["race"] = df["race"].str.strip().str.capitalize()
df["gender"] = df["gender"].str.strip().str.capitalize()

# 3. TRIAGE FILTER (Women, Periphery, Low Education, Age 18-45)
selected_locality = "Periphery"
selected_education = "Low"
min_age, max_age = 18, 45

triage_filtered = df[
    (df["gender"] == "Female")
    & (df["locality"] == selected_locality)
    & (df["education_level"] == selected_education)
    & (df["age"].between(min_age, max_age))
]

# 4. PROBABILITY CALCULATION (Fiocruz Approach)
total_triage_group = len(triage_filtered)
if total_triage_group > 0:
  positive_cases = len(triage_filtered[triage_filtered["hiv_status"] == "Positive"])
  probability = (positive_cases / total_triage_group) * 100
  print("==================================================")
  print(f"📊 FIOCRUZ-INSPIRED VULNERABILITY DASHBOARD METRICS")
  print("==================================================")
  print(f"Target Group: Women in {selected_locality} | Low Education | Age {min_age}-{max_age}")
  print(f"Total evaluated in triage group: {total_triage_group}")
  print(f"Positive cases recorded: {positive_cases}")
  print(f"Calculated Probability of Vulnerability/Infection: {probability:.1f}%")
  print("==================================================\n")

# 5. GENERATING THE DASHBOARD (Multi-plot Visualization)
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: HIV Status Distribution across Racial Groups within the Triage Filter
sns.countplot(
    data=triage_filtered,
    x="race",
    hue="hiv_status",
    palette="Set2",
    ax=axes[0],
    order=["Black", "Mixed", "White"],
)
axes[0].set_title("Vulnerability by Racial Group (Trained Triage)", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Racial Group", fontsize=10)
axes[0].set_ylabel("Number of Records", fontsize=10)
axes[0].legend(title="HIV Status")

# Plot 2: Locality vs Education Level Impact on the entire dataset
sns.countplot(
    data=df,
    x="locality",
    hue="education_level",
    palette="muted",
    ax=axes[1],
)
axes[1].set_title("Socioeconomic Overview: Locality & Education", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Locality", fontsize=10)
axes[1].set_ylabel("Number of Records", fontsize=10)
axes[1].legend(title="Education Level")

plt.tight_layout()
plt.show()