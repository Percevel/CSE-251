"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
from numpy import character
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
            #print(f'{self.response}/n')
        else:
            print('RESPONSE = ', response.status_code)

# TODO Add any functions you need here

def get_info(dal):
  threadl = []
  ret = []
  for x in dal:
    threadl.append(Request_thread(x))
  for x in threadl:
    x.start()
  for x in threadl:
    x.join()
    ret.append(x.response['name'])
  return ret


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')



    # TODO Retrieve Top API urls
    response = requests.get(TOP_API_URL)
    # TODO Retireve Details on film 6
    if response.status_code == 200:
        data = response.json()
        #print(data)

		# Example to get person 1 url
        #print( f'{data["films"]}6')
        theUrl = Request_thread(f'{data["films"]}6')
        theUrl.start()
        theUrl.join()
        title = theUrl.response['title']
        director = theUrl.response['director']
        producer = theUrl.response['producer']
        release = theUrl.response['release_date']
        person = get_info(theUrl.response['characters'])
        planets = get_info(theUrl.response['planets'])
        starship = get_info(theUrl.response['starships'])
        vehicles = get_info(theUrl.response['vehicles'])
        species = get_info(theUrl.response['species'])

        print('----------------------------')
        print(f'Title: {title}')
        print(f'Director: {director}')
        print(f'Producer: {producer}')
        print(f'Release: {release}')

        print(f'Characters: {len(person)}')
        print(f'{person} \n')
        print(f'planets: {len(planets)}')
        print(f'{planets} \n')
        print(f'starship: {len(starship)}')
        print(f'{starship} \n')
        print(f'vehicles: {len(vehicles)}')
        print(f'{vehicles} \n')
        print(f'species: {len(species)}')
        print(f'{species} \n')
    else:
        print('Error in requesting ID')
    # TODO Display results

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
