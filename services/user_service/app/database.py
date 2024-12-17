from arango import ArangoClient
from .config import Settings
import logging

settings = Settings()

def init_db():
    client = ArangoClient(hosts=settings.ARANGO_URL)
    
    # Connect to system database
    sys_db = client.db('_system', username='root', password=settings.ARANGO_ROOT_PASSWORD)
    
    # Create database if it doesn't exist
    if not sys_db.has_database(settings.ARANGO_DB):
        sys_db.create_database(settings.ARANGO_DB)
    
    # Connect to app database
    db = client.db(settings.ARANGO_DB, username='root', password=settings.ARANGO_ROOT_PASSWORD)
    
    # Create collections if they don't exist
    if not db.has_collection('users'):
        users = db.create_collection('users')
        users.add_hash_index(fields=['email'], unique=True)
    
    return db

def get_db():
    try:
        client = ArangoClient(hosts=settings.ARANGO_URL)
        db = client.db(settings.ARANGO_DB, username='root', password=settings.ARANGO_ROOT_PASSWORD)
        return db
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        raise
