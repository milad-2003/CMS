from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":

    # |==================================================================================================|
    # |We use the following code to create the database and add the csv records to it by running it once:|
    # |==================================================================================================|

    # with app.app_context():
    #     db.create_all()


    # import pandas as pd
    # import sqlite3

    # connection = sqlite3.connect("instance/data.db")

    # images = pd.read_csv("csv/images.csv")
    # articles = pd.read_csv("csv/articles.csv")

    # images.to_sql('images', connection, index=False)
    # articles.to_sql('articles', connection, index=False)

    # connection.close()

    app.run(debug=True)
