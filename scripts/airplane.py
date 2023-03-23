#!/usr/bin/env python3

import os

import pandas as pd

import constants, helpers


def clean_airplane_datasets(airplane_dir, carrier_dir):
  if not os.path.exists(airplane_dir) or not os.path.exists(carrier_dir):
    print("Airplane or Carrier Directory does not exist!")
    return

  for a_filename in os.listdir(airplane_dir):

    if not os.path.isfile(os.path.join(airplane_dir, a_filename)) or a_filename == '.DS_Store':
      continue

    airplane_filepath = os.path.join(airplane_dir, a_filename)
    airplane_df = pd.read_csv(airplane_filepath)

    for c_filename in os.listdir(carrier_dir):

      if not os.path.isfile(os.path.join(carrier_dir, c_filename)) or c_filename == '.DS_Store':
        continue

      carrier_filepath = os.path.join(carrier_dir, c_filename)
      carrier_df = pd.read_csv(carrier_filepath)

      airplane_df.dropna(inplace=True)
      airplane_df.reset_index(inplace=True, drop=True)
      carrier_df = carrier_df[carrier_df['ORIGIN'] != carrier_df['DEST']]
      carrier_df.dropna(inplace=True)
      carrier_df.reset_index(inplace=True, drop=True)

      selected_carrier_df = carrier_df[constants.CARRIER_FEATURES]
      selected_airplane_df = airplane_df[constants.AIRPLANE_FEATURES]

      selected_carrier_df.rename(columns=constants.CARRIER_COLS_RENAME, inplace=True)
      selected_airplane_df.rename(columns=constants.AIRPLANE_COLS_RENAME, inplace=True)
      selected_airplane_df = selected_carrier_df.merge(selected_airplane_df.set_index(['Airplane']), on=['Airplane'], how='left')
      selected_airplane_df.dropna(inplace=True)
      selected_airplane_df.reset_index(inplace=True, drop=True)

      mode_airplane_df = selected_airplane_df.groupby(['Origin', 'Destination', 'Carrier Code']).agg(lambda x:x.value_counts().index[0]).reset_index()
      helpers.print_df_preview(mode_airplane_df, "Airplane")

      if not os.path.exists(constants.AIRPLANE_OUTPUT_DIR) or not os.path.isdir(constants.AIRPLANE_OUTPUT_DIR):
        os.mkdir(constants.AIRPLANE_OUTPUT_DIR)

      new_filename = f"{constants.AIRPLANE_OUTPUT_DIR}/cleaned_airplane.csv"
      mode_airplane_df.to_csv(new_filename, index=False)
      return
