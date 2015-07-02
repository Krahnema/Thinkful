import sqlite3 as lite
import pandas as pd

con = lite.connect('getting_started.db')

cities = (('New York City', 'NY'), ('Boston', 'MA'), ('Chicago', 'IL'), ('Miami', 'FL'), ('Dallas', 'TX'), ('Seattle', 'WA'), ('Portand', 'OR'), ('San Francisco', 'CA'), ('Los Angeles', 'CA'))

weather = (('New York City', 2013, 'July', 'January', 62), ('Boston', 2013, 'July', 'January', 59), ('Chicago', 2013, 'July', 'January', 59), ('Miami', 2013, 'August', 'January', 84), ('Dallas', 20123, 'July', 'January', 77), ('Seattle', 2013, 'July', 'January', 61), ('Portland', 2013, 'July', 'December', 63), ('San Francisco', 2013, 'September', 'December', 64), ('Los Angeles', 2013, 'September', 'December', 75))

with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS cities")
	cur.execute("DROP TABLE IF EXISTS weather")
	cur.execute("CREATE TABLE cities (name text, state text)")
	cur.execute("CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)")
	cur.executemany("INSERT INTO cities VALUES(?, ?)", cities)
	cur.executemany("INSERT INTO weather VALUES(?, ?, ?, ?, ?)", weather)
	cur.execute("INSERT INTO cities VALUES('Washington', 'DC')")
	cur.execute("INSERT INTO weather VALUES('Washington', 2013, 'July', 'January', 60)")
	cur.execute("SELECT name, state FROM weather INNER JOIN cities on name = city WHERE warm_month = 'July'")
	rows = cur.fetchall()
	df = pd.DataFrame(rows)


with con:
	cur = con.cursor()
	cur.execute("SELECT name, state FROM weather INNER JOIN cities on name = city WHERE warm_month = 'July'")
	data = cur.fetchall()
	df2 = pd.DataFrame(data)
	str = ', '

	def July_func(x):
		for y in x:
			print str.join(y) ,



	print "The cities that are warmest in July are:" ,
	for i in df2.index:
   		print df2[0][i] + ", " + df2[1][i] + ", " ,
   		
	# July_func(data)

	# print "The cities that are warmest in July are: " + df.ix[0][0] + ", " + df.ix[0][1]

	# for i in data:
		# print df.ix[i][0] + ", " + df.ix[i][1]

	# for index, row in df.iterrows():
		# print row[0] + ", " + row[1]
		# print str.join(row)




	# print "The cities that are warmest in July are:"
	# {}".format(July_func(data))

	# for x in data:
		# print "The cities that are the warmest in July are: {}".format(str.join(x))

	# print "The cities that are warmest in July are: {}".format(data)













