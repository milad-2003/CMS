import pandas as pd
import sqlite3


def is_database_empty():
    import os


    database_path = os.path.join(os.path.dirname(__file__), 'instance', 'data.db')
    if not os.path.exists(database_path):
        return True
    else:
        return False

 
def import_data(app, db):

    # Create the database
    with app.app_context():
        db.create_all()

    # Create a connection
    connection = sqlite3.connect("instance/data.db")

    # Read the csv files using pandas
    images = pd.read_csv("csv/images.csv")
    articles = pd.read_csv("csv/articles.csv")

    # Adding the records of csv files into the database
    images.to_sql('images', connection, index=False)
    articles.to_sql('articles', connection, index=False)

    # Getting the information of photographers and writers
    photographers = connection.execute("SELECT DISTINCT photographer_code, photographer_name, photographer_email FROM images")
    writers = connection.execute("SELECT DISTINCT writer_code, writer_name, writer_email FROM articles")

    # Creating a table for photographers and writers
    connection.execute("""CREATE TABLE photographers (
                    photographer_code VARCHAR(10),
                    photographer_name VARCHAR(255),
                    photographer_email VARCHAR(255),
                    PRIMARY KEY(photographer_code)
                    )""")
    connection.execute("""CREATE TABLE writers (
                    writer_code VARCHAR(10),
                    writer_name VARCHAR(255),
                    writer_email VARCHAR(255),
                    PRIMARY KEY(writer_code)
                    )""")

    # Adding the information of photographers and writers into their tables
    for photographer in photographers:
        connection.execute(f"INSERT INTO photographers VALUES {photographer}")
    for writer in writers:
        connection.execute(f"INSERT INTO writers VALUES {writer}")

    # Removing the extra columns of the images and articles table
    connection.execute("""CREATE TABLE new_images (
                    i_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path VARCHAR(255),
                    title VARCHAR(255),
                    tags VARCHAR(255),
                    description VARCHAR(255),
                    category VARCHAR(255),
                    photographer_code VARCHAR(10),
                    FOREIGN KEY(photographer_code) REFERENCES photographers(photographer_code)
                    )""")
    connection.execute("""CREATE TABLE new_articles (
                    a_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content VARCHAR(255),
                    keywords VARCHAR(255),
                    title VARCHAR(255),
                    category VARCHAR(255),
                    writer_code VARCHAR(10),
                    FOREIGN KEY(writer_code) REFERENCES writers(writer_code)
                    )""")
    connection.execute("""INSERT INTO new_images (image_path, title, tags, description, category, photographer_code)
                    SELECT image_path, title, tags, description, category, photographer_code
                    FROM images
                    """)
    connection.execute("""INSERT INTO new_articles (content, keywords, title, category, writer_code)
                    SELECT content, keywords, title, category, writer_code
                    FROM articles
                    """)
    connection.execute("DROP TABLE images")
    connection.execute("DROP TABLE articles")
    connection.execute("ALTER TABLE new_images RENAME TO images")
    connection.execute("ALTER TABLE new_articles RENAME TO articles")

    # Commit and close the connection
    connection.commit()
    connection.close()
        
