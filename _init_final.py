'''
Imports for Dataspark Project
'''
from content_management import Content,Level1List,TableList, ColumnList
import datetime
import dbfunctions
from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from flask_oauthlib.client import OAuth
import gc
import MySQLdb
from MySQLdb import escape_string as thwart
from flaskext.mysql import MySQL
from functools import wraps
from passlib.hash import sha256_crypt
import pymysql
from secret import stripekey
import stripe
from wtforms import Form, BooleanField, TextField, PasswordField, validators


'''
Initial Values
'''
app = Flask(__name__)
app.secret_key = "super secret key"
mysql = MySQL()
stripe_keys = stripekey()
stripe.api_key = stripe_keys['secret_key']
app.config['GOOGLE_ID'] = '736251434024-lcvhav3jh7me2c8g4d3u6sasi5r6lqf7.apps.googleusercontent.com'
app.config['GOOGLE_SECRET'] = 'g_EKGXUAh6-JwtmKsBmIwVDU'
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

###Special  Initializations
##Content Manager Values
TOPIC_DICT = Content()
LEVEL_1_DICT = Level1List()
TABLE_DICT = TableList()
COLUMNSLIST = []
tablelist = []

'''
Google Login Credentials
'''
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)

'''
Configurations for MySQL DB
'''
## MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'opendata101'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gY2pxWPikJzy4k6pyb'
app.config['MYSQL_DATABASE_DB'] = 'opendaas'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_HOST'] = "opendataasaservice.cxp4zxlvqfy4.ap-southeast-2.rds.amazonaws.com"
mysql.init_app(app)

##MySQL DB connection function
def connection():
	conn = mysql.connect()
	c = conn.cursor()
	return c, conn

'''
Form Definitions - Classes
'''

##Registration Form Class
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])

##Subscription Form Class
class SubscriptionForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
'''
Main Pages
'''

##Home Page
@app.route('/', methods=["GET","POST"])
def homepage():
    return render_template("main.html")

## Page about us
@app.route('/about/', methods=["GET", "POST"])
def about_page():
    return render_template("about.html")


## Page for contact
@app.route('/contact/', methods=["GET", "POST"])
def contact_page():
    return render_template("contact.html")



##Login Page
@app.route('/login/', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":
            if request.form.get('submit') == 'Log In':##For functional button under unsubbutton
                passwrd = c.execute("SELECT * FROM users WHERE username = (%s)",
                                 thwart(request.form['username']))
                passwrd = c.fetchone()[2]
                if sha256_crypt.verify(request.form['password'], passwrd):
                    email1 = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(request.form['username']))
                    email1 = c.fetchone()[3]
                    sid = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(request.form['username']))
                    sid = c.fetchone()[4]
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    session['email'] = email1
                    session['stripe_id'] = sid
                    session['pass'] = passwrd
                    mesg ="You are now logged in as " + session['email'] 
                    flash(mesg  )
                    return redirect(url_for("dashboard"))

                else:
                    error = "Invalid password, try again."
                print("altCheck")
                gc.collect()
            elif request.form.get('submit') == "Sign Up":
                print("checkit")
                return redirect(url_for("register_page"))
        return render_template("login.html", error=error)

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again later."
        return render_template("login.html", error = error)  
	
##Login Required Function
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))
    return wrap
		
@app.route("/logout/")
@login_required
def logout():
    session.pop('google_token', None)
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('homepage'))

