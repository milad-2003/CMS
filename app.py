from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from import_data import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Photographer(db.Model):
    __tablename__ = 'photographers'
    photographer_code = db.Column(db.String(10), primary_key=True)
    photographer_name = db.Column(db.String(255), nullable=False)
    photographer_email = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Photographer {self.photographer_name}>'


class Writer(db.Model):
    __tablename__ = 'writers'
    writer_code = db.Column(db.String(10), primary_key=True)
    writer_name = db.Column(db.String(255), nullable=False)
    writer_email = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Writer {self.writer_name}>'


class Image(db.Model):
    __tablename__ = 'images'
    i_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_path = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(255), nullable=False)
    photographer_code = db.Column(db.String(10), db.ForeignKey('photographers.photographer_code'), nullable=False)
    photographer = db.relationship('Photographer', backref=db.backref('images', lazy=True))

    def __repr__(self):
        return f'<Image {self.title}>'


class Article(db.Model):
    __tablename__ = 'articles'
    a_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    writer_code = db.Column(db.String(10), db.ForeignKey('writers.writer_code'), nullable=False)
    writer = db.relationship('Writer', backref=db.backref('articles', lazy=True))

    def __repr__(self):
        return f'<Article {self.title}>'


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

