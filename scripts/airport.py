#!/usr/bin/env python3

import os

import pandas as pd

import constants, helpers


def clean_airport_datasets(directory, year):
  successfully_cleaned = []
  unsuccessfully_cleaned = []
  show_sample = True

  if not os.path.exists(directory):
    print("Directory does not exist!")
    return

  for filename in os.listdir(directory):

    if not os.path.isfile(os.path.join(directory, filename)) or filename == '.DS_Store':
      continue

    filepath = os.path.join(directory, filename)

    airport_df = pd.read_csv(filepath)
    selected_year_airport_df = airport_df[airport_df['Year'] == int(year)]
    renamed_selected_df = selected_year_airport_df.rename(columns=constants.AIRPORT_COLS_RENAME)

    if show_sample:
      helpers.print_df_preview(renamed_selected_df, "Airport")
      show_sample = False

    if not os.path.exists(constants.AIRPORT_OUTPUT_DIR) or not os.path.isdir(constants.AIRPORT_OUTPUT_DIR):
      os.mkdir(constants.AIRPORT_OUTPUT_DIR)
    
    new_filename = f"{constants.AIRPORT_OUTPUT_DIR}/cleaned_airport_{year}.csv"
    renamed_selected_df.to_csv(new_filename, index=False)
    successfully_cleaned.insert(0, year)
    unsuccessfully_cleaned.append('')

  helpers.print_success_status_table(successfully_cleaned, unsuccessfully_cleaned)
