#!/usr/bin/env python3

import os

import pandas as pd
import numpy as np
from tabulate import tabulate

COLS = [
    'time',
    'precipitation_sum (mm)',
    'rain_sum (mm)',
    'snowfall_sum (cm)',
    'windspeed_10m_max (km/h)',
    'windgusts_10m_max (km/h)',
    'et0_fao_evapotranspiration (mm)',
]

COLS_MAP = {
    'time': 'Date',
    'precipitation_sum (mm)': 'Precipitation',
    'rain_sum (mm)': 'Rain',
    'snowfall_sum (cm)': 'Snowfall',
    'windspeed_10m_max (km/h)': 'Windspeed',
    'windgusts_10m_max (km/h)': 'Windgusts',
    'et0_fao_evapotranspiration (mm)': 'Evapotranspiration'
}

OUTPUT_DIR = 'cleaned_weather'

TABLE_HEADERS = ['Successful', 'Unsuccessful']

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def read_files_from_directory(directory, year):
  successfully_cleaned = []
  unsuccessfully_cleaned = []
  show_sample = True

  if not os.path.exists(directory):
    return "Directory does not exist!"

  counter = 0

  for filename in os.listdir(directory):
    if (counter % 20 == 0 and counter != 0):
      print(f"{bcolors.OKGREEN}{counter} files checked")

    counter += 1

    if not os.path.isfile(os.path.join(directory, filename)):
      continue

    filepath = os.path.join(directory, filename)
    df = pd.read_csv(filepath, skiprows=[0,1,2])
    df['time'] = df['time'].apply(pd.to_datetime)

    if df[df['time'].dt.year == int(year)].shape[0] == 0:
      unsuccessfully_cleaned.insert(0,filename)
      successfully_cleaned.append('')
      continue

    df = df[df['time'].dt.year == int(year)]
    selected_df = df[COLS]
    renamed_selected_df = selected_df.rename(columns=COLS_MAP)

    if show_sample:
      print(f"{bcolors.WARNING}\nColumn Preview:\n")
      print(renamed_selected_df.head())
      col_len = len(''.join(list(renamed_selected_df.columns)))
      print(f"\n{'-'*col_len}\n")
      show_sample = False

    if not os.path.exists(OUTPUT_DIR) or not os.path.isdir(OUTPUT_DIR):
      os.mkdir(OUTPUT_DIR)

    new_filename = f"{OUTPUT_DIR}/cleaned_{year}_{filename}"
    selected_df.to_csv(new_filename, index=False)
    successfully_cleaned.insert(0,filename)
    unsuccessfully_cleaned.append('')

  table = np.stack([successfully_cleaned, unsuccessfully_cleaned], axis=-1)
  print('')
  print(tabulate(table, TABLE_HEADERS, tablefmt="simple_outline"))


if __name__ == '__main__':
  directory = input("Enter the weather datasets directory path: ")
  year = input("Enter year: ")
  read_files_from_directory(directory, year)
