from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM books')
    books = cur.fetchall()
    cur.close()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO books (title, author) VALUES (%s, %s)', (title, author))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        cur.execute('UPDATE books SET title = %s, author = %s WHERE id = %s', (title, author, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    cur.execute('SELECT * FROM books WHERE id = %s', (id,))
    book = cur.fetchone()
    cur.close()
    return render_template('edit_book.html', book=book)

@app.route('/delete_book/<int:id>')
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM books WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
