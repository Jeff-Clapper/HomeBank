from flask.globals import request
from flask_app.config.mysqlconnection import connectToMySQL
from server import db, client_id, secret

from datetime import date
from flask import flash




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
            transaction_info = {
                "account_id": account_id['id'],
                "plaid_transaction_id": transaction['transaction_id'],
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

"""Old code for pagination, May not need anymore """
# def days_in_month(year,month):
#     thirty_day = [4,6,9,11]
#     if (month == 2) and (year % 4 == 0):
#         return 29
#     elif month ==2:
#         return 28
#     elif month in thirty_day:
#         return 30
#     else:
#         return 31

"""Old code for pagination, May not need anymore """
# def two_months_ago(today):
#     year = int(today.year)
#     month = int(today.month)
#     day = int(today.day)
#     if month <= 2:
#         year -= 1
#         month += 10
#     else:
#         month -= 2
#     daysInMonth = days_in_month(year,month)
#     if daysInMonth < day:
#         day = daysInMonth
#     month = str(month).zfill(2)
#     day = str(day).zfill(2)
#     twoMonthsAgo = (f'{year}-{month}-{day}')
#     return date.fromisoformat(twoMonthsAgo)