from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    search = request.args.get('search', '')
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    if search:
        c.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", 
                  ('%' + search + '%', '%' + search + '%'))
    else:
        c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts, search=search)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                  (name, phone, email, address))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        c.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
                  (name, phone, email, address, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM contacts WHERE id=?", (id,))
        contact = c.fetchone()
        conn.close()
        return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
