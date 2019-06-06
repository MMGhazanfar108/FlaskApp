from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
from content_management import Content
from flask.ext.mysql import MySQL
from functools import wraps

app = Flask(__name__)
app.secret_key = "super secret key"
mysql = MySQL()


TOPIC_DICT = Content()

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])
    

	

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'pythonprogramming'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

import MySQLdb

def connection():
	conn = mysql.connect()
	c = conn.cursor()
	return c, conn

@app.route('/', methods=["GET","POST"])
def homepage():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
	try:
		return render_template("dashboard.html", TOPIC_DICT = TOPIC_DICT)
	except Exception as e:
	    return render_template("500.html", error = str(e))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
	
@app.errorhandler(405)
def page_not_found(e):
    return render_template("405.html")
	
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html",error = str(e))



@app.route('/login/', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":

            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                             thwart(request.form['username']))
            
            data = c.fetchone()[2]

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for("dashboard"))

            else:
                error = "Invalid password, try again."

        gc.collect()

        return render_template("login.html", error=error)

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again later."
        return render_template("login.html", error = error)  
	
		
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
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
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))
			
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
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('dashboard'))


###Webpages

@app.route(TOPIC_DICT["Basics"][0][1], methods=['GET', 'POST'])
def Python_Introduction():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/introduction-to-python-programming.html", curLink = TOPIC_DICT["Basics"][0][1], curTitle=TOPIC_DICT["Basics"][0][0],  nextLink = TOPIC_DICT["Basics"][1][1], nextTitle = TOPIC_DICT["Basics"][1][0])




@app.route(TOPIC_DICT["Basics"][1][1], methods=['GET', 'POST'])
def Print_Function_and_Strings():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-tutorial-print-function-strings.html", curLink = TOPIC_DICT["Basics"][1][1], curTitle=TOPIC_DICT["Basics"][1][0],  nextLink = TOPIC_DICT["Basics"][2][1], nextTitle = TOPIC_DICT["Basics"][2][0])




@app.route(TOPIC_DICT["Basics"][2][1], methods=['GET', 'POST'])
def Math_with_Python():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/math-basics-python-3-beginner-tutorial.html", curLink = TOPIC_DICT["Basics"][2][1], curTitle=TOPIC_DICT["Basics"][2][0],  nextLink = TOPIC_DICT["Basics"][3][1], nextTitle = TOPIC_DICT["Basics"][3][0])




@app.route(TOPIC_DICT["Basics"][3][1], methods=['GET', 'POST'])
def Variables():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-3-variables-tutorial.html", curLink = TOPIC_DICT["Basics"][3][1], curTitle=TOPIC_DICT["Basics"][3][0],  nextLink = TOPIC_DICT["Basics"][4][1], nextTitle = TOPIC_DICT["Basics"][4][0])




@app.route(TOPIC_DICT["Basics"][4][1], methods=['GET', 'POST'])
def While_Loop():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-3-loop-tutorial.html", curLink = TOPIC_DICT["Basics"][4][1], curTitle=TOPIC_DICT["Basics"][4][0],  nextLink = TOPIC_DICT["Basics"][5][1], nextTitle = TOPIC_DICT["Basics"][5][0])




@app.route(TOPIC_DICT["Basics"][5][1], methods=['GET', 'POST'])
def For_Loop():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/loop-python-3-basics-tutorial.html", curLink = TOPIC_DICT["Basics"][5][1], curTitle=TOPIC_DICT["Basics"][5][0],  nextLink = TOPIC_DICT["Basics"][6][1], nextTitle = TOPIC_DICT["Basics"][6][0])




@app.route(TOPIC_DICT["Basics"][6][1], methods=['GET', 'POST'])
def If_Statement():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/if-statement-python-3-basics-tutorial.html", curLink = TOPIC_DICT["Basics"][6][1], curTitle=TOPIC_DICT["Basics"][6][0],  nextLink = TOPIC_DICT["Basics"][7][1], nextTitle = TOPIC_DICT["Basics"][7][0])




@app.route(TOPIC_DICT["Basics"][7][1], methods=['GET', 'POST'])
def If_Else():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/else-python-3-tutorial.html", curLink = TOPIC_DICT["Basics"][7][1], curTitle=TOPIC_DICT["Basics"][7][0],  nextLink = TOPIC_DICT["Basics"][8][1], nextTitle = TOPIC_DICT["Basics"][8][0])




@app.route(TOPIC_DICT["Basics"][8][1], methods=['GET', 'POST'])
def If_Elif_Else():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/elif-else-python-3-tutorial.html", curLink = TOPIC_DICT["Basics"][8][1], curTitle=TOPIC_DICT["Basics"][8][0],  nextLink = TOPIC_DICT["Basics"][9][1], nextTitle = TOPIC_DICT["Basics"][9][0])




@app.route(TOPIC_DICT["Basics"][9][1], methods=['GET', 'POST'])
def Functions():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/functions-python-3-basics-tutorial.html", curLink = TOPIC_DICT["Basics"][9][1], curTitle=TOPIC_DICT["Basics"][9][0],  nextLink = TOPIC_DICT["Basics"][10][1], nextTitle = TOPIC_DICT["Basics"][10][0])




@app.route(TOPIC_DICT["Basics"][10][1], methods=['GET', 'POST'])
def Function_Parameters():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/function-parameters-python-3-basics.html", curLink = TOPIC_DICT["Basics"][10][1], curTitle=TOPIC_DICT["Basics"][10][0],  nextLink = TOPIC_DICT["Basics"][11][1], nextTitle = TOPIC_DICT["Basics"][11][0])




@app.route(TOPIC_DICT["Basics"][11][1], methods=['GET', 'POST'])
def Function_Parameter_Defaults():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/function-parameter-defaults-python-3-basics.html", curLink = TOPIC_DICT["Basics"][11][1], curTitle=TOPIC_DICT["Basics"][11][0],  nextLink = TOPIC_DICT["Basics"][12][1], nextTitle = TOPIC_DICT["Basics"][12][0])




@app.route(TOPIC_DICT["Basics"][12][1], methods=['GET', 'POST'])
def Global_and_Local_Variables():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/global-local-variables.html", curLink = TOPIC_DICT["Basics"][12][1], curTitle=TOPIC_DICT["Basics"][12][0],  nextLink = TOPIC_DICT["Basics"][13][1], nextTitle = TOPIC_DICT["Basics"][13][0])




@app.route(TOPIC_DICT["Basics"][13][1], methods=['GET', 'POST'])
def Installing_Modules():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/installing-modules-python-3.html", curLink = TOPIC_DICT["Basics"][13][1], curTitle=TOPIC_DICT["Basics"][13][0],  nextLink = TOPIC_DICT["Basics"][14][1], nextTitle = TOPIC_DICT["Basics"][14][0])




@app.route(TOPIC_DICT["Basics"][14][1], methods=['GET', 'POST'])
def How_to_download_and_install_Python_Packages_and_Modules_with_Pip_():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/using-pip-install-for-python-modules.html", curLink = TOPIC_DICT["Basics"][14][1], curTitle=TOPIC_DICT["Basics"][14][0],  nextLink = TOPIC_DICT["Basics"][15][1], nextTitle = TOPIC_DICT["Basics"][15][0])




@app.route(TOPIC_DICT["Basics"][15][1], methods=['GET', 'POST'])
def Common_Errors():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/common-errors-python-3-basics.html", curLink = TOPIC_DICT["Basics"][15][1], curTitle=TOPIC_DICT["Basics"][15][0],  nextLink = TOPIC_DICT["Basics"][16][1], nextTitle = TOPIC_DICT["Basics"][16][0])




@app.route(TOPIC_DICT["Basics"][16][1], methods=['GET', 'POST'])
def Writing_to_a_File():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/writing-file-python-3-basics.html", curLink = TOPIC_DICT["Basics"][16][1], curTitle=TOPIC_DICT["Basics"][16][0],  nextLink = TOPIC_DICT["Basics"][17][1], nextTitle = TOPIC_DICT["Basics"][17][0])




@app.route(TOPIC_DICT["Basics"][17][1], methods=['GET', 'POST'])
def Appending_Files():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/appending-file-python-3-tutorial.html", curLink = TOPIC_DICT["Basics"][17][1], curTitle=TOPIC_DICT["Basics"][17][0],  nextLink = TOPIC_DICT["Basics"][18][1], nextTitle = TOPIC_DICT["Basics"][18][0])




@app.route(TOPIC_DICT["Basics"][18][1], methods=['GET', 'POST'])
def Reading_from_Files():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/reading-file-python-3-tutorial.html", curLink = TOPIC_DICT["Basics"][18][1], curTitle=TOPIC_DICT["Basics"][18][0],  nextLink = TOPIC_DICT["Basics"][19][1], nextTitle = TOPIC_DICT["Basics"][19][0])




@app.route(TOPIC_DICT["Basics"][19][1], methods=['GET', 'POST'])
def Classes():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/classes-python-3-basics-tutorial.html", curLink = TOPIC_DICT["Basics"][19][1], curTitle=TOPIC_DICT["Basics"][19][0],  nextLink = TOPIC_DICT["Basics"][20][1], nextTitle = TOPIC_DICT["Basics"][20][0])




@app.route(TOPIC_DICT["Basics"][20][1], methods=['GET', 'POST'])
def Frequently_asked_Questions():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/frequently-asked-questions-python-3.html", curLink = TOPIC_DICT["Basics"][20][1], curTitle=TOPIC_DICT["Basics"][20][0],  nextLink = TOPIC_DICT["Basics"][21][1], nextTitle = TOPIC_DICT["Basics"][21][0])




@app.route(TOPIC_DICT["Basics"][21][1], methods=['GET', 'POST'])
def Getting_User_Input():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/user-input-python-3-tutorial.html", curLink = TOPIC_DICT["Basics"][21][1], curTitle=TOPIC_DICT["Basics"][21][0],  nextLink = TOPIC_DICT["Basics"][22][1], nextTitle = TOPIC_DICT["Basics"][22][0])




@app.route(TOPIC_DICT["Basics"][22][1], methods=['GET', 'POST'])
def Statistics_Module():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/statistics-python-3-module-mean-standard-deviation.html", curLink = TOPIC_DICT["Basics"][22][1], curTitle=TOPIC_DICT["Basics"][22][0],  nextLink = TOPIC_DICT["Basics"][23][1], nextTitle = TOPIC_DICT["Basics"][23][0])




@app.route(TOPIC_DICT["Basics"][23][1], methods=['GET', 'POST'])
def Module_import_Syntax():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/module-import-syntax-python-3-tutorial.html", curLink = TOPIC_DICT["Basics"][23][1], curTitle=TOPIC_DICT["Basics"][23][0],  nextLink = TOPIC_DICT["Basics"][24][1], nextTitle = TOPIC_DICT["Basics"][24][0])




@app.route(TOPIC_DICT["Basics"][24][1], methods=['GET', 'POST'])
def Making_your_own_Modules():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/making-modules.html", curLink = TOPIC_DICT["Basics"][24][1], curTitle=TOPIC_DICT["Basics"][24][0],  nextLink = TOPIC_DICT["Basics"][25][1], nextTitle = TOPIC_DICT["Basics"][25][0])




@app.route(TOPIC_DICT["Basics"][25][1], methods=['GET', 'POST'])
def Python_Lists_vs_Tuples():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-lists-vs-tuples.html", curLink = TOPIC_DICT["Basics"][25][1], curTitle=TOPIC_DICT["Basics"][25][0],  nextLink = TOPIC_DICT["Basics"][26][1], nextTitle = TOPIC_DICT["Basics"][26][0])




@app.route(TOPIC_DICT["Basics"][26][1], methods=['GET', 'POST'])
def List_Manipulation():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-3-list-manipulation.html", curLink = TOPIC_DICT["Basics"][26][1], curTitle=TOPIC_DICT["Basics"][26][0],  nextLink = TOPIC_DICT["Basics"][27][1], nextTitle = TOPIC_DICT["Basics"][27][0])




@app.route(TOPIC_DICT["Basics"][27][1], methods=['GET', 'POST'])
def Multi_dimensional_lists():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-3-multi-dimensional-list.html", curLink = TOPIC_DICT["Basics"][27][1], curTitle=TOPIC_DICT["Basics"][27][0],  nextLink = TOPIC_DICT["Basics"][28][1], nextTitle = TOPIC_DICT["Basics"][28][0])




@app.route(TOPIC_DICT["Basics"][28][1], methods=['GET', 'POST'])
def Reading_CSV_files_in_Python():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/reading-csv-files-python-3.html", curLink = TOPIC_DICT["Basics"][28][1], curTitle=TOPIC_DICT["Basics"][28][0],  nextLink = TOPIC_DICT["Basics"][29][1], nextTitle = TOPIC_DICT["Basics"][29][0])




@app.route(TOPIC_DICT["Basics"][29][1], methods=['GET', 'POST'])
def Try_and_Except_Error_handling():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/handling-exceptions-try-except-python-3.html", curLink = TOPIC_DICT["Basics"][29][1], curTitle=TOPIC_DICT["Basics"][29][0],  nextLink = TOPIC_DICT["Basics"][30][1], nextTitle = TOPIC_DICT["Basics"][30][0])




@app.route(TOPIC_DICT["Basics"][30][1], methods=['GET', 'POST'])
def Multi_Line_printing():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/multi-line-printing-python-3.html", curLink = TOPIC_DICT["Basics"][30][1], curTitle=TOPIC_DICT["Basics"][30][0],  nextLink = TOPIC_DICT["Basics"][31][1], nextTitle = TOPIC_DICT["Basics"][31][0])




@app.route(TOPIC_DICT["Basics"][31][1], methods=['GET', 'POST'])
def Python_dictionaries():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/dictionaries-tutorial-python-3.html", curLink = TOPIC_DICT["Basics"][31][1], curTitle=TOPIC_DICT["Basics"][31][0],  nextLink = TOPIC_DICT["Basics"][32][1], nextTitle = TOPIC_DICT["Basics"][32][0])




