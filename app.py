"""
Routes and views for the flask application.
"""
"""
The flask application package.
"""

from flask import Flask, render_template, redirect, url_for, request
import gunicorn

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """Renders the home page."""
    return render_template('s.html')


@app.route("/Salesenquiry", methods=['GET', 'POST'])
def Salesenquiry():
  return render_template("Salesenquiry.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run()
