from tabulate import tabulate

import constants

def print_df_preview(df, dataset_type):
  print(f"{constants.bcolors.WARNING}\n{dataset_type} Column Preview:\n")
  print(df.head())
  print('')


def print_success_status_table(successfully_cleaned, unsuccessfully_cleaned):
  table = np.stack([successfully_cleaned, unsuccessfully_cleaned], axis=-1)
  print('')
  print(tabulate(table, constants.TABLE_HEADERS, tablefmt="simple_outline", showindex="always"))
