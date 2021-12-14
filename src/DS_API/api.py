from flask import Blueprint, request, jsonify
from bs4 import BeautifulSoup
import requests, json, re


bp = Blueprint('api_v1', __name__, url_prefix="/api")

@bp.route('/results', methods=["post"])
def results():
    
    # the server wants unencrypted form data from us... so we give it exactly that
    # this exploits a CSRF vulnerability in the website. 
    # There doesn't seem to be any check to make sure that the request 
    # really originated where it's supposed to 
    payload = {
        "id": request.json["id"],
        "passwd": request.json["passwd"],
    }
    
    # since this API is deprecated and i don't know any active OKUSON servers, 
    # i just did the bare minimum to set one up. see
    # https://www.math.rwth-aachen.de/~OKUSON/ for more info
    # url = f'https://www2.math.rwth-aachen.de/DS${request.json["year"]}/QueryResults'
    url_local = f'http://localhost:8324/QueryResults' 
    req = requests.post(url_local, data=payload)
    
    return jsonify(get_results(req.text))
    
# so you got html data, now you need a nice object you can send, this is where it gets made.
def get_results(html_doc: str) -> list:
    document = BeautifulSoup(html_doc, 'html.parser')
    point_patt = r'^(?P<pts>\d{1,2})'
    arr = []
    
    # get all rows from the results table
    for rows in document.find_all("tr"):
        columns = rows.contents # get columns
        
        # check if columns exist and whether they are columns and not table headers
        if columns[0].name == "td" and len(columns) > 0:
            online = re.search(point_patt, columns[1].string)
            
            # the basic response object. we assume that there is at least one set of points.
            # if that's not filled... good luck
            obj = {
                "exNum": int(columns[0].string),
                "points": {
                    "online": online.group("pts") if online != None else 0
                }
            }
            
            # don't give information that doesn't exist in the first place. 
            # this actually fixes a bug from the NodeJS version
            if len(columns) > 2: 
                written =  re.search(point_patt, columns[2].string)
                obj["points"]["written"] = written.group("pts")
            
            arr.append(obj)
        
    return arr
