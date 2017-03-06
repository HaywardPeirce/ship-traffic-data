#from lxml import html
import requests
import json
import time
import os
from subprocess import *
import xlrd
import csv

lastCheckTime = {
    "sources":[
    {
        "name":"PMV",
        "file":"lastPMVCheckTime.txt",
        "time": 0
    },
    {
        "name":"PPA",
        "file":"lastPilotCheckTime.txt",
        "time": 0
    }
    ]
}

#print(getShips())

#page = requests.get('https://pilot.kleinsystems.com/public/PPA/PPA_CurrentTraffic.aspx')

#tree = html.fromstring(page.content)

#ships = tree.xpath('//tr[@class="dxgvFocusedRow_Office2003_Silver"]/text()')

file = open('piloturl.txt', 'r')
pilotURL = file.readline().replace("\n", '')
file.close()
    
#get the number of each type of ship in the harbour
def getPMVShipTypes():
    
    pmvdata = checkPMVShips()
    
    pmvshiptypes = pmvdata['VesselReport']['InPortList']
    
    return pmvshiptypes

#get the list of ships in port
def getPMVShips():
    
    pmvdata = checkPMVShips()
    
    pmvships = pmvdata['VesselReport']['InPortDetail']

    # each ship name can be references using pmvships[0]['Vessel_Name']
    return pmvships

#main fuction called to lookup list of PPA ships
def getPilotShips():
    pilotdata = checkPilotShips()
    
    return pilotdata

#retrieve the PMV data, If data is over an hour old retrieve a new copy
def checkPMVShips():
    tempTime = time.time()
    
    #print type(lastCheckTime['sources'][0]['time'])
    
    lastCheckTime['sources'][0]['time'] = LastCheckTime(lastCheckTime['sources'][0]['file'], lastCheckTime['sources'][0]['time'])
    
    #print type(lastCheckTime['sources'][0]['time'])
    
    print 'timedif: ' + str(tempTime - lastCheckTime['sources'][0]['time'])
    
    if (tempTime - lastCheckTime['sources'][0]['time']) > 3600:
        
        pmvresponse = requests.get('http://www1.portmetrovancouver.com/COGS_Chart/Mobile/GetCurrentData')
        
        putVanPortFile(pmvresponse.json())
        LastCheckTime(lastCheckTime['sources'][0]['file'], str(tempTime))
    
    pmvdata = getVanPortFile()
    
    return pmvdata
    
def checkPilotShips():
    tempTime = time.time()
    
    lastCheckTime['sources'][1]['time'] = LastCheckTime(lastCheckTime['sources'][1]['file'], lastCheckTime['sources'][1]['time'])
    
    print 'timedif: ' + str(tempTime - lastCheckTime['sources'][1]['time'])
    
    if (tempTime - lastCheckTime['sources'][1]['time']) > 3600:
        
        #pilotresponse = requests.get(pilotURL)
        
        run_cmd(pilotURL)
        
        xls_to_csv()
    
    pilotdata = getPilotFile()
    
    return pilotdata

#without arguments lookup last time the data from PMV was retrieved, with arguement of time, write that to file
def LastCheckTime(filename, *tempTime):
    
    #print filename
    #print type(filename)
    
    #print tempTime[0]
    #print type(tempTime)
    
    if os.path.isfile(filename):
        if (tempTime):
            file = open(filename, 'w')
            file.write(str(tempTime[0]))
            file.close()
            
            return float(tempTime[0])
            
        else:
            file = open(filename, 'r')
            time = file.readline().replace("\n", '')
            file.close()
            
            return float(time)
    else: 
        file = open(filename, 'w')
        file.write('0')
        file.close()
        return 0



#write the PMV request JSON to file
def putVanPortFile(pmvdata):
    with open('./vanPortCurrentData.json', 'w') as outfile:
        json.dump(pmvdata, outfile)

#get the PMV JSON from file
def getVanPortFile():
    with open('./vanPortCurrentData.json') as sources_file:    
        data = json.load(sources_file)
    
    return data
    
#get the PPA CSV file
def getPilotFile():
    
    with open('pilotships.csv', 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print ', '.join(row)
    
    return data
    
def xls_to_csv():

    x =  xlrd.open_workbook('pilotships.xls')
    x1 = x.sheet_by_name('Sheet1')
    csvfile = open('pilotships.csv', 'wb')
    writecsv = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        writecsv.writerow(x1.row_values(rownum))

    csvfile.close()
    
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output