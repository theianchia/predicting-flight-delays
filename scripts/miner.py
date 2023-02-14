#!/usr/bin/env python3

import os

import inquirer
import pandas as pd
import numpy as np
from tabulate import tabulate
from sklearn.preprocessing import StandardScaler

pd.options.mode.chained_assignment = None

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

ORIGIN_WEATHER_COLS = {
    'Precipitation': 'Origin Precipitation', 
    'Rain': 'Origin Rain', 
    'Snowfall': 'Origin Snowfall',
    'Windspeed': 'Origin Windspeed', 
    'Windgusts': 'Origin Windgusts',
    'Evapotranspiration': 'Origin Evapotranspiration'
}

DEST_WEATHER_COLS = {
    'Precipitation': 'Dest Precipitation', 
    'Rain': 'Dest Rain', 
    'Snowfall': 'Dest Snowfall',
    'Windspeed': 'Dest Windspeed', 
    'Windgusts': 'Dest Windgusts',
    'Evapotranspiration': 'Dest Evapotranspiration'
}

WEATHER_ORIGIN_FEATURE_COLS = [
  'Date', 'Origin', 'Precipitation', 'Rain', 'Snowfall', 'Windspeed', 'Windgusts', 'Evapotranspiration'
]

WEATHER_DEST_FEATURE_COLS = [
  'Date', 'Destination', 'Precipitation', 'Rain', 'Snowfall', 'Windspeed', 'Windgusts', 'Evapotranspiration'
]

WITHOUT_AIRLINE_COLS = [
  'Delay', 'Origin Precipitation', 'Origin Rain', 'Origin Snowfall', 
  'Origin Windspeed', 'Origin Windgusts', 'Origin Evapotranspiration', 
  'Dest Precipitation', 'Dest Rain', 'Dest Snowfall', 'Dest Windspeed', 
  'Dest Windgusts', 'Dest Evapotranspiration'
]

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
    print("Directory does not exist!")
    return

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
    print("Directory does not exist!")
    return

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
    selected_df['Origin'] = filename.split('.')[0]
    selected_df['Destination'] = filename.split('.')[0]
    renamed_selected_df = selected_df.rename(columns=WEATHER_COLS_MAP)

    if show_sample:
      print(f"{bcolors.WARNING}\nColumn Preview:\n")
      print(renamed_selected_df.head())
      print('')
      show_sample = False

    if not os.path.exists(WEATHER_OUTPUT_DIR) or not os.path.isdir(WEATHER_OUTPUT_DIR):
      os.mkdir(WEATHER_OUTPUT_DIR)

    new_filename = f"{WEATHER_OUTPUT_DIR}/cleaned_{year}_{filename}"
    renamed_selected_df.to_csv(new_filename, index=False)
    successfully_cleaned.insert(0,filename)
    unsuccessfully_cleaned.append('')

  table = np.stack([successfully_cleaned, unsuccessfully_cleaned], axis=-1)
  print('')
  print(tabulate(table, TABLE_HEADERS, tablefmt="simple_outline"))


def eda(directory, year):
  if not os.path.exists(directory):
    return "Directory does not exist!"

  CLEANED_AIRLINE_FILEPATH = f"{directory}/{AIRLINE_OUTPUT_DIR}/cleaned_airline_cancel_data_{year}.csv"
  CLEANED_WEATHER_FILEDIR = f"{directory}/{WEATHER_OUTPUT_DIR}"

  show_weather_sample = True
  counter = 0

  if not os.path.isfile(CLEANED_AIRLINE_FILEPATH):
    print("Cleaned Airline Dataset does not exist!")
    return

  airline_df = pd.read_csv(CLEANED_AIRLINE_FILEPATH)
  
  print(f"{bcolors.WARNING}\n Airline Column Preview:\n")
  print(airline_df.head())
  print('')

  for filename in os.listdir(CLEANED_WEATHER_FILEDIR):
    if (counter % 20 == 0 and counter != 0):
      print(f"{bcolors.OKGREEN}{counter} origin weather files merged")

    counter += 1

    if not os.path.isfile(os.path.join(CLEANED_WEATHER_FILEDIR, filename)) or filename == '.DS_Store':
      continue

    weather_filepath = os.path.join(CLEANED_WEATHER_FILEDIR, filename)
    weather_df = pd.read_csv(weather_filepath)

    if show_weather_sample:
      print(f"{bcolors.WARNING}Weather Column Preview:\n")
      print(weather_df.head())
      print('')
      show_weather_sample = False

    weather_origin_df = weather_df[WEATHER_ORIGIN_FEATURE_COLS]
    airline_df = airline_df.merge(weather_origin_df.set_index(['Date', 'Origin']), on=['Date', 'Origin'], how='left')

    if counter == 1:
      airline_df.rename(columns = ORIGIN_WEATHER_COLS, inplace = True)

    else:
      for k,v in ORIGIN_WEATHER_COLS.items():
        airline_df[v] = airline_df[v].fillna(airline_df[k])
        airline_df.drop(k, axis=1, inplace=True)

  counter = 0

  for filename in os.listdir(CLEANED_WEATHER_FILEDIR):
    if (counter % 20 == 0 and counter != 0):
      print(f"{bcolors.OKGREEN}{counter} destination weather files merged")

    counter += 1

    if not os.path.isfile(os.path.join(CLEANED_WEATHER_FILEDIR, filename)) or filename == '.DS_Store':
      continue

    weather_filepath = os.path.join(CLEANED_WEATHER_FILEDIR, filename)
    weather_df = pd.read_csv(weather_filepath)
    
    weather_dest_df = weather_df[WEATHER_DEST_FEATURE_COLS]
    airline_df = airline_df.join(weather_dest_df.set_index(['Date', 'Destination']), on=['Date', 'Destination'], how='left')
    
    if counter == 1:
      airline_df.rename(columns = DEST_WEATHER_COLS, inplace = True)
    else:
      for k,v in DEST_WEATHER_COLS.items():
        airline_df[v] = airline_df[v].fillna(airline_df[k])
        airline_df.drop(k, axis=1, inplace=True)

  scaler = StandardScaler()
  features_df = airline_df[WITHOUT_AIRLINE_COLS]
  scaled_features_np = scaler.fit_transform(features_df)
  scaled_features_df = pd.DataFrame(scaled_features_np , columns=WITHOUT_AIRLINE_COLS)

  print(f"{bcolors.WARNING}\n EDA Column Preview:\n")
  print(weather_df.head())
  print('')

  scaled_features_df.to_csv(f"eda_{year}", index=False)


if __name__ == '__main__':
  get_purpose = [
    inquirer.List('purpose',
      message="What's your purpose of use?",
      choices=['Preprocessing', 'EDA'],
    ),
  ]
  purpose = inquirer.prompt(get_purpose)

  if purpose['purpose'] == 'EDA':
    print(f"{bcolors.WARNING}Please ensure cleaned datasets are grouped together by year in the same directory\n")

    get_cleaned_datasets = [
      inquirer.Text('dir', message="Relative file path to cleaned datasets"),
      inquirer.Text('year', message="Year of cleaned datasets"),
    ]
    answers = inquirer.prompt(get_cleaned_datasets)
    eda(answers['dir'], answers['year'])

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

    elif dataset['dataset'] ==  'Airline':
      get_airline_data = [
        inquirer.Text('dir', message="Relative file path to airline dataset"),
      ]
      answers = inquirer.prompt(get_airline_data)
      clean_airline_datasets(answers['dir'])