'''
Registration and Account Pages
'''
		
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST":
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()
            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                customer = stripe.Customer.create(email=email)
                c.execute("INSERT INTO users (username, password, email, stripe_id) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart(customer.id)))
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username
                session['email'] = email
                session['stripe_id'] = customer.id
                return redirect(url_for('dashboard'))
        else:
            if 'google_token' in session:
                me = google.get('userinfo')
                altdata = jsonify({"data": me.data})
                email = altdata.data.email
                username = altdata.data.id
                c, conn = connection()
                x = c.execute("SELECT * FROM users WHERE username = (%s)",
                              (thwart(username)))

                if int(x) > 0:
                    flash("That username already exists, please choose another method for signup")
                    return render_template('register.html', form=form)

                else:
                    customer = stripe.Customer.create(
                        email=email
                        )
                
                    c.execute("INSERT INTO users (username, email, stripe_id, tracking) VALUES (%s, %s, %s, %s)",
                              (thwart(username), thwart(email), thwart(customer.id), thwart("/introduction-to-python-programming/")))
                    
                    conn.commit()
                    flash("Thanks for registering!")
                    c.close()
                    conn.close()
                    gc.collect()

                    session['logged_in'] = True
                    session['username'] = username
                    session['email'] = email
                    session['stripe_id'] = customer.id
                    return redirect(url_for('dashboard'))
                
        return render_template("register.html", form=form, key=stripe_keys['publishable_key'] )

    except Exception as e:
        return(str(e))
			
### Account Details Page

@app.route('/accounts/', methods=['GET','POST'])
@login_required
def accounts():
    try:
        if request.method == 'POST':
            if request.form.get('unsubbutton') == 'Unsubscribe':##For functional button under unsubbutton
                c, conn = connection()
                subid = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(session['username']))
                subid = c.fetchone()[5]
                accid = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(session['username']))
                accid = c.fetchone()[6]
                accpw = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(session['username']))
                accpw = c.fetchone()[7]
                if (subid != '0'):
                    subscription = stripe.Subscription.retrieve(subid)
                    subscription.delete()
                    c.execute("UPDATE users SET subscription = '0',account = '', dbpassword = '' WHERE username = (%s)",(thwart(session['username'])))
                    print('unsub1')
                    dbfunctions.userDelete(accid,accpw)
                    conn.commit()
                    print('unsub2 Success')
                    flash('Subscription Cancelled')
                else:
                    flash('No Current Subscriptions')
                c.close()
                conn.close()
                gc.collect()
                return render_template('accounts.html')
            elif request.form.get('updatepass') == 'Update WebApp Password':##For functional button under Change Password
                print('check 1')
                c, conn = connection()
                currpass = request.form.get('currentpassword')
                print(currpass)
                password = sha256_crypt.encrypt((str(currpass)))
                newpass = request.form.get('newpass')
                newcon  = request.form.get('newpassconfirm')
                syspass = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(session['username']))
                syspass = c.fetchone()[2]
                print('check 2')
                print(syspass)
                print(password)
                if (sha256_crypt.verify(currpass, syspass)):
                    print('check 3')
                    if (newcon==newpass):
                        buff = sha256_crypt.encrypt((str(newpass)))
                        c.execute("UPDATE users SET password = %s WHERE username = (%s)",(thwart(buff),thwart(session['username'])))
                        print('check 4')
                        conn.commit()
                        flash('Password Updated')
                    else:
                        print('check 5')
                        flash('New Passwords do not match')
                else:
                    print('check 6')
                    flash('Incorrect Password')
                c.close()
                conn.close()
                gc.collect()
                print('check 7')
                return render_template('accounts.html')
            elif request.form.get('deview') == 'Remove all Views':##For functional button under delete Views
                c, conn = connection()
                subid = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(session['username']))
                subid = c.fetchone()[5]
                accid = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(session['username']))
                accid = c.fetchone()[6]
                accpw = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(session['username']))
                accpw = c.fetchone()[7]
                if (subid != '0'):
                    allviews = dbfunctions.getViewNames(accid, accpw)
                    dbfunctions.viewsDelete(accid,accpw,allviews)
                    conn.commit()
                    print('unsub2 Success')
                    flash('All user views deleted')
                else:
                    flash('No Views Attached to User')
                c.close()
                conn.close()
                gc.collect()
                print('check 7')
                return redirect(url_for("accounts"))
            elif request.form.get('DBPass') == 'Update Database Password':##For functional button under update DB Password
                c, conn = connection()
                subid = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(session['username']))
                subid = c.fetchone()[5]
                accid = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(session['username']))
                accid = c.fetchone()[6]
                accpw = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(session['username']))
                accpw = c.fetchone()[7]
                currpass = request.form.get('currentpassword1')
                newpass = request.form.get('newpass1')
                newcon  = request.form.get('newpassconfirm1')
                if (subid != '0'):
                    if (accpw ==currpass):
                        if (newpass == newcon):
                            dbfunctions.userUpdatePassword(accid, newpass)
                            c.execute("UPDATE users SET dbpassword = %s WHERE username = (%s)",(thwart(newpass),thwart(session['username'])))
                            conn.commit()
                            msg='Password for Database User '+accid+' has changed'
                            flash(msg)
                        else:
                            flash('New Passwords do not match')
                    else:
                        flash('Current password does not match with user')
                else:
                    flash('User has not subscribed to service.')
                c.close()
                conn.close()
                gc.collect()
                print('check 7')
                return redirect(url_for("accounts"))
        return render_template('accounts.html')
    except Exception as e:
        return render_template("500.html", error = str(e))

