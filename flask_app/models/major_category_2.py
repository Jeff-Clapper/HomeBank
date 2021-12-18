from flask_app.config.mysqlconnection import connectToMySQL
from server import db

class Major_Category_2:
    @staticmethod
    def get_major_cats_2():
        query = "SELECT * FROM major_cats_2"
        results = connectToMySQL(db).query_db(query)
        if results:
            return True
        else:
            return False

    @staticmethod
    def update_major_cats_2():
        query = "INSERT INTO major_cats_2 (name) VALUES (%(name)s)" 
        values = ['Want','Need','Savings']
        for value in values:
            data = {"name": value}
            connectToMySQL(db).query_db(query,data)
        
        return "complete"