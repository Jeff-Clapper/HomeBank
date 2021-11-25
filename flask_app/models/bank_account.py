from flask_app.models.transaction import Transaction
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from server import db, client_id, secret
import requests
import json
from server import db,client_id, secret

class Bank_Account:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.subtype = data['subtype']
        self.mask = data['mask']
        self.available_balance = data['available_balance']
        self.current_balance = data['current_balance']
        self.account_limit = data['limit']
        self.iso_currency_code = data['iso_currency_code']
        self.transactions = []

    @classmethod
    def initialize_accounts(cls,data):

        response = Transaction.get_transactions(data)
        accounts = response['accounts']
        transactions = response['transactions']
        item_id = data['item_id']
        
        for account in accounts:
            account_info = {
                "item_id": item_id,
                "plaid_account_id": account['account_id'], 
                "name": account['name'],
                "type": account['type'],
                "subtype": account['subtype'], 
                "mask": account['mask'], 
                "available_balance": account['balances']['available'], 
                "current_balance": account['balances']['current'], 
                "account_limit": account['balances']['limit'], 
                "iso_currency_code": account['balances']['iso_currency_code']
            }
            Bank_Account.save_account(account_info)
        return Transaction.initializing_transaction(transactions)

    """MAY HAVE CHANGED PLANS FOR THIS AND FORGOT TO DELETE"""
    @classmethod
    def get_family_bank_data(data):
        family_accounts = Bank_Account.get_family_account_info(data)

    


    # OLD, MAY BE OBSOLETE
    # @classmethod
    # def get_single_account_transactions(cls, data):
    #     query = "Select bank_accounts.*, transactions.id AS transactions_id, transactions.bank_account_id, transactions.date, transactions.name AS transactions_name, transactions.amount, transactions.iso_currency_code, "\
    #         "transactions.category, transactions.pending,transactions.created_at AS transactions_created_at,transactions.updated_at AS transactions_updated_at "\
    #         "FROM bank_accounts JOIN transactions ON bank_accounts.id =  transactions.bank_account_id WHERE family_id = 2 ORDER BY date desc"
    #     results = connectToMySQL(db).query_db(query,data)
    #     account = Bank_Account(results[0])
    #     for result in results:
    #         transaction_data = {
    #             'id' : result['transactions_id'],
    #             'bank_account_id' : result['bank_account_id'],
    #             'date' : result['date'],
    #             'name': result['transactions_name'],
    #             'amount' : result['password'],
    #             'iso_currency_code' : result['iso_currency_code'],
    #             'created_at' : result['transactions_created_at'],
    #             'updated_at' : result['transactions_updated_at']                
    #         }
    #         transact = Transaction(transaction_data)
    #         account.transactions.append(transact)
    #         return account

    """THIS IS OBSOLETE AND NEEDS TO BE CHANGED FOR THE NEW DB OR REMOVED"""
    @classmethod
    def get_account_name(cls,data):
        query = 'SELECT name as bank_account_name FROM bank_accounts WHERE id = %(bank_account_id)s;' 
        results = connectToMySQL(db).query_db(query,data)
        return results

    
    # This may not be necessary. Check this later
    @classmethod
    def remove_account(cls,data):
        query = 'DELETE FROM families WHERE id = %(family_id)s'
        return connectToMySQL(db).query_db(query,data)

    # This may not be necessary. Check this later OR MAY NEED TO BE CHANGED TO UNLINK FROM MY DB AND PLAID API DB
    @classmethod
    def unlinkAccount(cls,data):
        query = 'DELETE FROM bank_accounts WHERE id = %(bank_account_id)s;'
        connectToMySQL(db).query_db(query,data)
        query = 'DELETE FROM transactions WHERE bank_account_id = %(bank_account_id)s'
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def save_account(data):
        query = "INSERT INTO accounts (item_id, plaid_account_id, name, type, subtype, mask, available_balance, current_balance, account_limit, iso_currency_code) VALUES (%(item_id)s, %(plaid_account_id)s, %(name)s, %(type)s, %(subtype)s, %(mask)s, %(available_balance)s, %(current_balance)s, %(account_limit)s, %(iso_currency_code)s)"
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    async def update_account_balances(data):
        query = "UPDATE accounts SET available_balance = %(available_balance)s, current_balance = %(current_balance)s, account_limit = %(account_limit)s WHERE plaid_account_id = %(plaid_account_id)s"

        for item in data['items']:
            results = await Bank_Account.get_balance(item)
            for result in results['accounts']:
                balance_data = {
                    "plaid_account_id" : result['account_id'],
                    "available_balance" : result['balances']['available'],
                    "current_balance" : result['balances']['current'],
                    "account_limit" : result['balances']['limit'],
                }
                connectToMySQL(db).query_db(query,balance_data)
        return "success"

    @staticmethod
    async def get_balance(data):
        url = "https://sandbox.plaid.com/accounts/balance/get"

        payload = json.dumps({
        "client_id": client_id,
        "secret": secret,
        "access_token": data['access_token']
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.text)
        return response
    
    @staticmethod
    def get_family_account_info(data):
        query = 'SELECT accounts.* FROM families LEFT JOIN items ON families.id = items.family_id LEFT JOIN accounts ON items.id = accounts.item_id WHERE families.id = %(family_id)s' 
        results = connectToMySQL(db).query_db(query,data)
        return results[0]
