from datetime import datetime
from flask import Response
from enum import Enum
import json


# FUNÇÃO QUE RETORNA O DATETIME PARA STRING 
def datetime_converser(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d')
        

# FUNÇÃO QUE RETORNA O MÊS CORRENTE EM STRING
def current_month():
    currentMonth = datetime.now().month
    currentMonth = "0" + str(7) if currentMonth < 10 else str(currentMonth)  
    return currentMonth


# FUNÇÃO PARA PADRONIZAR RESPONSE 
def pattern_response(data, sucess, status):
    body = {}
    body['data'] = data
    body['sucess'] = sucess
    return Response(json.dumps(body), status=status, mimetype="application/json")
