from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.major_category_1 import Major_Category_1
from server import db, client_id, secret, plaid_address, key
import requests
import json
from datetime import date, timedelta
from cryptography.fernet import Fernet

class Transaction:
    def __init__(self,data):
        self.id = data['id']
        self.account_id = data['account_id']
        self.plaid_transaction_id = data['plaid_transaction_id']
        self.date = data['date']
        self.name= data['name']
        self.amount = data['amount']
        self.iso_currency_code = data['iso_currency_code']
        self.category_1 = data['category_1']
        self.category_2 = data['category_2']
        self.payment_channel = data['payment_channel']
        self.pending = data['pending']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def initializing_transaction(cls, transactions):
        for transaction in transactions:
            account_id = Transaction.get_account_id({"account_id": transaction['account_id']})
            plaid_transaction_id = transaction['transaction_id']
            
            if Transaction.verify_tranaction({'plaid_transaction_id':plaid_transaction_id}):
                continue

            if len(transaction['category'])>1:
                category_data = {
                    "major_cat": transaction['category'][0],
                    "minor_cat": transaction['category'][1]
                }
            else:
                category_data = {
                    "major_cat": transaction['category'][0],
                    "minor_cat": "None"
                }

            category_1_id = Major_Category_1.get_transaction_category_1_id(category_data)

            transaction_info = {
                "account_id": account_id['id'],
                "plaid_transaction_id": plaid_transaction_id,
                "date": transaction['date'],
                "name": transaction['name'],
                "amount": transaction['amount'],
                "iso_currency_code": transaction['iso_currency_code'],
                "category_1_id": category_1_id, 
                "category_2_id": 4, #THIS WILL NEED TO CHANGE LATER TO REFERENCE PREVIOUS AND CHANGE TO THE CAT2 value
                "payment_channel": transaction['payment_channel'],
                "pending": transaction['pending']
            }
            Transaction.register_transactions(transaction_info)
        return "success"


    @classmethod
    async def get_recent_transactions(cls, data):
        for item in data['items']:
            results = await Transaction.async_get_transactions(item)
            Transaction.initializing_transaction(results['transactions'])
        return "success"


    @staticmethod
    def get_account_id(data):
        query = "SELECT id FROM accounts WHERE plaid_account_id = %(account_id)s"
        results = connectToMySQL(db).query_db(query,data)
        return results[0]


    @staticmethod
    def register_transactions(data):
        query = "INSERT INTO transactions (account_id, plaid_transaction_id, date, name, amount, iso_currency_code, category_1_id, category_2_id, payment_channel, pending) VALUES (%(account_id)s, %(plaid_transaction_id)s, %(date)s, %(name)s, %(amount)s, %(iso_currency_code)s, %(category_1_id)s, %(category_2_id)s, %(payment_channel)s, %(pending)s)"
        return connectToMySQL(db).query_db(query,data)


    @staticmethod
    async def async_get_transactions(data):        
        url = f"{plaid_address}/transactions/get"

        offset = timedelta(-2)
        start_date = Transaction.get_last_transaction(data)
        start_date = start_date['date']
        start_date = start_date+offset
        end_date = date.today()

        decrypted_access_token = Transaction.decrypt_access_token(data['access_token'])

        payload = json.dumps({
            "client_id": client_id,
            "secret": secret,
            "access_token": decrypted_access_token,
            "start_date": date.strftime(start_date, "%Y-%m-%d"),
            "end_date": date.strftime(end_date, "%Y-%m-%d")
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.text)
        return response


    @staticmethod
    def get_transactions_history(data):
        url = f"{plaid_address}/transactions/get"

        end_date = date.today()
        start_date = end_date.replace(year= end_date.year -1)

        decrypted_access_token = Transaction.decrypt_encoded_access_token(data['access_token'])

        payload = json.dumps({
        "client_id": client_id,
        "secret": secret,
        "access_token": decrypted_access_token,
        "start_date": date.strftime(start_date, "%Y-%m-%d"),
        "end_date": date.strftime(end_date, "%Y-%m-%d")
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.text)
        return response


    @staticmethod
    def verify_tranaction(data):
        query = "SELECT * FROM transactions WHERE plaid_transaction_id = %(plaid_transaction_id)s"
        results = connectToMySQL(db).query_db(query,data)
        return results


    @staticmethod
    def get_last_transaction(data):
        query = "SELECT transactions.date FROM items LEFT JOIN accounts ON items.id = accounts.item_id LEFT JOIN transactions ON accounts.id = transactions.account_id WHERE items.id = %(items_id)s ORDER BY transactions.date desc LIMIT 1;"
        result = connectToMySQL(db).query_db(query,data)
        return result[0]


    @staticmethod
    def get_account_transactions(data):
        if data['account_id'] != "all":
            query = "SELECT transactions.* FROM families LEFT JOIN items ON families.id = items.family_id LEFT JOIN accounts ON items.id = accounts.item_id LEFT JOIN transactions ON accounts.id = transactions.account_id WHERE families.id = %(family_id)s AND accounts.id = %(account_id)s AND transactions.date BETWEEN %(start_date)s AND %(end_date)s ORDER BY transactions.date desc;"
        else:
            query = "SELECT transactions.* FROM families LEFT JOIN items ON families.id = items.family_id LEFT JOIN accounts ON items.id = accounts.item_id LEFT JOIN transactions ON accounts.id = transactions.account_id WHERE families.id = %(family_id)s AND transactions.date BETWEEN %(start_date)s AND %(end_date)s ORDER BY transactions.date desc;"
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def decrypt_access_token(token):
        token = token.encode()
        f_obj = Fernet(key)
        decrypted_access_token = f_obj.decrypt(token)
        decrypted_access_token = decrypted_access_token.decode('utf-8')
        return decrypted_access_token

    @staticmethod
    def decrypt_encoded_access_token(token):
        f_obj = Fernet(key)
        decrypted_access_token = f_obj.decrypt(token)
        decrypted_access_token = decrypted_access_token.decode('utf-8')
        return decrypted_access_token