'''
Subscription Model Pages
'''

@app.route('/subscribe/', methods=['GET','POST'])
@login_required
def subscribe():
    try:
        cus = stripe.Customer.retrieve(session['stripe_id'])
        subs = cus.subscriptions
        if len(subs)>0:
            flash("User already subscribed")
            return redirect(url_for("dashboard"))
        else:
            return render_template('subscribe.html', key=stripe_keys['publishable_key'], email = session['email'])
    except Exception as e:
        return render_template("500.html", error = str(e))
   

@app.route('/charge', methods=['GET','POST'])
@login_required
def charge():
    # Amount in cents
    amount = 1000
    stripe.Customer.modify(session['stripe_id'],
    source=request.form['stripeToken'],
    )
    charge = stripe.Subscription.create(
        items=[{'plan': 'plan_CcnWYO752Yw8S6'}],
        customer = session['stripe_id'],
    )
    sub = charge.id
    c, conn = connection()
    c.execute("UPDATE users SET subscription = (%s) WHERE username = (%s)",(thwart(sub), thwart(session['username'])))
    conn.commit()
    c.close()
    conn.close()
    gc.collect()
    
    msg = 'You just subscribed for '+'%.2f'%(amount/100)+' AUD!!'
    flash(msg)
    return redirect(url_for('subregister'))
    #return render_template('charge.html', amount=amount)

@app.route('/chargeyearly', methods=['GET','POST'])
@login_required
def chargeyearly():
    # Amount in cents
    amount = 10000
    stripe.Customer.modify(session['stripe_id'],
    source=request.form['stripeToken'],
    )
    charge = stripe.Subscription.create(
        items=[{'plan': 'plan_ChC97qvzmnNQl3'}],
        customer = session['stripe_id'],
    )
    sub = charge.id
    c, conn = connection()
    c.execute("UPDATE users SET subscription = %s WHERE username = %s",(thwart(sub), thwart(session['username'])))
    conn.commit()
    c.close()
    conn.close()
    gc.collect()

    msg = 'You just subscribed for '+'%.2f'%(amount/100)+' AUD!!'
    flash(msg)
    return redirect(url_for('subregister'))

@app.route('/subregister/', methods=["GET","POST"])
@login_required
def subregister():
    try:
        form = SubscriptionForm(request.form)

        if request.method == "POST" and form.validate():
            account  = form.username.data
            dbpassword = (form.password.data)
            if (dbfunctions.checkUser(account)):
                flash("Database Account Already exists, please choose a new Username.")
                return render_template('subregister.html', form=form)
            
            c, conn = connection()
            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(session['username'])))

            if int(x) > 0:
                c.execute("UPDATE users SET account=%s, dbpassword = %s WHERE username =%s",
                          (thwart(account), thwart(dbpassword), thwart(session['username'])))
                conn.commit()
                flash("Please remember your Database Account Details")
                c.close()
                conn.close()
                gc.collect()
                tablenames = [i[0] for i in TABLE_DICT['ABS']]
                dbfunctions.createUser(account, dbpassword,tablenames)
            
                return redirect(url_for('dashboard'))

            else:
                flash("Try Again Please")
                return render_template('subregister.html', form=form)
        return render_template("subregister.html", form=form)

    except Exception as e:
        return(str(e))
 
'''
Database Catalog Pages
'''
### Main Dashboard

@app.route('/dashboard/')
def dashboard():
	try:
		return render_template("dashboard.html", TOPIC_DICT = TOPIC_DICT)
	except Exception as e:
	    return render_template("500.html", error = str(e))

### Database Catalog Items

