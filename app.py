from flask import Flask, render_template, request,redirect, url_for, session
from flask_mysqldb import MySQL
from english_words import english_words_set
from werkzeug.security import generate_password_hash, check_password_hash
import re, requests
from datetime import datetime, date
import datetime as yolo
import smtplib, ssl
import hashlib
import hmac

app = Flask(__name__)

#Config for database
app.config['MYSQL_HOST'] = 'us-cdbr-east-03.cleardb.com'
app.config['MYSQL_USER'] = 'be46b56a23df04'
app.config['MYSQL_PASSWORD'] = '9f8e51cc'
app.config['MYSQL_DB'] = 'heroku_d9dccebc3492f63'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'M1mrvWyJyVMcLR2vT03XNx5oWRbxnmiu'

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'securitylogin'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#app.secret_key = 'M1mrvWyJyVMcLR2vT03XNx5oWRbxnmiu'

mysql = MySQL(app)

#Starting pagee of the website
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    #Creates a session if no sesssion is present
    if 'created_at' in session:
        createdat = session['created_at']
        horoscope = session['horoscope']
        data = dailyHoroscope(horoscope)
        
        horos_id = inputToHoroscope(horoscope, data['color'], data['compatibility'], data['lucky_number'], data['description'])
        link = "sharer/" + horos_id
        return render_template('welcome.html', username = session['username'], created_at = createdat, horoscope = data, horoscopeName = horoscope , link = link)
    elif 'username' in session:
        horoscope = session['horoscope']
        data = dailyHoroscope(horoscope)
        horos_id = inputToHoroscope(horoscope, data['color'], data['compatibility'], data['lucky_number'], data['description'])
        link = "sharer/" + horos_id
        return render_template('welcome.html', username = session['username'], created_at = "", horoscope = data, horoscopeName = horoscope, link = link)
    else:
        return redirect(url_for('index'))

#Login Module
@app.route('/login', methods=['GET','POST'])
def login():
    error = ""
    #Creates a lock session if none is found
    if 'lock' not in session:
        session['lock'] = 0

    if request.method == 'POST':
        #Checks if lock limit is reached
        if(not lock()):
            #Gets the form from the login module
            today = date.today()
            username = request.form['username']
            password = request.form['password']

            #Checks if username is in database
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users where username = %s" , [username])
            userid = cur.fetchone()
            cur.close()

            if(userid != None and len(username) != 0):
                #Checks if password is in correct with username
                horos = userid['horoscope']
                isVerified = userid['isVerified']
                userid = userid['id']
                cur = mysql.connection.cursor()
                cur.execute("SELECT password, DATE(created_at) as created_at FROM userpasswords where userid = %s and isActive = %s" , [userid, 1])
                activePass = cur.fetchone()
                cur.close()

                if(activePass != None and len(activePass) !=0 and isVerified == "1"):
                    #Checks if password hashed is correct with the inputted password
                    if(check_password_hash(activePass['password'], password)):
                        session['username'] = username
                        session['id'] = userid
                        session['horoscope'] = horos

                        #Checks validity of password
                        created_at = str(activePass['created_at'])

                        datetimeobject = datetime.strptime(created_at,'%Y-%m-%d')
                        date1 = datetimeobject.strftime('%Y,%m,%d')
                        date1 = datetime.strptime(date1,'%Y,%m,%d').date()
                        
                        #Checks the validity/expiration of password
                        if(numOfDays(date1, today)> 30):
                            session.pop('username', None)
                            session.pop('lock', None)
                            return redirect(url_for('forceChange'))
                        elif(numOfDays(date1,today) >10):
                            session['created_at'] = numOfDays(date1,today)
                            session.pop('lock', None)
                            return redirect(url_for('welcome'))
                        else:
                            session.pop('lock', None)
                            return redirect(url_for('welcome'))
                    error = "Password does not match"
                    if 'lock' not in session:
                        session['lock'] = 0
                    session['lock'] = int(session['lock']) + 1
                    return render_template('index.html', error = error)
            error = "Username Does not exist or not yet verified"
            session['lock'] = int(session['lock']) + 1
            return render_template('index.html', error = error)
        else:
            error = "Try again at "+ str(session['timelock'].strftime("%H:%M:%S"))
            return render_template('index.html', error = error)
    else:
        return render_template('index.html')

