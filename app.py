from flask import Flask
from flask_cors import CORS

from controllers.sportman import sportman
from controllers.assessment import evaluation




app = Flask(__name__)

CORS(app)

app.register_blueprint(sportman)
app.register_blueprint(evaluation)

@app.route('/')
def home():
    return "ruta principal"

if __name__=='__main__':
    app.run(debug=True)