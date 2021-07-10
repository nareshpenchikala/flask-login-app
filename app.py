"""
Routes and views for the flask application.
"""
"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
from flask import render_template,url_for
import gunicorn

@app.route('/', methods=['GET', 'POST'])
def home():
    """Renders the home page."""
    return render_template('s.html')


@app.route("/Salesenquiry", methods=['GET', 'POST'])
def Salesenquiry():
  return render_template("Salesenquiry.html")


if __name__ == "__main__":
    app.run()
