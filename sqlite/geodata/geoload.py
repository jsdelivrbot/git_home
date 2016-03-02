import urllib
import sqlite3
import json
import time
import ssl

# If you are in China use this URL:
# serviceurl = "http://maps.google.cn/maps/api/geocode/json?"
serviceurl = "http://maps.googleapis.com/maps/api/geocode/json?" # pass the url

# Deal with SSL certificate anomalies Python > 2.7
#scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
scontext = None # optional

conn = sqlite3.connect('geodata.sqlite') # establish connection to sqlite
cur = conn.cursor() # define cursor

# create table to store location data
cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

fh = open("where.data") # make file handle on text data
count = 0 # count the stored locations
for line in fh:
    if count > 200 : break # define the upper limit of locations
    address = line.strip() # trim off spaces and \n
    print ''
    # buffer() gives a reference to the (full) slice of address
    cur.execute("SELECT geodata FROM Locations WHERE address= ?", (buffer(address), ))

    try:
        data = cur.fetchone()[0]
        print "Found in database ",address
        continue # if the address is found in the database it will be skipped
    except:
        pass

    print 'Resolving', address
    # create a full url of the location 
    url = serviceurl + urllib.urlencode({"sensor":"false", "address": address})
    print 'Retrieving', url
    uh = urllib.urlopen(url) # open the google url of the searched location
    data = uh.read() # read in the data
    print 'Retrieved',len(data),'characters',data[:20].replace('\n',' ')
    count = count + 1 # make a new count of the added location
    try: 
        js = json.loads(str(data)) # parse the returned JSON data
        # print js  # We print in case unicode causes an error
    except: 
        continue # if the data is not parsed correctly then ignore it

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') : 
        print '==== Failure To Retrieve ===='
        print data
        break

    # insert the location into database
    cur.execute('''INSERT INTO Locations (address, geodata) 
            VALUES ( ?, ? )''', ( buffer(address),buffer(data) ) )
    conn.commit() 
    time.sleep(1)

print "Run geodump.py to read the data from the database so you can visualize it on a map."
