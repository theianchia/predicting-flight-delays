#!/usr/bin/env python3

import os

import pandas as pd

import constants, helpers


def clean_airline_datasets(directory):
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
    df = pd.read_csv(filepath)

    df['Flight Delay'] = df['ACTUAL_ELAPSED_TIME'] - df['CRS_ELAPSED_TIME']
    selected_df = df[constants.AIRLINE_COLS]
    selected_df.rename(columns=constants.AIRLINE_COLS_RENAME, inplace=True)

    # selected_df['Carrier Code'].replace(constants.AIRLINES_RENAME, inplace=True)
    # encoded_airlines_df = pd.get_dummies(selected_df['Carrier Code'])
    selected_df[['Carrier Delay', 'Weather Delay', 'NAS Delay', 'Security Delay', 'Late Aircraft Delay']] = selected_df[['Carrier Delay', 'Weather Delay', 'NAS Delay', 'Security Delay', 'Late Aircraft Delay']].fillna(0)
    selected_df.dropna(inplace=True)
    selected_df.reset_index(inplace=True, drop=True)
    # cleaned_df = pd.concat([selected_df, encoded_airlines_df], axis=1)

    if show_sample:
      helpers.print_df_preview(selected_df, "Airline")
      show_sample = False

    if not os.path.exists(constants.AIRLINE_OUTPUT_DIR) or not os.path.isdir(constants.AIRLINE_OUTPUT_DIR):
      os.mkdir(constants.AIRLINE_OUTPUT_DIR)

    new_filename = f"{constants.AIRLINE_OUTPUT_DIR}/cleaned_{filename}"
    selected_df.to_csv(new_filename, index=False)
    successfully_cleaned.insert(0, filename)
    unsuccessfully_cleaned.append('')

  helpers.print_success_status_table(successfully_cleaned, unsuccessfully_cleaned)
