"""
Routes and views for the flask application.
"""
"""
The flask application package.
"""

from flask import Flask, render_template, redirect, url_for, request, session
import gunicorn

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['admin'] = request.form['username']
            return render_template('cafe-home.html')
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run()
