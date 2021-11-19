from flask_app.models.transaction import Transaction
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import requests
import json

db = 'homebank'

class Bank_Account:
    def __init__(self,data):
        self.id = data['id']
        self.item_id = data['item_id']
        self.plaid_account_id = data['plaid_account_id']
        self.name = data['name']
        self.type = data['type']
        self.subtype = data['subtype']
        self.mask = data['mask']
        self.available_balance = data['available_balance']
        self.current_balance = data['current_balance']
        self.account_limit = data['limit']
        self.iso_currency_code = data['iso_currency_code']
        self.create_at = data['created_at']
        self.updated_at = data['updated_at']
        self.transactions = []

    """SHOULDN'T NEED THIS AS I AM NOW LINKING ITEMS"""
    # @classmethod
    # def register_account(cls, data):
    #     query = "INSERT INTO bank_accounts(name,account_number,routing_number,plaid_account_id,family_id,created_at,updated_at,current_balance,available_balance) VALUES (%(name)s,%(account_number)s,%(routing_number)s,%(plaid_account_id)s,%(family_id)s,NOW(),NOW(),%(current_balance)s,%(available_balance)s);"
    #     return connectToMySQL(db).query_db(query,data)

    @classmethod
    def initialize_accounts(cls,data):
        url = "https://sandbox.plaid.com/transactions/get" # LATER: CREATE A VARIABLE FOR AT LEAST THE FIRST PORTION

        payload = json.dumps({
        "client_id": "615386ab5732020010712561",
        "secret": "e12ac64123623a95b312ecd75e3675",
        "access_token": data['access_token'],
        "start_date": "2021-10-01",
        "end_date": "2021-11-13"
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.text)
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

    @classmethod
    def get_account_name(cls,data):
        query = 'SELECT name as bank_account_name FROM bank_accounts WHERE id = %(bank_account_id)s;' 
        results = connectToMySQL(db).query_db(query,data)
        return results

    @classmethod
    def get_account_info(cls, data):
        query = 'SELECT * FROM families LEFT JOIN bank_accounts ON families.id = bank_accounts.family_id WHERE families.id = %(family_id)s' 
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
            results = await """PLAID BALANCE API REQUEST HERE""" #MUST UPDATE STILL
            for result in results['accounts']:
                balance_data = {
                    "plaid_account_id" : result['account_id'],
                    "available_balance" : results['balances']['available'],
                    "current_balance" : results['balances']['current'],
                    "account_limit" : results['balances']['limit'],
                }
                return connectToMySQL(db).query_db(query,balance_data)

