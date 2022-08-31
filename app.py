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
def home():
    """Renders the home page."""
    return render_template('s.html')

@app.route('/home', methods=['GET', 'POST'])
def form_example():
    if 'admin' not in session:
        return render_template('login.html')
    else:
        return render_template('cafe-home.html')


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
            session['admin'] = request.form['username']
            return redirect(url_for('form_example'))
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run()
