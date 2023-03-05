WEATHER_OUTPUT_DIR = 'cleaned_weather'
AIRLINE_OUTPUT_DIR = 'cleaned_airline'
AIRPORT_OUTPUT_DIR = 'cleaned_airport'

TABLE_HEADERS = ['Successful', 'Unsuccessful']

AIRLINE_COLS = [
  'FL_DATE',
  'OP_CARRIER',
  'OP_CARRIER_FL_NUM',
  'CRS_DEP_TIME',
  'ORIGIN',
  'DEST',
  'DISTANCE',
  'DEP_DELAY',
]

AIRLINE_COLS_RENAME = {
  'FL_DATE': 'Date',
  'ORIGIN': 'Origin',
  'DEST': 'Destination',
  'OP_CARRIER': 'Carrier',
  'OP_CARRIER_FL_NUM': 'Flight Num',
  'CRS_DEP_TIME': 'Departure Time',
  'DISTANCE': 'Distance',
  'DEP_DELAY': 'Delay'
}

AIRLINES_RENAME = {
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

WEATHER_COLS_RENAME = {
  'time': 'Date',
  'precipitation_sum (mm)': 'Precipitation',
  'rain_sum (mm)': 'Rain',
  'snowfall_sum (cm)': 'Snowfall',
  'windspeed_10m_max (km/h)': 'Windspeed',
  'windgusts_10m_max (km/h)': 'Windgusts',
  'et0_fao_evapotranspiration (mm)': 'Evapotranspiration',
  'shortwave_radiation_sum (MJ/m²)': 'Shortwave Radiation',
}

MERGED_WEATHER_COLS_RENAME = {
  'Precipitation': 'Origin Precipitation', 
  'Rain': 'Origin Rain', 
  'Snowfall': 'Origin Snowfall',
  'Windspeed': 'Origin Windspeed', 
  'Windgusts': 'Origin Windgusts',
  'Evapotranspiration': 'Origin Evapotranspiration',
  'Shortwave Radiation': 'Origin Shortwave Radiation',
}

AIRPORT_COLS_RENAME = {
  'Airport': 'Origin', 
  'TotalOperations': 'Total Operations', 
}

AIRPORT_COLS = [
  'Year',
  'Month',
  'Origin',
  'Total Operations',
]

MERGED_AIRPORT_COLS_RENAME = {
  'Total Operations': 'Origin Total Operations',
}

EDA_WITHOUT_AIRLINE_COLS = [
  'Origin Total Operations',
  'Origin Precipitation', 'Origin Rain', 'Origin Snowfall', 
  'Origin Windspeed', 'Origin Windgusts', 'Origin Evapotranspiration',
  'Origin Shortwave Radiation',
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
