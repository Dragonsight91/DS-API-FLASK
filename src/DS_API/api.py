from flask import Blueprint, request, jsonify
from bs4 import BeautifulSoup
import requests, json, re


api_bp = Blueprint('api_v1', __name__, url_prefix="/api")

@api_bp.route('/results', methods=["post"])
def results():
    
    payload = {
        "id": request.json["id"],
        "passwd": request.json["passwd"],
    }
    
    #url = f'https://www2.math.rwth-aachen.de/DS${request.json["year"]}/QueryResults'
    url_local = f'http://localhost:8324/QueryResults'
    req = requests.post(url_local, data=payload)
    
    return jsonify(get_results(req.text))
    

def get_results(html_doc: str) -> list:
    document = BeautifulSoup(html_doc, 'html.parser')
    point_patt = r'^(?P<pts>\d{1,2})'
    arr = []
    
    
    for rows in document.find_all("tr"):
        columns = rows.contents
        
        if columns[0].name == "td" and len(columns) > 0:
            online = re.search(point_patt, columns[1].string)
            
            obj = {
                "exNum": int(columns[0].string),
                "points": {
                    "online": online.group("pts")
                }
            }
            
            if len(columns) > 2: 
                written =  re.search(point_patt, columns[2].string)
                obj["points"]["written"] = written.group("pts")
            
            arr.append(obj)
        
    return arr
