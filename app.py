from flask import render_template, request
from config import app, db
from import_data import *
from models import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/images', methods=['GET', 'POST'])
def images():
    selected_category = request.form.get('category', 'All')
    categories = db.session.query(Image.category.distinct()).all()
    categories = [category[0] for category in categories]

    if selected_category == 'All':
        images = Image.query.all()
    else:
        images = Image.query.filter_by(category=selected_category).all()

    return render_template('images.html', images=images, categories=categories, selected_category=selected_category)



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

