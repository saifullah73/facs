import pandas as pd
import numpy as np
import sys

def read_age_csv(csv_name, header_name=""):
  df = pd.read_csv(csv_name)
  df.columns = map(str.lower, df.columns)
  if header_name not in df.columns:
    header_name = "islamabad"
  ages = df[header_name.lower()].to_numpy()
  # return fractions instead of actual distribution
  return ages / np.sum(ages)

