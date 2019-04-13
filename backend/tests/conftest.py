from models import define_database

db = define_database(provider='sqlite', filename='test_db.sqlite', create_db=True)
