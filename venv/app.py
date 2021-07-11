from typing import final
from flask import Flask, json, jsonify, request
from flask.templating import render_template
import glob
import csv
import pandas as pd

app = Flask(__name__)

# use "venv\Scripts\activate" before running

# index page route


@app.route("/")
def index():
    return render_template('index.html')

# API to fetch the files


@app.route('/getFiles')
def getFiles():

    formated_files = []

    # Retrieve csv files present inside the Files folder
    try:
        files = (glob.glob("venv\Files\*.csv"))
        for file in files:
            formated_files.append(file.replace('venv\\Files\\', ''))

        print(formated_files)

    except:
        return 'NO Files Found', 400

    # Returning list of files into JSON format
    return jsonify(formated_files)

# API to fetch the columns from a file (Since columns are same for all files)


@app.route('/getColumns')
def getColumns():

    files = (glob.glob("venv\Files\*.csv"))

    # Storing the column titles from the first file of the list
    with open(files[0], "r") as f:
        reader = csv.reader(f)
        column_titles = next(reader)

    # Returning list of column titles into JSON format
    return jsonify(column_titles)

# API to post the request with the file name and the selected columns and receive the response


@app.route('/getData', methods=['POST'])
def getData():
    if request.method == 'POST':
        posted_data = request.get_json()

        if posted_data['filename'] == 'select option':
            return 'bad request!', 400
        # Feeding the filename and the selected columns
        try:

            filename = 'venv\\Files\\{}'.format(posted_data['filename'])

            columns = posted_data['columns']
            if not columns:
                return 'bad request!', 400

            with open(filename) as file:

                # Reading CSV file using pandas and filtering only the selected columns
                data = pd.read_csv(file, usecols=columns)

                # Converting DataFrame to dictionary
                results = data.to_dict('list')
                print(results)
        except FileNotFoundError:
            return 'bad request!', 400
        return results


@app.errorhandler(404)
def not_found(e):
    print("Page not found")
