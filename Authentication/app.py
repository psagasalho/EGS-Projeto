"""
Para aceder a base de dados: sqlite3 database.db 
ver o que ela tem: select * from user;
apagar os utilizadores todos: delete from user;
"""

from flask import Flask, render_template,url_for, redirect, jsonify
#from fastapi import FastAPI
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_uuid import FlaskUUID
import uuid

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from flask_bcrypt import Bcrypt

app = Flask(__name__)
FlaskUUID(app) # use uuid to create a token
db= SQLAlchemy(app) # creates the database
bcrypt = Bcrypt (app) # used in passwords
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # connects the app to the database
app.config['SECRET_KEY'] = 'thisisasercretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#database table
# id, username, nMec, email, hash da password, token
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique = True) 
    nMec = db.Column(db.Integer, nullable=False, unique = True)
    email = db.Column(db.String(30), nullable=False, unique = True)
    password = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(80), nullable=False, unique = True) 
   
class RegisterFrom(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"placeholder" : "Username"})
    nMec = StringField(validators=[InputRequired(),Length(
        min=1, max=20)], render_kw={"placeholder" : "nMec"})
    email = StringField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"placeholder" : "email"})
    password = PasswordField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"placeholder" : "Password"})
    confirmPassword = PasswordField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"placeholder" : "confirm password"})
    submit = SubmitField("Register")
   
    # check if the created username already exists, if it does, choose another
    def validate_username(self,username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")

    # check if the created email already exists, if it does, choose another 
    def validate_email(self,email):
        existing_user_email=  User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError("That email already exists. Please choose a different one.")
    
    # check if the created nMec already exists, if it does, choose another
    def validate_nMec(self,nMec):
        existing_user_nMec=  User.query.filter_by(nMec=nMec.data).first()
        if existing_user_nMec:
            raise ValidationError("That nMec already exists. Please choose a different one.")
    

class LoginFrom(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"placeholder" : "Username"})
    password = PasswordField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"placeholder" : "Password"})
    submit = SubmitField("Login")

@app.route('/')
def home():
    return render_template ('home.html')

@app.route('/user/login', methods = ['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user: # if you are registered, check your password and enter
            passCheck = str(str(form.password.data) + str("ThisIsSecret"))
            if bcrypt.check_password_hash(user.password, passCheck):
                login_user(user)
                return redirect(url_for('dashboard')) 
    return render_template ('login.html', form = form)


@app.route('/dashboard', methods = ['GET', 'POST']) #see if the login worked
@login_required
def dashboard():
    return render_template ('dashboard.html')

@app.route('/user/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user
    return redirect(url_for('login'))

@app.route('/user' ,methods = ['GET', 'POST'])
def register():
    form = RegisterFrom()
    # it only registers if it is valid
    if form.validate_on_submit() and form.password.data == form.confirmPassword.data:
        string_password = str(str(form.password.data) + str("ThisIsSecret"))
        hashed_password = bcrypt.generate_password_hash(string_password) 
        random_uuid = str(uuid.uuid4()) #uuid to generate the token
        token_username = User.query.filter_by(token=random_uuid).first() 
        #as long as there is a username associated with the token = that token already exists
        while token_username: 
            random_uuid = str(uuid.uuid4()) #uuid to generate the token until no other exists
        new_user = User(username = form.username.data, nMec = form.nMec.data, email= form.email.data, password=hashed_password, token=random_uuid)
        db.session.add(new_user)
        db.session.commit()
        return redirect (url_for('login'))
    return render_template ('register.html', form = form)

#see if the token is valid or not returning the username
@app.route('/user/token/<token>',methods = ['GET', 'POST'])
def token(token):
    token_username = User.query.filter_by(token=token).first() 
    if token_username: #if there is a user associated with the token -> token valid
        #username_aux = token_username.username
        #print(username_aux)
        return jsonify(token = "valid", username = token_username.username), 200
    return jsonify(token = "invalid"), 500

"""
#return the email giving me the token
@app.route('/user/email/<token>',methods = ['GET', 'POST'])
def email(token):
    token_username = User.query.filter_by(token=token).first()
    if token_username:#if there is a user associated with the token -> token valid -> exists email
        return jsonify(token = "valido", email = token_username.email), 200
    return jsonify(token = "invalido"), 500

#return the nMec giving me the token
@app.route('/user/nMec/<token>',methods = ['GET', 'POST'])
def nMec(token):
    token_username = User.query.filter_by(token=token).first()
    if token_username: #if there is a user associated with the token -> token valid ->  exists nMec
        return jsonify(token = "valido", nMec = token_username.nMec), 200
    return jsonify(token = "invalido"), 500
"""
if __name__=="__main__":
    app.run(debug=True)
