import requests
import json
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.bank_account import Bank_Account
from server import db, client_id, secret, plaid_address, key
from cryptography.fernet import Fernet



class Item:
    def __init__(self,data):
        self.id = data['id']
        self.plaid_item_id = data['plaid_item_id']
        self.access_token = data['access_token']
        self.family_id = data['family_id']
        self.create_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    #This exchanges the public token for the permenant access token that will need to be stored in the DB
    def exchange_pub_tok(cls, data,family_id):
        url = f"{plaid_address}/item/public_token/exchange"

        payload = json.dumps({
            "client_id": client_id,
            "secret": secret,
            "public_token": data['public_token']
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        results = json.loads(response.text)
        
        access_token = results['access_token'].encode()
        f_obj = Fernet(key)
        encrypted_access_token = f_obj.encrypt(access_token)
        
        data = {
            "access_token": encrypted_access_token,
            "plaid_item_id": results['item_id'],
            "family_id": family_id
        }
        data = Item.register_item(data)
        return Bank_Account.initialize_accounts(data)

    @classmethod
    def register_item(cls,data):
        query = "INSERT INTO items (plaid_item_id, access_token,family_id) VALUES (%(plaid_item_id)s,%(access_token)s,%(family_id)s)"
        connectToMySQL(db).query_db(query,data)
        query = "SELECT id FROM items WHERE plaid_item_id = %(plaid_item_id)s"
        results = connectToMySQL(db).query_db(query,data)
        data['item_id'] = results[0]['id']
        return data
        

    @staticmethod
    #This create the link token that will be used for the LINK FLOW process
    def create_link_token(user_id):
        url = f"{plaid_address}/link/token/create"

        payload = json.dumps({
            "client_id": client_id,
            "secret": secret,
            "client_name": "NA",
            "country_codes": ["US"],
            "language": "en",
            "user": {"client_user_id": f'{user_id}'},
            "products": ["transactions"]
            })
        headers = {'Content-Type': 'application/json'}

        response = requests.request("POST", url, headers=headers, data=payload)
        results = json.loads(response.text)
        return results

    @staticmethod
    def get_family_items(data):
        query = "SELECT items.id AS items_id, access_token FROM families LEFT JOIN items ON families.id = items.family_id WHERE families.id = %(family_id)s;"
        results = connectToMySQL(db).query_db(query,data)
        return results

    """CHANGED MY MIND NOT USING THIS AT THIS TIME"""
    @staticmethod
    def get_fimaily_item_ids(data):
        query = "SELECT id FROM items WHERE family_id = %(family_id)s;"
        results = connectToMySQL(db).query_db(query,data)
        return results[0]
