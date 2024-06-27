import csv
import os


def is_database_empty():
    database_path = os.path.join(os.path.dirname(__file__), 'instance', 'data.db')
    if not os.path.exists(database_path):
        return True
    else:
        return False 


photographers_data = []
images_data = []
def read_csv_images(filename):
    seen_photographer_codes = set()
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            image_data = {
                'image_path': row['image_path'],
                'title': row['title'],
                'tags': row['tags'],
                'description': row['description'],
                'category': row['category'],
                'photographer_code': row['photographer_code']
            }
            images_data.append(image_data)

            photographer_code = row['photographer_code']
            if photographer_code not in seen_photographer_codes:
                photographer_data = {
                'photographer_code': row['photographer_code'],
                'photographer_name': row['photographer_name'],
                'photographer_email': row['photographer_email']
            }
                photographers_data.append(photographer_data)
                seen_photographer_codes.add(photographer_code)


writers_data = []
articles_data = []
def read_csv_articles(filename):
    seen_writer_codes = set()
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            article_data = {
                'content': row['content'],
                'keywords': row['keywords'],
                'title': row['title'],
                'category': row['category'],
                'writer_code': row['writer_code']
            }
            articles_data.append(article_data)

            writer_code = row['writer_code']
            if writer_code not in seen_writer_codes:
                writer_data = {
                    'writer_code': writer_code,
                    'writer_name': row['writer_name'],
                    'writer_email': row['writer_email']
                }
                writers_data.append(writer_data)
                seen_writer_codes.add(writer_code)



def import_data(app, db, Photographer, Writer, Image, Article):
    read_csv_images("csv/images.csv")
    read_csv_articles("csv/articles.csv")
    
    with app.app_context():
        db.create_all()
        with db.session.begin():
            db.session.bulk_insert_mappings(Photographer, photographers_data)
            db.session.bulk_insert_mappings(Writer, writers_data)
            db.session.bulk_insert_mappings(Image, images_data)
            db.session.bulk_insert_mappings(Article, articles_data)
