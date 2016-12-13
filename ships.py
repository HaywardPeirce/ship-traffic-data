#from lxml import html
import requests
import json
import time
import os

lastCheckTime = 0
#print(getShips())

#page = requests.get('https://pilot.kleinsystems.com/public/PPA/PPA_CurrentTraffic.aspx')

#tree = html.fromstring(page.content)

#ships = tree.xpath('//tr[@class="dxgvFocusedRow_Office2003_Silver"]/text()')

#retrieve the PMV data, If data is over an hour old retrieve a new copy
def checkShips():
    tempTime = time.time()
    
    lastCheckTime = LastCheckTime()
    
    print 'timedif: ' + str(tempTime - lastCheckTime)
    
    if (tempTime - lastCheckTime) > 3600:
        
        pmvresponse = requests.get('http://www1.portmetrovancouver.com/COGS_Chart/Mobile/GetCurrentData')
        
        putVanPortFile(pmvresponse.json())
        LastCheckTime(str(tempTime))
    
    pmvdata = getVanPortFile()
    
    return pmvdata

#without arguments lookup last time the data from PMV was retrieved, with arguement of time, write that to file
def LastCheckTime(*tempTime):
      
    if os.path.isfile('lastCheckTime.txt'):
        if (tempTime):
            file = open('lastCheckTime.txt', 'w')
            file.write(str(tempTime[0]))
            file.close()
            
        else:
            file = open('lastCheckTime.txt', 'r')
            time = file.readline().replace("\n", '')
            file.close()
            
            return float(time)
    else: 
        file = open('lastCheckTime.txt', 'w')
        file.write('0')
        file.close()
        return 0

#get the number of each type of ship in the harbour
def getShipTypes():
    
    pmvdata = checkShips()
    
    pmvshiptypes = pmvdata['VesselReport']['InPortList']
    
    return pmvshiptypes

#get the list of ships in port
def getShips():
    
    pmvdata = checkShips()
    
    pmvships = pmvdata['VesselReport']['InPortDetail']

    # each ship name can be references using pmvships[0]['Vessel_Name']
    return pmvships

#write the PMV request JSON to file
def putVanPortFile(pmvdata):
    with open('./vanPortCurrentData.json', 'w') as outfile:
        json.dump(pmvdata, outfile)

#get the PMV JSON from file
def getVanPortFile():
    with open('./vanPortCurrentData.json') as sources_file:    
        data = json.load(sources_file)
    
    return data