@app.route(TOPIC_DICT["Basics"][32][1], methods=['GET', 'POST'])
def Built_in_functions():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/built-functions-python-3.html", curLink = TOPIC_DICT["Basics"][32][1], curTitle=TOPIC_DICT["Basics"][32][0],  nextLink = TOPIC_DICT["Basics"][33][1], nextTitle = TOPIC_DICT["Basics"][33][0])




@app.route(TOPIC_DICT["Basics"][33][1], methods=['GET', 'POST'])
def OS_Module():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-3-os-module.html", curLink = TOPIC_DICT["Basics"][33][1], curTitle=TOPIC_DICT["Basics"][33][0],  nextLink = TOPIC_DICT["Basics"][34][1], nextTitle = TOPIC_DICT["Basics"][34][0])




@app.route(TOPIC_DICT["Basics"][34][1], methods=['GET', 'POST'])
def SYS_module():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/sys-module-python-3.html", curLink = TOPIC_DICT["Basics"][34][1], curTitle=TOPIC_DICT["Basics"][34][0],  nextLink = TOPIC_DICT["Basics"][35][1], nextTitle = TOPIC_DICT["Basics"][35][0])




@app.route(TOPIC_DICT["Basics"][35][1], methods=['GET', 'POST'])
def Python_urllib_tutorial_for_Accessing_the_Internet():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/urllib-tutorial-python-3.html", curLink = TOPIC_DICT["Basics"][35][1], curTitle=TOPIC_DICT["Basics"][35][0],  nextLink = TOPIC_DICT["Basics"][36][1], nextTitle = TOPIC_DICT["Basics"][36][0])




@app.route(TOPIC_DICT["Basics"][36][1], methods=['GET', 'POST'])
def Regular_Expressions_with_re():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/regular-expressions-regex-tutorial-python-3.html", curLink = TOPIC_DICT["Basics"][36][1], curTitle=TOPIC_DICT["Basics"][36][0],  nextLink = TOPIC_DICT["Basics"][37][1], nextTitle = TOPIC_DICT["Basics"][37][0])




@app.route(TOPIC_DICT["Basics"][37][1], methods=['GET', 'POST'])
def How_to_Parse_a_Website_with_regex_and_urllib():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/parse-website-using-regular-expressions-urllib.html", curLink = TOPIC_DICT["Basics"][37][1], curTitle=TOPIC_DICT["Basics"][37][0],  nextLink = TOPIC_DICT["Basics"][38][1], nextTitle = TOPIC_DICT["Basics"][38][0])




@app.route(TOPIC_DICT["Basics"][38][1], methods=['GET', 'POST'])
def Tkinter_intro():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-3-tkinter-basics-tutorial.html", curLink = TOPIC_DICT["Basics"][38][1], curTitle=TOPIC_DICT["Basics"][38][0],  nextLink = TOPIC_DICT["Basics"][39][1], nextTitle = TOPIC_DICT["Basics"][39][0])




@app.route(TOPIC_DICT["Basics"][39][1], methods=['GET', 'POST'])
def Tkinter_buttons():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/tkinter-python-3-tutorial-adding-buttons.html", curLink = TOPIC_DICT["Basics"][39][1], curTitle=TOPIC_DICT["Basics"][39][0],  nextLink = TOPIC_DICT["Basics"][40][1], nextTitle = TOPIC_DICT["Basics"][40][0])




@app.route(TOPIC_DICT["Basics"][40][1], methods=['GET', 'POST'])
def Tkinter_event_handling():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/tkinter-tutorial-python-3-event-handling.html", curLink = TOPIC_DICT["Basics"][40][1], curTitle=TOPIC_DICT["Basics"][40][0],  nextLink = TOPIC_DICT["Basics"][41][1], nextTitle = TOPIC_DICT["Basics"][41][0])




@app.route(TOPIC_DICT["Basics"][41][1], methods=['GET', 'POST'])
def Tkinter_menu_bar():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/tkinter-menu-bar-tutorial.html", curLink = TOPIC_DICT["Basics"][41][1], curTitle=TOPIC_DICT["Basics"][41][0],  nextLink = TOPIC_DICT["Basics"][42][1], nextTitle = TOPIC_DICT["Basics"][42][0])




@app.route(TOPIC_DICT["Basics"][42][1], methods=['GET', 'POST'])
def Tkinter_images_text_and_conclusion():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/tkinter-adding-text-images.html", curLink = TOPIC_DICT["Basics"][42][1], curTitle=TOPIC_DICT["Basics"][42][0],  nextLink = TOPIC_DICT["Basics"][43][1], nextTitle = TOPIC_DICT["Basics"][43][0])




@app.route(TOPIC_DICT["Basics"][43][1], methods=['GET', 'POST'])
def Threading_module():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/threading-tutorial-python.html", curLink = TOPIC_DICT["Basics"][43][1], curTitle=TOPIC_DICT["Basics"][43][0],  nextLink = TOPIC_DICT["Basics"][44][1], nextTitle = TOPIC_DICT["Basics"][44][0])




@app.route(TOPIC_DICT["Basics"][44][1], methods=['GET', 'POST'])
def CX_Freeze():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/converting-python-scripts-exe-executables.html", curLink = TOPIC_DICT["Basics"][44][1], curTitle=TOPIC_DICT["Basics"][44][0],  nextLink = TOPIC_DICT["Basics"][45][1], nextTitle = TOPIC_DICT["Basics"][45][0])




@app.route(TOPIC_DICT["Basics"][45][1], methods=['GET', 'POST'])
def The_Subprocess_Module():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-3-subprocess-tutorial.html", curLink = TOPIC_DICT["Basics"][45][1], curTitle=TOPIC_DICT["Basics"][45][0],  nextLink = TOPIC_DICT["Basics"][46][1], nextTitle = TOPIC_DICT["Basics"][46][0])




@app.route(TOPIC_DICT["Basics"][46][1], methods=['GET', 'POST'])
def Matplotlib_Crash_Course():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/matplotlib-python-3-basics-tutorial.html", curLink = TOPIC_DICT["Basics"][46][1], curTitle=TOPIC_DICT["Basics"][46][0],  nextLink = TOPIC_DICT["Basics"][47][1], nextTitle = TOPIC_DICT["Basics"][47][0])




@app.route(TOPIC_DICT["Basics"][47][1], methods=['GET', 'POST'])
def Python_ftplib_Tutorial():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/ftp-transfers-python-ftplib.html", curLink = TOPIC_DICT["Basics"][47][1], curTitle=TOPIC_DICT["Basics"][47][0],  nextLink = TOPIC_DICT["Basics"][48][1], nextTitle = TOPIC_DICT["Basics"][48][0])




@app.route(TOPIC_DICT["Basics"][48][1], methods=['GET', 'POST'])
def Sockets_with_Python_Intro():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-sockets.html", curLink = TOPIC_DICT["Basics"][48][1], curTitle=TOPIC_DICT["Basics"][48][0],  nextLink = TOPIC_DICT["Basics"][49][1], nextTitle = TOPIC_DICT["Basics"][49][0])




@app.route(TOPIC_DICT["Basics"][49][1], methods=['GET', 'POST'])
def Simple_Port_Scanner_with_Sockets():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-port-scanner-sockets.html", curLink = TOPIC_DICT["Basics"][49][1], curTitle=TOPIC_DICT["Basics"][49][0],  nextLink = TOPIC_DICT["Basics"][50][1], nextTitle = TOPIC_DICT["Basics"][50][0])




@app.route(TOPIC_DICT["Basics"][50][1], methods=['GET', 'POST'])
def Threaded_Port_Scanner():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-threaded-port-scanner.html", curLink = TOPIC_DICT["Basics"][50][1], curTitle=TOPIC_DICT["Basics"][50][0],  nextLink = TOPIC_DICT["Basics"][51][1], nextTitle = TOPIC_DICT["Basics"][51][0])




@app.route(TOPIC_DICT["Basics"][51][1], methods=['GET', 'POST'])
def Binding_and_Listening_with_Sockets():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-binding-listening-sockets.html", curLink = TOPIC_DICT["Basics"][51][1], curTitle=TOPIC_DICT["Basics"][51][0],  nextLink = TOPIC_DICT["Basics"][52][1], nextTitle = TOPIC_DICT["Basics"][52][0])




@app.route(TOPIC_DICT["Basics"][52][1], methods=['GET', 'POST'])
def Client_Server_System_with_Sockets():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/client-server-python-sockets.html", curLink = TOPIC_DICT["Basics"][52][1], curTitle=TOPIC_DICT["Basics"][52][0],  nextLink = TOPIC_DICT["Basics"][53][1], nextTitle = TOPIC_DICT["Basics"][53][0])




@app.route(TOPIC_DICT["Basics"][53][1], methods=['GET', 'POST'])
def Python_2to3_for_Converting_Python_2_scripts_to_Python_3():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/converting-python2-to-python3-2to3.html", curLink = TOPIC_DICT["Basics"][53][1], curTitle=TOPIC_DICT["Basics"][53][0],  nextLink = TOPIC_DICT["Basics"][54][1], nextTitle = TOPIC_DICT["Basics"][54][0])




@app.route(TOPIC_DICT["PyGame"][0][1], methods=['GET', 'POST'])
def Introduction_to_PyGame():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/pygame-python-3-part-1-intro.html", curLink = TOPIC_DICT["PyGame"][0][1], curTitle=TOPIC_DICT["PyGame"][0][0],  nextLink = TOPIC_DICT["PyGame"][1][1], nextTitle = TOPIC_DICT["PyGame"][1][0])




@app.route(TOPIC_DICT["PyGame"][1][1], methods=['GET', 'POST'])
def Displaying_images_with_PyGame():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/displaying-images-pygame.html", curLink = TOPIC_DICT["PyGame"][1][1], curTitle=TOPIC_DICT["PyGame"][1][0],  nextLink = TOPIC_DICT["PyGame"][2][1], nextTitle = TOPIC_DICT["PyGame"][2][0])




@app.route(TOPIC_DICT["PyGame"][2][1], methods=['GET', 'POST'])
def Moving_an_image_around_in_PyGame():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/pygame-tutorial-moving-images-key-input.html", curLink = TOPIC_DICT["PyGame"][2][1], curTitle=TOPIC_DICT["PyGame"][2][0],  nextLink = TOPIC_DICT["PyGame"][3][1], nextTitle = TOPIC_DICT["PyGame"][3][0])




@app.route(TOPIC_DICT["PyGame"][3][1], methods=['GET', 'POST'])
def Adding_boundaries():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/adding-boundaries-pygame-video-game.html", curLink = TOPIC_DICT["PyGame"][3][1], curTitle=TOPIC_DICT["PyGame"][3][0],  nextLink = TOPIC_DICT["PyGame"][4][1], nextTitle = TOPIC_DICT["PyGame"][4][0])




@app.route(TOPIC_DICT["PyGame"][4][1], methods=['GET', 'POST'])
def Displaying_text_to_PyGame_screen():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/displaying-text-pygame-screen.html", curLink = TOPIC_DICT["PyGame"][4][1], curTitle=TOPIC_DICT["PyGame"][4][0],  nextLink = TOPIC_DICT["PyGame"][5][1], nextTitle = TOPIC_DICT["PyGame"][5][0])




@app.route(TOPIC_DICT["PyGame"][5][1], methods=['GET', 'POST'])
def Drawing_objects_with_PyGame():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/drawing-objects-pygame-tutorial.html", curLink = TOPIC_DICT["PyGame"][5][1], curTitle=TOPIC_DICT["PyGame"][5][0],  nextLink = TOPIC_DICT["PyGame"][6][1], nextTitle = TOPIC_DICT["PyGame"][6][0])




@app.route(TOPIC_DICT["PyGame"][6][1], methods=['GET', 'POST'])
def Crashing():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/pygame-crashing-objects.html", curLink = TOPIC_DICT["PyGame"][6][1], curTitle=TOPIC_DICT["PyGame"][6][0],  nextLink = TOPIC_DICT["PyGame"][7][1], nextTitle = TOPIC_DICT["PyGame"][7][0])




@app.route(TOPIC_DICT["PyGame"][7][1], methods=['GET', 'POST'])
def PyGame_Score():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/adding-score-pygame-video-game.html", curLink = TOPIC_DICT["PyGame"][7][1], curTitle=TOPIC_DICT["PyGame"][7][0],  nextLink = TOPIC_DICT["PyGame"][8][1], nextTitle = TOPIC_DICT["PyGame"][8][0])




@app.route(TOPIC_DICT["PyGame"][8][1], methods=['GET', 'POST'])
def Drawing_Objects_and_Shapes_in_PyGame():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/pygame-drawing-shapes-objects.html", curLink = TOPIC_DICT["PyGame"][8][1], curTitle=TOPIC_DICT["PyGame"][8][0],  nextLink = TOPIC_DICT["PyGame"][9][1], nextTitle = TOPIC_DICT["PyGame"][9][0])




@app.route(TOPIC_DICT["PyGame"][9][1], methods=['GET', 'POST'])
def Creating_a_start_menu():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/pygame-start-menu-tutorial.html", curLink = TOPIC_DICT["PyGame"][9][1], curTitle=TOPIC_DICT["PyGame"][9][0],  nextLink = TOPIC_DICT["PyGame"][10][1], nextTitle = TOPIC_DICT["PyGame"][10][0])




@app.route(TOPIC_DICT["PyGame"][10][1], methods=['GET', 'POST'])
def PyGame_Buttons_part_1_drawing_the_rectangle():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/pygame-buttons-part-1-button-rectangle.html", curLink = TOPIC_DICT["PyGame"][10][1], curTitle=TOPIC_DICT["PyGame"][10][0],  nextLink = TOPIC_DICT["PyGame"][11][1], nextTitle = TOPIC_DICT["PyGame"][11][0])




