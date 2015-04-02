from stocker import app, db, model
import datetime
import requests



def add_stock_data(ticker, start_date):
	"""Insert the prior data into the stocks table in the database"""
	today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

	r = requests.get('http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22{0}%22%20and%20startDate%20%3D%20%22{1}%22%20and%20endDate%20%3D%20%22{2}%22&format=json&env=http%3A%2F%2Fdatatables.org%2Falltables.env'.format(ticker, start_date, today)).json()

	for data in r['query']['results']['quote']:
		stock_data = model.Stocks(ticker=data['Symbol'], date=data['Date'], openp=data['Open'], high=data['High'], low=data['Low'] , close=data['Close'], volume=data['Volume'], adjusted_close=data['Adj_Close'])
		db.session.add(stock_data)
	db.session.commit()
	return

def query_max_date():
	qry = db.session.query(model.Stocks.ticker, db.func.max(model.Stocks.date).label('max_date'))
	qry = qry.group_by(model.Stocks.ticker)
	return qry.all()

def add_new_stock_data():
	for results in query_max_date():
		start_date = (results[1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		add_stock_data(results[0], start_date) 
