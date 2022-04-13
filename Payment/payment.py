from email import message
from pickle import FALSE, TRUE
import random
from re import sub
from flask import Flask, render_template,url_for, redirect, jsonify, request
import requests
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= TRUE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#method table
class methodsList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(80), nullable=False)

#database table - transactions
class transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.String(80),nullable=False)
    successful = db.Column(db.String(80),nullable=False)

class Wallet:
    user = ""
    amount = 0
    def __init__(self, username,amount):
        self.user = username
        self.amount = amount
    
    def registerWallet(self):
        return {}

    def performPayment(self,price):
        return self.amount-price

class MethodForm(FlaskForm):
    type = StringField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"placeholder" : "Username"})

#método de pagamento
@app.route('/payment/<int:product_id>', methods=["GET", "POST"] )
def method(product_id):
    methodList=db.Query("SELECT * FROM methodsList order by method")
    return render_template("method.html",templates=methodList )
    #methods = ['Credit', 'Debit', 'MB']
    #return render_template('method.html', templates=methods)
    #form = MethodForm()
    #if form.validate_on_submit():
    #    return redirect(url_for('dashboard')) 
    #return render_template ('method.html', form = form)

@app.route('/payment/<product_id>/<method_id>/<token>', methods=["POST"])
def transact(product_id,method_id,token):
    
    #name = request.json.get('token')
    name = token
    price = product_id
    #price = request.json.get('product_id')
    amount = 1000
    wallet = Wallet(name, amount)
    #user id = token
    #token = request.json.get('token')

    if price.isdigit() == False :
        return (jsonify({
            "message" : "invalid amount"
        }))
    #elif len(name) != 12:
    #    return (jsonify({
    #        "message" : "invalid username"
    #    }))
    elif not token:
        return (jsonify({"message": "invalid user"}))
    else:
        new_transaction = transaction(user_id=token, successful="no", amount=price)
        db.session.add(new_transaction)
        db.session.commit()

        return "complete transaction"#url for "complete_trasaction"

#complete transaction
@app.route('/payment/<string:token>', methods=["POST"])
def complete_trasaction(token):
    #otp =  request.json.get('otp')
    #if user proceeds to pay
    otp=TRUE
    if otp:
        successful = transaction.query.filter_by(user_id=token).update(dict(successful= "yes"))
        db.session.commit()
        return  (jsonify({"message": "transaction successful"}))
    else:
        return (jsonify({"message": "transaction not successful"}))

#atualizar estado do pagamento
#@app.route('/payment/<int:product_id>/<string:token>/state', methods=['PUT'])
#def put(product_id):
#    return 0

#retornar informação
@app.route('/payment/<int:product_id>/<string:token>', methods=['GET'])
def get(product_id,token):
    return {"product" :product_id}

if __name__ == "__main__":
    app.run(debug=True)

