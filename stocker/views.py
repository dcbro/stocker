from stocker import app, db, model, controller
from flask import request, render_template, session, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError
import json
import datetime
import sys
import re


def valid_ticker(ticker):
	valid_ticker = re.match('[A-Z]{1,5}$', ticker)
	if valid_ticker is not None:
		url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.stocks%20where%20symbol%3D%22{0}%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'.format(ticker)
		r = controller.make_api_call(url)

		if len(r['query']['results']['stock']) > 1:
			return
		else:
			return "{0} is not a valid stock ticker!".format(ticker)
	else:
		return "{0} is an incorrect formatted ticker!".format(ticker)


@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('add_ticker'))
	return render_template('index.html', error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))


@app.route('/add', methods=['POST', 'GET'])
def add_ticker():
	error = None
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	start_date = (datetime.datetime.utcnow() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
	
	if request.method == 'GET':
		return render_template('add.html')

	if request.method == 'POST':
		stock = request.form['ticker'].upper()

		check_ticker = valid_ticker(stock)
		if check_ticker is not None:
			return render_template('add.html', error=check_ticker)
	
		try:
			ticker = model.Ticker(stock)
			db.session.add(ticker)
			db.session.commit()
			controller.add_stock_data(stock, start_date)
		except IntegrityError:
			db.session.rollback()
			error = "{0} has already been added!".format(stock)
			return render_template('add.html', error=error)
		return render_template('add.html', ticker=stock)


@app.route('/deleteall')
def delete_all():
	try:
		model.RSI.query.delete()
		model.Stocks.query.delete()
		model.Ticker.query.delete()
		db.session.commit()
	except:
		db.session.rollback()
		return render_template('deleteall.html', error='Error deleting table data!')	
	return render_template('deleteall.html')
