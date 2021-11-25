from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from server import db

name_regex = re.compile(r'^[a-zA-Z]+$')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        # self.password = data['password']
        # self.created_at = data['created_at']
        # self.updated_at = data['updated_at']
        self.family_id = data['family_id']

    @classmethod
    def register(cls,data):
        query = "INSERT INTO users(first_name,last_name,email,password,created_at,updated_at, family_id) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW(), %(family_id)s);"
        connectToMySQL(db).query_db(query,data)
        query = 'SELECT id FROM users WHERE email = %(email)s;'
        results = connectToMySQL(db).query_db(query,data)
        return results

    @classmethod
    def get_current_user(cls, data):
        user = User.get_user(data)
        user_data = {
            "id": user['id'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "email": user['user']
        }
        current_user = User(user_data)
        return current_user
    
    @staticmethod
    def get_user(data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return results[0]



    @staticmethod
    def password_compare(pw1,pw2):
        if len(pw1) < 8:
            flash('Passwords must be a mininum of 8 characters.')
            return False
        elif pw1 != pw2:
            flash('Passwords must match.')
            return False
        else:
            return True

    @staticmethod
    def registration_validation(data):
        is_valid = True
        query = 'SELECT id FROM users where email = %(email)s'
        results = connectToMySQL(db).query_db(query,data)
        if len(results) > 0:
            flash('This email is already exists.')
            is_valid = False
            return is_valid
        if (len(data['first_name']) < 2) or (len(data['last_name']) < 2):
            flash('first and last name must be at least two letters long.')
            is_valid = False
        if not name_regex.match(data['first_name']):
            flash("First name should be only letters.")
            is_valid = False
        if not name_regex.match(data['last_name']):
            flash("Last name should be only letters.")
            is_valid = False
        if not email_regex.match(data['email']):
            flash('Please use a valid email address.')
            is_valid = False
        if data['password'] == False:
            is_valid = False
        return is_valid

    @staticmethod
    def login_validation(email):
        is_valid = True
        if not email_regex.match(email):
            is_valid = False
        return is_valid

