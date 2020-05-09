from jira import JIRA
from prefect import task, Flow, Parameter
from prefect.tasks.secrets import PrefectSecret
from prefect.tasks.airtable.airtable import WriteAirtableRow
import googlemaps
from datetime import datetime

airtable_key = 'keyHKEqYHW4scXnKi'
gmaps_key = 'AIzaSyBjmn3npk07CADF9HEQhyZZR-TJ7p_LemA'

@task
def getDrivingDistance(home, destination):
    gmaps = googlemaps.Client(gmaps_key)
    # Geocoding an address
    home_string = home
    home_geocode = gmaps.geocode(home_string)
    destination_string = destination
    other_geocode = gmaps.geocode(destination_string)
    # Look up an address with reverse geocoding
    #reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions(home_string,
                                    destination_string,
                                    mode="driving",
                                    departure_time=now)
    return directions_result[0]['legs'][0]['duration']['text']

putIntoAirTable = WriteAirtableRow()

with Flow(name='DrivingDistance') as flow:
    home = Parameter('home', default = '530 Grand Street, New York, NY' )
    destination = Parameter('destination', default = '298 Stony Kill Road, Accord, NY')
    driveTime = getDrivingDistance(home= home, destination = destination)
    putIntoAirTable(data={'Drive Time':driveTime, 'Name': destination}, base_key = 'appumtumKiwnohjlO', table_name='prospects', api_key=airtable_key)

# flow.run() 
flow.register('Jenny')