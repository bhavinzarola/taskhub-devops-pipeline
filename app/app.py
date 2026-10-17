import os
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db():
    """
    Connects to the PostgreSQL database using environment variables.
    Includes a retry loop to handle database container initialization delays.
    """
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    # Retry loop: Keeps trying to connect for 30 seconds
    for attempt in range(5):
        try:
            return psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password
            )
        except Exception as e:
            print(f"Database connection attempt {attempt+1} failed: {e}")
            time.sleep(5)  # Wait 5 seconds before retrying
    
    # If it still fails, raise the error
    raise Exception("Could not connect to database after multiple attempts.")

def init_db():
    """Initializes the database schema if it doesn't exist."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT id, title, created_at FROM notes ORDER BY id DESC')
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO notes (title, content) VALUES (%s, %s)', (title, content))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create_note.html')

@app.route('/note/<int:id>')
def view_note(id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM notes WHERE id = %s', (id,))
    note = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('view_note.html', note=note)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cur.execute('UPDATE notes SET title=%s, content=%s WHERE id=%s', (title, content, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    cur.execute('SELECT * FROM notes WHERE id = %s', (id,))
    note = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('edit_note.html', note=note)

@app.route('/delete/<int:id>')
def delete_note(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    # Initialize the database table when the app starts
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)