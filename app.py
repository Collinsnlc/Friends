from flask import Flask, render_template,url_for,request,redirect
import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'

#initialize db
db = SQLAlchemy(app)

#create a db model
class Friends(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200),nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	#Create function to return a string when we add something
	def __repr__(self):
		return '<Name %r>' % self.id



subscribers = []

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	names = ['John','Neal','Sam','Kevin']
	return render_template('about.html',names=names)

@app.route('/subscribe',methods=['GET','POST'])
def subscribe():
	return render_template('subscribe.html')


@app.route('/form',methods=['POST','GET'])
def form():
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	email = request.form.get('email')
	
	if first_name and last_name and email:
		message = "You have been subscribed to my email newsletter"
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login("nlczombie9@gmail.com","Moose998!")
		server.sendmail("nlczombie9@gmail.com", email, message)
	
	else:
		error = "Please Fill Out All Forms"
		return render_template("subscribe.html",error=error)
	
	subscribers.append(f"{first_name} {last_name} {email}")
	return render_template('form.html',subscribers=subscribers)

@app.route('/friends',methods=['POST','GET'])
def friends():
	if request.method == "POST":
		friend_name = request.form['name']
		new_friend = Friends(name=friend_name)

		#push to database
		try:
			db.session.add(new_friend)
			db.session.commit()
			return redirect('/friends')
		except:
			return "There was an error adding your friend"

	else:
		friends = Friends.query.order_by(Friends.date_created)
		return render_template('friends.html',friends=friends)

@app.route('/delete/<int:id>')
def delete(id):
	friend_to_delete = Friends.query.get_or_404(id)

	try:
		db.session.delete(friend_to_delete)
		db.session.commit()
		return redirect('/friends')

	except:
		return "There was a problem deleting that friend..."


@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
	friend_to_update = Friends.query.get_or_404(id)
	if request.method == "POST":
		friend_to_update.name = request.form['name']
		try:
			db.session.commit()
			return redirect('/friends')
		except:
			return "There was a problem updating that friend"
	else:
		return render_template('update.html',friend_to_update=friend_to_update)


	
			