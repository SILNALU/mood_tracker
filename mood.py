from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db
from auth import login_required
import random
from datetime import date

mood_bp = Blueprint('mood', __name__)

MOODS = [
    'Happy', 'Excited', 'Peaceful', 'Grateful', 'Energetic',
    'Tired', 'Anxious', 'Stressed', 'Sad', 'Motivated'
]

def analyze_mood_state(selected_moods):
    positive_moods = set(['Happy', 'Excited', 'Peaceful', 'Grateful', 'Motivated', 'Energetic'])
    positive_count = sum(1 for mood in selected_moods if mood in positive_moods)
    
    if positive_count >= 2:
        return 'Mostly_Positive'
    elif positive_count <= 1:
        return 'Mostly_Challenging'
    return 'Mixed'

@mood_bp.route('/mood', methods=['GET', 'POST'])
@login_required
def select_mood():
    if request.method == 'POST':
        selected_moods = request.form.getlist('moods')
        print(f"Selected moods: {selected_moods}")
        
        if len(selected_moods) != 3:
            flash("Please select exactly 3 moods")
            return render_template('mood/mood.html', moods=MOODS)
        
        try:
            mood_state = analyze_mood_state(selected_moods)
            db = get_db()

            # Get one random response for each type
            motivation = db.execute('''
                SELECT content FROM mood_responses 
                WHERE mood_state = ? AND response_type = 'motivation'
                ORDER BY RANDOM() LIMIT 1
            ''', (mood_state,)).fetchone()

            neuroscience = db.execute('''
                SELECT content FROM mood_responses 
                WHERE mood_state = ? AND response_type = 'neuroscience'
                ORDER BY RANDOM() LIMIT 1
            ''', (mood_state,)).fetchone()

            challenge = db.execute('''
                SELECT content FROM mood_responses 
                WHERE mood_state = ? AND response_type = 'challenge'
                ORDER BY RANDOM() LIMIT 1
            ''', (mood_state,)).fetchone()

            if not all([motivation, neuroscience, challenge]):
                flash("No responses available for this mood state.")
                return render_template('mood/mood.html', moods=MOODS)

            # Store mood entry
            db.execute(
                'INSERT INTO mood_entries (user_id, date, mood1, mood2, mood3) VALUES (?, ?, ?, ?, ?)',
                (session['user_id'], date.today().isoformat(), *selected_moods)
            )
            db.commit()
            
            return render_template('mood/response.html', 
                                selected_moods=selected_moods,
                                motivation=motivation['content'],
                                neuroscience=neuroscience['content'],
                                challenge=challenge['content'])

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            flash(f"An error occurred: {str(e)}")
            return render_template('mood/mood.html', moods=MOODS)
    
    return render_template('mood/mood.html', moods=MOODS)

@mood_bp.route('/history')
@login_required
def history():
    db = get_db()
    entries = db.execute(
        '''SELECT date, mood1, mood2, mood3 
           FROM mood_entries 
           WHERE user_id = ? 
           ORDER BY date DESC''', 
        (session['user_id'],)
    ).fetchall()
    
    return render_template('mood/history.html', entries=entries)