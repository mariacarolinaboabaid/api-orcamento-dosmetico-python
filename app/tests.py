import unittest
import json
import requests
from app import app
from database_setup import db 
from model import Expense, PaymentEnum
from flask import Flask
from datetime import datetime, date


class TestApp(unittest.TestCase):
    
    # Configurando o ambiente Flask para testes
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app = app.test_client()    
        
        with app.app_context():
            db.session.query(Expense).delete()
            db.session.commit()    
    
    # Test Get 200
    def test_get_expenses_success(self):
        
        expense_test1 = Expense(
            value=100.50,
            description="Teste 1",
            category="Testando",
            date=datetime.now().date(),
            payment=PaymentEnum.DINHEIRO
        )
        
        expense_test2 = Expense(
            value=50.75,
            description="Teste 2",
            category="Testando",
            date=date(2023, 6, 5),
            payment=PaymentEnum.DINHEIRO
        )

        with app.app_context():
            db.session.add(expense_test1)
            db.session.add(expense_test2)
            db.session.commit()

        response = self.app.get('/api/despesas')
        
        response_json = response.get_data(as_text=True)
        response_object = json.loads(response_json)
        
        data_json = response_object['data']
        sucess = response_object['sucess']
        data = json.loads(data_json) 
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['value'], 100.50)
        self.assertEqual(data[0]['description'], 'Teste 1')
        self.assertEqual(data[0]['category'], 'Testando')
        self.assertEqual(sucess, True)
   
   
    # Test Get 404
    def test_get_expenses_not_found(self):
        response = self.app.get('/api/despesas')
        
        response_json = response.get_data(as_text=True)
        response_object = json.loads(response_json)
        
        data_json = response_object['data']
        sucess = response_object['sucess']
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data_json, None)
        self.assertEqual(sucess, False)


    # Test Post 200 - Cenário de Sucesso
    def test_post_expense_success(self):
        data = {
            'value': 100.00,
            'description': 'Teste 3',
            'category': 'Testando',
            'date': '2023-04-21',
            'payment': 'dinheiro'
        }

        response = self.app.post('/api/despesas', data=json.dumps(data), content_type='application/json')
        response_json = json.loads(response.get_data(as_text=True))
        
        data_json = response_json['data']
        sucess = response_json['sucess']

        self.assertEqual(response.status_code, 201)
        self.assertEqual(sucess, True)
        self.assertIsNotNone(data_json)
        self.assertEqual(response_json['data']['id'], 1)


    # Test Post 400 - Sem o preenchimento de todos os campos
    def test_post_expense_missing_fields(self):
        data = {
            'value': 100,
            'description': 'Teste 4',
        }

        response = self.app.post('/api/despesas', data=json.dumps(data), content_type='application/json')
        response_json = json.loads(response.get_data(as_text=True))
        
        data_json = response_json['data']
        sucess = response_json['sucess']

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data_json, None)
        self.assertEqual(sucess, False)
        
        
    # Test Post 400 - Campo valor com negativo
    def test_post_expense_invalid_value(self):
        data = {
            'value': -50,
            'description': 'Teste 5',
            'category': 'Testando',
            'date': '2023-07-21',
            'payment': 'dinheiro'
        }

        response = self.app.post('/api/despesas', data=json.dumps(data), content_type='application/json')
        response_json = json.loads(response.get_data(as_text=True))
        
        data_json = response_json['data']
        sucess = response_json['sucess']

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data_json, None)
        self.assertEqual(sucess, False)
        

    # Test Post 400 - Campo data com formato inválido
    def test_post_expense_invalid_date(self):
        data = {
            'value': 100,
            'description': 'Teste 6',
            'category': 'Testando',
            'date': '2023/07/21',  
            'payment': 'dinheiro'
        }

        response = self.app.post('/api/despesas', data=json.dumps(data), content_type='application/json')
        response_json = json.loads(response.get_data(as_text=True))
        
        data_json = response_json['data']
        sucess = response_json['sucess']

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data_json, None)
        self.assertEqual(sucess, False)
        

    # Test Post 400 - Campo EnumPayment inválido
    def test_post_expense_invalid_payment(self):
        data = {
            'value': 100,
            'description': 'Teste 7',
            'category': 'Testando',
            'date': '2023-07-21',
            'payment': 'INVALID_PAYMENT'  
        }

        response = self.app.post('/api/despesas', data=json.dumps(data), content_type='application/json')
        response_json = json.loads(response.get_data(as_text=True))
        
        data_json = response_json['data']
        sucess = response_json['sucess']

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data_json, None)
        self.assertEqual(sucess, False)
        
        
if __name__ == '__main__':
    unittest.main()


