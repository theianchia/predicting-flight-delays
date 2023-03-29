#!/usr/bin/env python3

import os

import pandas as pd

import constants, helpers


def clean_holidays_datasets(directory, year):
  if not os.path.exists(directory):
    print("Directory does not exist!")
    return

  for filename in os.listdir(directory):

    if not os.path.isfile(os.path.join(directory, filename)) or filename == '.DS_Store':
      continue

    filepath = os.path.join(directory, filename)

    holidays_df = pd.read_csv(filepath)
    holidays_df = holidays_df[holidays_df['Year'] == int(year)][constants.HOLIDAY_COLS].reset_index(drop=True)
    holidays_df.rename(columns = {'WeekDay': 'Day of Holiday'}, inplace = True)
    helpers.print_df_preview(holidays_df, "Holidays")

    if not os.path.exists(constants.HOLIDAYS_OUTPUT_DIR) or not os.path.isdir(constants.HOLIDAYS_OUTPUT_DIR):
      os.mkdir(constants.HOLIDAYS_OUTPUT_DIR)

    new_filename = f"{constants.HOLIDAYS_OUTPUT_DIR}/cleaned_holidays_{year}.csv"
    holidays_df.to_csv(new_filename, index=False)
