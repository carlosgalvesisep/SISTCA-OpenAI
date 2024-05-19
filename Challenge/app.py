from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from movie_assistant import get_cinema_info

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply_filters', methods=['GET'])
def submit():
    type_filter = request.args.get('type')
    genre_filter = request.args.get('genre')
    quantity_filter = request.args.get('quantity')
    
    print(f"{type_filter}, {genre_filter}, {quantity_filter}")
    response =  get_cinema_info(type_filter, genre_filter, quantity_filter)
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
