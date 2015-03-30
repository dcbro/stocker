from stocker import app, db, model
from flask import request, render_template
from sqlalchemy.exc import IntegrityError
import requests
import json
import datetime
import sys


def add_stock_data(ticker):
	"""Insert the prior data into the stocks table in the database"""
	today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
	start_date = (datetime.datetime.utcnow() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")

	r = requests.get('http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22{0}%22%20and%20startDate%20%3D%20%22{1}%22%20and%20endDate%20%3D%20%22{2}%22&format=json&env=http%3A%2F%2Fdatatables.org%2Falltables.env'.format(ticker, start_date, today)).json()

	for data in r['query']['results']['quote']:
		stock_data = model.Stocks(ticker=data['Symbol'], date=data['Date'], openp=data['Open'], high=data['High'], low=data['Low'] , close=data['Close'], volume=data['Volume'], adjusted_close=data['Adj_Close'])
		db.session.add(stock_data)
	db.session.commit()
	return



@app.route('/add', methods=['POST', 'GET'])
def add_ticker():
	error = None
	if request.method == 'GET':
		return render_template('add.html', ticker=None)

	if request.method == 'POST':
		stock = request.form['ticker'].upper()
		ticker = model.Ticker(stock)
		db.session.add(ticker)
		try:
			db.session.commit()
			add_stock_data(stock)
		except IntegrityError:
			error = "{0} has already been added!".format(stock)
		return render_template('add.html', ticker=stock, error=error)