@app.route(TOPIC_DICT["Catalog"][0][1], methods=['GET', 'POST'])
@login_required
def ABS__Census_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Catalog/abs_census.html", curLink = TOPIC_DICT["Catalog"][0][1], curTitle=TOPIC_DICT["Catalog"][0][0],  nextLink = TOPIC_DICT["Catalog"][1][1], nextTitle = TOPIC_DICT["Catalog"][1][0],LEVEL_1_DICT = LEVEL_1_DICT)


@app.route(TOPIC_DICT["Catalog"][1][1], methods=['GET', 'POST'])
def Weather_TBD():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Catalog/weather.html", curLink = TOPIC_DICT["Catalog"][1][1], curTitle=TOPIC_DICT["Catalog"][1][0],  nextLink = TOPIC_DICT["Catalog"][2][1], nextTitle = TOPIC_DICT["Catalog"][2][0])

### ABS Selection Cycle

##Currently defaulted to all tables in set (110 tables)
@app.route('/abs_tables/' ,methods=['GET', 'POST'])
@login_required
def abs_tables():
    try:
        c, conn = connection()
        subid = c.execute("SELECT * FROM users WHERE username = (%s)", thwart(session['username']))
        subid = c.fetchone()[5]
        if (subid == '0'):
            flash('Please Subscribe before proceeding!')
            return redirect(url_for('dashboard'))
        else:
            return render_template("abs_tables.html",TABLE_DICT = TABLE_DICT)
    except Exception as e:
        return render_template("500.html", error = str(e))


##Columns of selected tables
@app.route('/tags/' ,methods=['GET', 'POST'])
def tags():
    try:
        tablelist = []
        COLUMNSLIST = []
        bufferval = []
        if request.method == "POST":
            if (request.form.get('submit')=='Submit'):
                tablelist = request.form.getlist('checks')
                session['tablelist'] = tablelist
                COLUMNSLIST = ColumnList(tablelist)
            elif (request.form.get('submit')=='Select all'):
                for tablenames in TABLE_DICT['ABS']:
                    tablelist.append(tablenames[0])
                session['tablelist'] = tablelist
                COLUMNSLIST = ColumnList(tablelist)
        else:
            COLUMNSLIST = "Bummer"
        return render_template("tags.html",TABLE_DICT = TABLE_DICT,tablelist = tablelist,COLUMNSLIST = COLUMNSLIST, bufferval = bufferval)
    except Exception as e:
        return render_template("500.html", error = str(e))

##View Generation functions called here
@app.route('/sqlgen/' ,methods=['GET', 'POST'])
def sqlgen():
    try:
        c, conn = connection()
        dataset = []
        tablelist = session['tablelist']
        if request.method == "POST":
            if (request.form.get('submit')=='Submit'):
                dataset = request.form.getlist('checks')
            elif (request.form.get('submit')=='Select all'):
                COLUMNSLIST = ColumnList(tablelist)
                for table in tablelist:
                    for columnName in COLUMNSLIST[table]:
                        dataset.append(columnName[0])
            viewname = request.form['viewname']
            account = c.execute("SELECT * FROM users WHERE username = (%s)",
                             thwart(session['username']))
            account = c.fetchone()[6]
            dbpass = c.execute("SELECT * FROM users WHERE username = (%s)",
                             thwart(session['username']))
            dbpass = c.fetchone()[7]
            a = dbfunctions.createView(tablelist, dataset, viewname, account, "DataSparkDataBase")
            return render_template("sqlgen.html",dataset = dataset, a = a)
        else:
            return render_template("sqlgen.html",dataset = dataset, a = "Whoops!!!")
    except Exception as e:
        return render_template("500.html", error = str(e))
        gc.collect()

'''
Error Functions
'''
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
	
@app.errorhandler(405)
def page_not_found(e):
    return render_template("405.html")
	
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html",error = str(e))

@app.errorhandler(400)
def page_not_found(e):
    return render_template("500.html",error = str(e))

'''
Alternate Logins
'''
### Google Stuff
@app.route('/googlelogin/')
def googlelogin():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('googlelogin'))


@app.route('/googleauth/')
def googleauth():
    return google.authorize(callback=url_for('googleauthorized', _external=True))


@app.route('/login/authorized')
def googleauthorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')



####Runtime	
if __name__ == "__main__":
    app.debug = True
    app.run()