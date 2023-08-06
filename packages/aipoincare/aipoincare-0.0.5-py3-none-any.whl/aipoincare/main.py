from flask import Flask, render_template, session
from flask import request
import os
from aipoincare.backend.training import train

app = Flask(__name__)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

def initialize():
	session['prepca'] = "yes"
	session['noise_threshold'] = "0.001"
	session['hidden_widths'] = "[256,256]"
	session['slope'] = "0.0"
	session['L'] = "[0.1]"
	session['opt'] = "Adam"
	session['learning_rate'] = "0.001"
	session['batch_size'] = "128"
	session['training_iteration'] = "2000"
	session['a'] = "2"
	session['n_walk'] = "2000"

@app.route('/')
def home():
	initialize()
	return render_template('home.html', session=session)

@app.route('/', methods=['GET', 'POST'])
def get_library_data():
	if request.method == 'POST':
		# Then get the data from the form
		model = request.form['HS']
		session['model'] = model
		print(model)
	dic = {"oned_harmonic": "./backend/data/oned_harmonic",
		   "twod_kepler": "./backend/data/twod_kepler",
		   "double_pendulum": "./backend/data/double_pendulum",
		   "magnetic_mirror": "./backend/data/magnetic_mirror",
		   "three_body": "./backend/data/three_body"
	}
	datapath = dic[model]
	return render_template('home.html', session=session)

@app.route('/upload', methods=['GET', 'POST'])
def get_own_data():
	f = request.files['filename']
	fm = f.filename
	if fm:
		session['model'] = fm
		f.save(os.path.join('./backend/data/', f.filename))
		model = f.filename
		print('file uploaded successfully')
	return render_template('home.html', session=session)


@app.route('/preference', methods=['GET', 'POST'])
def get_parameter():
	change_mode = request.form['submit']
	if change_mode == "Save":
		session['prepca'] = request.form['prepca']
		session['noise_threshold'] = request.form['noise_threshold']
		session['hidden_widths'] = request.form['hidden_widths']
		session['slope'] = request.form['slope']
		session['L'] = request.form['L']
		session['opt'] = request.form['opt']
		session['learning_rate'] = request.form['learning_rate']
		session['batch_size'] = request.form['batch_size']
		session['training_iteration'] = request.form['training_iteration']
		session['a'] = request.form['a']
		session['n_walk'] = request.form['n_walk']
		save = True
		return render_template('home.html', session=session, save=save)
	else:
		initialize()
		save = False
		return render_template('home.html', session=session, save=save)

@app.route('/train', methods=['GET', 'POST'])
def training():
	print("Training...")
	#train(session)
	neff, remove_dim, confidence = train(session)
	update = True
	return render_template('home.html', session=session, update=update, neff=neff, remove_dim=remove_dim, confidence=confidence)
	
def run():
	app.run(debug=True, use_reloader=False)

#if __name__ == '__main__':
#	app.run(debug=True)