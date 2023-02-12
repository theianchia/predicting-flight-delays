#!/usr/bin/env python3

import os

import inquirer
import pandas as pd
import numpy as np
from tabulate import tabulate

WEATHER_COLS = [
    'time',
    'precipitation_sum (mm)',
    'rain_sum (mm)',
    'snowfall_sum (cm)',
    'windspeed_10m_max (km/h)',
    'windgusts_10m_max (km/h)',
    'et0_fao_evapotranspiration (mm)',
]

WEATHER_COLS_MAP = {
    'time': 'Date',
    'precipitation_sum (mm)': 'Precipitation',
    'rain_sum (mm)': 'Rain',
    'snowfall_sum (cm)': 'Snowfall',
    'windspeed_10m_max (km/h)': 'Windspeed',
    'windgusts_10m_max (km/h)': 'Windgusts',
    'et0_fao_evapotranspiration (mm)': 'Evapotranspiration'
}

WEATHER_OUTPUT_DIR = 'cleaned_weather'

AIRLINE_COLS = [
  'FL_DATE',
  'OP_CARRIER',
  'ORIGIN',
  'DEST',
  'Delay'
]

AIRLINE_COLS_MAP = {
  'FL_DATE': 'Date',
  'ORIGIN': 'Origin',
  'DEST': 'Destination',
  'OP_CARRIER': 'Carrier'
}

AIRLINES_MAP = {
  'UA':'United Airlines',
  'AS':'Alaska Airlines',
  '9E':'Endeavor Air',
  'B6':'JetBlue Airways',
  'EV':'ExpressJet',
  'F9':'Frontier Airlines',
  'G4':'Allegiant Air',
  'HA':'Hawaiian Airlines',
  'MQ':'Envoy Air',
  'NK':'Spirit Airlines',
  'OH':'PSA Airlines',
  'OO':'SkyWest Airlines',
  'VX':'Virgin America',
  'WN':'Southwest Airlines',
  'YV':'Mesa Airline',
  'YX':'Republic Airways',
  'AA':'American Airlines',
  'DL':'Delta Airlines'
}

AIRLINE_OUTPUT_DIR = 'cleaned_airline'

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

def clean_airline_datasets(directory):
  successfully_cleaned = []
  unsuccessfully_cleaned = []
  show_sample = True

  if not os.path.exists(directory):
    return "Directory does not exist!"

  for filename in os.listdir(directory):

    if not os.path.isfile(os.path.join(directory, filename)) or filename == '.DS_Store':
      continue
    
    filepath = os.path.join(directory, filename)
    df = pd.read_csv(filepath)
    df['Delay'] = (df['ACTUAL_ELAPSED_TIME'] - df['CRS_ELAPSED_TIME']).to_numpy()

    selected_df = df[AIRLINE_COLS]
    print(selected_df.head())
    selected_df.rename(columns=AIRLINE_COLS_MAP, inplace=True)
    selected_df['Carrier'].replace(AIRLINES_MAP, inplace=True)

    encoded_airlines_df = pd.get_dummies(selected_df['Carrier'])

    selected_df.drop('Carrier', axis=1, inplace=True)
    selected_df.dropna(inplace=True)
    cleaned_df = pd.concat([selected_df, encoded_airlines_df], axis=1)

    if show_sample:
      print(f"{bcolors.WARNING}\nColumn Preview:\n")
      print(cleaned_df.head())
      col_len = len(''.join(list(cleaned_df.columns)))
      print('')
      show_sample = False

    if not os.path.exists(AIRLINE_OUTPUT_DIR) or not os.path.isdir(AIRLINE_OUTPUT_DIR):
      os.mkdir(AIRLINE_OUTPUT_DIR)

    new_filename = f"{AIRLINE_OUTPUT_DIR}/cleaned_{filename}"
    cleaned_df.to_csv(new_filename, index=False)
    successfully_cleaned.insert(0,filename)
    unsuccessfully_cleaned.append('')

  table = np.stack([successfully_cleaned, unsuccessfully_cleaned], axis=-1)
  print('')
  print(tabulate(table, TABLE_HEADERS, tablefmt="simple_outline"))


def clean_weather_datasets(directory, year):
  successfully_cleaned = []
  unsuccessfully_cleaned = []
  show_sample = True

  if not os.path.exists(directory):
    return "Directory does not exist!"

  counter = 0

  for filename in os.listdir(directory):
    if (counter % 20 == 0 and counter != 0):
      print(f"{bcolors.OKGREEN}{counter} files touched")

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
    selected_df = df[WEATHER_COLS]
    renamed_selected_df = selected_df.rename(columns=WEATHER_COLS_MAP)

    if show_sample:
      print(f"{bcolors.WARNING}\nColumn Preview:\n")
      print(renamed_selected_df.head())
      col_len = len(''.join(list(renamed_selected_df.columns)))
      print('')
      show_sample = False

    if not os.path.exists(WEATHER_OUTPUT_DIR) or not os.path.isdir(WEATHER_OUTPUT_DIR):
      os.mkdir(WEATHER_OUTPUT_DIR)

    new_filename = f"{WEATHER_OUTPUT_DIR}/cleaned_{year}_{filename}"
    selected_df.to_csv(new_filename, index=False)
    successfully_cleaned.insert(0,filename)
    unsuccessfully_cleaned.append('')

  table = np.stack([successfully_cleaned, unsuccessfully_cleaned], axis=-1)
  print('')
  print(tabulate(table, TABLE_HEADERS, tablefmt="simple_outline"))


if __name__ == '__main__':
  get_purpose = [
    inquirer.List('purpose',
      message="What's your purpose of use?",
      choices=['Preprocessing', 'EDA'],
    ),
  ]
  purpose = inquirer.prompt(get_purpose)

  if purpose['purpose'] == 'EDA':
    pass

  else:
    get_dataset = [
      inquirer.List('dataset',
        message='Which dataset are you cleaning?',
        choices=['Weather', 'Airline'],
      ),
    ]
    dataset = inquirer.prompt(get_dataset)

    if dataset['dataset'] == 'Weather':
      get_weather_data = [
        inquirer.Text('dir', message="Relative file path to weather dataset"),
        inquirer.Text('year', message="Year of weather dataset"),
      ]
      answers = inquirer.prompt(get_weather_data)
      clean_weather_datasets(answers['dir'], answers['year'])

    elif answers['dataset'] ==  'Airline':
      get_airline_data = [
        inquirer.Text('dir', message="Relative file path to airline dataset"),
      ]
      answers = inquirer.prompt(get_airline_data)
      clean_airline_datasets(answers['dir'])
