from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib



app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'


mysql = MySQL(app)


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    
    msg = ''
     
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        
        email = request.form['email']
        password = request.form['password']
        
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        
                
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password,))
        
        account = cursor.fetchone()
        
        

        
        if account:
        
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
        
            return 'Logged in successfully!'
        else:
        
            msg = 'Incorrect email/password!'
    return render_template('index.html', msg='')
    


@app.route('/pythonlogin/logout')
def logout():

   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)

   return redirect(url_for('login'))
   
   
   


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():

    msg = ''

    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'password' in request.form and 'email' in request.form:

        fname = request.form['fname']
        lname = request.form['lname']
        password = request.form['password']
        email = request.form['email']
        
                
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
        account = cursor.fetchone()
       
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', fname):
            msg = 'First name must contain only characters and numbers!'
        elif not re.match(r'[A-Za-z0-9]+', fname):
            msg = 'Last name must contain only characters and numbers!'
        elif not fname or not lname or not password or not email:
            msg = 'Please fill out the form!'
        else:
            
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s,  %s, %s, %s)', (fname, lname, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
        
    elif request.method == 'POST':

        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)
    
    


@app.route('/pythonlogin/home')
def home():

    if 'loggedin' in session:

        return render_template('home.html', email=session['email'])

    return redirect(url_for('login'))
    
    


@app.route('/pythonlogin/profile')
def profile():

    if 'loggedin' in session:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

        return render_template('profile.html', account=account)

    return redirect(url_for('login'))