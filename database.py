from flask import current_app, g
import sqlite3
from mood_responses_data import mood_responses_data

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('mood_tracker.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    # Create tables if they don't exist
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    # Check if mood_responses table is empty
    responses_count = db.execute('SELECT COUNT(*) as count FROM mood_responses').fetchone()['count']
    
    if responses_count == 0:
        try:
            # Iterate through each mood state and its responses
            for mood_state, responses_list in mood_responses_data.items():
                # Insert each set of responses
                for response_set in responses_list:
                    # Add each type of response
                    for response_type in ['motivation', 'neuroscience', 'challenge']:
                        db.execute('''
                            INSERT INTO mood_responses (mood_state, response_type, content)
                            VALUES (?, ?, ?)
                        ''', (mood_state, response_type, response_set[response_type]))
            
            db.commit()
            print("Database initialized with all responses!")
            
            # Verify the count of inserted responses
            counts = db.execute('''
                SELECT mood_state, response_type, COUNT(*) as count 
                FROM mood_responses 
                GROUP BY mood_state, response_type
            ''').fetchall()
            
            for row in counts:
                print(f"{row['mood_state']} - {row['response_type']}: {row['count']} responses")
            
        except Exception as e:
            print(f"Error seeding database: {e}")
            db.rollback()
    else:
        print("Database already contains responses.")

def init_app(app):
    app.teardown_appcontext(close_db)