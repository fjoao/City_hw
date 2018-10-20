from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
import pymysql
import getpass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

def get_pass():
	return getpass.getpass('password: ')
def open(pswd):
	return pymysql.connect(host='35.238.36.135', user='root', password=pswd, db='cities')

	#c = db.cursor()
	#c.execute(x, (s, i))
	#db.commit()
	#db.close()

class AddForm(FlaskForm):

	city = StringField('What is the name of the city?', validators=[DataRequired()])
	pop = IntegerField('What is the population of the city?', validators=[DataRequired()])
	submit = SubmitField('Submit')

class DelForm(FlaskForm):

	city = StringField('What is the name of the city?', validators=[DataRequired()])
	submit = SubmitField('Submit')

@app.route('/add', methods=['GET', 'POST'])
def index():
	city = None
	pop = None
	form = AddForm()

	if form.validate_on_submit():
		city = form.city.data
		pop = form.pop.data
		form.city.data = ''
		form.pop.data = ''
		base = open(get_pass())
		c = base.cursor()
		c.execute('INSERT into city_pop values(%s, %s)', (city, pop))
		base.commit()
		base.close()

	return render_template('index.html', form=form, city=city)


@app.route('/', methods=['GET', 'POST'])
def display():
	pswd = getpass.getpass('Password: ')
	db = pymysql.connect(host='35.238.36.135', user='root', password=pswd, db='cities')
	c = db.cursor()
	c.execute('SELECT name from city_pop')
	n = c.fetchall()
	c.execute('SELECT population from city_pop')
	p = c.fetchall()
	db.close()
	num = len(n)

	return render_template('view.html', city=n, pop=p, num=num)


@app.route('/del', methods=['Get', 'POST'])
def remove():
	city = None
	pop = None
	form = DelForm()

	if form.validate_on_submit():
		city = form.city.data
		form.city.data = ''
		ba = open(get_pass())
		c = ba.cursor()
		c.execute('DELETE FROM city_pop where name = \"'+city+'\"')
		ba.commit()
		ba.close()

	return render_template('index1.html', form=form, city=city)

