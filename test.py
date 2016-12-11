from lxml import html
import requests
import json

page = requests.get('https://pilot.kleinsystems.com/public/PPA/PPA_CurrentTraffic.aspx')


tree = html.fromstring(page.content)


ships = tree.xpath('//tr[@class="dxgvFocusedRow_Office2003_Silver"]/text()')

pmvrequest = requests.get('http://www1.portmetrovancouver.com/COGS_Chart/Mobile/GetCurrentData')

pmvshiptypes = pmvrequest.json()['VesselReport']['InPortList']

pmvships = pmvrequest.json()['VesselReport']['InPortDetail']

# each ship name can be references using pmvships[0]['Vessel_Name']

print ships

