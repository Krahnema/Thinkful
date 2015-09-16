# Record the number of bikes available every minute for an hour across all
# of NYC to see which station is the most active.
# Activity is defined as total number of bikes taken out or returned in an 
# hour.


import requests

r = requests.get('http://www.citibikenyc.com/stations/json')

r.text
# basic view of text type

r.json()
# formatted into JavaScript Object Notation

r.json().keys()
# get a list of all keys

r.json()['executionTime']
# string of time when file created

r.json()['stationBeanList']
# list of all stations

len(r.json()['stationBeanList'])
# number of docks


# test you have all fields for setting up database by gathering them together
key_list = []
for station in r.json()['stationBeanList']:
	for k in station.keys():
		if k not in key_list:
			key_list.append(k)

key_list


# get data into a data frame. You have to treat it differently because it is 
# in JSON format.

from pandas.io.json import json_normalize

df = json_normalize(r.json()['stationBeanList'])
# don't take the whole JSON, just the stationBeanList to create data frame


import matplotlib.pyplot as plt
import pandas as pd


# look at the range of available bikes
df['availableBikes'].hist()
plt.show()

# look at the range of total docks
df['totalDocks'].hist()
plt.show()

df['availableBikes'].mean()
df['availableDocks'].mean()
df['totalDocks'].mean()



test_list = []
for x in df['testStation']:
	if x == "True":
		test_list.append(x)

# There are no test stations	


df[df.statusValue == "Not In Service"].shape[0]
# subset the dataset to only not in service stations. .shape gives you 
# a data frame's dimensions. We are only interested in the first dimension,
# which is the number of rows, i.e. the number of stations not in service.


out_of_service_list = []
for x in df['statusValue']:
	if x != "In Service":
		out_of_service_list.append(x)

out_of_service_list.count("Not In Service")

# There are 144 stations not in service.


# data frame that only includes In Service stations
newdf = df[df.statusValue == "In Service"]

newdf['availableBikes'].mean()
newdf['availableBikes'].median()
# mean and median went up. Median went up drastically from 3 to 15


# Now we need to get everything in a database

import sqlite3 as lite

con = lite.connect('citi_bike.db')
cur = con.cursor()

with con:
	cur.execute('DROP TABLE citibike_reference')
	cur.execute('DROP TABLE available_bikes')

with con:
	cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT)')


sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

with con:
	for station in r.json()['stationBeanList']:
		cur.execute(sql, (station['id'], station['totalDocks'], station['city'], station['altitude'], station['stAddress2'], station['longitude'], station['postalCode'], station['testStation'], station['stAddress1'], station['stationName'], station['landMark'], station['latitude'], station['location']))


# We want to get multiple readings by minute so we need to have the
# availableBikes table be different. The station ID will be the column
# name, but it cannot start with a number, so we need to put a character
# in front.

# first extract the ID column from the data frame and put it into a list.
station_ids = df['id'].tolist()

# add the character to the station column and add data type for SQLite
station_ids = ['_' + str(x) + ' INT' for x in station_ids]

# now we can create the table. We will concatenate the string and joining
# all station ids in their new format
with con:
	cur.execute("CREATE TABLE available_bikes ( execution_time INT, " + ", ".join(station_ids) + ");")


import time
# a package with datetime objects

from dateutil.parser import parse
# this is a package for parsing a string into a Python datetime object

import collections

exec_time = parse(r.json()['executionTime'])
# the above string we created is now parsed into a Python datetime object

with con:
	cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))
# inserted into the database - the strftime('%s') will put it in seconds


id_bikes = collections.defaultdict(int)
# to store available bikes by station

for station in r.json()['stationBeanList']:
	id_bikes[station['id']] = station['availableBikes']
# loops through each station and adds them to our defaultdict

with con:
	for k, v in id_bikes.iteritems():
		cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")
# iterates through the defaultdict from above and updates the values in our
# database.


from time import sleep
'''

con = lite.connect('citi_bike.db')
cur = con.cursor
'''

with con:
	cur.execute('DELETE FROM available_bikes')

for i in range(60):
	r = requests.get('http://www.citibikenyc.com/stations/json', timeout = 0.001)
	exec_time = parse(r.json()['executionTime'])


	with con:
		cur.execute('INSERT INTO available_bikes (execution_time) VALUES(?)', (exec_time.strftime('%s'),))
		con.commit()
	
	id_bikes = collections.defaultdict(int)
	for station in r.json()['stationBeanList']:
		id_bikes[station['id']] = station['availableBikes']

	with con:
		for k, v in id_bikes.iteritems():
			cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")
			con.commit()

	sleep(60)


con.close()




# We want to see the change for each station for every minute. 
# To do so, we first need to process each column and calculate the change 
# each minute.

con = lite.connect('citi_bike.db')
cur = con.cursor()

df3 = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')


hour_change = collections.defaultdict(int)
for col in df3.columns:
	station_vals = df3[col].tolist() # make the columns into a list
	station_id = col[1:] # this gets rid of the '_' (underscore)
	station_change = 0
	for k, v in enumerate(station_vals):  # enumerate returns item and its index
		if k < len(station_vals) - 1:  # run the loop until k = index for second to last element
			station_change += abs(station_vals[k] - station_vals[k+1])  # add it to our new variable
	hour_change[int(station_id)] = station_change # converts it to an integer

# We are only interested in the column output, which is how many bikes are
# 	available.
# We then have to get rid of the underscore in front of the index: col[1:]
# Set an empty variable to 0 and then run a for loop: for each station value
#	we take the change to the next value (but absolute bc it could be negative).
# 	We add it all to the dictionary: the higher the number, the more active
#	the station because bikes are taken and brought back frequently.
# This change will then get to be added to the dictionary with each ID
#	corresponding to its change number.


# Which station is the busiest, so the most active?

def keywithmaxval(d): # creates a list of the dict's keys and values
	v = list(d.values())
	k = list(d.keys())
	return k[v.index(max(v))] #returns the key with the max value

max_station = keywithmaxval(hour_change) # apply function to our case

# now we can query the reference table we have created earlier for 
# information such as location

import datetime

cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print "The most active station is station id %s at %s latitude: %s longitude: %s " % data
print "With " + str(hour_change[max_station]) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df3.index[0])).strftime('%Y-%m-%d %H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df3.index[-1])).strftime('%Y-%m-%d %H:%M:%S')


plt.bar(hour_change.keys(), hour_change.values())
plt.show()










