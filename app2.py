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
from flask import Flask, render_template, redirect, url_for, request, session, flash
import gunicorn
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secret key for session encryption

options_file_path = os.path.abspath('options.txt')
if not os.path.exists(options_file_path):
    with open(options_file_path, 'w') as options_file:
        options_file.write("Enter the options" + '\n')
options=[]
if os.path.exists(options_file_path):
    with open(options_file_path, 'r') as options_file:
        options = options_file.read().splitlines()

# Load options from the local file on server startup    
@app.route('/add_option', methods=['POST'])
def add_option():
    options_file_path = os.path.abspath('options.txt')    
    data = request.json
    new_option = data.get('newOption')
    if not os.path.exists(options_file_path):
        with open(options_file_path, 'w') as options_file:
            options_file.write(new_option + '\n')
    else:
        # Append the new option to the existing file
        with open(options_file_path, 'a') as options_file:
            options_file.write(new_option + '\n')

    
    return jsonify({'message': 'Option added successfully'})


# Simulated user database (replace with your own authentication system)
users = {'admin': 'admin'}


@app.route('/')
def index():
    return render_template('login_auth.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['logged_in'] = True
        return redirect(url_for('billing'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('index'))
    
@app.route('/billing')
def billing():
    if session.get('logged_in'):
        menu_data = {}  # Create a dictionary to hold menu data for each category
        categories = ["Tea menu", "Coffee and Milk", "Maggie and Fries", "Fast Food", "Starters and Biryani", "Fresh Juices", "Today's Special"]  # List of category names

        for category in categories:
            menu_data[category] = []  # Initialize an empty list for each category
            csv_filename = f"{category.replace(' ', '_').lower()}.csv"  # Generate the CSV file name based on the category
            with open(csv_filename, mode='r', newline='') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    menu_data[category].append(row)  # Append menu items to the category's list

        return render_template('v2.html', menu_data=menu_data)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Perform any logout actions here (e.g., clearing session data)
    session.clear()
    return redirect(url_for('index'))

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

@app.route('/add-new-item', methods=['POST'])
def add_new_item():
    data = request.get_json()
    newItemName = data['newItemName']
    newItemPrice = data['newItemPrice']

    csv_filename = "today's_special.csv"

    try:
        # Append the new item to the CSV file
        with open(csv_filename, mode='a', newline='') as file:
            fieldnames = ['Item', 'Price']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the new item data
            csv_writer.writerow({'Item': newItemName, 'Price': newItemPrice})

        return jsonify({'message': 'New item added successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    
@app.route('/clear-items', methods=['POST'])
def clear_items():
    csv_filename = "today's_special.csv"

    try:
        # Clear the CSV file by opening it in write mode
        with open(csv_filename, mode='w', newline='') as file:
            fieldnames = ['Item', 'Price']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()

        return jsonify({'message': 'All items and prices cleared successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/raw_material_purchase')
def raw_material_purchase():
    return render_template('purchase.html', options=options)

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
    app.run(host='0.0.0.0', port=5000, debug=True)
