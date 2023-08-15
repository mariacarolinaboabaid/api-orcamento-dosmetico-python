from flask_sqlalchemy import SQLAlchemy
import os

# CONFIGURAÇÃO DO BANCO DE DADOS
path_directory = os.path.abspath(os.path.dirname(__file__))
data_base_name = 'bancoDados.sqlite'
path_data_base = os.path.join(path_directory, data_base_name)

db = SQLAlchemy()


