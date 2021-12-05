from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import asyncio
from server import db

from flask_app.models.bank_account import Bank_Account
from flask_app.models.item import Item
from flask_app.models.transaction import Transaction
from flask_app.models.user import User

class Family:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.current_user = data['current_user']
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
    def get_profile(cls,data):
        family = Family.get_family_info(data)
        current_user = User.get_current_user(data)
        
        family_data = {
            "id": family[0]['id'],
            "name": family[0]['name'],
            "current_user": current_user,
        }
        profile = Family(family_data)
        
        for member in family:
            member_data = {
                "member_id": member['id'],
                "member_name": member['member_name'],
                "member_email": member['member_email']
            }
            profile.members.append(member_data)
        
        family_accounts = Bank_Account.get_family_account_info(data)
        if family_accounts:
            for account in family_accounts:
                if account['available_balance']:
                    funds = float(account['available_balance'])
                else:
                    funds = float(account['current_balance'])

                if (account['type'] == "credit") or (account['type'] == "loan"):
                    funds *= -1
                
                if funds > 0:
                    isPos = True
                else:
                    isPos = False

                # This assumes that all money is in USD, will need to change if I decide to expand
                funds = "{:.2f}".format(funds)
                funds = f"${funds}"
                
                family_account_info = {
                    "id": account['id'],
                    "name": account['name'],
                    "type": account['type'],
                    "subtype": account['subtype'],
                    "mask": account['mask'],
                    "available_balance": account['available_balance'],
                    "current_balance": account['current_balance'],
                    "account_limit": account['account_limit'],
                    "iso_currency_code": account['iso_currency_code'],
                    "funds": funds,
                    "isPos": isPos
                }
                profile.bank_accounts.append(Bank_Account(family_account_info))

        return profile

    @staticmethod
    def get_family_info(data):
        query = 'SELECT families.id, families.name, users.id as member_id, CONCAT(first_name, " " ,last_name) as member_name, users.email as member_email FROM families LEFT JOIN users ON families.id = users.family_id WHERE families.id = %(family_id)s;'
        results = connectToMySQL(db).query_db(query,data)
        return results




    """THIS MAY BE OBSOLETE"""
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
        if items[0]['items_id']:
            task_1 = asyncio.create_task(Transaction.get_recent_transactions({"items":items}))
            task_2 = asyncio.create_task(Bank_Account.update_account_balances({"items":items}))
            
            await task_1
            await task_2
        
        return "complete"