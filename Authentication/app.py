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
FlaskUUID(app) # vamos usar o uuid para criar um token
db= SQLAlchemy(app) # cria a base de dados
bcrypt = Bcrypt (app) # para as passwords
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # coneta a app à base de dados
app.config['SECRET_KEY'] = 'thisisasercretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#tabela da base de dados
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique = True) 
    # 20 caracteres no maximo -> unique = cada pessoa so pode ter um username e um token
    password = db.Column(db.String(80), nullable=False) # 80 caracteres no maximo
    token = db.Column(db.String(80), nullable=False, unique = True) 

class RegisterFrom(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"placeholder" : "Username"})
    password = PasswordField(validators=[InputRequired(),Length(
        min=4, max=20)], render_kw={"placeholder" : "Password"})
   # nMex_number = StringField(validators=[InputRequired(),Length(
   #     min=4, max=20)], render_kw={"placeholder" : "NMec"})  
    submit = SubmitField("Register")
    # juntar o username na db e ver se existe
    def validate_username(self,username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists.Please choose a different one.")

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
        if user: # se estiver registado, verifica a password e entra
            if user.password == form.password.data:
            #if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard')) # se a pessoa se poder autenticar- gerar o token e usa lo como argumento na funcao de retornar o token
    return render_template ('login.html', form = form)


@app.route('/dashboard', methods = ['GET', 'POST']) #para ver se o login funcionou
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
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data)
        random_uuid = str(uuid.uuid4()) #uuid para gerar o token
        new_user = User(username = form.username.data, password=form.password.data, token=random_uuid)
        db.session.add(new_user)
        db.session.commit()
        return redirect (url_for('login'))
    return render_template ('register.html', form = form)

#dao me o token e eu digo se e valido ou nao e retorno o username
@app.route('/user/token/<token>',methods = ['GET', 'POST'])
def token(token): #token em vez de username
    token_username = User.query.filter_by(token=token).first() #ve se existe um user associado ao token
    #token_user = token_aux.token # -> devolve o token
    #print(token_username)
    if token_username: # se existir um user associado ao token -> token valido
        username_aux = token_username.username
        #print(username_aux)
        return jsonify(token = "valido", username = token_username.username), 200
    return jsonify(token = "invalido"), 500


if __name__=="__main__":
    app.run(debug=True)
