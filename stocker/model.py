from stocker import app, db
from datetime import datetime


class Ticker(db.Model):
	ticker = db.Column(db.String(5), primary_key=True)
	timestamp = db.Column(db.DateTime)

	def __init__(self, ticker, timestamp=None):
		self.ticker = ticker
		if timestamp is None:
			timestamp = datetime.utcnow()
		self.timestamp = timestamp

	def __repr__(self):
		return '<Ticker %r>' % self.ticker

class Stocks(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ticker = db.Column(db.String(5), db.ForeignKey('ticker.ticker'))
	openp = db.Column(db.Float)
	high = db.Column(db.Float)
	low = db.Column(db.Float)
	close = db.Column(db.Float)
	volume = db.Column(db.Integer)
	adjusted_close = db.Column(db.Float)
	timestamp = db.Column(db.DateTime)

	def __init__(self, ticker, openp, high, low, close, volume, adjusted_close, timestamp=None):
		self.ticker = tickerp
		self.openp = openp
		self.high = high
		self.low = low
		self.close = close
		self.volume = volume
		self.adjusted_close = adjusted_close
		if timestamp is None:
			timesstamp = datetime.utcnow()
		self.timestamp = timestam
	
	def __repr__(self):
		return '<Stocks %r>' % self.ticker


class RSI(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ticker = db.Column(db.String(5), db.ForeignKey('ticker.ticker'))
	date = db.Column(db.DateTime) 
	avg_14_up = db.Column(db.Float)
	avg_14_down = db.Column(db.Float)
	rsi = db.Column(db.Float)
	timestamp = db.Column(db.DateTime)

	def __init__(self, ticker, date, avg_14_up, avg_14_down, rsi, timestamp=None):
		self.ticker = ticker
		self.date = date
		self.avg_14_up = avg_14_up
		self.avg_14_down = avg_14_down
		self.rsi = rsi
		if timestamp is None:
			timesstamp = datetime.utcnow()
		self.timestamp = timestamp

	def __repr__(self):
		return '<RSI %r>' % self.ticker
