from requests.models import Response
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.major_category_2 import Major_Category_2
from server import db, plaid_address
import requests
import json

class Major_Category_1:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.minor_cat = data['minor_cat']
        self.sub_cat = data['sub_cat']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def update_categories():
        if not Major_Category_1.get_major_cats_1():
            url = plaid_address+'categories/get'
            payload = json.dumps({})
            header = {'Content-Type': 'application/json'}

            resp = requests.request("POST",url,data=payload,headers=header)
            resp = resp.json()

            previous_maj_cat = None
            maj_cat_id = None
            previous_min_cat = None
            min_cat_id = None

            for category in resp['categories']:
                current_maj_cat = category['hierarchy'][0]
                if len(category['hierarchy']) == 2:
                    current_min_cat = category['hierarchy'][1]
                
                if current_maj_cat != previous_maj_cat:
                    previous_maj_cat = current_maj_cat 
                    data = {"major_cat": current_maj_cat}
                    maj_cat_id = Major_Category_1.update_major_cats_1(data)
                
                elif current_min_cat != previous_min_cat:
                    previous_min_cat = current_min_cat
                    data = {
                        "minor_cat": current_min_cat,
                        "major_cat_id": maj_cat_id
                    }
                    min_cat_id = Major_Category_1.update_minor_cats(data)
                
                else:
                    data = {
                        "sub_cat": category['hierarchy'][2],
                        "min_cat_id": min_cat_id
                    }
        
        if not Major_Category_2.get_major_cats_2():
            Major_Category_2.update_major_cats_2()
        
        return "complete"

    
    @staticmethod
    def get_major_cats_1():
        query = 'SELECT id FROM financial_groups LIMIT 1;'
        results = connectToMySQL(db).query_db(query)
        if results:
            return True
        else:
            return False


    @staticmethod
    def update_major_cats_1(data):
        query = 'INSERT INTO major_cats_1 (name) VALUES (%(major_cat)s);'
        connectToMySQL(db).query_db(query,data)
        query = 'SELECT id FROM major_cats_1 WHERE name = %(major_cat)s;'
        result = connectToMySQL(db).query_db(query,data)
        return result[0]['id']


    @staticmethod
    def update_minor_cats(data):
        query = 'INSERT INTO minor_cats (name, major_cat_id) VALUES (%(minor_cat)s,%(major_cat_id)s);'
        connectToMySQL(db).query_db(query,data)
        query = 'SELECT id FROM minor_cats WHERE name = %(minor_cat)s AND major_cat_id = %(major_cat_id)s;'
        result = connectToMySQL(db).query_db(query,data)
        return result[0]['id']


    @staticmethod
    def update_sub_cats(data):
        query = 'INSERT INTO sub_cats (name, minor_cat_id) VALUES (%(sub_cat)s,%(min_cat_id)s);'
        return connectToMySQL(db).query_db(query,data)

