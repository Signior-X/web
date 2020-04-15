from flask import Flask, render_template, request, session, redirect, jsonify, url_for, flash
from webdb.mysqlconnect import mycursor, mydb, sqlerror, create_insert_statement

app = Flask(__name__)
app.secret_key="priyamsethrandofosdfonad"

'''
Urls help
/register 			 For Browsers to Register  (GET) (POST)
/login 				 For Browsers to Login   (GET) (POST)
/logout 			 For Browser and Android Both   (GET) and (POST)

# For android take care of cookies
/api/login  		For Android to login   (POST)
/api/register	 	For Android to Register  (POST)

Database help
loginDetails : username, password

'''

# Home Page
@app.route('/')
def home():
	if 'logged_in' not in session:
		return redirect(url_for('login'))

	return render_template('home.html', username=session['username'])

# Register Page - Browser 
# For POST send the data in either JSON Body or Form body
# data needed username and password
# Get method to show the HTML Page
@app.route('/register', methods=['POST','GET'])
def register():
	if 'logged_in' in session:
		return redirect(url_for('home'))

	if request.method == 'POST':
		# Posting JSON Data
		if request.is_json:
			#print("YES JSON DATA")
			data = request.get_json()
		# If it is not json certainly it is form data
		else:
			username = request.form['username']
			password = request.form['password']
			data = {
				"username":username,
				"password":password
			}
		if data['username'] == "":
			flash("Empty Username not allowed!")
			return redirect(url_for('register'))
		
		# Requests taken now do the insertion part
		data['tablename']='loginDetails'
		stmt = create_insert_statement(data)
		try:
			mycursor.execute(stmt)
			mydb.commit()
		except sqlerror as err:
			mydb.rollback()
			flash(str(err))
			return redirect(url_for('register'))
	
		# This means the statement has been successfully executed
		session['logged_in']=1
		session['username']=data['username']
		flash('Success fully created new Account!')
		return redirect(url_for('home'))
		# Post Method Done
	else:
		# Get method - For Browsers
		return render_template('register.html')
# Register Page and api - For Browser


# Login Page - Browser
# For POST send the data in either JSON Body or Form body
# data needed username and password
# Get method to show the HTML Page
@app.route('/login', methods=['POST','GET'])
def login():
	if 'logged_in' in session:
		return redirect(url_for('home'))
	
	if request.method == 'POST':
		# Posting JSON Data
		if request.is_json:
			#print("YES JSON DATA")
			data = request.get_json()
		# If it is not json certainly it is form data
		else:
			username = request.form['username']
			password = request.form['password']
			data = {
				"username":username,
				"password":password
			}
		try:
			stmt = "SELECT password from loginDetails where username='"+data['username']+"';"
			mycursor.execute(stmt)
			sqlpasswordtuple = mycursor.fetchone()
			if sqlpasswordtuple: #User exists
				if sqlpasswordtuple[0]==data['password']:
					session['logged_in']=1
					session['username']=data['username']
					return redirect(url_for('home'))  # Successfully loggined
				else:
					flash("Invalid Password!")
					return render_template('login.html')
			else:
				flash("username does not exist!")
				return render_template('login.html')

		except sqlerror as err:
			flash("SQL Error :",str(err))
			flash(" Could not Login! ")
			return render_template('login.html')
			# POST method completed
	else:
		#GET Method
		return render_template('login.html')
# Login Page and API for browser

# For logging out Android + FLask
@app.route('/logout', methods=['GET','POST'])
def logout():
	if 'logged_in' in session:
		session.pop('logged_in', None)
		session.pop('username', None)
		flash("Successfully logged out")
		if request.method == 'GET':
			return redirect(url_for('login'))
		else:
			return jsonify(success=1, msg="Logged out!")
	else:
		flash("Please Login First!")
		if request.method == 'GET':
			return redirect(url_for('login'))
		else:
			return jsonify(success=0, msg="Already logged out!")
# API + Page for Logout


# Login API - Android
# data ={
# 	username
#	password
# }
# errorcodes = {
# 0 : Already logged In
# 1 : Invalid Data Sent - Try to send in JSON Form in the Body
# 2 : Any SQL Error
# 3 : Invalid Credentials
# }
@app.route('/api/login', methods=['POST'])
def api_login():
	if 'logged_in' in session:
		print("Logged in already")
		return jsonify(success=0,msg="Already Logged In", errorcode=0)
	try:
		# Posting JSON Data
		if request.is_json:
			#print("YES JSON DATA")
			data = request.get_json()
		# If it is not json certainly it is form data
		else:
			username = request.form['username']
			password = request.form['password']
			data = {
				"username":username,
				"password":password
			}
	except:
		jsonify(success=0,msg="Invalid Response sent", errorcode=1)
	if 'password' not in data:  # checking that password is sent
		return jsonify(success=0,msg="No Password Sent", errorcode=1)
	if 'username' not in data: # checking that the password is sent
		return jsonify(success=0,msg="No username Sent", errorcode=1)
	
	# Checked for constrainsts all set
	try:
		stmt = "SELECT password from loginDetails where username='"+data['username']+"';"
		mycursor.execute(stmt)
		sqlpasswordtuple = mycursor.fetchone()  #sqlpassword is at index 0 of the tuple

		if sqlpasswordtuple: #User exists
			if sqlpasswordtuple[0]==data['password']:
				# ALL Things are good

				session['logged_in']=1
				session['username']=data['username']

				return jsonify(success=1,msg="Logged in & session created",username=data['username'])
			else:
				return jsonify(success=0,msg="Invalid Password",errorcode=3)
		else:
			return jsonify(success=0,msg="User does not exist",errorcode=3)
	
	except sqlerror as err:
		return jsonify(success=1,msg=str(err), errorcode=2)
	# POST method completed
# API Login for Android


# Register API - Android
# data ={
# 	username
#	password
# }
# errorcodes = {
# 0 : Already logged In
# 1 : Invalid Data Sent - Try to send in JSON Form in the Body
# 2 : Any SQL Error
# }
@app.route('/api/register', methods=['POST'])
def api_register():
	if 'logged_in' in session:
		return jsonify(success=0,msg="Already Logged In", errorcode=0)

	# Posting JSON Data
	try:
		if request.is_json:
			#print("YES JSON DATA")
			data = request.get_json()
		# If it is not json certainly it is form data
		else:
			username = request.form['username']
			password = request.form['password']
			data = {
				"username":username,
				"password":password
			}
	except:
		return jsonify(success=0,msg="Invalid Response Sent", errorcode=1)
	if 'password' not in data:  # checking that password is sent
		return jsonify(success=0,msg="No Password Sent", errorcode=1)
	if 'username' not in data: # checking that the password is sent
		return jsonify(success=0,msg="No username Sent", errorcode=1)
	if data['username'] == "":
		return jsonify(success=0,msg="Username is Empty", errorcode=1)
	
	# All set
	# Requests taken now do the insertion part
	data['tablename']='loginDetails'
	stmt = create_insert_statement(data)
	try:
		mycursor.execute(stmt)
		mydb.commit()
	except sqlerror as err:
		mydb.rollback()
		return jsonify(success=0, msg=str(err), errorcode=2)
	
	# This means the statement has been successfully executed
	session['logged_in']=1
	session['username']=data['username']
	return jsonify(success=1,msg="Successfully registered and session started!", username=data['username'])
	# Register Post Method Done
# API Register for Android




if __name__ == "__main__":
	app.run()
