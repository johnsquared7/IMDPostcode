from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Load the IMD data from CSV
imd_data = pd.read_csv('final.csv')

# Convert postcodes to lowercase for case-insensitive search
imd_data['postcode'] = imd_data['postcode'].str.lower()

@app.route('/imd', methods=['GET'])
def get_imd_data():
    # Get the postcode from the query parameter
    postcode = request.args.get('postcode', '').lower()

    # Find the row matching the postcode
    result = imd_data[imd_data['postcode'] == postcode]

    if result.empty:
        return jsonify({'error': 'Postcode not found'}), 404

    # Convert the result to a dictionary
    imd_info = result.to_dict(orient='records')[0]

    # Return the result as JSON
    return jsonify(imd_info)

if __name__ == '__main__':
    app.run(debug=True)
