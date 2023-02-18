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
  'shortwave_radiation_sum (MJ/m²)',
]

WEATHER_COLS_MAP = {
  'time': 'Date',
  'precipitation_sum (mm)': 'Precipitation',
  'rain_sum (mm)': 'Rain',
  'snowfall_sum (cm)': 'Snowfall',
  'windspeed_10m_max (km/h)': 'Windspeed',
  'windgusts_10m_max (km/h)': 'Windgusts',
  'et0_fao_evapotranspiration (mm)': 'Evapotranspiration',
  'shortwave_radiation_sum (MJ/m²)': 'Shortwave Radiation',
}

WEATHER_OUTPUT_DIR = 'cleaned_weather'

AIRLINE_COLS = [
  'FL_DATE',
  'OP_CARRIER',
  'OP_CARRIER_FL_NUM',
  'CRS_DEP_TIME',
  'ORIGIN',
  'DISTANCE',
  'DEP_DELAY',
]

AIRLINE_COLS_MAP = {
  'FL_DATE': 'Date',
  'ORIGIN': 'Origin',
  'DEST': 'Destination',
  'OP_CARRIER': 'Carrier',
  'OP_CARRIER_FL_NUM': 'Flight Num',
  'CRS_DEP_TIME': 'Departure Time',
  'DISTANCE': 'Distance',
  'DEP_DELAY': 'Delay'
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
  'Evapotranspiration': 'Origin Evapotranspiration',
  'Shortwave Radiation': 'Origin Shortwave Radiation',
}

WEATHER_ORIGIN_FEATURE_COLS = [
  'Date', 'Origin', 'Precipitation', 'Rain', 'Snowfall', 'Windspeed', 'Windgusts', 'Evapotranspiration', 'Shortwave Radiation'
]

WITHOUT_AIRLINE_COLS = [
  'Origin Precipitation', 'Origin Rain', 'Origin Snowfall', 
  'Origin Windspeed', 'Origin Windgusts', 'Origin Evapotranspiration',
  'Origin Shortwave Radiation',
]

MASTER_AIRPORT_FILE = ('T_MASTER_CORD.csv')

AIRPORT_OUTPUT_DIR = 'cleaned_airport'

AIRPORT_COLS_MAP = {
  'DOMESTIC': 'Total Monthly Domestic', 
  'INTERNATIONAL': 'Total Monthly International', 
}

AIRPORT_COLS = [
  'Year',
  'Month',
  'Origin',
  'Total Monthly Domestic',
  'Total Monthly International',
]

ORIGIN_AIRPORT_COLS = {
  'Total Monthly Domestic': 'Origin Total Monthly Domestic',
  'Total Monthly International': 'Origin Total Monthly International',
}

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


