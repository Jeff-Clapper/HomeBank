from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.major_category_2 import Major_Category_2
import requests
import json

db = 'homebank'
plaid_address = "https://sandbox.plaid.com"

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
            url = plaid_address+'/categories/get'
            payload = json.dumps({})
            header = {'Content-Type': 'application/json'}

            resp = requests.request("POST",url,data=payload,headers=header)
            resp = resp.json()

            prev_plaid_cat_id = None

            for category in resp['categories']:
                curr_plaid_cat_id = category['category_id'][0:5]
                current_maj_cat = category['hierarchy'][0]
                
                if len(category['hierarchy']) > 1:
                    current_min_cat = category['hierarchy'][1]
                else:
                    current_min_cat = "None"
                
                if curr_plaid_cat_id != prev_plaid_cat_id:
                    prev_plaid_cat_id = curr_plaid_cat_id 
                    data = {
                        "plaid_cat_id": curr_plaid_cat_id,
                        "major_cat": current_maj_cat,
                        "minor_cat": current_min_cat
                        }
                    Major_Category_1.update_major_cats_1(data)
                
                else:
                    continue
        
        if not Major_Category_2.get_major_cats_2():
            Major_Category_2.update_major_cats_2()
        
        return "complete"

    
    @staticmethod
    def get_major_cats_1():
        query = 'SELECT id FROM categories_1 LIMIT 1;'
        results = connectToMySQL(db).query_db(query)
        if results:
            return True
        else:
            return False

    @staticmethod
    def update_major_cats_1(data):
        query = 'INSERT INTO categories_1 (plaid_cat_id, major_cat, minor_cat) VALUES (%(plaid_cat_id)s,%(major_cat)s,%(minor_cat)s);'
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def get_transaction_category_1_id(data):
        query = 'SELECT ID FROM categories_1 WHERE major_cat = %(major_cat)s AND minor_cat = %(minor_cat)s'
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        return results[0]
