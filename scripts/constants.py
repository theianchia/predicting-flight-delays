WEATHER_OUTPUT_DIR = 'cleaned_weather'
AIRLINE_OUTPUT_DIR = 'cleaned_airline'
AIRPORT_OUTPUT_DIR = 'cleaned_airport'
AIRPLANE_OUTPUT_DIR = 'cleaned_airplane'

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
  'Flight Delay'
]

AIRLINE_COLS_RENAME = {
  'FL_DATE': 'Date',
  'ORIGIN': 'Origin',
  'DEST': 'Destination',
  'OP_CARRIER': 'Carrier',
  'OP_CARRIER_FL_NUM': 'Flight Num',
  'CRS_DEP_TIME': 'Departure Time',
  'DISTANCE': 'Distance',
  'DEP_DELAY': 'Departure Delay'
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

CARRIER_FEATURES = ["ORIGIN", "DEST", "UNIQUE_CARRIER",  "AIRCRAFT_TYPE", "SEATS"]

AIRPLANE_FEATURES = ["aircraft_type", "age"]

CARRIER_COLS_RENAME = {
    "ORIGIN": "Origin",
    "DEST": "Destination",
    "UNIQUE_CARRIER": "Carrier Code",
    "YEAR": "Year",
    "MONTH": "Month",
    "AIRCRAFT_TYPE": "Airplane",
    "SEATS": "Seats"
}

AIRPLANE_COLS_RENAME = {
    "aircraft_type": "Airplane",
    "age": "Airplane Age",
}

MERGED_ORIGIN_AIRPORT_COLS_RENAME = {
  'Total Operations': 'Origin Total Operations',
}

MERGED_DEST_AIRPORT_COLS_RENAME = {
  'Total Operations': 'Destination Total Operations',
}

MERGED_ORIGIN_WEATHER_COLS_RENAME = {
  'Precipitation': 'Origin Precipitation', 
  'Rain': 'Origin Rain', 
  'Snowfall': 'Origin Snowfall',
  'Windspeed': 'Origin Windspeed', 
  'Windgusts': 'Origin Windgusts',
  'Evapotranspiration': 'Origin Evapotranspiration',
  'Shortwave Radiation': 'Origin Shortwave Radiation',
}

MERGED_DEST_WEATHER_COLS_RENAME = {
  'Precipitation': 'Destination Precipitation', 
  'Rain': 'Destination Rain', 
  'Snowfall': 'Destination Snowfall',
  'Windspeed': 'Destination Windspeed', 
  'Windgusts': 'Destination Windgusts',
  'Evapotranspiration': 'Destination Evapotranspiration',
  'Shortwave Radiation': 'Destination Shortwave Radiation',
}

EDA_WITHOUT_AIRLINE_COLS = [
  'Seats',	'Airplane Age',
  'Distance', 'Departure Time',
  'Origin Total Operations',
  'Origin Precipitation', 'Origin Rain', 'Origin Snowfall', 
  'Origin Windspeed', 'Origin Windgusts', 'Origin Evapotranspiration',
  'Origin Shortwave Radiation',
  'Destination Total Operations',
  'Destination Precipitation', 'Destination Rain', 'Destination Snowfall', 
  'Destination Windspeed', 'Destination Windgusts', 'Destination Evapotranspiration',
  'Destination Shortwave Radiation',
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
