from logging import StreamHandler
from dotenv import load_dotenv
import os, time, requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.create_db import CurrentCamera
from backend.database.create_cam_weather_zones import zones
import logging

load_dotenv()
request_string = os.getenv("MAP_SERVER_REQUEST")
engine = create_engine(os.getenv('SQLite_DB_LOC'))

zones_with_condition = []
for zone in zones:
    zones_with_condition.append([zone[0], zone[1], zone[2], 0])


def send_web_request(request_str):
    try:
        response = requests.get(request_str, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request to {request_str} returned status code {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print(f"Request to {request_str} timed out.")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred for {request_str}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request to {request_str}: {e}")
        return None


#look for offline cameras in json response, look for offline cameras in database
def prepare_changes_in_cam_info(data):
    #get offline list from data
    offline_list = []
    features = data.get('features', [])
    for feature in features:
        if feature[0]['attributes']['status'] == 'Offline':
            offline_list.append([feature[0]['attributes']['id'],
                                 feature[0]['attributes']['oid'],
                                 feature[0]['attributes']['status']])




def process_daily_weather_request(data, retry=5):
    for retry in range(1,6):
        try:
            sunrise = data['daily']['sunrise'][0]
            sunset = data['daily']['sunset'][0]
            return sunrise, sunset
        except KeyError:
            print("Daily key is missing from request")
    raise Exception("Dict from daily request had nothing to process")

def make_daily_request(retry = 5):
    initial_zone_lat = zones[0][1]
    initial_zone_lon = zones[0][2]
    daily_weather_request_1 = 'https://api.open-meteo.com/v1/forecast?latitude=' + str(
        initial_zone_lat) + '&longitude=' + str(initial_zone_lon)
    daily_weather_request_2 = '&daily=sunrise,sunset,daylight_duration,sunshine_duration,precipitation_probability_max&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timeformat=unixtime&timezone=America%2FNew_York&temporal_resolution=native&forecast_days=1'
    daily_weather_request = daily_weather_request_1 + daily_weather_request_2
    for i in range(1,retry+1):
        json = send_web_request(daily_weather_request)
        if type(json) is dict:
            return process_daily_weather_request(json)
        else:
            print("Request to open-meteo failed")
            time.sleep(60)
    raise Exception("Daily weather request could not be made")

def get_current_weather(lat, long):
    current_weather_request = ('https://api.open-meteo.com/v1/forecast?latitude='
                               + str(lat) + '&longitude=' + str(long)
                               +'&current=is_day,precipitation,rain,showers,snowfall,weather_code&minutely_15=precipitation,rain,snowfall,weather_code,is_day,diffuse_radiation_instant&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timeformat=unixtime&timezone=America%2FNew_York&temporal_resolution=native&forecast_days=1&forecast_minutely_15=4&models=best_match')
    for i in range(1, 4):
        json = send_web_request(current_weather_request)
        if type(json) is dict:
            return json
        else:
            print("Request to open-meteo failed")
            time.sleep(20)
    raise Exception("Current weather request could not be made")

def measure_conditions(zone_weather):

    #checking for precipitation
    internal_weather_code = 0
    current_dict = zone_weather['current']
    if current_dict['snowfall'] > 0:
        internal_weather_code = 2
    elif current_dict['rain'] > 0 or current_dict['showers'] > 0:
        internal_weather_code = 1

    #checking for darkness
    current_time = time.time()
    dark =  (current_time < (sunrise_time + 900)) or (current_time > (sunset_time - 900))

    if dark:
        internal_weather_code += 10

    #checking for imminent changes
    future_fifteen_dict = zone_weather['minutely_15']
    rain_expected = False
    for rain in future_fifteen_dict['rain']:
        if rain > 0.0:
            rain_expected = True
    snow_expected = False
    for snow in future_fifteen_dict['snowfall']:
        if snow > 0.0:
            snow_expected = True

    #passing along potential changes, increasing or decreasing sampling rate of weather
    #not putting in rain->snow or snow->rain currently
    expected_changes = (False, None)
    #from clear to rain
    if ((internal_weather_code == 0) or (internal_weather_code == 10 )) and rain_expected:
        if dark:
            expected_changes = (True,11)
        else:
            expected_changes = (True,1)
    #from clear to snow
    elif ((internal_weather_code == 0) or (internal_weather_code == 10)) and snow_expected:
        if dark:
            expected_changes = (True, 12)
        else:
            expected_changes = (True, 2)
    #from rain to clear
    elif ((internal_weather_code == 1) or (internal_weather_code == 11)) and not rain_expected:
        if dark:
            expected_changes = (True, 10)
        else:
            expected_changes = (True, 0)
    #from snow to clear
    elif ((internal_weather_code == 2) or (internal_weather_code == 12)) and not snow_expected:
        if dark:
            expected_changes = (True, 10)
        else:
            expected_changes = (True, 0)

    return internal_weather_code, expected_changes

#logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[StreamHandler()]
)

#starter
sunrise_time = 0
sunset_time = 0
start_indicator = True
condition_code = 0
imminent_weather_change = False


logging.info("Starting the main auxiliary loop.")#main auxiliary loop

###ADD IN HOURLY CHECK OF API FOR CAM STATUS
###NEEDED FOR PASS_TO_NEXT_LOOP in MAIN PROGRAM

while True:
    try:
        logging.info("Starting a new loop iteration.")
        #start the clock
        start_time = time.time()
        # starting and closing session each loop to ensure SQL writes are finished each loop
        Session = sessionmaker(bind=engine)
        session = Session()
        #change modes to night or day on start
        if start_indicator:
            daily_conditions = make_daily_request()
            sunrise_time = daily_conditions[0]
            sunset_time = daily_conditions[1]
            start_indicator = False
            logging.info(f"Updated sunrise_time: {sunrise_time}, sunset_time: {sunset_time}")

        #iterating through geographic zones
        for zone in zones_with_condition:
            logging.info(f"Processing zone: {zone[0]} at coordinates ({zone[1]}, {zone[2]})")
            zone_weather = get_current_weather(zone[1], zone[2])
            expected_weather = measure_conditions(zone_weather)

            if expected_weather[1][0]:
                imminent_weather_change = True

            #if there are changes in current conditions, update the database
            if expected_weather[0] != zone[3]:
                logging.info(f"Condition change detected for zone {zone[0]}: {zone[3]} -> {expected_weather[0]}")
                zone[3] = expected_weather[0]
                try:
                    all_cameras_in_zone =session.query(CurrentCamera).filter(CurrentCamera.zone == zone[0]).all()
                    for camera in all_cameras_in_zone:
                        camera.conditions = expected_weather[0]

                    session.commit()
                    logging.info(f"Database updated for zone {zone[0]}")
                except Exception as e:
                    session.rollback()
                    logging.error(f"Error updating database for zone {zone[0]}: {e}")

        session.commit()
        session.close()

        #normal hourly checks = 3600 seconds
        #half hourly checks on imminent change = 1800 seconds
        current_date_and_time = datetime.fromtimestamp(time.time())
        #-----------most constricted, if we change at the most rapid every 30 minutes, then we know switches for midnight across days will take place at hour 23
        if current_date_and_time.hour == 23:
            minutes_left = (60 - current_date_and_time.minute)
            #judging whether we can get another 30 min cycle in before the day change
            if imminent_weather_change:
                if minutes_left <= 40:
                    start_indicator = True
                    time.sleep((minutes_left+5) * 60)
                #if we can get a change in before midnight, wait normally
                else:
                    time.sleep(1800)
            #if imminent weather isn't a problem, then just go past midnight
            else:
                start_indicator = True
                time.sleep(3600)
        #-----if we are at any time of day and sunrise or sunset is coming up, we need to aim for that time to effectively switch in time
        # dark =  (current_time < (sunrise_time + 900)) or (current_time > (sunset_time - 900))
        elif 0 < (sunrise_time-600)-time.time() < 3600 :
            time_until_sunrise = (sunrise_time-600)-time.time()
            time.sleep(time_until_sunrise)
        elif 0 < (sunset_time - 600) - time.time() < 3600:
            time_until_sunset = (sunset_time - 600) - time.time()
            time.sleep(time_until_sunset)
        #----------------------------------
        #if it isn't the last hour and it isn't before sunset or sunrise, don't worry
        else:
            if imminent_weather_change:
                time.sleep(1800)
            else:
                time.sleep(3600)

    except Exception as e:
        logging.error(f"Unhandled error in main loop: {e}")
        break



#don't forget to reload database
