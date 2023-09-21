# models.py

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['pau_para_toda_obra']

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Professional:
    def __init__(self, name, email, password, company_name, services, whatsapp, price_range, image_url=None):
        self.name = name
        self.email = email
        self.password = password
        self.company_name = company_name
        self.services = services
        self.whatsapp = whatsapp
        self.price_range = price_range
        self.image_url = image_url  # New field for image URL
