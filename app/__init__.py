import pyodbc

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask_login import LoginManager, login_required, logout_user, login_user
from wtforms import Form, PasswordField

cnxn = pyodbc.connect('DSN=mssql;UID=mssql;PWD=mssql;')
cursor = cnxn.cursor()
app = Flask(__name__)
login_manager = LoginManager(app)

class SignInForm(Form):
    password = PasswordField('password')

@app.route('/goadmin', methods=['GET'])
def goadmin():
    form = SignInForm(request.form)
    return render_template('goadmin.html', title='Go admin', form=form)


@app.route('/goadmin', methods=['POST'])
def trygoadmin():
    form = SignInForm(request.form)
    if form.validate():
        login_user(user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/', methods=['GET'])
def index():
    tables = [x for x in cursor.tables() if x.table_type == "TABLE" and x[1] == 'dbo']
    return render_template("index.html", tables=tables)

@app.route('/<string:table>')
def show_table(table):
    cursor.execute("select * from " + table)
    rows = cursor.fetchall()
    tables = [x for x in cursor.tables() if x.table_type == "TABLE" and x[1] == 'dbo']
    columns = [x for x in cursor.columns(table)]
    return render_template("table.html", tables=tables, columns=columns, rows=rows)