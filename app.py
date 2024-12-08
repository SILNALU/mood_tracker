from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db, init_db, init_app
from auth import auth_bp
from mood import mood_bp

def create_app():
    # Create Flask application
    app = Flask(__name__)
    
    # Configure application
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
    app.config['PERMANENT_SESSION_LIFETIME'] = 604800  # 7 days in seconds
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(mood_bp)
    
    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    @app.route('/')
    def index():
        if 'user_id' not in session:
            return redirect('/login')
        return redirect('/mood')
    
    # Initialize db
    with app.app_context():
        init_db()
    
    return app

# Initialize the application
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)