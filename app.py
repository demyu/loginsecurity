from flask import Flask, render_template, request,redirect, url_for, session
from flask_mysqldb import MySQL
from english_words import english_words_set
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime, date

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'securitylogin'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'M1mrvWyJyVMcLR2vT03XNx5oWRbxnmiu'

mysql = MySQL(app)

#@TODO Make Login attempts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    if 'created_at' in session:
        createdat = session['created_at']
        print(createdat)
        return render_template('welcome.html', username = session['username'], created_at = createdat)
    elif 'username' in session:
        return render_template('welcome.html', username = session['username'], created_at = "")
    else:
        return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    error = ""
    if request.method == 'POST':

        today = date.today()

        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users where username = %s" , [username])
        userid = cur.fetchone()
        cur.close()

        if(userid != None and len(username) != 0):
            userid = userid['id']
            cur = mysql.connection.cursor()
            cur.execute("SELECT password, created_at FROM userpasswords where userid = %s and isActive = %s" , [userid, 1])
            activePass = cur.fetchone()
            cur.close()

            if(activePass != None and len(activePass) !=0):
                if(check_password_hash(activePass['password'], password)):
                    session['username'] = username
                    session['id'] = userid

                    #Checks validity of password
                    created_at = str(activePass['created_at'])

                    datetimeobject = datetime.strptime(created_at,'%Y-%m-%d')
                    date1 = datetimeobject.strftime('%Y,%m,%d')
                    date1 = datetime.strptime(date1,'%Y,%m,%d').date()

                    if(numOfDays(date1, today)> 30):
                        session.pop('username', None)
                        return redirect(url_for('forceChange'))
                    elif(numOfDays(date1,today) >20):
                        session['created_at'] = numOfDays(date1,today)
                        return redirect(url_for('welcome'))
                    else:
                        return redirect(url_for('welcome'))
                error = "Password does not match"
                return render_template('index.html', error = error)
        error = "Username Does not exist"
        return render_template('index.html', error = error)
    else:
        return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('id', None)
    if 'created_at' in session:
        session.pop('created_at', None)
    return redirect(url_for('index'))

@app.route('/register' ,methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users where username = %s" , [username])
        users = cur.fetchall()
        cur.close()

        if(len(users) == 0):

            #Creates a hashed password
            password = generate_password_hash(password)

            #Insert username password to database 
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, email) VALUES (%s,%s)" , (username, email))
            mysql.connection.commit()
            cur.close()

            #Get ID of the inserted username
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM users where username = %s" , [username])
            userid = cur.fetchone()
            cur.close()
            userid = userid['id']

            
            #Add password to password table
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO userpasswords (userid, password, isActive) VALUES (%s,%s,%s)" , (userid, password,1))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('index'))
        return "Username Already taken"
    else:
        return redirect(url_for('index'))

@app.route('/checkPass' ,methods=['GET','POST'])
def checkPass():
    
    if request.method == 'POST':
        username = request.form['username']
        data = request.form['password']
    
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        regex2 = re.compile('[a-zA-Z]')
        
        if(regex.search(data) != None):
            if(regex2.search(data) != None):
                if(not data.islower() and not data.isupper() and any(map(str.isdigit, data))):
                    return checkDict(data, username)
        return "Password must be at least (10) characters long, which consist of at least (1) upper case letter, 1 lower case letter, 1 number and 1 special character"
    else:
        return redirect(url_for('index'))


@app.route('/updatePassword' ,methods=['GET','POST'])
def updatePassword():
    if request.method == 'POST':
        password = request.form['password']
        userid = session['id']

        #Fetches all password using session id to check history of passwords
        cur = mysql.connection.cursor()
        cur.execute("Select * from userpasswords where userid = %s" , [userid])
        listofPassword = cur.fetchall()
        cur.close()

        for pasowordo in listofPassword:
            if check_password_hash(pasowordo['password'], password):
                return "Password already used"
            
        #Disables old passwords 
        cur = mysql.connection.cursor()
        cur.execute("Update userpasswords set isActive = 0 where userid = %s" , [userid])
        mysql.connection.commit()
        cur.close()

        #Generate hash password
        password = generate_password_hash(password)

        #Add password to password table
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO userpasswords (userid, password, isActive) VALUES (%s,%s,%s)" , (userid, password,1))
        mysql.connection.commit()
        cur.close()

        if(len(listofPassword)==6):
            id = listofPassword[0]['id']
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM userpasswords where id = %s" , [id])
            mysql.connection.commit()
            cur.close()
        return "Sucess"

    else:
        return redirect(url_for('index'))

@app.route('/forceChange')
def forceChange():
    return render_template('forcechange.html')


#Checks if word is in dictionary
def checkDict(word, username):

    error = ""
    names = []  
    temp = ""
    username = str(username)
    word = str(word)

    res = [word[i: j] for i in range(len(word)) 
          for j in range(i + 1, len(word) + 1)] 

    
    for x in range(len(username)):
        if(username[x] != " "):
            temp += username[x]
        else:
            names.append(temp)
            temp=""
        if(x == len(username)-1):
            names.append(temp)
            
    for words in res:
        if len(words) < 4:
            continue
        elif (words in names):
            error = "Username cannot be in password"
            return error
        elif words in english_words_set:
            error = "Dictionary Word detected"
            return error
        else:
            error = " "
    return error

def loginattempt(username):
    cur = mysql.connection.cursor()
    cur.execute("Select loginattempt from users where username = %s" , [username])
    loginattempt = cur.fetchone()
    cur.close()

    if(loginattempt['loginattempt'] == '3'):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (isSuspended) VALUES (%s) where " , (userid, password,1))
        mysql.connection.commit()
        cur.close()



#Function to get validity of date
def numOfDays(date1, date2):
    return (date2-date1).days

app.run(debug=True)