@app.route(TOPIC_DICT["PyGame"][11][1], methods=['GET', 'POST'])
def PyGame_Buttons_part_2_making_the_buttons_interactive():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/making-interactive-pygame-buttons.html", curLink = TOPIC_DICT["PyGame"][11][1], curTitle=TOPIC_DICT["PyGame"][11][0],  nextLink = TOPIC_DICT["PyGame"][12][1], nextTitle = TOPIC_DICT["PyGame"][12][0])




@app.route(TOPIC_DICT["PyGame"][12][1], methods=['GET', 'POST'])
def PyGame_Buttons_part_3_adding_text_to_the_button():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/placing-text-pygame-buttons.html", curLink = TOPIC_DICT["PyGame"][12][1], curTitle=TOPIC_DICT["PyGame"][12][0],  nextLink = TOPIC_DICT["PyGame"][13][1], nextTitle = TOPIC_DICT["PyGame"][13][0])




@app.route(TOPIC_DICT["PyGame"][13][1], methods=['GET', 'POST'])
def PyGame_Buttons_part_4_creating_a_general_PyGame_button_function():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/pygame-button-function.html", curLink = TOPIC_DICT["PyGame"][13][1], curTitle=TOPIC_DICT["PyGame"][13][0],  nextLink = TOPIC_DICT["PyGame"][14][1], nextTitle = TOPIC_DICT["PyGame"][14][0])




@app.route(TOPIC_DICT["PyGame"][14][1], methods=['GET', 'POST'])
def PyGame_Buttons_part_5_running_functions_on_a_button_click():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/pygame-button-function-events.html", curLink = TOPIC_DICT["PyGame"][14][1], curTitle=TOPIC_DICT["PyGame"][14][0],  nextLink = TOPIC_DICT["PyGame"][15][1], nextTitle = TOPIC_DICT["PyGame"][15][0])




@app.route(TOPIC_DICT["PyGame"][15][1], methods=['GET', 'POST'])
def Converting_PyGame_to_an_executable():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/converting-pygame-executable-cx_freeze.html", curLink = TOPIC_DICT["PyGame"][15][1], curTitle=TOPIC_DICT["PyGame"][15][0],  nextLink = TOPIC_DICT["PyGame"][16][1], nextTitle = TOPIC_DICT["PyGame"][16][0])




@app.route(TOPIC_DICT["PyGame"][16][1], methods=['GET', 'POST'])
def Adding_a_pause_function_to_our_game_and_Game_Over():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/pause-game-pygame.html", curLink = TOPIC_DICT["PyGame"][16][1], curTitle=TOPIC_DICT["PyGame"][16][0],  nextLink = TOPIC_DICT["PyGame"][17][1], nextTitle = TOPIC_DICT["PyGame"][17][0])




@app.route(TOPIC_DICT["PyGame"][17][1], methods=['GET', 'POST'])
def PyGame_Icon():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/changing-pygame-icon.html", curLink = TOPIC_DICT["PyGame"][17][1], curTitle=TOPIC_DICT["PyGame"][17][0],  nextLink = TOPIC_DICT["PyGame"][18][1], nextTitle = TOPIC_DICT["PyGame"][18][0])




@app.route(TOPIC_DICT["PyGame"][18][1], methods=['GET', 'POST'])
def Sounds_and_Music_with_PyGame():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyGame/adding-sounds-music-pygame.html", curLink = TOPIC_DICT["PyGame"][18][1], curTitle=TOPIC_DICT["PyGame"][18][0],  nextLink = TOPIC_DICT["PyGame"][19][1], nextTitle = TOPIC_DICT["PyGame"][19][0])




@app.route(TOPIC_DICT["PyOpenGL"][0][1], methods=['GET', 'POST'])
def OpenGL_with_PyOpenGL_introduction_and_creation_of_Rotating_Cube():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyOpenGL/opengl-rotating-cube-example-pyopengl-tutorial.html", curLink = TOPIC_DICT["PyOpenGL"][0][1], curTitle=TOPIC_DICT["PyOpenGL"][0][0],  nextLink = TOPIC_DICT["PyOpenGL"][1][1], nextTitle = TOPIC_DICT["PyOpenGL"][1][0])




@app.route(TOPIC_DICT["PyOpenGL"][1][1], methods=['GET', 'POST'])
def Coloring_Surfaces_as_well_as_understand_some_of_the_basic_OpenGL_code():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyOpenGL/coloring-pyopengl-surfaces-python-opengl.html", curLink = TOPIC_DICT["PyOpenGL"][1][1], curTitle=TOPIC_DICT["PyOpenGL"][1][0],  nextLink = TOPIC_DICT["PyOpenGL"][2][1], nextTitle = TOPIC_DICT["PyOpenGL"][2][0])




@app.route(TOPIC_DICT["PyOpenGL"][2][1], methods=['GET', 'POST'])
def Understanding_navigation_within_the_3D_environment_via_OpenGL():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyOpenGL/navigating-3d-environment.html", curLink = TOPIC_DICT["PyOpenGL"][2][1], curTitle=TOPIC_DICT["PyOpenGL"][2][0],  nextLink = TOPIC_DICT["PyOpenGL"][3][1], nextTitle = TOPIC_DICT["PyOpenGL"][3][0])




@app.route(TOPIC_DICT["PyOpenGL"][3][1], methods=['GET', 'POST'])
def Moving_the_player_automatically_towards_the_cube():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyOpenGL/moving-towards-pyopengl-cube.html", curLink = TOPIC_DICT["PyOpenGL"][3][1], curTitle=TOPIC_DICT["PyOpenGL"][3][0],  nextLink = TOPIC_DICT["PyOpenGL"][4][1], nextTitle = TOPIC_DICT["PyOpenGL"][4][0])




@app.route(TOPIC_DICT["PyOpenGL"][4][1], methods=['GET', 'POST'])
def Random_Cube_Position():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyOpenGL/random-cube-position-pyopengl-tutorial.html", curLink = TOPIC_DICT["PyOpenGL"][4][1], curTitle=TOPIC_DICT["PyOpenGL"][4][0],  nextLink = TOPIC_DICT["PyOpenGL"][5][1], nextTitle = TOPIC_DICT["PyOpenGL"][5][0])




@app.route(TOPIC_DICT["PyOpenGL"][5][1], methods=['GET', 'POST'])
def Adding_Many_Cubes_to_our_Game():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyOpenGL/multiple-opengl-cubes.html", curLink = TOPIC_DICT["PyOpenGL"][5][1], curTitle=TOPIC_DICT["PyOpenGL"][5][0],  nextLink = TOPIC_DICT["PyOpenGL"][6][1], nextTitle = TOPIC_DICT["PyOpenGL"][6][0])




@app.route(TOPIC_DICT["PyOpenGL"][6][1], methods=['GET', 'POST'])
def Adding_a_ground_in_OpenGL():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyOpenGL/adding-ground-pyopengl-tutorial.html", curLink = TOPIC_DICT["PyOpenGL"][6][1], curTitle=TOPIC_DICT["PyOpenGL"][6][0],  nextLink = TOPIC_DICT["PyOpenGL"][7][1], nextTitle = TOPIC_DICT["PyOpenGL"][7][0])




@app.route(TOPIC_DICT["PyOpenGL"][7][1], methods=['GET', 'POST'])
def Infinite_flying_cubes():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyOpenGL/infinite-3d-pyopengl-flying-cubes-tutorial.html", curLink = TOPIC_DICT["PyOpenGL"][7][1], curTitle=TOPIC_DICT["PyOpenGL"][7][0],  nextLink = TOPIC_DICT["PyOpenGL"][8][1], nextTitle = TOPIC_DICT["PyOpenGL"][8][0])




@app.route(TOPIC_DICT["PyOpenGL"][8][1], methods=['GET', 'POST'])
def Optimizing_the_processing_for_infinite_cubes():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyOpenGL/improving-infinite-3d-cubes-pyopengl-tutorial.html", curLink = TOPIC_DICT["PyOpenGL"][8][1], curTitle=TOPIC_DICT["PyOpenGL"][8][0],  nextLink = TOPIC_DICT["PyOpenGL"][9][1], nextTitle = TOPIC_DICT["PyOpenGL"][9][0])




@app.route(TOPIC_DICT["Kivy"][0][1], methods=['GET', 'POST'])
def Kivy_with_Python_tutorial_for_Mobile_Application_Development_Part_1():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/kivy-application-development-tutorial.html", curLink = TOPIC_DICT["Kivy"][0][1], curTitle=TOPIC_DICT["Kivy"][0][0],  nextLink = TOPIC_DICT["Kivy"][1][1], nextTitle = TOPIC_DICT["Kivy"][1][0])




@app.route(TOPIC_DICT["Kivy"][1][1], methods=['GET', 'POST'])
def Kivy_Widgets_and_Labels():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/kivy-widgets-labels.html", curLink = TOPIC_DICT["Kivy"][1][1], curTitle=TOPIC_DICT["Kivy"][1][0],  nextLink = TOPIC_DICT["Kivy"][2][1], nextTitle = TOPIC_DICT["Kivy"][2][0])




@app.route(TOPIC_DICT["Kivy"][2][1], methods=['GET', 'POST'])
def The_Kivy_kv_Language():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/kivy-language-tutorial.html", curLink = TOPIC_DICT["Kivy"][2][1], curTitle=TOPIC_DICT["Kivy"][2][0],  nextLink = TOPIC_DICT["Kivy"][3][1], nextTitle = TOPIC_DICT["Kivy"][3][0])




@app.route(TOPIC_DICT["Kivy"][3][1], methods=['GET', 'POST'])
def Kivy_kv_Language_contd():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/more-kivy-language.html", curLink = TOPIC_DICT["Kivy"][3][1], curTitle=TOPIC_DICT["Kivy"][3][0],  nextLink = TOPIC_DICT["Kivy"][4][1], nextTitle = TOPIC_DICT["Kivy"][4][0])




@app.route(TOPIC_DICT["Kivy"][4][1], methods=['GET', 'POST'])
def Dynamic_Resizable_Placement():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/dynamic-kivy-content-placement.html", curLink = TOPIC_DICT["Kivy"][4][1], curTitle=TOPIC_DICT["Kivy"][4][0],  nextLink = TOPIC_DICT["Kivy"][5][1], nextTitle = TOPIC_DICT["Kivy"][5][0])




@app.route(TOPIC_DICT["Kivy"][5][1], methods=['GET', 'POST'])
def Layouts_Float_Layout():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/kivy-float-layout.html", curLink = TOPIC_DICT["Kivy"][5][1], curTitle=TOPIC_DICT["Kivy"][5][0],  nextLink = TOPIC_DICT["Kivy"][6][1], nextTitle = TOPIC_DICT["Kivy"][6][0])




@app.route(TOPIC_DICT["Kivy"][6][1], methods=['GET', 'POST'])
def Getting_Mouse_Press_Touch_Input():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/getting-mouse-press-touch-input-kivy.html", curLink = TOPIC_DICT["Kivy"][6][1], curTitle=TOPIC_DICT["Kivy"][6][0],  nextLink = TOPIC_DICT["Kivy"][7][1], nextTitle = TOPIC_DICT["Kivy"][7][0])




@app.route(TOPIC_DICT["Kivy"][7][1], methods=['GET', 'POST'])
def Simple_Drawing_Application():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/kivy-drawing-application-tutorial.html", curLink = TOPIC_DICT["Kivy"][7][1], curTitle=TOPIC_DICT["Kivy"][7][0],  nextLink = TOPIC_DICT["Kivy"][8][1], nextTitle = TOPIC_DICT["Kivy"][8][0])




@app.route(TOPIC_DICT["Kivy"][8][1], methods=['GET', 'POST'])
def Builder_for_loading_kv_Files():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/kivy-loader-for-style.html", curLink = TOPIC_DICT["Kivy"][8][1], curTitle=TOPIC_DICT["Kivy"][8][0],  nextLink = TOPIC_DICT["Kivy"][9][1], nextTitle = TOPIC_DICT["Kivy"][9][0])




@app.route(TOPIC_DICT["Kivy"][9][1], methods=['GET', 'POST'])
def Screen_Manager_for_Multiple_Screens():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/kivy-screen-manager-tutorial.html", curLink = TOPIC_DICT["Kivy"][9][1], curTitle=TOPIC_DICT["Kivy"][9][0],  nextLink = TOPIC_DICT["Kivy"][10][1], nextTitle = TOPIC_DICT["Kivy"][10][0])




@app.route(TOPIC_DICT["Kivy"][10][1], methods=['GET', 'POST'])
def Drawing_Application_with_Screen_Manager():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/drawing-application-with-screen-manager.html", curLink = TOPIC_DICT["Kivy"][10][1], curTitle=TOPIC_DICT["Kivy"][10][0],  nextLink = TOPIC_DICT["Kivy"][11][1], nextTitle = TOPIC_DICT["Kivy"][11][0])




@app.route(TOPIC_DICT["Kivy"][11][1], methods=['GET', 'POST'])
def Adding_better_Navigation():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Kivy/kivy-application-navigation.html", curLink = TOPIC_DICT["Kivy"][11][1], curTitle=TOPIC_DICT["Kivy"][11][0],  nextLink = TOPIC_DICT["Kivy"][12][1], nextTitle = TOPIC_DICT["Kivy"][12][0])




@app.route(TOPIC_DICT["PyQt"][0][1], methods=['GET', 'POST'])
def PyQt_Tutorials_coming_soon():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/PyQt/pyqt-python-programming-tutorials.html", curLink = TOPIC_DICT["PyQt"][0][1], curTitle=TOPIC_DICT["PyQt"][0][0],  nextLink = TOPIC_DICT["PyQt"][1][1], nextTitle = TOPIC_DICT["PyQt"][1][0])




