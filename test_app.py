import pytest
from app import app, init_db, insert_sample_data
import sqlite3

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
            insert_sample_data()
        yield client

def test_init_db(client):
    # Test if the database initializes correctly
    conn = sqlite3.connect('spam_detector.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='spam_messages'")
    assert c.fetchone() is not None
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='spam_words'")
    assert c.fetchone() is not None
    conn.close()

def test_insert_sample_data(client):
    # Test if sample data is inserted correctly
    conn = sqlite3.connect('spam_detector.db')
    c = conn.cursor()
    c.execute("SELECT word FROM spam_words WHERE word='buy'")
    assert c.fetchone() is not None
    c.execute("SELECT word FROM spam_words WHERE word='discount'")
    assert c.fetchone() is not None
    c.execute("SELECT word FROM spam_words WHERE word='offer'")
    assert c.fetchone() is not None
    conn.close()

def test_spam_detection(client):
    # Test the spam detection functionality
    response = client.post('/', data={'message': 'This is a special offer just for you!'})
    assert b'spam' in response.data
