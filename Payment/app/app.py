from email import message
import logging
from pickle import FALSE, TRUE
import os
import requests
from re import sub
import sys
from flask import Flask, render_template,url_for, redirect, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#try:
#    f = open('/var/run/Payment/secret.txt',"r")
#    secret = f.read().strip()
#    app.config['SQLALCHEMY_DATABASE_URI'] = str(secret)
#    print("DB Secret loaded")
#except:
#    logging.exception("Unable to load db secret")
#    sys.exit(0)

#app.config['SQLALCHEMY_DATABASE_URI'] = str(f.read().strip())
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:example@payment-db/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)

#database table - transactions
class Transaction(db.Model):
    transaction_id = db.Column(db.String(120), primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    method_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.String(80),nullable=False)
    successful = db.Column(db.String(80),nullable=False)

@app.route('/createDB')
def createDatabase():
  db.create_all()
  return jsonify({'message':'Success'})

#method to obtain order payment information
@app.route('/payment/<int:order_id>', methods=["GET"] )
def method(order_id):
    transaction = Transaction.query.filter_by(order_id=order_id).first() 
    return jsonify({"order_id" : transaction.order_id},{"method" : transaction.method_id},{"price" : transaction.amount},{"username" : transaction.user_id})

#confirm payment
@app.route('/payment/<int:order_id>/<int:method_id>', methods=["POST"])
def transact(order_id, method_id):
    if 'price' not in request.values:
        return jsonify('Bad Request'),400
    if 'username' not in request.values:
        return jsonify('Bad Request'),400
    price=request.values['price']
    username=request.values['username']
    #transaction id is the primary key of the database, and is the concatenation of the order id and the username
    transaction_id=str(str(order_id)+username)
    
    new_transaction = Transaction(transaction_id=transaction_id,order_id=order_id,method_id=method_id, user_id=username, successful=str("no"), amount=price)
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({ 'message' : 'Confirm Payment'})

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
    headers = { "accept":"*/*"}
    r = requests.get('http://authapi-service:6000/user/'+token,headers=headers)
    if r.json()['token'] == 'valid':
        successful = Transaction.query.filter_by(transaction_id=transaction_id).update(dict(successful= "yes"))
        db.session.commit()
        return  (jsonify({"message": "Transaction Successful"}))
    else:
        return (jsonify({"message": "Transaction not Successful"}))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
