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
        
        cursor.execute("""UPDATE customers SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s""", (name, email, phone, address, id))
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
        
        cursor.execute("""UPDATE vehicles SET brand=%s, model=%s, year=%s, color=%s, price=%s WHERE id=%s""", (brand, model, year, color, price, id))
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
@app.route('/sales')
def sales():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT v.id,
        c.name AS customer_name,
        s.brand AS vehicle_brand,
        s.model AS vehicle_model,
        s.color AS vehicle_color,
        v.price,
        v.sale_date
    FROM sales v
    JOIN customers c ON v.customer_id = c.id
    JOIN vehicles s ON v.vehicle_id = s.id
    ORDER BY v.sale_date DESC
    """)
    sales = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('sales.html', sales=sales)

@app.route('/sale/new', methods=['GET', 'POST'])
def new_sale():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM customers")
    customers = cursor.fetchall()
    cursor.execute("SELECT id, brand, model FROM vehicles")
    vehicles = cursor.fetchall()

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        vehicle_id = request.form['vehicle_id']
        sale_date = request.form['sale_date']
        price = request.form['price']
        
        cursor.execute("INSERT INTO sales (customer_id, vehicle_id, sale_date, price) VALUES (%s, %s, %s, %s)", (customer_id, vehicle_id, sale_date, price))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('sales'))
    
    cursor.close()
    conn.close()
    return render_template('sale_form.html', customers=customers, vehicles=vehicles)

@app.route('/sale/edit/<int:id>', methods=['GET', 'POST'])
def edit_sale(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM customers")
    customers = cursor.fetchall()
    cursor.execute("SELECT id, brand, model FROM vehicles")
    vehicles = cursor.fetchall()

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        vehicle_id = request.form['vehicle_id']
        sale_date = request.form['sale_date']
        price = request.form['price']
        
        cursor.execute("""UPDATE sales SET customer_id=%s, vehicle_id=%s, sale_date=%s, price=%s WHERE id=%s""", (customer_id, vehicle_id, sale_date, price, id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('sales'))
    
    cursor.execute("""
        SELECT
            v.id,
            v.customer_id,
            v.vehicle_id,
            v.sale_date,
            v.price,
            c.name AS customer_name,
            s.brand AS vehicle_brand,
            s.model AS vehicle_model
        FROM sales v
        JOIN customers c ON v.customer_id = c.id
        JOIN vehicles s ON v.vehicle_id = s.id
        WHERE v.id=%s
    """, (id,))
    sale = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('sale_form.html', sale=sale, customers=customers, vehicles=vehicles)

@app.route('/sale/delete/<int:id>')
def delete_sale(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sales WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('sales'))

#-- Run the App --#
if __name__ == '__main__':
    app.run(debug=True)