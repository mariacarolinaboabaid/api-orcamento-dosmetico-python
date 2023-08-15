from database_setup import db
from enum import Enum


# CLASSE TIPO DE PAGAMENTO E DESPESA
class PaymentEnum(Enum):
    DINHEIRO = 'dinheiro'
    DEBITO = 'debito'
    CREDITO = 'credito'
    PIX = 'pix'


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    payment = db.Column(db.Enum(PaymentEnum), nullable=False,
                        default=PaymentEnum.DINHEIRO)


    def convert_object_to_json(self):
        return {"id": self.id,
                "value": self.value,
                "description": self.description,
                "category": self.category,
                "date": self.date,
                "payment": self.payment.value}
        
        
    def return_sucess_post(self):
        return {"id": self.id }