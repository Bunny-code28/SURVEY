import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
from flask import jsonify
from collections import Counter
from pymongo import MongoClient
from PIL import Image



logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = os.urandom(24)  # a strong, random secret key
app.config['SESSION_COOKIE_SECURE'] = True  
app.config['SESSION_COOKIE_HTTPONLY'] = True  
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  

DB_TYPE = os.environ.get('DB_TYPE', 'sqlite')  # 'sqlite' or 'mongodb'

if DB_TYPE == 'mongodb':
    from pymongo import MongoClient
    from bson import ObjectId
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['survey_system']
        users = db['users']
        surveys = db['surveys']
        
        # Create a unique index on email for users collection
        users.create_index('email', unique=True)
        
        # Create an index on email for surveys collection
        surveys.create_index('email')
    except Exception as e:
        logging.error(f"MongoDB setup failed. Error: {str(e)}")
        DB_TYPE = 'sqlite'

    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['survey_system']
        users = db['users']
        surveys = db['surveys']
        print("MongoDB connection successful!")
    except Exception as e:
        print(f"MongoDB connection failed: {str(e)}")

if DB_TYPE == 'sqlite':
    DB_NAME = 'survey_system.db'
    
    def get_db():
        db = sqlite3.connect(DB_NAME)
        db.row_factory = sqlite3.Row
        return db
    
    def init_sqlite_db():
        with get_db() as db:
            # Create users table
            db.execute('''CREATE TABLE IF NOT EXISTS users
                        (email TEXT PRIMARY KEY,
                        user_id TEXT, 
                        password TEXT, 
                        name TEXT)''')
            
            # Create surveys table
            db.execute('''CREATE TABLE IF NOT EXISTS surveys
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT, 
                        topic TEXT, 
                        answers TEXT, 
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (email) REFERENCES users(email))''')
            
            # Check if email column exists 
            cursor = db.execute("PRAGMA table_info(surveys)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Add email column 
            if 'email' not in columns:
                db.execute('ALTER TABLE surveys ADD COLUMN email TEXT')
                db.execute('CREATE INDEX IF NOT EXISTS idx_surveys_email ON surveys(email)')
                logging.info("Added 'email' column to 'surveys' table")
            
            db.commit()
    
    # Call init_sqlite_db() 
    init_sqlite_db()

# Survey topics and questions
SURVEY_TOPICS = ['sports', 'arts', 'literature']
SURVEY_QUESTIONS = {
    'sports': [
        "How often do you engage in sports activities?",
        "What's your favorite sport?",
        "Do you prefer team sports or individual sports?",
        "How often do you watch sports on TV?",
        "Have you ever participated in a sports competition?"
    ],
    'arts': [
        "How often do you engage in artistic activities?",
        "What's your favorite art form?",
        "Do you prefer creating art or appreciating others' work?",
        "How often do you visit art galleries or museums?",
        "Have you ever sold a piece of art you created?"
    ],
    'literature': [
        "How often do you read books?",
        "What's your favorite genre of literature?",
        "Do you prefer physical books or e-books?",
        "How often do you visit libraries or bookstores?",
        "Have you ever written a story or poem?"
    ]
}

def resize_image(image_path, size=(800, 400)):
    """Resize an image to the specified size while maintaining aspect ratio"""
    try:
        with Image.open(image_path) as img:
            # Convert image to RGB if it's not
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate aspect ratio
            aspect_ratio = img.size[0] / img.size[1]
            target_ratio = size[0] / size[1]
            
            if aspect_ratio > target_ratio:
                # Image is wider than target
                new_width = size[0]
                new_height = int(new_width / aspect_ratio)
            else:
                # Image is taller than target
                new_height = size[1]
                new_width = int(new_height * aspect_ratio)
            
            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create new image with target size and paste resized image centered
            new_img = Image.new('RGB', size, (0, 0, 0))
            paste_x = (size[0] - new_width) // 2
            paste_y = (size[1] - new_height) // 2
            new_img.paste(img, (paste_x, paste_y))
            
            # Save the processed image
            output_path = image_path.rsplit('.', 1)[0] + '_processed.jpg'
            new_img.save(output_path, 'JPEG', quality=85)
            return output_path
    except Exception as e:
        print(f"Error processing image {image_path}: {str(e)}")
        return None

@app.before_first_request
def process_carousel_images():
    image_dir = os.path.join(app.static_folder, 'images')
    carousel_images = ['survey1.png', 'survey2.png', 'survey3.png']
    
    for image_name in carousel_images:
        image_path = os.path.join(image_dir, image_name)
        if os.path.exists(image_path):
            resize_image(image_path)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    return render_template('login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if DB_TYPE == 'mongodb':
            user = users.find_one({'email': email})
        else:
            with get_db() as db:
                user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session.clear()  # Clear any existing session data
            session['email'] = email
            session['logged_in'] = True
            flash('Logged in successfully', 'success')
            return redirect(url_for('topic_selection'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            logging.warning(f"Failed login attempt for email: {email}")
            return render_template('login.html'), 401  # Return 401 Unauthorized status
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        
        # Check if email already exists
        if DB_TYPE == 'mongodb':
            existing_user = users.find_one({'email': email})
        else:
            with get_db() as db:
                existing_user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if existing_user:
            flash('Email already registered. Please login or use a different email.', 'error')
            return render_template('register.html'), 400  # Bad Request
        
        hashed_password = generate_password_hash(password)
        
        if DB_TYPE == 'mongodb':
            users.insert_one({'email': email, 'user_id': user_id, 'password': hashed_password, 'name': name})
        else:
            with get_db() as db:
                db.execute('INSERT INTO users (email, user_id, password, name) VALUES (?, ?, ?, ?)',
                           (email, user_id, hashed_password, name))
        
        flash('Registered successfully. Please login with your new account.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear all session 
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/topic_selection')
@login_required
def topic_selection():
    return render_template('topic_selection.html', topics=SURVEY_TOPICS)

@app.route('/survey/<topic>')
@login_required
def survey(topic):
    if topic in SURVEY_QUESTIONS:
        dict_topic = topic
    elif topic.endswith('s') and topic[:-1] in SURVEY_QUESTIONS:
        dict_topic = topic[:-1]
    elif topic + 's' in SURVEY_QUESTIONS:
        dict_topic = topic + 's'
    else:
        flash('Invalid survey topic', 'error')
        return redirect(url_for('topic_selection'))
    
    questions = SURVEY_QUESTIONS[dict_topic]
    return render_template(f'{dict_topic}_survey.html', topic=dict_topic, questions=questions)

@app.route('/submit_survey', methods=['POST'])
@login_required
def submit_survey():
    try:
        email = session['email']
        topic = request.form['topic']
        logging.info(f"Received survey submission for email: {email}, topic: {topic}")
        
        # Handle both singular and plural forms of the topic
        if topic in SURVEY_QUESTIONS:
            dict_topic = topic
        elif topic.endswith('s') and topic[:-1] in SURVEY_QUESTIONS:
            dict_topic = topic[:-1]
        elif topic + 's' in SURVEY_QUESTIONS:
            dict_topic = topic + 's'
        else:
            logging.warning(f"Invalid survey topic: {topic}")
            flash('Invalid survey topic', 'error')
            return redirect(url_for('topic_selection'))
        
        logging.info(f"Processed topic: {dict_topic}")
        
        answers = {
            f'q{i+1}': request.form[f'q{i+1}']
            for i in range(len(SURVEY_QUESTIONS[dict_topic]))
        }
        logging.info(f"Collected answers: {answers}")
        
        if DB_TYPE == 'mongodb':
            surveys.insert_one({'email': email, 'topic': dict_topic, 'answers': answers})
            logging.info("Survey inserted into MongoDB")
        else:
            with get_db() as db:
                db.execute('INSERT INTO surveys (email, topic, answers) VALUES (?, ?, ?)',
                           (email, dict_topic, str(answers)))
            logging.info("Survey inserted into SQLite")
        
        flash('Survey submitted successfully', 'success')
        logging.info(f"Survey submitted successfully for email: {email}, topic: {dict_topic}")
        return redirect(url_for('analysis'))
    except Exception as e:
        logging.error(f"Error in submit_survey function: {str(e)}", exc_info=True)
        flash('An error occurred while submitting the survey. Please try again.', 'error')
        return redirect(url_for('topic_selection'))

@app.route('/analysis')
@login_required
def analysis():
    try:
        logging.info("Entered analysis function")
        if DB_TYPE == 'mongodb':
            all_surveys = list(surveys.find({}, {'_id': 0, 'email': 0}))
        else:
            with get_db() as db:
                all_surveys = db.execute('SELECT topic, answers FROM surveys').fetchall()
        
        logging.info(f"Retrieved {len(all_surveys)} surveys from {'MongoDB' if DB_TYPE == 'mongodb' else 'SQLite'}")
        
        analysis_data = {}
        for survey in all_surveys:
            topic = survey['topic']
            answers = eval(survey['answers']) if DB_TYPE == 'sqlite' else survey['answers']
            
            if topic not in analysis_data:
                analysis_data[topic] = {f'q{i+1}': Counter() for i in range(len(SURVEY_QUESTIONS[topic]))}
            
            for q, a in answers.items():
                analysis_data[topic][q][a] += 1
        
        logging.info(f"Processed analysis data for topics: {list(analysis_data.keys())}")
        logging.info(f"Analysis data: {analysis_data}")
        logging.info(f"Survey questions: {SURVEY_QUESTIONS}")
        
        return render_template('analysis.html', analysis_data=analysis_data, survey_questions=SURVEY_QUESTIONS)
    except Exception as e:
        logging.error(f"Error in analysis function: {str(e)}", exc_info=True)
        flash('An error occurred while processing the analysis. Please try again.', 'error')
        return redirect(url_for('topic_selection'))
    
@app.route('/thank_you')
@login_required
def thank_you():
    return render_template('thank_you.html')

@app.route('/user_surveys')
@login_required
def user_surveys():
    email = session['email']
    
    if DB_TYPE == 'mongodb':
        user_surveys = list(surveys.find({'email': email}))
    else:
        with get_db() as db:
            user_surveys = db.execute('SELECT * FROM surveys WHERE email = ?', (email,)).fetchall()
    
    return render_template('user_surveys.html', surveys=user_surveys)

@app.route('/view_database')
def view_database():
    if DB_TYPE == 'sqlite':
        with get_db() as db:
            #  all table names
            cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            database_content = {}
            
            for table in tables:
                table_name = table['name']
                cursor = db.execute(f"SELECT * FROM {table_name}")
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                
                database_content[table_name] = {
                    'columns': columns,
                    'data': [dict(row) for row in rows]
                }
            
            return jsonify(database_content)
    else:
        return jsonify({'error': 'This route is only available for SQLite databases'})

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    init_sqlite_db()  
    app.run(debug=True)