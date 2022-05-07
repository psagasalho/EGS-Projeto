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

#database table - transactions
class transaction(db.Model):
    transaction_id = db.Column(db.String(120), primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    method_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.String(80),nullable=False)
    successful = db.Column(db.String(80),nullable=False)

#selects payment method and get payment information
@app.route('/payment/<int:order_id>', methods=["GET", "POST"] )
def method(order_id):
    if 'method' not in request.values:
        return jsonify("Bad Request"),400
    if 'price' not in request.values:
        return jsonify("Bad Request"),400
    if 'username' not in request.values:
        return jsonify("Bad Request"),400

    method=request.values['method']
    price=request.values['price']
    username=request.values['username']
    if None not in (method,price,username):
        result = (jsonify({"order_id" : order_id},{"method" : method},{"price" : price},{"username" : username}))

    return result

#confirm payment
@app.route('/payment/<int:order_id>/<int:method_id>', methods=["POST"])
def transact(order_id, method_id):
    if 'price' not in request.values:
        return jsonify("Bad Request"),400
    if 'username' not in request.values:
        return jsonify("Bad Request"),400
    if 'nif' not in request.values:
        return jsonify("Bad Request"),400
    price=request.values['price']
    username=request.values['username']
    nif=request.values['nif']
    #transaction id is the primary key of the database, and is the concatenation of the order id and the username
    transaction_id=str(str(order_id)+username)
    if nif.isdigit() == False :
        return (jsonify({
            "message" : "invalid NIF"
        }))
    elif len(nif) != 9:
        return (jsonify({
            "message" : "invalid NIF"
        }))
    else:
        new_transaction = transaction(transaction_id=transaction_id,order_id=order_id,method_id=method_id, user_id=username, successful="no", amount=price)
        db.session.add(new_transaction)
        db.session.commit()
        return (jsonify({ "message" : "confirm payment"}))

#complete transaction and update payment state
@app.route('/payment/<string:token>', methods=["POST"])
def complete_trasaction(token):
    if 'order_id' not in request.values:
        return jsonify("Bad Request"),400
    if 'username' not in request.values:
        return jsonify("Bad Request"),400
    order_id=request.values['order_id']
    username=request.values['username']
    transaction_id=str(str(order_id)+username)
    if token is not None:
        successful = transaction.query.filter_by(transaction_id=transaction_id).update(dict(successful= "yes"))
        db.session.commit()
        return  (jsonify({"message": "transaction successful"}))
    else:
        return (jsonify({"message": "transaction not successful"}))

if __name__ == "__main__":
    app.run(debug=True)
