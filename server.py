from flask_app import app
from flask_app.controllers import users 
import os

db = 'homebank'
client_id = os.getenv("CLIENT_ID")
secret = os.getenv("SECRET")

"""Before I delete this section, review the try and except and either add it to my code or create its like in my code"""
# @app.route("/OLDcreate_link_token", methods=['POST'])
# def OLDcreate_link_token():
#     # try:
#         #Get the client_user_id by searching for the current user
#         user = 'user_good' #THIS MAY NEED TO JUST BE WHAT I HAVE ON MY RECORD. This looks to have been done on the demo with User.find(NAME). Guessing this is a method to query db. Which seems to return the entire list
#         client_user_id = "1" #THIS IS MAKING THE CLIENT ID THE ID NUMBER IN MY DB FROM THE RESULTS IN THE LINE ABOVE

#         #Create a link_token for the given user
#         request = LinkTokenCreateRequest(
#             products=[Products("auth")],  #THIS MAY BE ABLE TO INCLUDE MORE PRODUCTS
#             client_name="NA",
#             country_codes=[CountryCode('US')],
#             language='en',
#             user=LinkTokenCreateRequestUser(client_user_id=str(time.time()))  #PREVIOUSLY client_user_id=client_user_id
#         )
#         user_id = session['user_id']
#         response = client.link_token_create(request)


#         #Send the data to the client
#         #.todict belongs to jsonify and recursively converts a bunch back into a dictionary (jeff notes)
#         print("before jsonify")
#         print(jsonify(response.todict()))
#         print("after jsonify")
#         return jsonify(response.todict())
    # except plaid.ApiException as e:
    #     return json.loads(e.body)


"""Before I delete this section, review the try and except and either add it to my code or create its like in my code"""
# @app.route('/accounts', methods=['GET'])
# def get_accounts():
#     try:
#         requests = AccountsGetRequest(access_token='')
#         accounts_response = client.accounts_get(requests)
#     except plaid.ApiException as e:
#         responses = json.loads(e.body)
#         return jsonify({'error': {'status_code': e.status, 'display_message':responses['error_message'], 'error_code': responses['error_code'],'error_type': response['error_type']}})
#     print(jsonify(accounts_response.to_dict()))
#     return jsonify(accounts_response.to_dict())





if __name__ == '__main__':
    app.run(debug=True)