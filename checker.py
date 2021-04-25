#!/usr/bin/env python3

import argparse
import time
import logging
import os
try:
  import requests
except ImportError:
  print("Trying to Install required module: requests\n")

  os.system('python3 -m pip install requests')
import requests



# url2 = "https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.ca.json?vaccineinfo"

# json_url = "https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{}.json?vaccineinfo"


def get_availability(state, cities):
    state = state.upper()
    cities =  [city.upper() for city in cities]

    url = f"https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{state}.json?vaccineinfo"
    
    ## Page header
    header_url = "https://www.cvs.com/immunizations/covid-19-vaccine"
    headers = {'Referer': header_url}

    try: 
        response =  requests.get(url, headers=headers)
        json = response.json()
        # logging.debug(json['responsePayloadData']['data'][state])
        status = {}
        for d in json['responsePayloadData']['data'][state]:
            # logging.debug(d['city'])
            if d['city'] in cities:
                status[d['city']] = d['status']
                # logging.debug(status)
        return status
    except:
        return {}
         
def check(every_x_mins, until_x_hours, state,cities):
    logging.info('Starting vaccine checker!\nctl+c to exit')

    every_x_mins = every_x_mins * 60
    until_x_hours = time.time() + until_x_hours * (60 * 60) 

    while time.time() < until_x_hours:
        for city, status in get_availability(state,cities).items():
            if status:
                logging.info(f'{city}\t{status}')
            else:
                logging.info(f'Something want error: city={city} status={status}')

        time.sleep(every_x_mins)

def main(): 

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

    # every_x_mins, until_x_hours = 1, 0.5
    # state, cities = "CA", ['san francisco']
    # check(every_x_mins, until_x_hours, state, cities)
    check(args.refresh, args.run_until, args.state, args.cities)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Check when vaccine appoinment becomes avaliable ')
    parser.add_argument("--run_until", '-u',
                        metavar="INT",
                        type=int,
                        help="Number of hours that scripts runs. Default [12]" ,
                        default=12)

    parser.add_argument("--refresh", '-r',
                        metavar='INT',
                        type=int,
                        help="Check every X mins. Default [10]",
                        default=10)

    parser.add_argument("--state", "-s",
                        metavar='STR',
                        help="State, ie: CA",
                        required=True)

    parser.add_argument("--cities", "-c",
                        metavar='STR',
                        nargs='+',
                        help="List of cities, ie: 'San Fernando' 'San Francisco' ",
                        required=True)

    # parse given command line arguments
    args = parser.parse_args()
    main()