# views.py

from flask import render_template
from flask import request
from app import app

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now you can import your module
import ships

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")
    
@app.route('/list')
def list():
    listType = request.args.get('listType')
    
    print 
    
    if listType == 'pmvShips':
        listEntries = ships.getPMVShips()
    elif listType == 'pmvShipTypes': 
        listEntries = ships.getPMVShipTypes()
    elif listType == 'pilotShips': 
        listEntries = ships.getPilotShips()
    else: listEntries = ships.getPMVShips()
    
    return render_template('list.html', listEntries=listEntries)
    
    