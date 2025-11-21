from flask import Flask
from flask_cors import CORS

from controllers.sportman import sportman



app = Flask(__name__)

CORS(app)

app.register_blueprint(sportman)
@app.route('/')
def home():
    return "ruta principal"

if __name__=='__main__':
    app.run(debug=True)