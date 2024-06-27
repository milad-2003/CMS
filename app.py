from flask import render_template
from config import app, db
from import_data import *
from models import *

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
        import_data(app, db, Photographer, Writer, Image, Article)
    
    app.run(debug=True)

