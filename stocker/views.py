from stocker import app, db, model
from flask import request, render_template

@app.route('/add', methods=['POST', 'GET'])
def add_ticker():
	if request.method == 'GET':
		return render_template('add.html', ticker=None)

	if request.method == 'POST':
		stock = request.form['ticker'].upper()
		ticker = model.Ticker(stock)
		db.session.add(ticker)
		db.session.commit()
		return render_template('add.html', ticker=stock)