@app.route(TOPIC_DICT["Finance"][0][1], methods=['GET', 'POST'])
def Section_under_construction():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Finance/under-construction.html", curLink = TOPIC_DICT["Finance"][0][1], curTitle=TOPIC_DICT["Finance"][0][0],  nextLink = TOPIC_DICT["Finance"][1][1], nextTitle = TOPIC_DICT["Finance"][1][0])




@app.route(TOPIC_DICT["Flask"][0][1], methods=['GET', 'POST'])
def Intro_and_environment_creation():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Flask/flask-web-development-introduction.html", curLink = TOPIC_DICT["Flask"][0][1], curTitle=TOPIC_DICT["Flask"][0][0],  nextLink = TOPIC_DICT["Flask"][1][1], nextTitle = TOPIC_DICT["Flask"][1][0])




@app.route(TOPIC_DICT["Flask"][1][1], methods=['GET', 'POST'])
def Basics_initpy_and_your_first_Flask_App():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Flask/creating-first-flask-web-app.html", curLink = TOPIC_DICT["Flask"][1][1], curTitle=TOPIC_DICT["Flask"][1][0],  nextLink = TOPIC_DICT["Flask"][2][1], nextTitle = TOPIC_DICT["Flask"][2][0])




@app.route(TOPIC_DICT["Flask"][2][1], methods=['GET', 'POST'])
def Incorporating_Variables_and_some_Logic():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Flask/templates-flask-variables-html.html", curLink = TOPIC_DICT["Flask"][2][1], curTitle=TOPIC_DICT["Flask"][2][0],  nextLink = TOPIC_DICT["Flask"][3][1], nextTitle = TOPIC_DICT["Flask"][3][0])




@app.route(TOPIC_DICT["Flask"][3][1], methods=['GET', 'POST'])
def Using_Bootstrap_to_make_things_pretty():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Flask/flask-bootstrap.html", curLink = TOPIC_DICT["Flask"][3][1], curTitle=TOPIC_DICT["Flask"][3][0],  nextLink = TOPIC_DICT["Flask"][4][1], nextTitle = TOPIC_DICT["Flask"][4][0])




@app.route(TOPIC_DICT["Flask"][4][1], methods=['GET', 'POST'])
def Using_javascript_plugins_with_a_Highcharts_example():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Flask/adding-js-plugins-flask-highcharts-example.html", curLink = TOPIC_DICT["Flask"][4][1], curTitle=TOPIC_DICT["Flask"][4][0],  nextLink = TOPIC_DICT["Flask"][5][1], nextTitle = TOPIC_DICT["Flask"][5][0])




@app.route(TOPIC_DICT["Flask"][5][1], methods=['GET', 'POST'])
def Incorporating_extends_for_templates():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Flask/flask-template-extends.html", curLink = TOPIC_DICT["Flask"][5][1], curTitle=TOPIC_DICT["Flask"][5][0],  nextLink = TOPIC_DICT["Flask"][6][1], nextTitle = TOPIC_DICT["Flask"][6][0])




@app.route(TOPIC_DICT["Django"][0][1], methods=['GET', 'POST'])
def Django_Development_Videos():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Django/python-web-development-django.html", curLink = TOPIC_DICT["Django"][0][1], curTitle=TOPIC_DICT["Django"][0][0],  nextLink = TOPIC_DICT["Django"][1][1], nextTitle = TOPIC_DICT["Django"][1][0])




@app.route(TOPIC_DICT["MySQL"][0][1], methods=['GET', 'POST'])
def Intro_to_MySQL():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/MySQL/mysql-intro.html", curLink = TOPIC_DICT["MySQL"][0][1], curTitle=TOPIC_DICT["MySQL"][0][0],  nextLink = TOPIC_DICT["MySQL"][1][1], nextTitle = TOPIC_DICT["MySQL"][1][0])




@app.route(TOPIC_DICT["MySQL"][1][1], methods=['GET', 'POST'])
def Creating_Tables_and_Inserting_Data_with_MySQL():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/MySQL/create-mysql-tables-insert.html", curLink = TOPIC_DICT["MySQL"][1][1], curTitle=TOPIC_DICT["MySQL"][1][0],  nextLink = TOPIC_DICT["MySQL"][2][1], nextTitle = TOPIC_DICT["MySQL"][2][0])




@app.route(TOPIC_DICT["MySQL"][2][1], methods=['GET', 'POST'])
def Update_Select_and_Delete_with_MySQL():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/MySQL/mysql-update-select-delete.html", curLink = TOPIC_DICT["MySQL"][2][1], curTitle=TOPIC_DICT["MySQL"][2][0],  nextLink = TOPIC_DICT["MySQL"][3][1], nextTitle = TOPIC_DICT["MySQL"][3][0])




@app.route(TOPIC_DICT["MySQL"][3][1], methods=['GET', 'POST'])
def Inserting_Variable_Data_with_MySQL():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/MySQL/mysql-insert-variable.html", curLink = TOPIC_DICT["MySQL"][3][1], curTitle=TOPIC_DICT["MySQL"][3][0],  nextLink = TOPIC_DICT["MySQL"][4][1], nextTitle = TOPIC_DICT["MySQL"][4][0])




@app.route(TOPIC_DICT["MySQL"][4][1], methods=['GET', 'POST'])
def Streaming_Tweets_from_Twitter_to_Database():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/MySQL/mysql-live-database-example-streaming-data.html", curLink = TOPIC_DICT["MySQL"][4][1], curTitle=TOPIC_DICT["MySQL"][4][0],  nextLink = TOPIC_DICT["MySQL"][5][1], nextTitle = TOPIC_DICT["MySQL"][5][0])




@app.route(TOPIC_DICT["SQLite"][0][1], methods=['GET', 'POST'])
def Inserting_into_a_Database_with_SQLite():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/SQLite/sql-database-python-part-1-inserting-database.html", curLink = TOPIC_DICT["SQLite"][0][1], curTitle=TOPIC_DICT["SQLite"][0][0],  nextLink = TOPIC_DICT["SQLite"][1][1], nextTitle = TOPIC_DICT["SQLite"][1][0])




@app.route(TOPIC_DICT["SQLite"][1][1], methods=['GET', 'POST'])
def Dynamically_Inserting_into_a_Database_with_SQLite():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/SQLite/sqlite-part-2-dynamically-inserting-database-timestamps.html", curLink = TOPIC_DICT["SQLite"][1][1], curTitle=TOPIC_DICT["SQLite"][1][0],  nextLink = TOPIC_DICT["SQLite"][2][1], nextTitle = TOPIC_DICT["SQLite"][2][0])




@app.route(TOPIC_DICT["SQLite"][2][1], methods=['GET', 'POST'])
def Read_from_Database_with_SQLite():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/SQLite/sqlite-part-3-reading-database-python.html", curLink = TOPIC_DICT["SQLite"][2][1], curTitle=TOPIC_DICT["SQLite"][2][0],  nextLink = TOPIC_DICT["SQLite"][3][1], nextTitle = TOPIC_DICT["SQLite"][3][0])




@app.route(TOPIC_DICT["SQLite"][3][1], methods=['GET', 'POST'])
def Graphing_example_from_SQLite():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/SQLite/graphing-from-sqlite-database.html", curLink = TOPIC_DICT["SQLite"][3][1], curTitle=TOPIC_DICT["SQLite"][3][0],  nextLink = TOPIC_DICT["SQLite"][4][1], nextTitle = TOPIC_DICT["SQLite"][4][0])




@app.route(TOPIC_DICT["Data Manipulation"][0][1], methods=['GET', 'POST'])
def Intro_to_Pandas_and_Saving_to_a_CSV_and_reading_from_a_CSV():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Manipulation/pandas-saving-reading-csv-file.html", curLink = TOPIC_DICT["Data Manipulation"][0][1], curTitle=TOPIC_DICT["Data Manipulation"][0][0],  nextLink = TOPIC_DICT["Data Manipulation"][1][1], nextTitle = TOPIC_DICT["Data Manipulation"][1][0])




@app.route(TOPIC_DICT["Data Manipulation"][1][1], methods=['GET', 'POST'])
def Pandas_Column_manipulation():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Manipulation/pandas-column-manipulation-spreadsheet-data.html", curLink = TOPIC_DICT["Data Manipulation"][1][1], curTitle=TOPIC_DICT["Data Manipulation"][1][0],  nextLink = TOPIC_DICT["Data Manipulation"][2][1], nextTitle = TOPIC_DICT["Data Manipulation"][2][0])




@app.route(TOPIC_DICT["Data Manipulation"][2][1], methods=['GET', 'POST'])
def Pandas_Column_Operations_basic_math_operations_and_moving_averages():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Manipulation/pandas-column-operations-calculations.html", curLink = TOPIC_DICT["Data Manipulation"][2][1], curTitle=TOPIC_DICT["Data Manipulation"][2][0],  nextLink = TOPIC_DICT["Data Manipulation"][3][1], nextTitle = TOPIC_DICT["Data Manipulation"][3][0])




@app.route(TOPIC_DICT["Data Manipulation"][3][1], methods=['GET', 'POST'])
def Pandas_2D_Visualization_of_Pandas_data_with_Matplotlib_including_plotting_dates():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Manipulation/2D-Visualization-of-Pandas-data-with-Matplotlib-including-plotting-dates.html", curLink = TOPIC_DICT["Data Manipulation"][3][1], curTitle=TOPIC_DICT["Data Manipulation"][3][0],  nextLink = TOPIC_DICT["Data Manipulation"][4][1], nextTitle = TOPIC_DICT["Data Manipulation"][4][0])




@app.route(TOPIC_DICT["Data Manipulation"][4][1], methods=['GET', 'POST'])
def Pandas_3D_Visualization_of_Pandas_data_with_Matplotlib():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Manipulation/3d-graphing-pandas-matplotlib.html", curLink = TOPIC_DICT["Data Manipulation"][4][1], curTitle=TOPIC_DICT["Data Manipulation"][4][0],  nextLink = TOPIC_DICT["Data Manipulation"][5][1], nextTitle = TOPIC_DICT["Data Manipulation"][5][0])




@app.route(TOPIC_DICT["Data Manipulation"][5][1], methods=['GET', 'POST'])
def Pandas_Standard_Deviation():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Manipulation/pandas-standard-deviation.html", curLink = TOPIC_DICT["Data Manipulation"][5][1], curTitle=TOPIC_DICT["Data Manipulation"][5][0],  nextLink = TOPIC_DICT["Data Manipulation"][6][1], nextTitle = TOPIC_DICT["Data Manipulation"][6][0])




@app.route(TOPIC_DICT["Data Manipulation"][6][1], methods=['GET', 'POST'])
def Pandas_Correlation_matrix_and_Statistics_Information_on_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Manipulation/pandas-statistics-correlation-tables-how-to.html", curLink = TOPIC_DICT["Data Manipulation"][6][1], curTitle=TOPIC_DICT["Data Manipulation"][6][0],  nextLink = TOPIC_DICT["Data Manipulation"][7][1], nextTitle = TOPIC_DICT["Data Manipulation"][7][0])




@app.route(TOPIC_DICT["Data Manipulation"][7][1], methods=['GET', 'POST'])
def Pandas_Function_mapping_for_advanced_Pandas_users():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Manipulation/python-function-mapping-pandas.html", curLink = TOPIC_DICT["Data Manipulation"][7][1], curTitle=TOPIC_DICT["Data Manipulation"][7][0],  nextLink = TOPIC_DICT["Data Manipulation"][8][1], nextTitle = TOPIC_DICT["Data Manipulation"][8][0])




@app.route(TOPIC_DICT["Data Visualization"][0][1], methods=['GET', 'POST'])
def Matplotlib_Visualization_Crash_Course():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/matplotlib-python-3-basics-tutorial.html", curLink = TOPIC_DICT["Data Visualization"][0][1], curTitle=TOPIC_DICT["Data Visualization"][0][0],  nextLink = TOPIC_DICT["Data Visualization"][1][1], nextTitle = TOPIC_DICT["Data Visualization"][1][0])




@app.route(TOPIC_DICT["Data Visualization"][1][1], methods=['GET', 'POST'])
def _3D_graphs_in_Matplotlib():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/3d-graphing-python-matplotlib.html", curLink = TOPIC_DICT["Data Visualization"][1][1], curTitle=TOPIC_DICT["Data Visualization"][1][0],  nextLink = TOPIC_DICT["Data Visualization"][2][1], nextTitle = TOPIC_DICT["Data Visualization"][2][0])




@app.route(TOPIC_DICT["Data Visualization"][2][1], methods=['GET', 'POST'])
def _3D_Scatter_Plot_with_Python_and_Matplotlib():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/matplotlib-3d-scatterplot-tutorial.html", curLink = TOPIC_DICT["Data Visualization"][2][1], curTitle=TOPIC_DICT["Data Visualization"][2][0],  nextLink = TOPIC_DICT["Data Visualization"][3][1], nextTitle = TOPIC_DICT["Data Visualization"][3][0])




@app.route(TOPIC_DICT["Data Visualization"][3][1], methods=['GET', 'POST'])
def More_3D_scatter_plotting_with_custom_colors():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/3d-scatter-plot-customizing.html", curLink = TOPIC_DICT["Data Visualization"][3][1], curTitle=TOPIC_DICT["Data Visualization"][3][0],  nextLink = TOPIC_DICT["Data Visualization"][4][1], nextTitle = TOPIC_DICT["Data Visualization"][4][0])




@app.route(TOPIC_DICT["Data Visualization"][4][1], methods=['GET', 'POST'])
def _3D_Barcharts():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/3d-bar-charts-python-matplotlib.html", curLink = TOPIC_DICT["Data Visualization"][4][1], curTitle=TOPIC_DICT["Data Visualization"][4][0],  nextLink = TOPIC_DICT["Data Visualization"][5][1], nextTitle = TOPIC_DICT["Data Visualization"][5][0])




