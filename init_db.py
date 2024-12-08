from database import get_db
from flask import current_app
from app import create_app

def init_database():
    app = create_app()
    with app.app_context():
        db = get_db()
        
        # Create the responses table and insert data
        try:
            db.execute('''
                INSERT INTO mood_responses (mood_state, response_type, content)
                VALUES 
                ('Mostly_Positive', 'motivation', 'Channel this energy - you''re unstoppable right now!'),
                ('Mostly_Positive', 'neuroscience', 'Your brain is releasing dopamine and serotonin!'),
                ('Mostly_Positive', 'challenge', 'Take on your biggest goal today!'),
                ('Mixed', 'motivation', 'Balance is your strength!'),
                ('Mixed', 'neuroscience', 'Your brain is processing multiple emotional states.'),
                ('Mixed', 'challenge', '20 minutes meditation followed by exercise.'),
                ('Mostly_Challenging', 'motivation', 'Every challenge builds strength.'),
                ('Mostly_Challenging', 'neuroscience', 'Your brain is building resilience pathways.'),
                ('Mostly_Challenging', 'challenge', 'Take a cold shower - reset your system.')
            ''')
            db.commit()
            print("Database initialized with responses!")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    init_database()