from flask import Blueprint, request
import pandas as pd

getdata = Blueprint('getdata', __name__,
                    static_folder='static', template_folder='templates')

# API to post the request with the file name and the selected columns and receive the response


@getdata.route('/getData', methods=['POST'])
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

        except FileNotFoundError:
            return 'bad request!', 400
        return results
