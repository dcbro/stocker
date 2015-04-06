from stocker import app, db, model
from celery import Celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import datetime
import requests


logger = get_task_logger(__name__)


#Function to make the API call with the exception handling included
def make_api_call(url, attributes=None):
	#Try to make a call to the API. If that doesn't work then write out the error message and exit the program
	try:
		call = requests.get(url)
	except:
		return 'Error making the API Call!'
	
	#Check that the status code returned from the API is a 200. 
	#If not return the error code and the message.
	if call.status_code == requests.codes.ok:
		return call.json()	
	else:
		return 'Error! HTTP Code: {0}'.format(str(call.status_code))


def add_stock_data(ticker, start_date):
	"""Insert the prior data into the stocks table in the database"""
	today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

	url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22{0}%22%20and%20startDate%20%3D%20%22{1}%22%20and%20endDate%20%3D%20%22{2}%22&format=json&env=http%3A%2F%2Fdatatables.org%2Falltables.env'.format(ticker, start_date, today)
	r = make_api_call(url)

	for data in r['query']['results']['quote']:
		stock_data = model.Stocks(ticker=data['Symbol'], date=data['Date'], openp=data['Open'], high=data['High'], low=data['Low'] , close=data['Close'], volume=data['Volume'], adjusted_close=data['Adj_Close'])
		db.session.add(stock_data)
	db.session.commit()
	return


def query_max_date():
	qry = db.session.query(model.Stocks.ticker, db.func.max(model.Stocks.date).label('max_date'))
	qry = qry.group_by(model.Stocks.ticker)
	return qry.all()

#@periodic_task(run_every=(crontab(hour="0", minute="0", day_of_week="mon,tue,wed,thu,fri")))
def add_new_stock_data():
	for results in query_max_date():
		start_date = (results[1] + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		add_stock_data(results[0], start_date)
