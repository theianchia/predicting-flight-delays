#!/usr/bin/env python3

import os

import pandas as pd

import constants, helpers

pd.options.mode.chained_assignment = None


def clean_weather_datasets(directory, year):
  successfully_cleaned = []
  unsuccessfully_cleaned = []
  show_sample = True

  if not os.path.exists(directory):
    print("Directory does not exist!")
    return

  counter = 0

  for filename in os.listdir(directory):
    if (counter % 20 == 0 and counter != 0):
      print(f"{constants.bcolors.OKGREEN}{counter} files touched")

    counter += 1

    if not os.path.isfile(os.path.join(directory, filename)) or filename == '.DS_Store':
      continue

    filepath = os.path.join(directory, filename)
    df = pd.read_csv(filepath, skiprows=[0,1,2])
    df['time'] = df['time'].apply(pd.to_datetime)

    if df[df['time'].dt.year == int(year)].shape[0] == 0:
      unsuccessfully_cleaned.insert(0,filename)
      successfully_cleaned.append('')
      continue

    df = df[df['time'].dt.year == int(year)]
    df['Origin'] = filename.split('.')[0]
    renamed_df = df.rename(columns=constants.WEATHER_COLS_RENAME)

    if show_sample:
      helpers.print_df_preview(renamed_df, "Weather")
      show_sample = False

    if not os.path.exists(constants.WEATHER_OUTPUT_DIR) or not os.path.isdir(constants.WEATHER_OUTPUT_DIR):
      os.mkdir(constants.WEATHER_OUTPUT_DIR)

    new_filename = f"{constants.WEATHER_OUTPUT_DIR}/cleaned_{year}_{filename}"
    renamed_df.to_csv(new_filename, index=False)
    successfully_cleaned.insert(0,filename)
    unsuccessfully_cleaned.append('')

  helpers.print_success_status_table(successfully_cleaned, unsuccessfully_cleaned)
