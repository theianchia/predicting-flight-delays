#!/usr/bin/env python3

import os

import pandas as pd
import numpy as np

import constants, helpers

pd.options.mode.chained_assignment = None


def merge_datasets(directory, year):
  if not os.path.exists(directory):
    return "Directory does not exist!"

  CLEANED_AIRLINE_FILEPATH = f"{directory}/{constants.AIRLINE_OUTPUT_DIR}/cleaned_airline_cancel_data_{year}.csv"
  CLEANED_AIRPORT_FILEPATH = f"{directory}/{constants.AIRPORT_OUTPUT_DIR}/cleaned_airport_{year}.csv"
  CLEANED_AIRPLANE_FILEPATH = f"{directory}/{constants.AIRPLANE_OUTPUT_DIR}/cleaned_airplane.csv"
  CLEANED_WEATHER_FILEDIR = f"{directory}/{constants.WEATHER_OUTPUT_DIR}"
  CLEANED_HOLIDAYS_FILEPATH = f"{directory}/{constants.HOLIDAYS_OUTPUT_DIR}/cleaned_holidays_{year}.csv"

  show_weather_sample = True
  counter = 0

  if not os.path.isfile(CLEANED_AIRLINE_FILEPATH):
    print("Cleaned Airline Dataset does not exist!")
    return

  airline_df = pd.read_csv(CLEANED_AIRLINE_FILEPATH)
  helpers.print_df_preview(airline_df, "Airline")

  airline_df['Date'] = airline_df['Date'].astype(str)
  airline_df = airline_df[airline_df['Date'] != 'nan']
  airline_df['Year'] = airline_df['Date'].apply(lambda x: int(str(x).split('-')[0]))
  airline_df['Month'] = airline_df['Date'].apply(lambda x: int(str(x).split('-')[1]))

  if not os.path.isfile(CLEANED_AIRPLANE_FILEPATH):
    print("Cleaned Airplane Dataset does not exist!")
    return

  airplane_df = pd.read_csv(CLEANED_AIRPLANE_FILEPATH)
  helpers.print_df_preview(airplane_df, "Airplane")

  airline_df = airline_df.merge(airplane_df.set_index(['Origin', 'Destination', 'Carrier Code']), on=['Origin', 'Destination', 'Carrier Code'], how='left')
  helpers.print_df_preview(airline_df, "After merging Airplane Data")


  if not os.path.isfile(CLEANED_AIRPORT_FILEPATH):
    print("Cleaned Airport Dataset does not exist!")
    return

  airport_df = pd.read_csv(CLEANED_AIRPORT_FILEPATH)
  helpers.print_df_preview(airport_df, "Airport")

  airline_df = airline_df.merge(airport_df.set_index(['Year', 'Month', 'Origin']), on=['Year', 'Month', 'Origin'], how='left')

  airline_df.rename(columns = constants.MERGED_ORIGIN_AIRPORT_COLS_RENAME, inplace = True)

  airport_df.rename(columns = {'Origin': 'Destination'}, inplace = True)
  airline_df = airline_df.merge(airport_df.set_index(['Year', 'Month', 'Destination']), on=['Year', 'Month', 'Destination'], how='left')

  airline_df.rename(columns = constants.MERGED_DEST_AIRPORT_COLS_RENAME, inplace = True)

  helpers.print_df_preview(airline_df, "After merging Airport Data")


  if not os.path.isfile(CLEANED_HOLIDAYS_FILEPATH):
    print("Cleaned Airport Dataset does not exist!")
    return

  holidays_df = pd.read_csv(CLEANED_HOLIDAYS_FILEPATH)
  helpers.print_df_preview(holidays_df, "Holidays")
  airline_df = airline_df.merge(holidays_df.set_index(['Date']), on=['Date'], how='left')

  helpers.print_df_preview(airline_df, "After merging Holidays Data")


  for filename in os.listdir(CLEANED_WEATHER_FILEDIR):
    if (counter % 10 == 0 and counter != 0):
      print(f"{constants.bcolors.OKGREEN}{counter} weather files merged")

    counter += 1

    if not os.path.isfile(os.path.join(CLEANED_WEATHER_FILEDIR, filename)) or filename == '.DS_Store':
      continue

    weather_filepath = os.path.join(CLEANED_WEATHER_FILEDIR, filename)
    weather_df = pd.read_csv(weather_filepath)

    if show_weather_sample:
      helpers.print_df_preview(weather_df, "Weather")
      show_weather_sample = False

    airline_df = airline_df.merge(weather_df.set_index(['Date', 'Origin']), on=['Date', 'Origin'], how='left')

    if counter == 1:
      airline_df.rename(columns = constants.MERGED_ORIGIN_WEATHER_COLS_RENAME, inplace = True)

      weather_df.rename(columns = {'Origin': 'Destination'}, inplace = True)
      airline_df = airline_df.merge(weather_df.set_index(['Date', 'Destination']), on=['Date', 'Destination'], how='left')
      airline_df.rename(columns = constants.MERGED_DEST_WEATHER_COLS_RENAME, inplace = True)

    else:
      for k,v in constants.MERGED_ORIGIN_WEATHER_COLS_RENAME.items():
        airline_df[v] = airline_df[v].fillna(airline_df[k])
        airline_df.drop(k, axis=1, inplace=True)

      weather_df.rename(columns = {'Origin': 'Destination'}, inplace = True)
      airline_df = airline_df.merge(weather_df.set_index(['Date', 'Destination']), on=['Date', 'Destination'], how='left')
      for k,v in constants.MERGED_DEST_WEATHER_COLS_RENAME.items():
        airline_df[v] = airline_df[v].fillna(airline_df[k])
        airline_df.drop(k, axis=1, inplace=True)

  airline_df['Carrier Code'].replace(constants.AIRLINES_RENAME, inplace=True)

  airline_df.reset_index(inplace=True)

  helpers.print_df_preview(airline_df[constants.EDA_WITHOUT_AIRLINE_COLS], "EDA Features w/o Airlines")

  print()
  print(airline_df.shape)
  print()

  airline_df.to_csv(f"eda_{year}.csv", index=False)
