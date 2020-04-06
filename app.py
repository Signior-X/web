from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, SelectField, SubmitField


app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f16d441f67567d671f2b6176a'
app.config.from_object(__name__)

@app.route('/')
def home():
	return render_template('home.html')

class ReusableForm(Form):
	name = TextField('Name:', validators=[validators.required()])

	@app.route('/todo', methods=['POST','GET'])
	def todo():
		form = ReusableForm(request.form)

		print(form.errors)
		if request.method == 'POST':
			name = request.form['name']
			print(name)
		
		if form.validate():
			#save the comment here
			flash('Hello' + name)
		else:
			flash('All the fields are required')
		
		return render_template('todo.jinja2', form=form)

@app.route('/user/<username>')
def hello(username):
	return render_template('todo.html', username=username)


if __name__ == "__main__":
	app.run()
