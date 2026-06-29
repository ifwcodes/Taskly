# Productivity Dashboard

A small Flask-based task tracker with a responsive dashboard, task filters, and theme controls.

## Project structure

- `app.py` - Flask application and SQLite database logic.
- `templates/home.html` - Main dashboard UI template.
- `static/app.js` - Front-end interactions, theme toggle, and UI behavior.
- `static/style.css` - Dashboard styling and layout.

## Setup and run

1. Install dependencies:

```bash
pip install flask
```

2. Run the app:

```bash
python app.py
```

3. Open the browser:

```text
http://127.0.0.1:5000/
```

## Features

- Add, edit, delete, and complete tasks.
- Filter tasks by status, priority, category, and search.
- Persistent task storage using SQLite.
- Dark/light theme toggle.

## Notes

- The app creates its SQLite database automatically in `static/todo.db`.
- Change `app.secret_key` in `app.py` before deploying.