#Destroys session
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
        #Gets form from register module
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        horoscope = request.form['horoscope']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users where username = %s" , [username])
        users = cur.fetchall()
        cur.close()

        if(len(users) == 0):

            #Creates a hashed password
            password = generate_password_hash(password)

            #Insert username password to database 
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, email, horoscope, isVerified) VALUES (%s,%s,%s,%s)" , (username, email, horoscope, 0))
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

            #Send email to user
            sendEmail(email)

            return redirect(url_for('index'))
        return "Username Already taken"
    else:
        return redirect(url_for('index'))

@app.route('/checkPass' ,methods=['GET','POST'])
def checkPass():
    
    if request.method == 'POST':
        username = request.form['username']
        data = request.form['password']

        #Checks password validation
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

        #Checks if password is in the last 6 passwords
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
    #Subtring of a string
    res = [word[i: j] for i in range(len(word)) 
          for j in range(i + 1, len(word) + 1)] 

    res = list(sorted(res, key = len))
    #Cuts username from spaces
    for x in range(len(username)):
        if(username[x] != " "):
            temp += username[x]
        else:
            names.append(temp)
            temp=""
        if(x == len(username)-1):
            names.append(temp)
    #Checks if password contains dictionary words and if password has a username    
    for words in res:
        if len(words) < 4:
            continue
        elif (words in names):
            error = "Username cannot be in password"
            break
        elif (words.lower() in english_words_set):
            error = "Dictionary Word detected"
            break
        else:
            error = " "
    return error

#Lock module if password or username fails
def lock():
    if session['lock'] >= 3:
        if 'timelock' in session:
            if ((session['timelock'] + yolo.timedelta(0,0)) <= (datetime.now() +yolo.timedelta(0,0))):
                session.pop('lock', None)
                session.pop('timelock', None)
                return False
        session['timelock'] = datetime.now() + yolo.timedelta(0,300) 

        return True
    return False

#Function to get validity of date
def numOfDays(date1, date2):
    return (date2-date1).days

def dailyHoroscope(horoscope):
    url = "https://sameer-kumar-aztro-v1.p.rapidapi.com/"
    querystring = {"sign": str(horoscope),"day":"today"}
    headers = {
        'x-rapidapi-key': "515b8b336amsh2436fb4f5ef076ep184143jsn8d433aaad72f",
        'x-rapidapi-host': "sameer-kumar-aztro-v1.p.rapidapi.com"
    }
    response = requests.request("POST", url, headers=headers, params=querystring)

    return response.json()
    #Aries
    #Taurus
    #Gemini
    #Cancer
    #Leo
    #Virgo
    #Libra
    #Scorpio
    #Sagittarius
    #Capricorn
    #Aquarius
    #Pisces

    #today
    #yesterday
    #tomorrow

@app.route('/sharer/<id>')
def share(id):
    postId = id
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM horoscopes where id = %s" , [postId])
    post = cur.fetchone()
    cur.close()

    return render_template('sharer.html', horoscope = post)

def inputToHoroscope(horoscopeName,color,compatibility,luckyNumber,description):
    today = date.today()
    d2 = today.strftime("%B %d, %Y")

    #Insert to database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO horoscopes (horoscopeName,dateToday, color, compatibility,luckyNumber,description) VALUES (%s,%s,%s,%s,%s,%s);" , (horoscopeName,d2, color, compatibility,luckyNumber,description))
    mysql.connection.commit()
    lastid =cur.lastrowid
    cur.close()

    return str(lastid)

def encry(email):
    message = bytes(email, 'utf-8')
    shared_secret_key = b'402xy54zy78#'
    #Generate cryptographic hash using md5
    my_hmac = hmac.new(shared_secret_key, message, hashlib.sha1)
    my_hmac.digest()
    my_hmac_cpy = my_hmac.copy()
    return str(my_hmac.hexdigest())

def sendEmail(receiver_email):
    domain = 'https://seclogin.herokuapp.com/confirmEmail/' + receiver_email + "/" + encry(receiver_email)
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "secloginzodiac@gmail.com"  # Enter your address
    receiver_email = receiver_email  # Enter receiver address
    password = "Seclogin51@"
    message = """\
    Subject: Email Verification

    Hi there! \n
    We welcome you to Horoscope! \n
    We check your daily horoscope everyday and we hope you have a nice stay with us \n
    To verify your email please click on this link 
    """ + domain
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

@app.route('/confirmEmail/<email>/<hash>')
def confirmEmail(email, hash):
    if hash == encry(email):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users where email = %s and isVerified = 0" , [email])
        post = cur.fetchone()
        cur.close()

        if post != None:
            post = post['id']
            cur = mysql.connection.cursor()
            cur.execute("Update users set isVerified = 1 where id = %s" , (post))
            mysql.connection.commit()
            cur.close()
            return render_template('notice.html')

app.run(debug=True)