@app.route(TOPIC_DICT["Data Visualization"][5][1], methods=['GET', 'POST'])
def _3D_Plane_wireframe_Graph():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/wireframe-graph-python.html", curLink = TOPIC_DICT["Data Visualization"][5][1], curTitle=TOPIC_DICT["Data Visualization"][5][0],  nextLink = TOPIC_DICT["Data Visualization"][6][1], nextTitle = TOPIC_DICT["Data Visualization"][6][0])




@app.route(TOPIC_DICT["Data Visualization"][6][1], methods=['GET', 'POST'])
def Live_Updating_Graphs_with_Matplotlib_Tutorial():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/python-matplotlib-live-updating-graphs.html", curLink = TOPIC_DICT["Data Visualization"][6][1], curTitle=TOPIC_DICT["Data Visualization"][6][0],  nextLink = TOPIC_DICT["Data Visualization"][7][1], nextTitle = TOPIC_DICT["Data Visualization"][7][0])




@app.route(TOPIC_DICT["Data Visualization"][7][1], methods=['GET', 'POST'])
def Modify_Data_Granularity_for_Graphing_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/modifying-data-granularity-matplotlib.html", curLink = TOPIC_DICT["Data Visualization"][7][1], curTitle=TOPIC_DICT["Data Visualization"][7][0],  nextLink = TOPIC_DICT["Data Visualization"][8][1], nextTitle = TOPIC_DICT["Data Visualization"][8][0])




@app.route(TOPIC_DICT["Data Visualization"][8][1], methods=['GET', 'POST'])
def Geographical_Plotting_with_Basemap_and_Python_p_1():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/geographical-plotting-basemap-tutorial.html", curLink = TOPIC_DICT["Data Visualization"][8][1], curTitle=TOPIC_DICT["Data Visualization"][8][0],  nextLink = TOPIC_DICT["Data Visualization"][9][1], nextTitle = TOPIC_DICT["Data Visualization"][9][0])




@app.route(TOPIC_DICT["Data Visualization"][9][1], methods=['GET', 'POST'])
def Geographical_Plotting_with_Basemap_and_Python_p_2():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/map-plotting-basemap-matplotlib-part-2.html", curLink = TOPIC_DICT["Data Visualization"][9][1], curTitle=TOPIC_DICT["Data Visualization"][9][0],  nextLink = TOPIC_DICT["Data Visualization"][10][1], nextTitle = TOPIC_DICT["Data Visualization"][10][0])




@app.route(TOPIC_DICT["Data Visualization"][10][1], methods=['GET', 'POST'])
def Geographical_Plotting_with_Basemap_and_Python_p_3():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/basemap-possibilities.html", curLink = TOPIC_DICT["Data Visualization"][10][1], curTitle=TOPIC_DICT["Data Visualization"][10][0],  nextLink = TOPIC_DICT["Data Visualization"][11][1], nextTitle = TOPIC_DICT["Data Visualization"][11][0])




@app.route(TOPIC_DICT["Data Visualization"][11][1], methods=['GET', 'POST'])
def Geographical_Plotting_with_Basemap_and_Python_p_4():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/plotting-maps-python-basemap.html", curLink = TOPIC_DICT["Data Visualization"][11][1], curTitle=TOPIC_DICT["Data Visualization"][11][0],  nextLink = TOPIC_DICT["Data Visualization"][12][1], nextTitle = TOPIC_DICT["Data Visualization"][12][0])




@app.route(TOPIC_DICT["Data Visualization"][12][1], methods=['GET', 'POST'])
def Geographical_Plotting_with_Basemap_and_Python_p_5():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/basemap-python-plotting-tutorial-part-5.html", curLink = TOPIC_DICT["Data Visualization"][12][1], curTitle=TOPIC_DICT["Data Visualization"][12][0],  nextLink = TOPIC_DICT["Data Visualization"][13][1], nextTitle = TOPIC_DICT["Data Visualization"][13][0])




@app.route(TOPIC_DICT["Data Visualization"][13][1], methods=['GET', 'POST'])
def Advanced_Matplotlib_Series_videos_and_ending_source_only():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Data Visualization/advanced-matplotlib-graphing-charting-tutorial.html", curLink = TOPIC_DICT["Data Visualization"][13][1], curTitle=TOPIC_DICT["Data Visualization"][13][0],  nextLink = TOPIC_DICT["Data Visualization"][14][1], nextTitle = TOPIC_DICT["Data Visualization"][14][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][0][1], methods=['GET', 'POST'])
def Simple_RSS_feed_scraping():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/scraping-parsing-rss-feed.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][0][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][0][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][1][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][1][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][1][1], methods=['GET', 'POST'])
def Simple_website_scraping():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/scraping-text-websites.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][1][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][1][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][2][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][2][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][2][1], methods=['GET', 'POST'])
def More_ParsingScraping():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/website-scraping-basics.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][2][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][2][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][3][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][3][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][3][1], methods=['GET', 'POST'])
def Installing_the_Natural_Language_Toolkit_NLTK():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/installing-nltk-nlp-python.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][3][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][3][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][4][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][4][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][4][1], methods=['GET', 'POST'])
def NLTK_Part_of_Speech_Tagging_Tutorial():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/natural-language-toolkit-nltk-part-speech-tagging.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][4][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][4][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][5][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][5][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][5][1], methods=['GET', 'POST'])
def Named_Entity_Recognition_NLTK_tutorial():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/named-entity-recognition-nltk-python.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][5][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][5][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][6][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][6][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][6][1], methods=['GET', 'POST'])
def Building_a_Knowledge_base():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/building-nlp-knowledge-base.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][6][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][6][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][7][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][7][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][7][1], methods=['GET', 'POST'])
def More_Named_Entity_Recognition_with_NLTK():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/more-named-entity-recognition.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][7][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][7][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][8][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][8][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][8][1], methods=['GET', 'POST'])
def Pulling_related_Sentiment_about_Named_Entities():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/finding-related-sentiment.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][8][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][8][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][9][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][9][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][9][1], methods=['GET', 'POST'])
def Populating_a_knowledge_base():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/populating-nlp-database.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][9][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][9][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][10][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][10][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][10][1], methods=['GET', 'POST'])
def What_next():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/what-next-nlp-tutorial.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][10][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][10][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][11][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][11][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][11][1], methods=['GET', 'POST'])
def Accuracy_Testing():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/accuracy-testing-basic-nlp.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][11][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][11][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][12][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][12][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][12][1], methods=['GET', 'POST'])
def Building_back_testing():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/back-testing-nlp-nltk.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][12][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][12][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][13][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][13][0])




@app.route(TOPIC_DICT["Natural Language Processing with NLTK"][13][1], methods=['GET', 'POST'])
def Machine_learning_and_Sentiment_Analysis():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Natural Language Processing with NLTK/learning-for-sentiment-analysis.html", curLink = TOPIC_DICT["Natural Language Processing with NLTK"][13][1], curTitle=TOPIC_DICT["Natural Language Processing with NLTK"][13][0],  nextLink = TOPIC_DICT["Natural Language Processing with NLTK"][14][1], nextTitle = TOPIC_DICT["Natural Language Processing with NLTK"][14][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][0][1], methods=['GET', 'POST'])
def Intro_to_Machine_Learning_with_Scikit_Learn_and_Python():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/machine-learning-python-sklearn-intro.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][0][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][0][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][1][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][1][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][1][1], methods=['GET', 'POST'])
def Simple_Support_Vector_Machine_SVM_example_with_character_recognition():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/support-vector-machine-svm-example-tutorial-scikit-learn-python.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][1][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][1][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][2][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][2][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][2][1], methods=['GET', 'POST'])
def Our_Method_and_where_we_will_be_getting_our_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/data-acquisition-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][2][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][2][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][3][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][3][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][3][1], methods=['GET', 'POST'])
def Parsing_data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/getting-data-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][3][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][3][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][4][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][4][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][4][1], methods=['GET', 'POST'])
def More_Parsing():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/parsing-data-website-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][4][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][4][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][5][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][5][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][5][1], methods=['GET', 'POST'])
def Structuring_data_with_Pandas():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/using-pandas-structure-process-data.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][5][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][5][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][6][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][6][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][6][1], methods=['GET', 'POST'])
def Getting_more_data_and_meshing_data_sets():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/getting-data-sp-500-index-value-comparison.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][6][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][6][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][7][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][7][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][7][1], methods=['GET', 'POST'])
def Labeling_of_data_part_1():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/labeling-data-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][7][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][7][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][8][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][8][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][8][1], methods=['GET', 'POST'])
def Labeling_data_part_2():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/labeling-data-machine-learning-part-2.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][8][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][8][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][9][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][9][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][9][1], methods=['GET', 'POST'])
def Finally_finishing_up_the_labeling():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/label-data-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][9][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][9][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][10][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][10][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][10][1], methods=['GET', 'POST'])
def Linear_SVC_Machine_learning_SVM_example_with_Python():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/linear-svc-example-scikit-learn-svm-python.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][10][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][10][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][11][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][11][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][11][1], methods=['GET', 'POST'])
def Getting_more_features_from_our_data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/collecting-features-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][11][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][11][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][12][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][12][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][12][1], methods=['GET', 'POST'])
def Linear_SVC_machine_learning_and_testing_our_data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/linear-svc-machine-learning-testing-data.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][12][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][12][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][13][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][13][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][13][1], methods=['GET', 'POST'])
def Scaling_Normalizing_and_machine_learning_with_many_features():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/preprocessing-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][13][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][13][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][14][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][14][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][14][1], methods=['GET', 'POST'])
def Shuffling_our_data_to_solve_a_learning_issue():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/shuffling-data-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][14][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][14][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][15][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][15][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][15][1], methods=['GET', 'POST'])
def Using_Quandl_for_more_data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/using-quandl-data.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][15][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][15][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][16][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][16][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][16][1], methods=['GET', 'POST'])
def Improving_our_Analysis_with_a_more_accurate_measure_of_performance_in_relation_to_fundamentals():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/improving-analysis-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][16][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][16][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][17][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][17][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][17][1], methods=['GET', 'POST'])
def Learning_and_Testing_our_Machine_learning_algorithm():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/learning-and-testing-svm.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][17][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][17][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][18][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][18][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][18][1], methods=['GET', 'POST'])
def More_testing_this_time_including_NA_data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/machine-learning-testing-with-na.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][18][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][18][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][19][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][19][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][19][1], methods=['GET', 'POST'])
def Back_testing_the_strategy():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/back-testing-machine-learning-investing-strategy.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][19][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][19][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][20][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][20][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][20][1], methods=['GET', 'POST'])
def Pulling_current_data_from_Yahoo():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/current-yahoo-data-for-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][20][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][20][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][21][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][21][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][21][1], methods=['GET', 'POST'])
def Building_our_New_Data_set():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/building-yahoo-data-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][21][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][21][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][22][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][22][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][22][1], methods=['GET', 'POST'])
def Searching_for_investment_suggestions():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/investment-suggestions-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][22][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][22][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][23][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][23][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][23][1], methods=['GET', 'POST'])
def Raising_investment_requirement_standards():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/raising-investment-suggestion-requirements.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][23][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][23][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][24][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][24][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][24][1], methods=['GET', 'POST'])
def Testing_raised_standards():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/machine-learning-testing-new-algo.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][24][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][24][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][25][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][25][0])




@app.route(TOPIC_DICT["Support Vector Machines (SVM)"][25][1], methods=['GET', 'POST'])
def Streamlining_the_changing_of_standards():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Support Vector Machines (SVM)/streamlining-changing-machine-learning.html", curLink = TOPIC_DICT["Support Vector Machines (SVM)"][25][1], curTitle=TOPIC_DICT["Support Vector Machines (SVM)"][25][0],  nextLink = TOPIC_DICT["Support Vector Machines (SVM)"][26][1], nextTitle = TOPIC_DICT["Support Vector Machines (SVM)"][26][0])




@app.route(TOPIC_DICT["Clustering (unsupervised learning)"][0][1], methods=['GET', 'POST'])
def Unsupervised_Machine_Learning_Flat_Clustering():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Clustering (unsupervised learning)/flat-clustering-machine-learning-python-scikit-learn.html", curLink = TOPIC_DICT["Clustering (unsupervised learning)"][0][1], curTitle=TOPIC_DICT["Clustering (unsupervised learning)"][0][0],  nextLink = TOPIC_DICT["Clustering (unsupervised learning)"][1][1], nextTitle = TOPIC_DICT["Clustering (unsupervised learning)"][1][0])




@app.route(TOPIC_DICT["Clustering (unsupervised learning)"][1][1], methods=['GET', 'POST'])
def Unsupervised_Machine_Learning_Hierarchical_Clustering():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Clustering (unsupervised learning)/hierarchical-clustering-machine-learning-python-scikit-learn.html", curLink = TOPIC_DICT["Clustering (unsupervised learning)"][1][1], curTitle=TOPIC_DICT["Clustering (unsupervised learning)"][1][0],  nextLink = TOPIC_DICT["Clustering (unsupervised learning)"][2][1], nextTitle = TOPIC_DICT["Clustering (unsupervised learning)"][2][0])




@app.route(TOPIC_DICT["Image Recognition"][0][1], methods=['GET', 'POST'])
def Introduction_and_Dependencies():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Image Recognition/image-recognition-python.html", curLink = TOPIC_DICT["Image Recognition"][0][1], curTitle=TOPIC_DICT["Image Recognition"][0][0],  nextLink = TOPIC_DICT["Image Recognition"][1][1], nextTitle = TOPIC_DICT["Image Recognition"][1][0])




@app.route(TOPIC_DICT["Image Recognition"][1][1], methods=['GET', 'POST'])
def Understanding_Pixel_Arrays():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Image Recognition/python-pixel-arrays.html", curLink = TOPIC_DICT["Image Recognition"][1][1], curTitle=TOPIC_DICT["Image Recognition"][1][0],  nextLink = TOPIC_DICT["Image Recognition"][2][1], nextTitle = TOPIC_DICT["Image Recognition"][2][0])




