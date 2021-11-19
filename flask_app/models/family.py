from flask.globals import request
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import asyncio

from flask_app.models.bank_account import Bank_Account
from flask_app.models.item import Item
from flask_app.models.transaction import Transaction
from flask_app.models.user import User

db = 'homebank'

class Family:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.members = []
        self.bank_accounts = []

    @classmethod
    def register_Family(cls,data):
        query = 'INSERT INTO families(name,created_at,updated_at) VALUES (%(name)s,NOW(),NOW());'
        connectToMySQL(db).query_db(query,data)
        query = 'SELECT id FROM families WHERE name=%(name)s ORDER BY created_at DESC LIMIT 1;'
        results = connectToMySQL(db).query_db(query,data)
        return results

    @classmethod
    def get_family(cls, data):
        query = 'SELECT * FROM families WHERE id = %(family_id)s'
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])






    @classmethod
    def get_bank_accounts(cls,data):
        results = Bank_Account.get_account_info(data)
        family = cls(results[0])
        for result in results:
            bank_account_data = {
                'id': result['bank_accounts.id'],
                'name': result['bank_accounts.name'],
                'account_number': result['account_number'],
                'routing_number': result['routing_number'],
                'plaid_account_id':result['plaid_account_id'],
                'family_id':result['family_id'],
                'created_at':result['bank_accounts.created_at'],
                'updated_at':result['bank_accounts.updated_at'],
                'current_balance':result['current_balance'],
                'available_balance':result['available_balance']
            }
            family.bank_accounts.append(Bank_Account(bank_account_data))
        family_members = Family.get_family_members(data)
        for family_member in family_members:
            family_member_data = {
                'id': family_member['id'],
                'first_name': family_member['first_name'],
                'last_name': family_member['last_name'],
                "email": family_member['email'],
                "password": family_member['password'],
                "created_at": family_member['created_at'],
                "updated_at": family_member['updated_at'],
                "family_id": family_member['family_id']
            }
            family.members.append(User(family_member_data))
        return family
    







    @classmethod
    def remove_Family(cls,data):
        query = 'DELETE FROM families WHERE id = %(family_id)s'
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def get_family_members(data):
        query = 'SELECT * FROM families LEFT JOIN users ON families.id = users.family_id WHERE family_id = %(family_id)s'
        results = connectToMySQL(db).query_db(query,data)
        return results

    @staticmethod
    def does_family_own_account(data,bank_account_id):
        query = 'SELECT * FROM bank_accounts WHERE family_id = %(family_id)s'
        results = connectToMySQL(db).query_db(query,data)
        for result in results:
            if result['id']== int(bank_account_id):
                return True
        return False

    @staticmethod
    def family_registration_validation(name):
        is_valid = True
        if len(name) < 2:
            flash('Family name must be at least 2 characters long.')
            is_valid = False
        return is_valid

    @staticmethod
    async def update_account_info(data):
        items = Item.get_family_items(data)
        task_1 = asyncio.create_task(Transaction.get_recent_transactions({"items":items})) #MUST CREATE STILL
        task_2 = asyncio.create_task(Bank_Account.update_account_balances({"items":items})) #STILL HAVE TO CREATE PLAID CALL
        
        await task_1
        await task_2
        
        return "complete"