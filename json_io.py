#!flask/bin/python

import sys
import os

from flask import Flask, render_template, request, redirect, url_for, Response
import random, json

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/img'

@app.route('/')
def output():
	return render_template('index.html')

@app.route('/restaurant', methods=['GET', 'POST'])
def postRestaurant():
	if request.method == 'POST':
		name = request.form['name']
		date = request.form['date']
		rating = request.form['name']
		comments = request.form['comments']
		data1 = {"name": name, "date": date, "rating": 4, "comments": comments}
		path = 'static'
		fileName = 'restaurants'
		id = request.args.get("id")
		writeToJSONFile(path, 'example', writeReview(readFromJSONFile(path, fileName), data1, id))
		return render_template('index.html')
	else:
		return render_template('restaurant.html')

@app.route('/admin', methods=['GET', 'POST'])
def newRestourant():
	if request.method == 'POST':
		restaurant_name = request.form['restaurant_name']
		address = request.form['adress']
		boro = request.form['boro']
		lat = request.form['lat']
		lng = request.form['lng']
		cuisine = request.form['cuisine']
		operating_hours = {"Monday": request.form['mon'], "Tuesday": request.form['tue'], "Wednesday": request.form['wed'], "Thursday": request.form['thu'], "Friday": request.form['fri'], "Saturday": request.form['sat'], "Sunday": request.form['sun']}
		file = request.files['image']
		f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
		file.save(f)
		path = 'static'
		fileName = 'restaurants'
		json_nr = readFromJSONFile('static', 'restaurants')
		id = len(json_nr['restaurants'])+1
		newResObj = {
				'id': id,
				'name': restaurant_name,
				"neighborhood": boro,
				"photograph": file.filename,
				"address": address,
				"latlng": { "lat": lat, "lng": lng },
				"cuisine_type": cuisine,
				"operating_hours": operating_hours,
				"reviews": [{},{},{}]
						}
		json_nr['restaurants'].append(newResObj)
		writeToJSONFile(path, fileName, json_nr)
		return redirect (url_for('output'))
	else:
		return render_template('admin.html')

def readFromJSONFile(path, fileName):
    filePathNameRExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameRExt, 'r') as f:
		json_load = json.load(f)
		return json_load

def writeReview(json_rv, data, id):
	for i in json_rv['restaurants']:
		if str(i['id']) == id:
			i['reviews'].insert(0,dict(data))
			return json_rv

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

if __name__ == '__main__':
	app.run("0.0.0.0", "8000")
