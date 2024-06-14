from sqlalchemy import create_engine, exists
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("sqlite:///db.sqlite3")
"""
    sqlite:///:memory: (or, sqlite://)
    sqlite:///relative/path/to/file.db
    sqlite:////absolute/path/to/file.db
"""

connection = engine.connect()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# class Connector:
#     connection = engine.connect()
#     Session = sessionmaker()
#     Session.configure(bind=engine)
#     session = Session()

#     def __init__(self) -> None:
#         pass

#     def __del__(self):
#         self.connection.close()
