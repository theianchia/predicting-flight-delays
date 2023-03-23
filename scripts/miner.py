#!/usr/bin/env python3

import os

import inquirer

import constants, helpers
import airline, airplane, airport, holidays, weather, merge


if __name__ == '__main__':
  get_purpose = [
    inquirer.List('purpose',
      message="What's your purpose of use?",
      choices=['Preprocessing', 'Merging'],
    ),
  ]
  purpose = inquirer.prompt(get_purpose)

  if purpose['purpose'] == 'Merging':
    print(f"{constants.bcolors.OKBLUE}Please ensure cleaned datasets are grouped together by year in the same directory\n")

    get_cleaned_datasets = [
      inquirer.Text('dir', message="Relative file path to cleaned datasets"),
      inquirer.Text('year', message="Year of cleaned datasets"),
    ]
    answers = inquirer.prompt(get_cleaned_datasets)
    merge.merge_datasets(answers['dir'], answers['year'])

  else:
    get_dataset = [
      inquirer.List('dataset',
        message='Which dataset are you cleaning?',
        choices=['Weather', 'Airline', 'Airport', 'Airplane', 'Holidays'],
      ),
    ]
    dataset = inquirer.prompt(get_dataset)

    if dataset['dataset'] == 'Weather':
      get_weather_data = [
        inquirer.Text('dir', message="Relative file path to weather dataset"),
        inquirer.Text('year', message="Year of weather dataset"),
      ]
      answers = inquirer.prompt(get_weather_data)
      weather.clean_weather_datasets(answers['dir'], answers['year'])

    elif dataset['dataset'] ==  'Airline':
      get_airline_data = [
        inquirer.Text('dir', message="Relative file path to airline dataset"),
      ]
      answers = inquirer.prompt(get_airline_data)
      airline.clean_airline_datasets(answers['dir'])

    elif dataset['dataset'] ==  'Airport':
      get_airport_data = [
        inquirer.Text('dir', message="Relative file path to airport dataset"),
        inquirer.Text('year', message="Year of airport dataset"),
      ]
      answers = inquirer.prompt(get_airport_data)
      airport.clean_airport_datasets(answers['dir'], answers['year'])

    elif dataset['dataset'] ==  'Airplane':
      get_airport_data = [
        inquirer.Text('airplane_dir', message="Relative file path to airplane dataset"),
        inquirer.Text('carrier_dir', message="Relative file path to carrier dataset"),
      ]
      answers = inquirer.prompt(get_airport_data)
      airplane.clean_airplane_datasets(answers['airplane_dir'], answers['carrier_dir'])

    elif dataset['dataset'] ==  'Holidays':
      get_holidays_data = [
        inquirer.Text('airplane_dir', message="Relative file path to holidays dataset"),
        inquirer.Text('carrier_dir', message="Year of holidays dataset"),
      ]
      answers = inquirer.prompt(get_holidays_data)
      holidays.clean_holidays_datasets(answers['airplane_dir'], answers['carrier_dir'])
