from flask import Flask, request, redirect, url_for, render_template, flash
import os
import sqlite3
from datetime import date
from pathlib import Path

app = Flask(__name__, static_folder='static')
app.secret_key = 'change-this-to-a-secure-secret'
DATABASE_PATH = os.path.join(app.static_folder, 'todo.db')


def init_db():
    Path(app.static_folder).mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            priority TEXT NOT NULL DEFAULT 'Medium',
            category TEXT NOT NULL DEFAULT 'General',
            due_date TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute('PRAGMA table_info(tasks)')
        existing_columns = {column[1] for column in cursor.fetchall()}
        extra_columns = {
            'completed': 'completed INTEGER NOT NULL DEFAULT 0',
            'priority': "priority TEXT NOT NULL DEFAULT 'Medium'",
            'category': "category TEXT NOT NULL DEFAULT 'General'",
            'due_date': 'due_date TEXT',
            'created_at': 'created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP',
        }
        for column_name, definition in extra_columns.items():
            if column_name not in existing_columns:
                cursor.execute(f'ALTER TABLE tasks ADD COLUMN {definition}')
        conn.commit()


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

init_db()


def get_filter_values():
    status = request.args.get('status', 'all')
    priority = request.args.get('priority', 'all')
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').strip()
    return status, priority, category, search


@app.route('/')
def home():
    status, priority, category, search = get_filter_values()
    conn = get_db_connection()

    base_query = 'SELECT id, task, completed, priority, category, due_date, created_at FROM tasks'
    filters = []
    params = []

    if status == 'completed':
        filters.append('completed = 1')
    elif status == 'pending':
        filters.append('completed = 0')

    if priority in ('High', 'Medium', 'Low'):
        filters.append('priority = ?')
        params.append(priority)

    if category and category != 'all':
        filters.append('category = ?')
        params.append(category)

    if search:
        filters.append('LOWER(task) LIKE ?')
        params.append(f'%{search.lower()}%')

    if filters:
        base_query += ' WHERE ' + ' AND '.join(filters)

    base_query += ' ORDER BY completed ASC, CASE WHEN due_date IS NULL OR due_date = "" THEN 1 ELSE 0 END, due_date, created_at DESC'
    tasks = conn.execute(base_query, params).fetchall()

    categories = [row['category'] for row in conn.execute('SELECT DISTINCT category FROM tasks WHERE category IS NOT NULL AND category != "" ORDER BY category').fetchall()]
    total_tasks = conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
    completed_tasks = conn.execute('SELECT COUNT(*) FROM tasks WHERE completed = 1').fetchone()[0]
    pending_tasks = total_tasks - completed_tasks
    completion_percentage = int((completed_tasks / total_tasks) * 100) if total_tasks else 0
    all_completed = total_tasks > 0 and completed_tasks == total_tasks
    recent_activity = conn.execute('SELECT task, completed, created_at FROM tasks ORDER BY created_at DESC LIMIT 5').fetchall()
    conn.close()

    return render_template(
        'home.html',
        tasks=tasks,
        categories=categories,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        completion_percentage=completion_percentage,
        all_completed=all_completed,
        search=search,
        status_filter=status,
        priority_filter=priority,
        category_filter=category,
        recent_activity=recent_activity,
        today_date=date.today().isoformat(),
    )


@app.route('/add', methods=['POST'])
def add():
    task_text = request.form.get('task', '').strip()
    priority = request.form.get('priority', 'Medium')
    category = request.form.get('category', 'General').strip() or 'General'
    due_date = request.form.get('due_date', '').strip() or None

    if task_text:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO tasks (task, completed, priority, category, due_date) VALUES (?, 0, ?, ?, ?)',
            (task_text, priority, category, due_date),
        )
        conn.commit()
        conn.close()
        flash('Task added successfully.')
    else:
        flash('Please enter a task before adding.', 'warning')

    return redirect(url_for('home'))


@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    task_text = request.form.get('task', '').strip()
    priority = request.form.get('priority', 'Medium')
    category = request.form.get('category', 'General').strip() or 'General'
    due_date = request.form.get('due_date', '').strip() or None

    if task_text:
        conn = get_db_connection()
        conn.execute(
            'UPDATE tasks SET task = ?, priority = ?, category = ?, due_date = ? WHERE id = ?',
            (task_text, priority, category, due_date, id),
        )
        conn.commit()
        conn.close()
        flash('Task updated successfully.')
    else:
        flash('Task text cannot be empty.', 'warning')

    return redirect(url_for('home'))


@app.route('/toggle/<int:id>')
def toggle(id):
    conn = get_db_connection()
    task = conn.execute('SELECT completed FROM tasks WHERE id = ?', (id,)).fetchone()
    if task is not None:
        new_state = 0 if task['completed'] else 1
        conn.execute('UPDATE tasks SET completed = ? WHERE id = ?', (new_state, id))
        conn.commit()
        flash('Task marked complete.' if new_state else 'Task marked incomplete.')
    conn.close()
    return redirect(url_for('home'))


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Task deleted successfully.')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
