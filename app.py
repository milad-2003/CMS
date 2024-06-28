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


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    selected_category = request.form.get('category', 'All')
    categories = db.session.query(Article.category.distinct()).all()
    categories = [category[0] for category in categories]  # Extract category names from tuples

    if selected_category == 'All':
        articles = Article.query.all()
    else:
        articles = Article.query.filter_by(category=selected_category).all()

    return render_template('articles.html', articles=articles, categories=categories, selected_category=selected_category)


@app.route('/creators')
def creators():
    photographers = Photographer.query.all()
    writers = Writer.query.all()
    return render_template('creators.html', photographers=photographers, writers=writers)


@app.route('/photographer_detail/<code>')
def photographer_detail(code):
    photographer = Photographer.query.filter_by(photographer_code=code).first()
    images = Image.query.filter_by(photographer_code=code).all()
    return render_template('photographer_detail.html', photographer=photographer, images=images)


@app.route('/writer_detail/<code>')
def writer_detail(code):
    writer = Writer.query.filter_by(writer_code=code).first()
    articles = Article.query.filter_by(writer_code=code).all()
    return render_template('writer_detail.html', writer=writer, articles=articles)


if __name__ == "__main__":
    if is_database_empty():
        import_data(app, db, Photographer, Writer, Image, Article)
    
    app.run(debug=True)