@app.route(TOPIC_DICT["Image Recognition"][2][1], methods=['GET', 'POST'])
def More_Pixel_Arrays():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Image Recognition/more-pixel-arrays.html", curLink = TOPIC_DICT["Image Recognition"][2][1], curTitle=TOPIC_DICT["Image Recognition"][2][0],  nextLink = TOPIC_DICT["Image Recognition"][3][1], nextTitle = TOPIC_DICT["Image Recognition"][3][0])




@app.route(TOPIC_DICT["Image Recognition"][3][1], methods=['GET', 'POST'])
def Graphing_our_images_in_Matplotlib():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Image Recognition/graphing-images-matplotlib.html", curLink = TOPIC_DICT["Image Recognition"][3][1], curTitle=TOPIC_DICT["Image Recognition"][3][0],  nextLink = TOPIC_DICT["Image Recognition"][4][1], nextTitle = TOPIC_DICT["Image Recognition"][4][0])




@app.route(TOPIC_DICT["Image Recognition"][4][1], methods=['GET', 'POST'])
def Thresholding():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Image Recognition/image-thresholding-python.html", curLink = TOPIC_DICT["Image Recognition"][4][1], curTitle=TOPIC_DICT["Image Recognition"][4][0],  nextLink = TOPIC_DICT["Image Recognition"][5][1], nextTitle = TOPIC_DICT["Image Recognition"][5][0])




@app.route(TOPIC_DICT["Image Recognition"][5][1], methods=['GET', 'POST'])
def Thresholding_Function():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Image Recognition/thresholding-python-function.html", curLink = TOPIC_DICT["Image Recognition"][5][1], curTitle=TOPIC_DICT["Image Recognition"][5][0],  nextLink = TOPIC_DICT["Image Recognition"][6][1], nextTitle = TOPIC_DICT["Image Recognition"][6][0])




@app.route(TOPIC_DICT["Image Recognition"][6][1], methods=['GET', 'POST'])
def Thresholding_Logic():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Image Recognition/automated-image-thresholding-python.html", curLink = TOPIC_DICT["Image Recognition"][6][1], curTitle=TOPIC_DICT["Image Recognition"][6][0],  nextLink = TOPIC_DICT["Image Recognition"][7][1], nextTitle = TOPIC_DICT["Image Recognition"][7][0])




@app.route(TOPIC_DICT["Image Recognition"][7][1], methods=['GET', 'POST'])
def Saving_our_Data_For_Training_and_Testing():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Image Recognition/saving-image-data.html", curLink = TOPIC_DICT["Image Recognition"][7][1], curTitle=TOPIC_DICT["Image Recognition"][7][0],  nextLink = TOPIC_DICT["Image Recognition"][8][1], nextTitle = TOPIC_DICT["Image Recognition"][8][0])




@app.route(TOPIC_DICT["Image Recognition"][8][1], methods=['GET', 'POST'])
def Basic_Testing():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Image Recognition/basic-image-recognition-testing.html", curLink = TOPIC_DICT["Image Recognition"][8][1], curTitle=TOPIC_DICT["Image Recognition"][8][0],  nextLink = TOPIC_DICT["Image Recognition"][9][1], nextTitle = TOPIC_DICT["Image Recognition"][9][0])




@app.route(TOPIC_DICT["Image Recognition"][9][1], methods=['GET', 'POST'])
def Testing_visualization_and_moving_forward():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Image Recognition/testing-visualization-and-conclusion.html", curLink = TOPIC_DICT["Image Recognition"][9][1], curTitle=TOPIC_DICT["Image Recognition"][9][0],  nextLink = TOPIC_DICT["Image Recognition"][10][1], nextTitle = TOPIC_DICT["Image Recognition"][10][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][0][1], methods=['GET', 'POST'])
def Introduction():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/machine-learning-pattern-recognition-algorithmic-forex-stock-trading.html", curLink = TOPIC_DICT["Forex Algo HFT"][0][1], curTitle=TOPIC_DICT["Forex Algo HFT"][0][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][1][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][1][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][1][1], methods=['GET', 'POST'])
def Quick_Look_at_our_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/pattern-recognition-dataset.html", curLink = TOPIC_DICT["Forex Algo HFT"][1][1], curTitle=TOPIC_DICT["Forex Algo HFT"][1][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][2][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][2][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][2][1], methods=['GET', 'POST'])
def Basics():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/forex-algo-pattern-rec-basics.html", curLink = TOPIC_DICT["Forex Algo HFT"][2][1], curTitle=TOPIC_DICT["Forex Algo HFT"][2][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][3][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][3][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][3][1], methods=['GET', 'POST'])
def Percent_Change():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/percent-change-python.html", curLink = TOPIC_DICT["Forex Algo HFT"][3][1], curTitle=TOPIC_DICT["Forex Algo HFT"][3][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][4][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][4][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][4][1], methods=['GET', 'POST'])
def Finding_Patterns():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/finding-forex-algo-patterns.html", curLink = TOPIC_DICT["Forex Algo HFT"][4][1], curTitle=TOPIC_DICT["Forex Algo HFT"][4][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][5][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][5][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][5][1], methods=['GET', 'POST'])
def Storing_Patterns():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/storing-found-patterns.html", curLink = TOPIC_DICT["Forex Algo HFT"][5][1], curTitle=TOPIC_DICT["Forex Algo HFT"][5][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][6][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][6][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][6][1], methods=['GET', 'POST'])
def Current_Pattern():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/recognizing-current-pattern.html", curLink = TOPIC_DICT["Forex Algo HFT"][6][1], curTitle=TOPIC_DICT["Forex Algo HFT"][6][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][7][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][7][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][7][1], methods=['GET', 'POST'])
def Predicting_outcomes():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/predicting-outcomes-of-patterns.html", curLink = TOPIC_DICT["Forex Algo HFT"][7][1], curTitle=TOPIC_DICT["Forex Algo HFT"][7][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][8][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][8][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][8][1], methods=['GET', 'POST'])
def More_predicting():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/more-predicting-outcomes.html", curLink = TOPIC_DICT["Forex Algo HFT"][8][1], curTitle=TOPIC_DICT["Forex Algo HFT"][8][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][9][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][9][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][9][1], methods=['GET', 'POST'])
def Increasing_pattern_complexity():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/increasing-pattern-complexity.html", curLink = TOPIC_DICT["Forex Algo HFT"][9][1], curTitle=TOPIC_DICT["Forex Algo HFT"][9][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][10][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][10][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][10][1], methods=['GET', 'POST'])
def More_on_Patterns():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/more-on-patterns-hft-forex.html", curLink = TOPIC_DICT["Forex Algo HFT"][10][1], curTitle=TOPIC_DICT["Forex Algo HFT"][10][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][11][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][11][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][11][1], methods=['GET', 'POST'])
def Displaying_all_patterns():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/displaying-our-forex-patterns.html", curLink = TOPIC_DICT["Forex Algo HFT"][11][1], curTitle=TOPIC_DICT["Forex Algo HFT"][11][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][12][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][12][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][12][1], methods=['GET', 'POST'])
def Variables_in_patterns():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/variables-in-forex-patterns.html", curLink = TOPIC_DICT["Forex Algo HFT"][12][1], curTitle=TOPIC_DICT["Forex Algo HFT"][12][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][13][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][13][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][13][1], methods=['GET', 'POST'])
def Past_outcomes_as_possible_predictions():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/past-pattern-outcomes-predictions.html", curLink = TOPIC_DICT["Forex Algo HFT"][13][1], curTitle=TOPIC_DICT["Forex Algo HFT"][13][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][14][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][14][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][14][1], methods=['GET', 'POST'])
def Predicting_from_patterns():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/predicting-from-patterns.html", curLink = TOPIC_DICT["Forex Algo HFT"][14][1], curTitle=TOPIC_DICT["Forex Algo HFT"][14][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][15][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][15][0])




@app.route(TOPIC_DICT["Forex Algo HFT"][15][1], methods=['GET', 'POST'])
def Average_outcomes_as_predictions():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Forex Algo HFT/average-outcomes-as-predictions-forex-hft.html", curLink = TOPIC_DICT["Forex Algo HFT"][15][1], curTitle=TOPIC_DICT["Forex Algo HFT"][15][0],  nextLink = TOPIC_DICT["Forex Algo HFT"][16][1], nextTitle = TOPIC_DICT["Forex Algo HFT"][16][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][0][1], methods=['GET', 'POST'])
def Robotics_with_the_Raspberry_Pi():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/robot-remote-control-car-with-the-raspberry-pi.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][0][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][0][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][1][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][1][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][1][1], methods=['GET', 'POST'])
def Programming_GPIO_example():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/gpio-example-raspberry-pi.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][1][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][1][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][2][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][2][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][2][1], methods=['GET', 'POST'])
def Running_GPIO():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/running-gpio-python-raspberry-pi.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][2][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][2][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][3][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][3][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][3][1], methods=['GET', 'POST'])
def Building_Autonomous_RC_car_intro():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/gpio-raspberry-pi-car-intro.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][3][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][3][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][4][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][4][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][4][1], methods=['GET', 'POST'])
def Supplies_needed():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/raspberry-pi-car-supplies.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][4][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][4][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][5][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][5][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][5][1], methods=['GET', 'POST'])
def Motor_Control():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/gpio-motor-control-raspberry-pi.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][5][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][5][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][6][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][6][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][6][1], methods=['GET', 'POST'])
def Connecting_the_four_motors():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/connecting-motors-raspberry-pi.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][6][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][6][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][7][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][7][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][7][1], methods=['GET', 'POST'])
def Forward_and_Reverse():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/forward-reverse-motors-raspberry-pi.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][7][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][7][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][8][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][8][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][8][1], methods=['GET', 'POST'])
def Turning():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/turning-raspberry-pi-car.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][8][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][8][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][9][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][9][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][9][1], methods=['GET', 'POST'])
def Pivoting():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/pivoting-raspberry-pi-car.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][9][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][9][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][10][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][10][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][10][1], methods=['GET', 'POST'])
def User_Control():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/user-control-raspberry-pi-car.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][10][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][10][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][11][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][11][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][11][1], methods=['GET', 'POST'])
def Remotely_controlling_the_car():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/raspberry-pi-car-remote-control.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][11][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][11][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][12][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][12][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][12][1], methods=['GET', 'POST'])
def Adding_a_distance_sensor_HC_SR04():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/raspberry-pi-car-distance-sensor.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][12][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][12][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][13][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][13][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][13][1], methods=['GET', 'POST'])
def Programming_with_the_distance_sensor():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/raspberry-pi-hc-sr04-programming.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][13][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][13][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][14][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][14][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][14][1], methods=['GET', 'POST'])
def Autopilot_andor_auto_correct():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/autopilot-raspberry-pi-car.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][14][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][14][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][15][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][15][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][15][1], methods=['GET', 'POST'])
def Autonomous_Beginnings():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/autonomous-raspberry-pi-car.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][15][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][15][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][16][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][16][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][16][1], methods=['GET', 'POST'])
def Testing_Autonomous_Code():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/testing-autonomous-raspberry-pi-car.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][16][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][16][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][17][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][17][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][17][1], methods=['GET', 'POST'])
def Streaming_video_example_one():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/streaming-video-from-raspberry-pi-camera.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][17][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][17][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][18][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][18][0])




@app.route(TOPIC_DICT["Robotics with the Raspberry Pi"][18][1], methods=['GET', 'POST'])
def Less_latency_streaming_option():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Robotics with the Raspberry Pi/low-latency-video-streaming-raspberry-pi.html", curLink = TOPIC_DICT["Robotics with the Raspberry Pi"][18][1], curTitle=TOPIC_DICT["Robotics with the Raspberry Pi"][18][0],  nextLink = TOPIC_DICT["Robotics with the Raspberry Pi"][19][1], nextTitle = TOPIC_DICT["Robotics with the Raspberry Pi"][19][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][0][1], methods=['GET', 'POST'])
def Build_a_Supercomputer_with_Raspberry_Pis():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/build-supercomputer-raspberry-pi.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][0][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][0][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][1][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][1][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][1][1], methods=['GET', 'POST'])
def Intro():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/supercomputer-intro.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][1][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][1][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][2][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][2][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][2][1], methods=['GET', 'POST'])
def Supplies():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/supplies-for-supercomputer.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][2][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][2][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][3][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][3][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][3][1], methods=['GET', 'POST'])
def Installing_Operating_System():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/installing-supercomputer-operating-system.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][3][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][3][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][4][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][4][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][4][1], methods=['GET', 'POST'])
def Downloading_and_installing_MPI():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/download-and-install-mpi-for-supercomputer.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][4][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][4][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][5][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][5][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][5][1], methods=['GET', 'POST'])
def Testing_Supercomputer():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/testing-supercomputer.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][5][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][5][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][6][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][6][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][6][1], methods=['GET', 'POST'])
def MPI_with_MPI4py_Introduction():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/learning-use-mpi-python-mpi4py-module.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][6][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][6][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][7][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][7][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][7][1], methods=['GET', 'POST'])
def Installing_mpi4py_for_use_with_Python_and_MPI():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/installing-testing-mpi4py-mpi-python-tutorial.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][7][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][7][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][8][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][8][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][8][1], methods=['GET', 'POST'])
def First_basic_MPI_script_with_mpi4py():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/basic-mpi4py-script-getting-node-rank.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][8][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][8][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][9][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][9][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][9][1], methods=['GET', 'POST'])
def Using_conditional_Python_statements_alongside_MPI_commands_example():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/conditional-statements-alongside-mpi-mpi4py.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][9][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][9][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][10][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][10][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][10][1], methods=['GET', 'POST'])
def Getting_network_processor_size_with_the_size_command():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/mpi4py-size-command-mpi.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][10][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][10][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][11][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][11][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][11][1], methods=['GET', 'POST'])
def Sending_and_Receiving_data_using_send_and_recv_commands_with_MPI():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/sending-receiving-data-messages-mpi4py.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][11][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][11][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][12][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][12][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][12][1], methods=['GET', 'POST'])
def Dynamically_sending_messages_to_and_from_processors_with_MPI_and_mpi4py():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/sending-receiving-messages-nodes-dynamically.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][12][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][12][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][13][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][13][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][13][1], methods=['GET', 'POST'])
def Message_and_data_tagging_for_send_and_recv_MPI_commands_tutorial():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/tagging-messages-mpi-multiple-messages.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][13][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][13][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][14][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][14][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][14][1], methods=['GET', 'POST'])
def MPI_broadcasting_tutorial_with_Python_mpi4py_and_bcast():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/mpi-broadcast-tutorial-mpi4py.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][14][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][14][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][15][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][15][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][15][1], methods=['GET', 'POST'])
def Scatter_with_MPI_tutorial_with_mpi4py():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/scatter-gather-mpi-mpi4py-tutorial.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][15][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][15][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][16][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][16][0])




