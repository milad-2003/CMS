from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from import_data import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    if is_database_empty():
        import_data(app, db)
    
    app.run(debug=True)

