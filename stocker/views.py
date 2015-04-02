from stocker import app, db, model, controller
from flask import request, render_template
from sqlalchemy.exc import IntegrityError
import requests
import json
import datetime
import sys
import re


def valid_ticker(ticker):
	valid_ticker = re.match('[A-Z]{1,5}$', ticker)
	if valid_ticker is not None:
		r = requests.get('http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.stocks%20where%20symbol%3D%22{0}%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'.format(ticker)).json()
		if len(r['query']['results']['stock']) > 1:
			return
		else:
			return "{0} is not a valid stock ticker!".format(ticker)
	else:
		return "{0} is an incorrect formatted ticker!".format(ticker)


@app.route('/add', methods=['POST', 'GET'])
def add_ticker():
	error = None
	start_date = (datetime.datetime.utcnow() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
	
	if request.method == 'GET':
		return render_template('add.html', ticker=None, error=None)

	if request.method == 'POST':
		stock = request.form['ticker'].upper()

		check_ticker = valid_ticker(stock)
		if check_ticker is not None:
			return render_template('add.html', ticker=None, error=check_ticker)
		
		ticker = model.Ticker(stock)
		db.session.add(ticker)
		try:
			db.session.commit()
			controller.add_stock_data(stock, start_date)
		except IntegrityError:
			error = "{0} has already been added!".format(stock)
		return render_template('add.html', ticker=stock, error=error)

