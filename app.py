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

#-- Main Routes --#
@app.route('/')
def index():
    return render_template('index.html')

#-- Customer Routes --#
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

@app.route('/customer/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        
        cursor.execute("UPDATE customers SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s", (name, email, phone, address, id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('customers'))
    
    cursor.execute("SELECT * FROM customers WHERE id=%s", (id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('customer_form.html', customer=customer)

@app.route('/customer/delete/<int:id>')
def delete_customer(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('customers'))

#-- Vehicle Routes --#
@app.route('/vehicles')
def vehicles():
    brand = request.args.get('brand', '').strip()
    model = request.args.get('model', '').strip()
    year = request.args.get('year', '').strip()
    color = request.args.get('color', '').strip()
    max_price = request.args.get('max_price', '').strip()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM vehicles WHERE 1=1"
    params = []

    if brand:
        sql += " AND brand LIKE %s"
        params.append(f"%{brand}%")

    if model:
        sql += " AND model LIKE %s"
        params.append(f"%{model}%")

    if year:
        sql += " AND year = %s"
        params.append(year)

    if color:
        sql += " AND color LIKE %s"
        params.append(f"%{color}%")

    if max_price:
        sql += " AND price <= %s"
        params.append(max_price)
        sql += " ORDER BY price DESC"

    cursor.execute(sql, params)
    vehicles = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('vehicles.html', vehicles=vehicles)

@app.route('/vehicle/new', methods=['GET', 'POST'])
def new_vehicle():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        color = request.form['color']
        price = request.form['price']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vehicles (brand, model, year, color, price) VALUES (%s, %s, %s, %s, %s)", (brand, model, year, color, price))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('vehicles'))
    
    return render_template('vehicle_form.html')

@app.route('/vehicle/edit/<int:id>', methods=['GET', 'POST'])
def edit_vehicle(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        color = request.form['color']
        price = request.form['price']
        
        cursor.execute("UPDATE vehicles SET brand=%s, model=%s, year=%s, color=%s, price=%s WHERE id=%s", (brand, model, year, color, price, id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('vehicles'))
    
    cursor.execute("SELECT * FROM vehicles WHERE id=%s", (id,))
    vehicle = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('vehicle_form.html', vehicle=vehicle)

@app.route('/vehicle/delete/<int:id>', methods=['POST'])
def delete_vehicle(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicles WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('vehicles'))

#-- Sales Routes --#



if __name__ == '__main__':
    app.run(debug=True)