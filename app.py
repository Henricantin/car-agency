from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "car_agency"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

if __name__ == '__main__':
    app.run(debug=True)

#-- Main Routes --#
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers')
def customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('customers.html', customers=customers)

@app.route('/customer/new', methods=['GET', 'POST'])
def new_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)", (name, email, phone, address))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('customers'))
    
    return render_template('customer_form.html')