@app.route(TOPIC_DICT["Build a Supercomputer and program with MPI"][16][1], methods=['GET', 'POST'])
def Gather_command_with_MPI_mpi4py_and_Python():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Build a Supercomputer and program with MPI/mpi-gather-command-mpi4py-python.html", curLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][16][1], curTitle=TOPIC_DICT["Build a Supercomputer and program with MPI"][16][0],  nextLink = TOPIC_DICT["Build a Supercomputer and program with MPI"][17][1], nextTitle = TOPIC_DICT["Build a Supercomputer and program with MPI"][17][0])




@app.route(TOPIC_DICT["Tkinter"][0][1], methods=['GET', 'POST'])
def Programming_GUIs_and_windows_with_Tkinter_and_Python_Introduction_():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/tkinter-depth-tutorial-making-actual-program.html", curLink = TOPIC_DICT["Tkinter"][0][1], curTitle=TOPIC_DICT["Tkinter"][0][0],  nextLink = TOPIC_DICT["Tkinter"][1][1], nextTitle = TOPIC_DICT["Tkinter"][1][0])




@app.route(TOPIC_DICT["Tkinter"][1][1], methods=['GET', 'POST'])
def Object_Oriented_Programming_Crash_Course_with_Tkinter():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/object-oriented-programming-crash-course-tkinter.html", curLink = TOPIC_DICT["Tkinter"][1][1], curTitle=TOPIC_DICT["Tkinter"][1][0],  nextLink = TOPIC_DICT["Tkinter"][2][1], nextTitle = TOPIC_DICT["Tkinter"][2][0])




@app.route(TOPIC_DICT["Tkinter"][2][1], methods=['GET', 'POST'])
def Passing_functions_with_Parameters_in_Tkinter_using_Lambda():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/passing-functions-parameters-tkinter-using-lambda.html", curLink = TOPIC_DICT["Tkinter"][2][1], curTitle=TOPIC_DICT["Tkinter"][2][0],  nextLink = TOPIC_DICT["Tkinter"][3][1], nextTitle = TOPIC_DICT["Tkinter"][3][0])




@app.route(TOPIC_DICT["Tkinter"][3][1], methods=['GET', 'POST'])
def How_to_change_and_show_a_new_window_in_Tkinter():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/change-show-new-frame-tkinter.html", curLink = TOPIC_DICT["Tkinter"][3][1], curTitle=TOPIC_DICT["Tkinter"][3][0],  nextLink = TOPIC_DICT["Tkinter"][4][1], nextTitle = TOPIC_DICT["Tkinter"][4][0])




@app.route(TOPIC_DICT["Tkinter"][4][1], methods=['GET', 'POST'])
def Styling_your_GUI_a_bit_using_TTK():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/styling-gui-bit-using-ttk.html", curLink = TOPIC_DICT["Tkinter"][4][1], curTitle=TOPIC_DICT["Tkinter"][4][0],  nextLink = TOPIC_DICT["Tkinter"][5][1], nextTitle = TOPIC_DICT["Tkinter"][5][0])




@app.route(TOPIC_DICT["Tkinter"][5][1], methods=['GET', 'POST'])
def How_to_embed_a_Matplotlib_graph_to_your_Tkinter_GUI():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/how-to-embed-matplotlib-graph-tkinter-gui.html", curLink = TOPIC_DICT["Tkinter"][5][1], curTitle=TOPIC_DICT["Tkinter"][5][0],  nextLink = TOPIC_DICT["Tkinter"][6][1], nextTitle = TOPIC_DICT["Tkinter"][6][0])




@app.route(TOPIC_DICT["Tkinter"][6][1], methods=['GET', 'POST'])
def How_to_make_the_Matplotlib_graph_live_in_your_application():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/embedding-live-matplotlib-graph-tkinter-gui.html", curLink = TOPIC_DICT["Tkinter"][6][1], curTitle=TOPIC_DICT["Tkinter"][6][0],  nextLink = TOPIC_DICT["Tkinter"][7][1], nextTitle = TOPIC_DICT["Tkinter"][7][0])




@app.route(TOPIC_DICT["Tkinter"][7][1], methods=['GET', 'POST'])
def Organizing_our_GUI():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/organizing-gui.html", curLink = TOPIC_DICT["Tkinter"][7][1], curTitle=TOPIC_DICT["Tkinter"][7][0],  nextLink = TOPIC_DICT["Tkinter"][8][1], nextTitle = TOPIC_DICT["Tkinter"][8][0])




@app.route(TOPIC_DICT["Tkinter"][8][1], methods=['GET', 'POST'])
def Plotting_Live_Updating_Data_in_Matplotlib_and_our_Tkinter_GUI():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/plotting-live-bitcoin-price-data-tkinter-matplotlib.html", curLink = TOPIC_DICT["Tkinter"][8][1], curTitle=TOPIC_DICT["Tkinter"][8][0],  nextLink = TOPIC_DICT["Tkinter"][9][1], nextTitle = TOPIC_DICT["Tkinter"][9][0])




@app.route(TOPIC_DICT["Tkinter"][9][1], methods=['GET', 'POST'])
def Customizing_an_embedded_Matplotlib_Graph_in_Tkinter():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/customizing-tkinter-matplotlib-graph.html", curLink = TOPIC_DICT["Tkinter"][9][1], curTitle=TOPIC_DICT["Tkinter"][9][0],  nextLink = TOPIC_DICT["Tkinter"][10][1], nextTitle = TOPIC_DICT["Tkinter"][10][0])




@app.route(TOPIC_DICT["Tkinter"][10][1], methods=['GET', 'POST'])
def Creating_our_Main_Menu_in_Tkinter():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/creating-main-menu-tkinter.html", curLink = TOPIC_DICT["Tkinter"][10][1], curTitle=TOPIC_DICT["Tkinter"][10][0],  nextLink = TOPIC_DICT["Tkinter"][11][1], nextTitle = TOPIC_DICT["Tkinter"][11][0])




@app.route(TOPIC_DICT["Tkinter"][11][1], methods=['GET', 'POST'])
def Building_a_pop_up_message_window():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/tkinter-popup-message-window.html", curLink = TOPIC_DICT["Tkinter"][11][1], curTitle=TOPIC_DICT["Tkinter"][11][0],  nextLink = TOPIC_DICT["Tkinter"][12][1], nextTitle = TOPIC_DICT["Tkinter"][12][0])




@app.route(TOPIC_DICT["Tkinter"][12][1], methods=['GET', 'POST'])
def Exchange_Choice_Option():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/adding-tkinter-menu-options.html", curLink = TOPIC_DICT["Tkinter"][12][1], curTitle=TOPIC_DICT["Tkinter"][12][0],  nextLink = TOPIC_DICT["Tkinter"][13][1], nextTitle = TOPIC_DICT["Tkinter"][13][0])




@app.route(TOPIC_DICT["Tkinter"][13][1], methods=['GET', 'POST'])
def Time_frame_and_sample_size_option():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/time-frame-sample-size-options.html", curLink = TOPIC_DICT["Tkinter"][13][1], curTitle=TOPIC_DICT["Tkinter"][13][0],  nextLink = TOPIC_DICT["Tkinter"][14][1], nextTitle = TOPIC_DICT["Tkinter"][14][0])




@app.route(TOPIC_DICT["Tkinter"][14][1], methods=['GET', 'POST'])
def Adding_indicator_Menus_3_videos():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/adding-indicator-choice-menu.html", curLink = TOPIC_DICT["Tkinter"][14][1], curTitle=TOPIC_DICT["Tkinter"][14][0],  nextLink = TOPIC_DICT["Tkinter"][15][1], nextTitle = TOPIC_DICT["Tkinter"][15][0])




@app.route(TOPIC_DICT["Tkinter"][15][1], methods=['GET', 'POST'])
def Trading_option_startstop_and_help_menu_options():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/adding-trading-option.html", curLink = TOPIC_DICT["Tkinter"][15][1], curTitle=TOPIC_DICT["Tkinter"][15][0],  nextLink = TOPIC_DICT["Tkinter"][16][1], nextTitle = TOPIC_DICT["Tkinter"][16][0])




@app.route(TOPIC_DICT["Tkinter"][16][1], methods=['GET', 'POST'])
def Tutorial_on_adding_a_tutorial():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/tutorial-for-tkinter-tutorial.html", curLink = TOPIC_DICT["Tkinter"][16][1], curTitle=TOPIC_DICT["Tkinter"][16][0],  nextLink = TOPIC_DICT["Tkinter"][17][1], nextTitle = TOPIC_DICT["Tkinter"][17][0])




@app.route(TOPIC_DICT["Tkinter"][17][1], methods=['GET', 'POST'])
def Allowing_the_exchange_choice_option_to_affect_actual_shown_exchange():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/exchange-choice-handling.html", curLink = TOPIC_DICT["Tkinter"][17][1], curTitle=TOPIC_DICT["Tkinter"][17][0],  nextLink = TOPIC_DICT["Tkinter"][18][1], nextTitle = TOPIC_DICT["Tkinter"][18][0])




@app.route(TOPIC_DICT["Tkinter"][18][1], methods=['GET', 'POST'])
def Adding_exchange_choice_contd():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/adding-exchanges-2.html", curLink = TOPIC_DICT["Tkinter"][18][1], curTitle=TOPIC_DICT["Tkinter"][18][0],  nextLink = TOPIC_DICT["Tkinter"][19][1], nextTitle = TOPIC_DICT["Tkinter"][19][0])




@app.route(TOPIC_DICT["Tkinter"][19][1], methods=['GET', 'POST'])
def Adding_exchange_choices_part_3():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/adding-exchanges-3.html", curLink = TOPIC_DICT["Tkinter"][19][1], curTitle=TOPIC_DICT["Tkinter"][19][0],  nextLink = TOPIC_DICT["Tkinter"][20][1], nextTitle = TOPIC_DICT["Tkinter"][20][0])




@app.route(TOPIC_DICT["Tkinter"][20][1], methods=['GET', 'POST'])
def Indicator_Support():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/adding-indicator-support.html", curLink = TOPIC_DICT["Tkinter"][20][1], curTitle=TOPIC_DICT["Tkinter"][20][0],  nextLink = TOPIC_DICT["Tkinter"][21][1], nextTitle = TOPIC_DICT["Tkinter"][21][0])




@app.route(TOPIC_DICT["Tkinter"][21][1], methods=['GET', 'POST'])
def Pulling_data_from_the_Sea_of_BTC_API():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/pulling-data-from-seaofbtc.html", curLink = TOPIC_DICT["Tkinter"][21][1], curTitle=TOPIC_DICT["Tkinter"][21][0],  nextLink = TOPIC_DICT["Tkinter"][22][1], nextTitle = TOPIC_DICT["Tkinter"][22][0])




@app.route(TOPIC_DICT["Tkinter"][22][1], methods=['GET', 'POST'])
def Setting_up_sub_plots_within_our_Tkinter_GUI():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/subplots-within-tkinter-gui.html", curLink = TOPIC_DICT["Tkinter"][22][1], curTitle=TOPIC_DICT["Tkinter"][22][0],  nextLink = TOPIC_DICT["Tkinter"][23][1], nextTitle = TOPIC_DICT["Tkinter"][23][0])




@app.route(TOPIC_DICT["Tkinter"][23][1], methods=['GET', 'POST'])
def Graphing_an_OHLC_candlestick_graph_embedded_in_our_Tkinter_GUI():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/graphing-ohlc-candlestick-in-tkinter.html", curLink = TOPIC_DICT["Tkinter"][23][1], curTitle=TOPIC_DICT["Tkinter"][23][0],  nextLink = TOPIC_DICT["Tkinter"][24][1], nextTitle = TOPIC_DICT["Tkinter"][24][0])




@app.route(TOPIC_DICT["Tkinter"][24][1], methods=['GET', 'POST'])
def Acquiring_RSI_data_from_Sea_of_BTC_API():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/getting-rsi-data-for-tkinter-gui.html", curLink = TOPIC_DICT["Tkinter"][24][1], curTitle=TOPIC_DICT["Tkinter"][24][0],  nextLink = TOPIC_DICT["Tkinter"][25][1], nextTitle = TOPIC_DICT["Tkinter"][25][0])




@app.route(TOPIC_DICT["Tkinter"][25][1], methods=['GET', 'POST'])
def Acquiring_MACD_data_from_Sea_of_BTC_API():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/getting-macd-data-for-tkinter-gui.html", curLink = TOPIC_DICT["Tkinter"][25][1], curTitle=TOPIC_DICT["Tkinter"][25][0],  nextLink = TOPIC_DICT["Tkinter"][26][1], nextTitle = TOPIC_DICT["Tkinter"][26][0])




