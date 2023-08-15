from flask import Flask, Response, request
from sqlalchemy import extract
from services import datetime_converser, current_month, pattern_response
from database_setup import db, path_data_base
from datetime import datetime
from model import Expense, PaymentEnum
import sqlite3
import json


# INICIANDO A APLICAÇÃO
app = Flask(__name__)


# CONFIGURANDO E INICIANDO O BANCO DE DADOS COM A APLICAÇÃO
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path_data_base
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
        db.create_all()


# MÉTODO GET
@app.route('/api/despesas', methods=['GET'])
def get_expenses():
    expenses_object = Expense.query.filter(
        extract('month', Expense.date) == current_month()).all()
    # Assuming expenses_object is a list
    if len(expenses_object) != 0:
        # Convertendo para uma lista com Json
        expenses_json = []
        for expense in expenses_object:
            expenses_json.append(expense.convert_object_to_json())
        # Convertendo a data
        json_data = json.dumps(expenses_json, default=datetime_converser)
        statusCode = Response.status_code
        print(statusCode)
        return pattern_response(json_data, True, 200)
    else:
        return pattern_response(None, False, 404)
    

# MÉTODO POST
@app.route('/api/despesas', methods=['POST'])
def post_expense():
    body = request.get_json()

    # Validações dos campos
    required_fields = ["value", "description", "category", "date", "payment"]
    if not all(field in body for field in required_fields):
        return pattern_response(None, False, 400)

    value = body.get("value")
    if not isinstance(value, (int, float)) or value <= 0:
        return pattern_response(None, False, 400)

    date_str = body.get("date")
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception as e:
        return pattern_response(None, False, 400)

    payment_str = body.get("payment").lower()
    valid_payment_values = [payment.value.lower() for payment in PaymentEnum]
    if payment_str not in valid_payment_values:
        return pattern_response(None, False, 400)
    
    description = body.get("description")
    category = body.get("category")

    try:      
        payment = PaymentEnum(payment_str)
        
        new_expense = Expense(
            value=value,
            description=description,
            category=category,
            date=date,
            payment=payment)
   
        db.session.add(new_expense)
        db.session.commit()
        return pattern_response(new_expense.return_sucess_post(), True, 201)

    except Exception as e:
        return pattern_response(None, False, 400)


# EXECUTAR O SERVIDOR
if __name__ == '__main__':
    app.run(debug=True)
