from flask import Flask, request, jsonify
from flask_cors import CORS
from movie_assistant import get_cinema_info

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    typeFilter = request.args.get('typeFilter')
    genreFilter = request.args.get('genreFilter')
    quantityFilter = request.args.get('quantityFilter')

    
    response = get_cinema_info(typeFilter, genreFilter, quantityFilter)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
