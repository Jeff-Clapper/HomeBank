from flask_app.config.mysqlconnection import connectToMySQL
from server import db, client_id, secret, plaid_address
import requests
import json
from datetime import date, timedelta

class Transaction:
    def __init__(self,data):
        self.id = data['id']
        self.account_id = data['account_id']
        self.plaid_transaction_id = data['plaid_transaction_id']
        self.date = data['date']
        self.name= data['name']
        self.amount = data['amount']
        self.iso_currency_code = data['iso_currency_code']
        self.category = data['category']
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

            transaction_info = {
                "account_id": account_id['id'],
                "plaid_transaction_id": plaid_transaction_id,
                "date": transaction['date'],
                "name": transaction['name'],
                "amount": transaction['amount'],
                "iso_currency_code": transaction['iso_currency_code'],
                "category": transaction['category'][0], #I may need to change this in the future as there can be more than one from Plaid
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
    
    """Old code, but may still be of use"""
    # @classmethod
    # def get_account_transactions(cls,bank_account_id,start_date = None,end_date = None):
    #     if end_date:
    #         ending_date = end_date
    #     else:    
    #         ending_date = date.today()
    #     if start_date:
    #         starting_date = start_date
    #     else:
    #         starting_date = two_months_ago(ending_date)
    #     data = {
    #         'bank_account_id':bank_account_id,
    #         'end_date': str(ending_date),
    #         'start_date': str(starting_date) 
    #     }
    #     query = 'SELECT transactions.*,bank_accounts.name AS bank_account_name FROM transactions LEFT JOIN bank_accounts ON bank_account_id = bank_accounts.id '\
    #         'WHERE (bank_account_id = %(bank_account_id)s) AND (date BETWEEN %(start_date)s AND %(end_date)s) ORDER BY DATE DESC LIMIT 100'
    #     results = connectToMySQL(db).query_db(query,data)
    #     return results

    @staticmethod
    def get_account_id(data):
        query = "SELECT id FROM accounts WHERE plaid_account_id = %(account_id)s"
        results = connectToMySQL(db).query_db(query,data)
        return results[0]

    @staticmethod
    def register_transactions(data):
        query = "INSERT INTO transactions (account_id, plaid_transaction_id, date, name, amount, iso_currency_code, category, payment_channel, pending) VALUES (%(account_id)s, %(plaid_transaction_id)s, %(date)s, %(name)s, %(amount)s, %(iso_currency_code)s, %(category)s, %(payment_channel)s, %(pending)s)"
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    async def async_get_transactions(data):        
        url = f"{plaid_address}/transactions/get"

        offset = timedelta(-2)
        start_date = Transaction.get_last_transaction(data)
        start_date = start_date['date']
        start_date = start_date+offset
        end_date = date.today()

        payload = json.dumps({
        "client_id": client_id,
        "secret": secret,
        "access_token": data['access_token'],
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

        payload = json.dumps({
        "client_id": client_id,
        "secret": secret,
        "access_token": data['access_token'],
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
