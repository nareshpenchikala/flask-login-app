"""
Routes and views for the flask application.
"""
"""
The flask application package.
"""
from flask import Flask, render_template, request, jsonify
from escpos.printer import Usb
import qrcode
import os
from flask import Flask, render_template, redirect, url_for, request, session
import gunicorn
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('v1.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            return render_template('cafe.html')
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/print_bill', methods=['POST'])
def print_bill():
    date = request.json.get('date')
    dayOfWeek = request.json.get('dayOfWeek')
    billno = request.json.get('billno')
    Time = request.json.get('time')
    selected_items = request.json.get('items')
    total = request.json.get('total')

    # Append data to CSV file
    csv_file_path = 'bill_data.csv'

    # Create CSV file if it doesn't exist
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Date','bill Number','Time', 'weekday', 'Item Name', 'Quantity', 'Cost'])

    # Append data to CSV file
    with open(csv_file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for item in selected_items:
            csv_writer.writerow([date, billno, Time,  dayOfWeek, item['name'], item['quantity'], item['subtotal']])

    return jsonify({'message': 'Bill data added to CSV'})




@app.route('/raw_material_purchase')
def raw_material_purchase():
    return render_template('purchase.html')

@app.route('/add_purchase', methods=['POST'])
def add_purchase():
    data = request.json
    date = request.json.get('currentDate')
    item_name = data.get('itemName')
    quantity = data.get('quantity')
    quantity_type = data.get('quantityType')
    unitprice = data.get('unitPrice')
    totalcost = data.get('totalCost')

    # Append data to CSV file
    csv_file_path = 'raw_material_purchases.csv'

    # Create CSV file if it doesn't exist
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Date', 'Item Name', 'Quantity', 'Quantity Type', 'Unit Price', 'Total cost'])

    # Append data to CSV file
    with open(csv_file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([date, item_name, quantity, quantity_type, unitprice, totalcost])

    return jsonify({'message': 'Purchase data added to CSV'})



if __name__ == "__main__":
    app.run()
