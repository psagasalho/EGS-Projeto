"""
Para aceder a base de dados: sqlite3 database.db 
ver o que ela tem: select * from user;
apagar os utilizadores todos: delete from user;
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_uuid import FlaskUUID
import uuid
import os
import sys

from flask_bcrypt import Bcrypt

app = Flask(__name__)
FlaskUUID(app) # use uuid to create a token

#try:
    #f = open('/var/run/Authentication/authentication_db_secret.txt',"r")
    #app.config['SQLALCHEMY_DATABASE_URI'] = f.read().strip()
    #print("DB Secret loaded")
#except:
    #logging.exception("Unable to load db secret")
    #sys.exit(0)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:example@auth-db/db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db= SQLAlchemy(app) # creates the database
bcrypt = Bcrypt (app) # used in passwords
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')



#database table
# id, username, nMec, email, hash da password, token
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique = True) 
    nMec = db.Column(db.Integer, nullable=False, unique = True)
    email = db.Column(db.String(30), nullable=False, unique = True)
    password = db.Column(db.String(80), nullable=False)
    is_logged = db.Column(db.Boolean, unique=False, default=False)
    token = db.Column(db.String(80), nullable=False, unique = True) 

@app.route('/createDB')
def createDatabase():
  db.create_all()
  return jsonify({'message':'Success'})

@app.route('/user/login', methods = ['POST'])
def login():
    if "username" not in request.values:
        return jsonify(message = "Bad Request"), 400
    if "password" not in request.values:
        return jsonify(message = "Bad Request"), 400

    user = User.query.filter_by(username=request.values['username']).first()
    if user: # if you are registered, check your password and enter
        passCheck = str(str(request.values['password']) + str("ThisIsSecret"))
        if bcrypt.check_password_hash(user.password, passCheck):
            user_token = User.query.filter_by(token=user.token).first() 
            user.is_logged = True
            db.session.commit()
            return jsonify(token = user_token.token, message = "Success"), 200
    return jsonify(message= "Bad Request"), 400
                 
@app.route('/user/logout/<token>', methods=['POST']) 
def logout(token):
    user = User.query.filter_by(token=token).first() 
    user.is_logged = False
    db.session.commit()
    return jsonify({'message':'Success'})

@app.route('/user/status/<token>', methods=['POST']) 
def status(token):
    user = User.query.filter_by(token=token).first() 
    return jsonify({'message':'Success','is_logged':str(user.is_logged)})

def checkUser(username, nMec, email):
    existing_user_username = User.query.filter_by(username=username).first()
    if existing_user_username is not None:
        return False
    existing_user_email=  User.query.filter_by(email=email).first()
    if existing_user_email is not None:
        return False
    existing_user_nMec=  User.query.filter_by(nMec=nMec).first()
    if existing_user_nMec is not None:
        return False  
    return True

@app.route('/user' ,methods = ['POST'])
def register():
    if "username" not in request.values:
        return jsonify(message = "Bad Request"), 400
    if "nMec" not in request.values:
        return jsonify(message = "Bad Request"), 400
    if "email" not in request.values:
        return jsonify(message = "Bad Request"), 400
    if "password" not in request.values:
        return jsonify(message = "Bad Request"), 400
    if "confirmPassword" not in request.values:
        return jsonify(message = "Bad Request"), 400

    varCheck = checkUser(request.values['username'], request.values['nMec'], request.values['email'])
    # it only registers if it is valid
    if  varCheck == True and request.values['password'] == request.values['confirmPassword']:
        string_password = str(str(request.values['password']) + str("ThisIsSecret"))
        hashed_password = bcrypt.generate_password_hash(string_password) 
        random_uuid = str(uuid.uuid4()) #uuid to generate the token
        token_username = User.query.filter_by(token=random_uuid).first() 
        #as long as there is a username associated with the token = that token already exists
        while token_username: 
            random_uuid = str(uuid.uuid4()) #uuid to generate the token until no other exists
        new_user = User(username = request.values['username'], 
                        nMec = request.values['nMec'], 
                        email= request.values['email'], 
                        password=hashed_password, token=random_uuid)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'Success'})
    return jsonify(message = "Bad Request"), 400
   
#see if the token is valid or not returning the username
@app.route('/user/<token>',methods = ['GET'])
def token(token):
    token_username = User.query.filter_by(token=token).first() 
    print(token_username)
    if token_username: #if there is a user associated with the token -> token valid
        #username_aux = token_username.username
        #print(username_aux)
        return jsonify(token = "valid", username = token_username.username), 200
    return jsonify(token = "invalid"), 500

"""
#return the email giving me the token
@app.route('/user/email/<token>',methods = ['GET'])
def email(token):
    token_username = User.query.filter_by(token=token).first()
    if token_username:#if there is a user associated with the token -> token valid -> exists email
        return jsonify(token = "valido", email = token_username.email), 200
    return jsonify(token = "invalido"), 500

#return the nMec giving me the token
@app.route('/user/nMec/<token>',methods = ['GET'])
def nMec(token):
    token_username = User.query.filter_by(token=token).first()
    if token_username: #if there is a user associated with the token -> token valid ->  exists nMec
        return jsonify(token = "valido", nMec = token_username.nMec), 200
    return jsonify(token = "invalido"), 500
"""
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
