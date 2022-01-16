from flask_app import app
from flask import json, render_template, redirect, request, flash, session, jsonify, url_for
import asyncio
from datetime import datetime, date, timedelta

from flask_app.models.user import User
from flask_app.models.bank_account import Bank_Account
from flask_app.models.family import Family
from flask_app.models.transaction import Transaction
from flask_app.models.item import Item
from flask_app.models.major_category_1 import Major_Category_1 
from flask_app.models.major_category_2 import Major_Category_2
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login():
    email = request.form['email']
    if not User.login_validation(email):
        flash('Invalid username/password')
        return redirect ('/')
    else:
        data = {'email':email}
    
    user = User.get_user(data)
    if not user:
        flash('Invalid username/password')
        return redirect ('/')
    if not bcrypt.check_password_hash(user['password'],request.form['password']):
        flash('Invalid username/password')
        return redirect ('/')
    
    session['user_id'] = user['id']
    session['email'] = user['email']
    session['family_id'] = user['family_id']

    asyncio.run(Family.update_account_info({"family_id": session['family_id']}))
    return redirect(f'/user/{user["id"]}/home')


@app.route('/family_registration')
def familyRegister():
    return render_template('family_registration.html')


@app.route('/register_family',methods=['POST'])
def registerFamily():
    family = request.form['family_name']
    if not Family.family_registration_validation(family):
        return redirect('/family_registration')
    else:
        data = {'name': family}
        results = Family.register_Family(data)
        session['family_id'] = results[0]['id']
        return redirect('/family_registration/user_registration') 


@app.route('/family_registration/user_registration')
def userRegister():
    try:
        if session['family_id']:
            try:
                if session['user_id']:
                    currentlyLoggedIn = session['user_id']
                    return render_template('user_registration.html',currentlyLoggedIn=currentlyLoggedIn)
            except:
                currentlyLoggedIn = False
                return render_template('user_registration.html',currentlyLoggedIn=currentlyLoggedIn)
    except:
        return redirect('/family_registration')


"""DOES THIS NEED A TRY AND EXCEPT? IF OTHERS CAN PASS THEIR OWN DATA, THEY COULD REGISTER AN ACCOUNT?"""
@app.route('/register_user',methods=['POST'] )
def registerUser():
    pw1 = request.form['password']
    pw2 = request.form['password_confirmed']
    results = User.password_compare(pw1,pw2)
    if not results:
        return redirect('/family_registration/user_registration')
    else:
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(pw1),
            'family_id': session['family_id']
        }
    if not User.registration_validation(data):
        return redirect('/family_registration/user_registration')
    else:
        results = User.register(data)
        user_id =  results[0]['id']
        session['user_id'] = user_id
        session['email'] = data['email']
        return redirect(f'/user/{user_id}/home') 


@app.route('/user/<int:user_id>/home')
def home(user_id):
    try:
        if (session['user_id'] == user_id): 
            data = {
                "user_id":session['user_id'],
                'family_id':session['family_id'],
                "email": session['email']
                }
            user_profile = Family.get_profile(data)
            family_accounts = []
            for account in user_profile.bank_accounts:
                family_accounts.append(
                    {"account_name": account.name, 
                    "account_id":account.id
                })

            session['family_accounts'] = family_accounts
            return render_template('home.html', user=user_profile)
        else:
            return redirect('/logout')
    except:
        return redirect('/logout')


"""THIS NEEDS A TRY EXCEPT. ONE EXSISTS, BUT IT WAS FOR PREVIOUS CODE"""
@app.route('/user/<int:user_id>/register_bank_account')
# def register_bank_account(user_id):
#     try:
#         if (session['user_id'] == user_id):
#             return render_template('link_account.html',user_id=user_id)    
#         else:
#             return redirect('/logout')
#     except:
#         return redirect('/logout')
def register_bank_account(user_id):
    return render_template('bank_account_registration.html',user_id=user_id)


@app.route("/create_link_token", methods=['POST'])
def create_link_token():
    user_id = session['user_id']
    results = Item.create_link_token(user_id)
    return jsonify(results)


