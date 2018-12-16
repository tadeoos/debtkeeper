from models import db

db.bind(provider='sqlite', filename='debtkeeper_testing.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
