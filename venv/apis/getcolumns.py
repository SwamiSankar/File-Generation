import glob
from flask import Blueprint,jsonify
import csv

getcolumns = Blueprint('getcolumns', __name__,
                     static_folder='static', template_folder='templates')

# API to fetch the columns from a file (Since columns are same for all files)


@getcolumns.route('/getColumns')
def getColumns():

    files = (glob.glob("venv\Files\*.csv"))

    # Storing the column titles from the first file of the list
    with open(files[0], "r") as f:
        reader = csv.reader(f)
        column_titles = next(reader)

    # Returning list of column titles into JSON format
    return jsonify(column_titles)