def clean_airport_datasets(directory):
  successfully_cleaned = []
  unsuccessfully_cleaned = []
  show_sample = True

  if not os.path.exists(os.path.join(directory, MASTER_AIRPORT_FILE)):
    print("Master Airport File does not exist!")
    return

  master_airport_df = pd.read_csv(os.path.join(directory, MASTER_AIRPORT_FILE))

  if not os.path.exists(directory):
    print("Directory does not exist!")
    return

  counter = 0

  for filename in os.listdir(directory):
    if (counter % 20 == 0 and counter != 0):
      print(f"{bcolors.OKGREEN}{counter} files touched")

    counter += 1

    if not os.path.isfile(os.path.join(directory, filename)) or filename == '.DS_Store'  or filename == MASTER_AIRPORT_FILE:
      continue

    filepath = os.path.join(directory, filename)

    with open(filepath) as f:
      firstline = f.readline()
    airport_name = firstline.split(':')[1].split('(Origin Airport)')[0].strip()

    target_airport = master_airport_df.loc[master_airport_df['DISPLAY_AIRPORT_NAME'] == airport_name]

    airport_history = master_airport_df.loc[master_airport_df['DISPLAY_AIRPORT_NAME'] == airport_name]
    airport_code = airport_history.loc[target_airport['AIRPORT_IS_LATEST'] == 1]['AIRPORT'].item()

    airport_df = pd.read_html(filepath)[0]
    airport_df = airport_df.loc[airport_df['Month'] != 'TOTAL']
    airport_df['Origin'] = airport_code
    airport_df = airport_df.rename(columns=AIRPORT_COLS_MAP)
    selected_airport_df = airport_df[AIRPORT_COLS]
    selected_airport_df['Total Monthly Domestic'].fillna(0, inplace=True)
    selected_airport_df['Total Monthly International'].fillna(0.0, inplace=True)

    if show_sample:
      print(f"{bcolors.WARNING}Column Preview:\n")
      print(selected_airport_df.head())
      print('')
      show_sample = False

    if not os.path.exists(AIRPORT_OUTPUT_DIR) or not os.path.isdir(AIRPORT_OUTPUT_DIR):
      os.mkdir(AIRPORT_OUTPUT_DIR)
    
    new_filename = f"{AIRPORT_OUTPUT_DIR}/cleaned_airport_{airport_code}.csv"
    selected_airport_df.to_csv(new_filename, index=False)
    successfully_cleaned.insert(0, airport_code)
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
    renamed_selected_df = selected_df.rename(columns=WEATHER_COLS_MAP)

    if show_sample:
      print(f"{bcolors.WARNING}Column Preview:\n")
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
  CLEANED_AIRPORT_FILEDIR = f"{directory}/{AIRPORT_OUTPUT_DIR}"

  show_weather_sample = True
  show_airport_sample = True
  counter = 0

  if not os.path.isfile(CLEANED_AIRLINE_FILEPATH):
    print("Cleaned Airline Dataset does not exist!")
    return

  airline_df = pd.read_csv(CLEANED_AIRLINE_FILEPATH)
  
  print(f"{bcolors.WARNING}Airline Column Preview:\n")
  print(airline_df.head())
  print('')

  airline_df['Date'] = airline_df['Date'].astype(str)
  airline_df = airline_df[airline_df['Date'] != 'nan']
  airline_df['Year'] = airline_df['Date'].apply(lambda x: int(str(x).split('-')[0]))
  airline_df['Month'] = airline_df['Date'].apply(lambda x: int(str(x).split('-')[1]))

  for filename in os.listdir(CLEANED_AIRPORT_FILEDIR):
    if (counter % 20 == 0 and counter != 0):
      print(f"{bcolors.OKGREEN}{counter} airport files merged")

    counter += 1

    if not os.path.isfile(os.path.join(CLEANED_AIRPORT_FILEDIR, filename)) or filename == '.DS_Store':
      continue

    airport_filepath = os.path.join(CLEANED_AIRPORT_FILEDIR, filename)
    airport_df = pd.read_csv(airport_filepath)

    airport_df['Total Monthly Domestic'].fillna(0, inplace=True)
    airport_df['Total Monthly International'].fillna(0.0, inplace=True)

    if show_airport_sample:
      print(f"{bcolors.WARNING}Airport Column Preview:\n")
      print(airport_df.head())
      print('')
      show_airport_sample = False

    airline_df = airline_df.merge(airport_df.set_index(['Year', 'Month', 'Origin']), on=['Year', 'Month', 'Origin'], how='left')

    if counter == 1:
      airline_df.rename(columns = ORIGIN_AIRPORT_COLS, inplace = True)

    else:
      for k,v in ORIGIN_AIRPORT_COLS.items():
        airline_df[v] = airline_df[v].fillna(airline_df[k])
        airline_df.drop(k, axis=1, inplace=True)

  counter = 0

  for filename in os.listdir(CLEANED_WEATHER_FILEDIR):
    if (counter % 20 == 0 and counter != 0):
      print(f"{bcolors.OKGREEN}{counter} weather files merged")

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

  # perform standardization in Jupyter Notebook instead
  # scaler = StandardScaler()
  # features_df = airline_df[WITHOUT_AIRLINE_COLS]
  # scaled_features_np = scaler.fit_transform(features_df)
  # scaled_features_df = pd.DataFrame(scaled_features_np , columns=WITHOUT_AIRLINE_COLS)
  # scaled_features_df['Delay'] = airline_df['Delay']
  # scaled_features_df[list(AIRLINES_MAP.values())] = airline_df[list(AIRLINES_MAP.values())]


  print(f"{bcolors.WARNING}EDA Features w/o Airlines Preview:\n")
  print(airline_df[WITHOUT_AIRLINE_COLS].head())
  print('')

  airline_df.to_csv(f"eda_{year}.csv", index=False)


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
        choices=['Weather', 'Airline', 'Airport'],
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

    elif dataset['dataset'] ==  'Airport':
      get_airport_data = [
        inquirer.Text('dir', message="Relative file path to airport dataset"),
      ]
      answers = inquirer.prompt(get_airport_data)
      clean_airport_datasets(answers['dir'])