@app.route('/exchanging_public_token', methods=['POST'])
def public_token_exchange():
    data = request.get_json()
    Item.exchange_pub_tok(data,family_id=session['family_id'])
    flash('Your Account has been successfully Linked!')
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/user/<int:user_id>/transactions')
def transactions(user_id):
    # try:
    #     if (session['user_id']==user_id) and (Family.does_family_own_account({'family_id': session['family_id']},bank_account_id)==True):
    #         user = User.get_user({'email' : session['email']})
    #         transacts = Transaction.get_account_transactions(bank_account_id)
    #         if not transacts:
    #             transacts = Bank_Account.get_account_name({'bank_account_id':bank_account_id})
    #             noTransactions = True
    #             return render_template('transactions.html',user=user,transactions=transacts)
    #         for transact in transacts:
    #             transact['date'] = str(transact['date'].strftime('%m/%d/%y'))
    #             if transact['pending'] == 0:
    #                 transact['pending'] = 'processed'
    #             else:
    #                 transact['pending'] = 'pending'
    #         noTransactions = False
    #         return render_template('transactions.html',user=user,transactions=transacts, noTransactions=noTransactions)
    #     else:
    #         return redirect('/logout')
    # except:
    #     return redirect('/')
    if session['user_id']==user_id:
        user = User.get_user({'email' : session['email']})
        accounts = session['family_accounts'] 
        return render_template('transactions.html',user=user,accounts=accounts)


@app.route('/user/<int:user_id>/get_transactions',methods=['POST'])
def get_transactions(user_id):
    if user_id == session['user_id']:
        end_date = request.form["end_date"]
        if end_date:
            end_date = datetime.strptime(end_date,"%m/%d/%Y")
        else:
            end_date = date.today()
        
        start_date = request.form["start_date"]
        if start_date:
            start_date = datetime.strptime(start_date,"%m/%d/%Y")
        else:
            offset = timedelta(30)
            start_date = end_date-offset

        data = {
            "family_id": request.form["family_id"],
            "account_id":  request.form["account_id"],
            "start_date": start_date,
            "end_date": end_date
        }

        family_transactions = Transaction.get_account_transactions(data)
        
        for transaction in family_transactions:
            transaction['date'] = datetime.strftime(transaction["date"],"%m/%d/%Y")
            if transaction['pending'] == 0:
                transaction['pending'] = "Completed"
            elif transaction['pending'] == 1:
                transaction['pending'] = "Pending"
            transaction['iso_currency_code'] = "$"
            transaction['account_name'] = Bank_Account.get_account_name({"account_id": transaction['account_id']})
            transaction['account_name'] = transaction['account_name']['name']
            transaction['amount'] *= -1
            transaction['amount'] = float(transaction['amount'])
            transaction['amount'] = "{:.2f}".format(transaction['amount'])

        return jsonify(family_transactions)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} # might possibly need this
    else:
        return redirect('/logout')


"""THIS NEEDS TO BE UPDATED TO REMOVE ITEM PER PLAID API ENDPOINT"""
# @app.route('/user/<int:user_id>/remove_bank_account')
# def unlink_bank_account(user_id):
#     try:
#         if (session['user_id'] == user_id):
#             bank_accounts = Family.get_bank_accounts({'family_id':session['family_id']})
#             return render_template('unlink_bank_account.html',user_id=user_id,bank_accounts=bank_accounts)
#         else:
#             return redirect('/logout')
#     except:
#         return redirect('/logout')


"""This may be used as the remove from above"""
# @app.route('/user/<int:user_id>/unlink_account', methods=['POST'])
# def unlink_account(user_id):
#     data = {
#         'bank_account_id':request.form['bank_account_id']
#     }
#     Bank_Account.unlinkAccount(data)
#     return redirect(f'/user/{user_id}/home')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') 


@app.route('/family_back')
def familyBack():
    data = {'family_id': session['family_id']}
    Family.remove_Family(data)
    session.clear()
    return redirect('/family_registration')


@app.route('/login_back')
def loginBack():
    data = {'family_id': session['family_id']}
    Family.remove_Family(data)
    session.clear()
    return redirect('/')



