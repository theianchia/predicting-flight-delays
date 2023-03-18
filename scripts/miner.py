#!/usr/bin/env python3

import os

import inquirer
import pandas as pd
import numpy as np
# from sklearn.preprocessing import StandardScaler

import constants, helpers

pd.options.mode.chained_assignment = None

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
    selected_df = df[constants.WEATHER_COLS]
    selected_df['Origin'] = filename.split('.')[0]
    renamed_selected_df = selected_df.rename(columns=constants.WEATHER_COLS_RENAME)

    if show_sample:
      helpers.print_df_preview(renamed_selected_df, "Weather")
      show_sample = False

    if not os.path.exists(constants.WEATHER_OUTPUT_DIR) or not os.path.isdir(constants.WEATHER_OUTPUT_DIR):
      os.mkdir(constants.WEATHER_OUTPUT_DIR)

    new_filename = f"{constants.WEATHER_OUTPUT_DIR}/cleaned_{year}_{filename}"
    renamed_selected_df.to_csv(new_filename, index=False)
    successfully_cleaned.insert(0,filename)
    unsuccessfully_cleaned.append('')

  helpers.print_success_status_table(successfully_cleaned, unsuccessfully_cleaned)


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


def eda(directory, year):
  if not os.path.exists(directory):
    return "Directory does not exist!"

  CLEANED_AIRLINE_FILEPATH = f"{directory}/{constants.AIRLINE_OUTPUT_DIR}/cleaned_airline_cancel_data_{year}.csv"
  CLEANED_AIRPORT_FILEPATH = f"{directory}/{constants.AIRPORT_OUTPUT_DIR}/cleaned_airport_{year}.csv"
  CLEANED_AIRPLANE_FILEPATH = f"{directory}/{constants.AIRPLANE_OUTPUT_DIR}/cleaned_airplane.csv"
  CLEANED_WEATHER_FILEDIR = f"{directory}/{constants.WEATHER_OUTPUT_DIR}"

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


  # perform standardization in Jupyter Notebook instead
  # scaler = StandardScaler()
  # features_df = airline_df[WITHOUT_AIRLINE_COLS]
  # scaled_features_np = scaler.fit_transform(features_df)
  # scaled_features_df = pd.DataFrame(scaled_features_np , columns=WITHOUT_AIRLINE_COLS)
  # scaled_features_df['Delay'] = airline_df['Delay']
  # scaled_features_df[list(AIRLINES_MAP.values())] = airline_df[list(AIRLINES_MAP.values())]

  airline_df['Carrier Code'].replace(constants.AIRLINES_RENAME, inplace=True)

  airline_df.dropna(inplace=True)
  airline_df.reset_index(inplace=True, drop=True)

  helpers.print_df_preview(airline_df[constants.EDA_WITHOUT_AIRLINE_COLS], "EDA Features w/o Airlines")

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
    print(f"{constants.bcolors.OKBLUE}Please ensure cleaned datasets are grouped together by year in the same directory\n")

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
        choices=['Weather', 'Airline', 'Airport', 'Airplane'],
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
        inquirer.Text('year', message="Year of airport dataset"),
      ]
      answers = inquirer.prompt(get_airport_data)
      clean_airport_datasets(answers['dir'], answers['year'])

    elif dataset['dataset'] ==  'Airplane':
      get_airport_data = [
        inquirer.Text('airplane_dir', message="Relative file path to airplane dataset"),
        inquirer.Text('carrier_dir', message="Relative file path to carrier dataset"),
      ]
      answers = inquirer.prompt(get_airport_data)
      clean_airplane_datasets(answers['airplane_dir'], answers['carrier_dir'])