@app.route(TOPIC_DICT["Tkinter"][26][1], methods=['GET', 'POST'])
def Converting_Tkinter_application_to_exe_and_installer_with_cx_Freeze():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Tkinter/converting-tkinter-to-exe-with-cx-freeze.html", curLink = TOPIC_DICT["Tkinter"][26][1], curTitle=TOPIC_DICT["Tkinter"][26][0],  nextLink = TOPIC_DICT["Tkinter"][27][1], nextTitle = TOPIC_DICT["Tkinter"][27][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][0][1], methods=['GET', 'POST'])
def Python_and_Pandas_with_Sentiment_Analysis_Database():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/python-and-pandas-for-sentiment-analysis-and-finance.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][0][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][0][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][1][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][1][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][1][1], methods=['GET', 'POST'])
def Pandas_Basics():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/pandas-basics-sentiment.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][1][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][1][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][2][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][2][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][2][1], methods=['GET', 'POST'])
def Looking_at_our_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/sentiment-analysis-data.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][2][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][2][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][3][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][3][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][3][1], methods=['GET', 'POST'])
def Data_Manipulation():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/simple-data-manipulation.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][3][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][3][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][4][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][4][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][4][1], methods=['GET', 'POST'])
def Removing_Outlier_Plots():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/removing-outliers-sentiment.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][4][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][4][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][5][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][5][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][5][1], methods=['GET', 'POST'])
def Basics_for_a_Strategy():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/simple-strategy-idea.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][5][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][5][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][6][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][6][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][6][1], methods=['GET', 'POST'])
def Dynamic_Moving_Averages():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/dynamic-moving-averages.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][6][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][6][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][7][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][7][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][7][1], methods=['GET', 'POST'])
def Strategy_Function():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/strategy-function-tutorial.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][7][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][7][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][8][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][8][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][8][1], methods=['GET', 'POST'])
def Mapping_function_to_dataframe():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/mapping-function-pandas-sentiment.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][8][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][8][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][9][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][9][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][9][1], methods=['GET', 'POST'])
def Beginning_to_back_test():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/back-testing-basics-sentiment.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][9][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][9][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][10][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][10][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][10][1], methods=['GET', 'POST'])
def More_Analysis():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/more-analysis-sentiment.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][10][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][10][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][11][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][11][0])




@app.route(TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][11][1], methods=['GET', 'POST'])
def Conclusion():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Python and Pandas with Sentiment Analysis Database/sentiment-conclusion.html", curLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][11][1], curTitle=TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][11][0],  nextLink = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][12][1], nextTitle = TOPIC_DICT["Python and Pandas with Sentiment Analysis Database"][12][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][0][1], methods=['GET', 'POST'])
def Monte_Carlo_Introduction():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/monte-carlo-simulator-python.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][0][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][0][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][1][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][1][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][1][1], methods=['GET', 'POST'])
def Monte_Carlo_dice_Function():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/monte-carlo-dice-function.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][1][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][1][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][2][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][2][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][2][1], methods=['GET', 'POST'])
def Creating_a_simple_Bettor():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/simple-bettor.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][2][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][2][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][3][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][3][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][3][1], methods=['GET', 'POST'])
def Plotting_Results_with_Matpltolib():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/plotting-monte-carlo-matplotlib.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][3][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][3][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][4][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][4][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][4][1], methods=['GET', 'POST'])
def Martingale_Strategy():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/martingale-strategy.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][4][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][4][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][5][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][5][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][5][1], methods=['GET', 'POST'])
def Bettor_Statistics():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/bettor-statistics-monte-carlo.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][5][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][5][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][6][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][6][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][6][1], methods=['GET', 'POST'])
def More_comparison():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/more-monte-carlo-comparison.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][6][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][6][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][7][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][7][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][7][1], methods=['GET', 'POST'])
def Graphing_Monte_Carlo():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/graphing-monte-carlo.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][7][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][7][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][8][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][8][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][8][1], methods=['GET', 'POST'])
def Fixing_Debt_Issues():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/fixing-debt-issues-monte-carlo.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][8][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][8][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][9][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][9][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][9][1], methods=['GET', 'POST'])
def Analyzing_Monte_Carlo_results():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/analyzing-monte-carlo-results.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][9][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][9][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][10][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][10][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][10][1], methods=['GET', 'POST'])
def Using_Monte_Carlo_to_find_Best_multiple():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/using-monte-carlo-to-snoop.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][10][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][10][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][11][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][11][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][11][1], methods=['GET', 'POST'])
def Checking_betting_results():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/checking-bettor-results.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][11][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][11][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][12][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][12][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][12][1], methods=['GET', 'POST'])
def DAlembert_Strategy():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/dalembert-strategy.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][12][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][12][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][13][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][13][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][13][1], methods=['GET', 'POST'])
def For_5050_Odds():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/50-50-odds.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][13][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][13][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][14][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][14][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][14][1], methods=['GET', 'POST'])
def Analysis_of_DAlembert():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/dalembert-analysis.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][14][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][14][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][15][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][15][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][15][1], methods=['GET', 'POST'])
def Comparing_Profitability():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/comparing-profitability.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][15][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][15][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][16][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][16][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][16][1], methods=['GET', 'POST'])
def Finding_best_DAlembert_Multiple():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/snooping-best-dalembert-multiple.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][16][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][16][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][17][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][17][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][17][1], methods=['GET', 'POST'])
def Two_dimensional_charting_monte_carlo():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/two-dimension-graph-monte-carlo.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][17][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][17][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][18][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][18][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][18][1], methods=['GET', 'POST'])
def Monte_Carlo_Simulation_and_Python():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/monte-carlo-python.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][18][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][18][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][19][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][19][0])




@app.route(TOPIC_DICT["Creating a Monte Carlo simulator"][19][1], methods=['GET', 'POST'])
def Labouchere_System_for_Gambling_Tested():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Creating a Monte Carlo simulator/testing-labouchere.html", curLink = TOPIC_DICT["Creating a Monte Carlo simulator"][19][1], curTitle=TOPIC_DICT["Creating a Monte Carlo simulator"][19][0],  nextLink = TOPIC_DICT["Creating a Monte Carlo simulator"][20][1], nextTitle = TOPIC_DICT["Creating a Monte Carlo simulator"][20][0])




@app.route(TOPIC_DICT["IBpy"][0][1], methods=['GET', 'POST'])
def IBPy_Tutorial_for_using_Interactive_Brokers_API_with_Python():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/IBpy/ibpy-tutorial-using-interactive-brokers-api-python.html", curLink = TOPIC_DICT["IBpy"][0][1], curTitle=TOPIC_DICT["IBpy"][0][0],  nextLink = TOPIC_DICT["IBpy"][1][1], nextTitle = TOPIC_DICT["IBpy"][1][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][0][1], methods=['GET', 'POST'])
def Programming_for_Fundamental_Investing():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/python-fundamental-investing.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][0][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][0][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][1][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][1][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][1][1], methods=['GET', 'POST'])
def Getting_Company_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/fundamental-company-data.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][1][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][1][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][2][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][2][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][2][1], methods=['GET', 'POST'])
def Price_to_Book_ratio_example():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/price-to-book-ratio.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][2][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][2][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][3][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][3][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][3][1], methods=['GET', 'POST'])
def Python_Stock_Screener_for_Price_to_Book():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/create-a-stock-screener-python.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][3][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][3][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][4][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][4][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][4][1], methods=['GET', 'POST'])
def Python_Screener_for_PEG_Ratio():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/peg-ratio-stock-screener.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][4][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][4][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][5][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][5][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][5][1], methods=['GET', 'POST'])
def Adding_Price_to_Earnings():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/price-to-earnings-screener.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][5][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][5][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][6][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][6][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][6][1], methods=['GET', 'POST'])
def Getting_all_Russell_3000_stock_tickers():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/compiling-russell-3000-tickers.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][6][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][6][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][7][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][7][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][7][1], methods=['GET', 'POST'])
def Getting_all_Russell_3000_stock_tickers_part_2():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/compiling-russell-3000-tickers-2.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][7][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][7][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][8][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][8][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][8][1], methods=['GET', 'POST'])
def More_stock_Screening():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/more-stock-screening.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][8][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][8][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][9][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][9][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][9][1], methods=['GET', 'POST'])
def Completing_Basic_Stock_Screener():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/completing-basic-stock-screener.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][9][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][9][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][10][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][10][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][10][1], methods=['GET', 'POST'])
def Connecting_with_Quandl_for_Annual_Earnings_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/connecting-with-quandl.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][10][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][10][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][11][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][11][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][11][1], methods=['GET', 'POST'])
def Organizing_Earnings_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/organizing-earnings-data.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][11][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][11][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][12][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][12][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][12][1], methods=['GET', 'POST'])
def Graphing_Finance_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/graphing-finance-data-fundamentals.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][12][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][12][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][13][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][13][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][13][1], methods=['GET', 'POST'])
def Finishing_the_Graphing():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/finishing-fundamental-graphing.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][13][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][13][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][14][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][14][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][14][1], methods=['GET', 'POST'])
def Adding_the_Graphing_to_the_Screener():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/incorporating-graphing-into-stock-screener.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][14][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][14][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][15][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][15][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][15][1], methods=['GET', 'POST'])
def Preparing_figure_to_Accept_Finance_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/preparing-figure-for-finance-data.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][15][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][15][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][16][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][16][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][16][1], methods=['GET', 'POST'])
def Adding_Historical_Earnings_to_Stock_Screener_Chart_Data():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/adding-historical-earnings.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][16][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][16][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][17][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][17][0])




@app.route(TOPIC_DICT["Programming for Fundamental Investing"][17][1], methods=['GET', 'POST'])
def Completing_the_Fundamental_Investing_Stock_Screeners():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Programming for Fundamental Investing/fundamental-investing-stock-screener-conclusion.html", curLink = TOPIC_DICT["Programming for Fundamental Investing"][17][1], curTitle=TOPIC_DICT["Programming for Fundamental Investing"][17][0],  nextLink = TOPIC_DICT["Programming for Fundamental Investing"][18][1], nextTitle = TOPIC_DICT["Programming for Fundamental Investing"][18][0])




@app.route(TOPIC_DICT["Virtual Private Server Basics"][0][1], methods=['GET', 'POST'])
def VPS_with_AWS_EC2_and_Python_intro():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Virtual Private Server Basics/python-vps-intro.html", curLink = TOPIC_DICT["Virtual Private Server Basics"][0][1], curTitle=TOPIC_DICT["Virtual Private Server Basics"][0][0],  nextLink = TOPIC_DICT["Virtual Private Server Basics"][1][1], nextTitle = TOPIC_DICT["Virtual Private Server Basics"][1][0])




@app.route(TOPIC_DICT["Virtual Private Server Basics"][1][1], methods=['GET', 'POST'])
def Navigating_the_Terminal():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Virtual Private Server Basics/navigating-terminal.html", curLink = TOPIC_DICT["Virtual Private Server Basics"][1][1], curTitle=TOPIC_DICT["Virtual Private Server Basics"][1][0],  nextLink = TOPIC_DICT["Virtual Private Server Basics"][2][1], nextTitle = TOPIC_DICT["Virtual Private Server Basics"][2][0])




@app.route(TOPIC_DICT["Virtual Private Server Basics"][2][1], methods=['GET', 'POST'])
def Navigating_the_Terminal_p2():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Virtual Private Server Basics/terminal-navigation.html", curLink = TOPIC_DICT["Virtual Private Server Basics"][2][1], curTitle=TOPIC_DICT["Virtual Private Server Basics"][2][0],  nextLink = TOPIC_DICT["Virtual Private Server Basics"][3][1], nextTitle = TOPIC_DICT["Virtual Private Server Basics"][3][0])




@app.route(TOPIC_DICT["Virtual Private Server Basics"][3][1], methods=['GET', 'POST'])
def Crontab_tutorial_for_cron_jobs():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Virtual Private Server Basics/cron-tutorial-vps.html", curLink = TOPIC_DICT["Virtual Private Server Basics"][3][1], curTitle=TOPIC_DICT["Virtual Private Server Basics"][3][0],  nextLink = TOPIC_DICT["Virtual Private Server Basics"][4][1], nextTitle = TOPIC_DICT["Virtual Private Server Basics"][4][0])




@app.route(TOPIC_DICT["Virtual Private Server Basics"][4][1], methods=['GET', 'POST'])
def Running_Multiple_Scripts_at_Once():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Virtual Private Server Basics/running-multiple-scripts.html", curLink = TOPIC_DICT["Virtual Private Server Basics"][4][1], curTitle=TOPIC_DICT["Virtual Private Server Basics"][4][0],  nextLink = TOPIC_DICT["Virtual Private Server Basics"][5][1], nextTitle = TOPIC_DICT["Virtual Private Server Basics"][5][0])




@app.route(TOPIC_DICT["Virtual Private Server Basics"][5][1], methods=['GET', 'POST'])
def Using_nohup_command_to_Keep_Scripts_Alive():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Virtual Private Server Basics/nohup-command.html", curLink = TOPIC_DICT["Virtual Private Server Basics"][5][1], curTitle=TOPIC_DICT["Virtual Private Server Basics"][5][0],  nextLink = TOPIC_DICT["Virtual Private Server Basics"][6][1], nextTitle = TOPIC_DICT["Virtual Private Server Basics"][6][0])




@app.route(TOPIC_DICT["Virtual Private Server Basics"][6][1], methods=['GET', 'POST'])
def Python_Anywhere_using_PythonAnywhere():
    #update_user_tracking()
    #completed_percentages = topic_completion_percent()
    return render_template("tutorials/Virtual Private Server Basics/python-anywhere.html", curLink = TOPIC_DICT["Virtual Private Server Basics"][6][1], curTitle=TOPIC_DICT["Virtual Private Server Basics"][6][0],  nextLink = TOPIC_DICT["Virtual Private Server Basics"][7][1], nextTitle = TOPIC_DICT["Virtual Private Server Basics"][7][0])



####Runtime	
if __name__ == "__main__":
   # app.debug = True
    app.run()