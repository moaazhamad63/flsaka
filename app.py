from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        product_name = request.form['product_name']
        cursor.execute("SELECT * FROM products WHERE name LIKE?", ('%' + product_name + '%',))
        products = cursor.fetchall()
        conn.close()
        return render_template('index.html', products=products, search_query=product_name)
    else:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        conn.close()
        return render_template('index.html', products=products)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'add_product' in request.form:
            print(request.form)  # Print out the form data to see what's being sent
            product_name = request.form['product_name']
            product_price = request.form['product_price']
            product_id = request.form['product_id']
            print(product_price)  # Print out the product price to see what value it has
            cursor.execute("INSERT INTO products (name, price, id) VALUES (?,?,?)", (product_name, product_price, product_id))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))
        elif 'delete_product' in request.form:
            product_id = request.form['product_id']
            cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))
        elif 'search_product' in request.form:
            product_name = request.form['product_name']
            cursor.execute("SELECT * FROM products WHERE name LIKE?", ('%' + product_name + '%',))
            products = cursor.fetchall()
            print(products)  # Print out the products to see what data is being retrieved from the database
            conn.close()
            return render_template('dashboard.html', products=products, search_query=product_name)

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    print(products)  # Print out the products to see what data is being retrieved from the database
    conn.close()
    return render_template('dashboard.html', products=products)


if __name__ == '__main__':
    app.run( debug=True, threaded=True)
