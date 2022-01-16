from flask_app.config.mysqlconnection import connectToMySQL

db = 'homebank'
plaid_address = "https://sandbox.plaid.com"

class Major_Category_2:
    @staticmethod
    def get_major_cats_2():
        query = "SELECT * FROM categories_2"
        results = connectToMySQL(db).query_db(query)
        if results:
            return True
        else:
            return False

    @staticmethod
    def update_major_cats_2():
        query = "INSERT INTO categories_2 (name) VALUES (%(name)s)" 
        values = ['Want','Need','Savings','Unknown']
        for value in values:
            data = {"name": value}
            connectToMySQL(db).query_db(query,data)
        
        return "complete"