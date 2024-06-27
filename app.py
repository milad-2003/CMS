from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from import_data import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/images')
def images():
    return render_template('images.html')


@app.route('/articles')
def articles():
    return render_template('articles.html')


@app.route('/writer-photographer')
def writer_photographer():
    return render_template('writer-photographer.html')


if __name__ == "__main__":
    if is_database_empty():
        import_data(app, db)
    
    app.run(debug=True)

