from flask import Flask
from flask.templating import render_template
from apis.getfiles import getfiles
from apis.getcolumns import getcolumns
from apis.getdata import getdata

app = Flask(__name__)

# Registering the blueprint of the API files

app.register_blueprint(getfiles)
app.register_blueprint(getcolumns)
app.register_blueprint(getdata)

# use "venv\Scripts\activate" before running


# index page route


@app.route("/")
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(e):
    print("Page not found")


if __name__ == '__main__':
    app.run()
