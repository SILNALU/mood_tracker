# TITLE: MOOD TRACKER
#### Video Demo:  <https://youtu.be/uuYBlEOQftI>
#### Description:
Introduction:
The Mood Tracker is a web-based application designed to help users monitor their emotional well-being while providing personalized scientific insights and actionable challenges. This unique approach combines emotional awareness with neuroscience and practical psychology to create a holistic wellness tool.

-Key Features-
Mood Tracking System:
Users can select three moods from a curated list of emotions
Tracks both positive (Happy, Excited, Peaceful) and challenging (Stressed, Anxious, Tired) emotional states
Daily tracking capability with historical view

Intelligent Response System:
Analyzes mood combinations to determine overall emotional state
Provides three types of personalized responses:
Motivational messages
Neuroscience explanations
Daily challenges

Scientific Basis:
Incorporates neuropsychological insights
Links emotional states to brain function
Provides science-based strategies for emotional regulation

User Experience:
Clean, intuitive interface
Secure user authentication
Personal mood history tracking
Boho-inspired design for a calming user experience

Technical Implementation:
Built using Python Flask framework
SQLite database for data persistence
Secure user authentication system
Responsive front-end design
Session management for user data

Benefits:
Emotional Awareness: Helps users identify and track their emotional patterns
Educational Value: Teaches users about the neuroscience behind their emotions
Actionable Insights: Provides practical challenges based on emotional state
Progress Tracking: Allows users to monitor their emotional journey over time

Breakdown of each file in the project:
app.py
This is like the main control center
Starts up your website and tells everything where to go
Handles basic setup stuff like sessions and security

auth.py
Deals with logging in and signing up
Makes sure users have good passwords
Keeps track of who's logged in

mood.py
The heart of your app
Handles all the mood tracking stuff
Contains the cool responses about brain science and challenges

database.py
Manages your SQLite database
Like a filing cabinet for all your users' data
Keeps track of everyone's moods and responses

init_db.py
Sets up your database for the first time
Like setting up that filing cabinet before you use it

mood_responses.py
Contains all those motivational messages
Stores the brain facts and challenges
Like a big book of responses

schema.sql
The blueprint for your database
Tells the database how to organize everything

Templates folder:
base.html: The basic layout all pages use
auth/: Login and register page templates
mood/: Templates for showing moods and responses

Static/css folder:
style.css: Makes everything look pretty
All your boho styling lives here


mood_tracker.db
The actual database file
Where all the user data and responses are stored