#!/usr/bin/python

import StringIO 

from flask import Flask, render_template, request, redirect, send_file, flash

from flask.ext.wtf import Form 
from wtforms import TextField, SubmitField, validators

import exporter

class ProjectForm(Form):
	username	= TextField("Username")
	submit = SubmitField ("Submit")

app = Flask(__name__)
app.secret_key = "mysuperdupersecretkey"

@app.route('/', methods=['GET', 'POST'])
def projects():
	form = ProjectForm()
	
	if request.method == 'GET':
		return render_template('projects.html', form=form)
	
	elif request.method == 'POST':
		projects = exporter.export(form.username.data)
		if projects == None:
			flash("Not a valid Ravelry username", 'error')
			return render_template('projects.html', form=form)

		else:
			sio = StringIO.StringIO()
			sio.write(projects)
			sio.seek(0)
			return send_file(sio, attachment_filename = "projects.csv", as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
