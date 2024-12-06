"""
Implementação da classe e seus métodos de interação com Banco de Dados

Author: Jean Lima
"""

import sqlalchemy as sal

#Classe conectora
class DataBaseConnector():
    def __init__(self, path):
        self.engine = sal.create_engine(path)

    def connect(self):
        self.conn = self.engine.connect()
    
    def close(self):
        self.conn.close()
        self.engine.dispose()