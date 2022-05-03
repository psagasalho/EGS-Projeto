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
    transaction_id = db.Column(db.String(120), primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(80), nullable=False)
    method_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.String(80),nullable=False)
    successful = db.Column(db.String(80),nullable=False)

class Wallet:
    user = ""
    amount = 0
    def __init__(self, username, amount):
        self.user = username
        self.amount = amount
    
    def registerWallet(self):
        return (jsonify({"user" : self.user},{"amount" : self.amount}))

    def performPayment(self,price):
        self.amount=self.amount-price
        return self.amount

class MethodForm(FlaskForm):
    type = StringField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"placeholder" : "Username"})

#selects payment method and get payment information
@app.route('/payment/<int:order_id>', methods=["GET", "POST"] )
def method(order_id, method=None, price=None, username=None):

    return (jsonify({"order_id" : order_id},{"method" : method},{"price" : price}, {"username" : username}))

#confirm payment
@app.route('/payment/<int:order_id>/<int:method_id>', methods=["POST"])
def transact(order_id,method_id,username=None,nif=None,price=None):
    #transaction id is the primary key of the database, and is the concatenation of the order id and the username
    transaction_id=str(order_id+username)
    if nif.isdigit() == False :
        return (jsonify({
            "message" : "invalid NIF"
        }))
    elif len(nif) != 9:
        return (jsonify({
            "message" : "invalid NIF"
        }))
    else:
        new_transaction = transaction(transaction_id=transaction_id,order_id=order_id, user_id=username, method_id=method_id, successful="no", amount=price)
        db.session.add(new_transaction)
        db.session.commit()
        return (jsonify({ "message" : "confirm payment"}))

#complete transaction and update payment state
@app.route('/payment/<transaction_id>', methods=["POST"])
def complete_trasaction(username, transaction_id):
    #TODO: check if user is valid
    if username is True:
        successful = transaction.query.filter_by(transaction_id=transaction_id).update(dict(successful= "yes"))
        db.session.commit()
        return  (jsonify({"message": "transaction successful"}))
    else:
        return (jsonify({"message": "transaction not successful"}))

if __name__ == "__main__":
    app.run(debug=True)

