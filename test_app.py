import pandas as pd
import pytest


# Simulando a função de carregamento de dados do app.py
def load_test_data():
  data = {
      "age": [25, 42, 19, 35],
      "locality": ["Urban Center", "Periphery", "Rural", "Urban Center"],
      "education_level": ["High", "Low", "Low", "Medium"],
      "race": ["White", "Black", "Mixed", "White"],
      "gender": ["Female", "Female", "Female", "Female"],
      "hiv_status": ["Negative", "Positive", "Positive", "Negative"],
  }
  df = pd.DataFrame(data)
  df["locality"] = df["locality"].str.strip().str.title()
  df["race"] = df["race"].str.strip().str.capitalize()
  return df


def test_dataframe_structure():
  df = load_test_data()
  # Verifica se as colunas essenciais existem
  assert "race" in df.columns
  assert "locality" in df.columns
  assert "hiv_status" in df.columns


def test_urban_filtering():
  df = load_test_data()
  urban_df = df[df["locality"] == "Urban Center"]
  # Garante que apenas o centro urbano foi filtrado
  assert len(urban_df) == 2
  assert all(urban_df["locality"] == "Urban Center")