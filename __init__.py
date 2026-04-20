from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

import os

# Load environment variables from .env file
load_dotenv()

# Setup of key Flask object (app)
app = Flask(__name__)

# ========== Session 配置（关键！修复 Cookie 问题） ==========
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # 允许跨站发送 Cookie
app.config['SESSION_COOKIE_SECURE'] = False  # 本地开发用 False（HTTP），生产环境用 True（HTTPS）
app.config['SESSION_COOKIE_PATH'] = '/'

# Configure Flask Port
app.config['FLASK_PORT'] = int(os.environ.get('FLASK_PORT') or 8428)

# Configure Flask to handle JSON with UTF-8 encoding versus default ASCII
app.config['JSON_AS_ASCII'] = False

# Initialize Flask-Login object
login_manager = LoginManager()
login_manager.init_app(app)

# ========== CORS 配置（简化版） ==========
CORS(app,
     supports_credentials=True,  # 必须为 True
     origins=[
         'http://localhost:4000',
         'http://127.0.0.1:4000',
         'http://localhost:4500',
         'http://127.0.0.1:4500',
         'http://localhost:4599',
         'http://127.0.0.1:4599',
         'http://localhost:4600',
         'http://127.0.0.1:4600',
         'http://localhost:8428',
         'http://127.0.0.1:8428',
         'https://open-coding-society.github.io',
         'https://pages.opencodingsociety.com',
     ],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     methods=["GET", "POST", "PUT", "OPTIONS", "DELETE"],
     expose_headers=["Set-Cookie"])  # 暴露 Set-Cookie 头

# Admin Defaults
app.config['ADMIN_USER'] = os.environ.get('ADMIN_USER') or 'Admin Name'
app.config['ADMIN_UID'] = os.environ.get('ADMIN_UID') or 'admin'
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD') or os.environ.get('DEFAULT_PASSWORD') or 'password'
app.config['ADMIN_PFP'] = os.environ.get('ADMIN_PFP') or 'default.png'
# Teacher Defaults
app.config['TEACHER_USER'] = os.environ.get('TEACHER_USER') or 'Teacher Name'
app.config['TEACHER_UID'] = os.environ.get('TEACHER_UID') or 'teacher'
app.config['TEACHER_PASSWORD'] = os.environ.get('TEACHER_PASSWORD') or os.environ.get('DEFAULT_PASSWORD') or 'password'
app.config['TEACHER_PFP'] = os.environ.get('TEACHER_PFP') or 'default.png'
# Default User Defaults
app.config['USER_NAME'] = os.environ.get('USER_NAME') or 'User Name'
app.config['USER_UID'] = os.environ.get('USER_UID') or 'user'
app.config['USER_PASSWORD'] = os.environ.get('USER_PASSWORD') or os.environ.get('DEFAULT_PASSWORD') or 'password'
app.config['USER_PFP'] = os.environ.get('USER_PFP') or 'default.png'
# Defaults
app.config['DEFAULT_PASSWORD'] = os.environ.get('DEFAULT_PASSWORD') or 'password'
app.config['DEFAULT_PFP'] = os.environ.get('DEFAULT_PFP') or 'default.png'
# Convenience user
app.config['MY_NAME'] = os.environ.get('MY_NAME') or 'convenience'
app.config['MY_UID'] = os.environ.get('MY_UID') or 'convenience'
app.config['MY_PASSWORD'] = os.environ.get('MY_PASSWORD') or os.environ.get('DEFAULT_PASSWORD') or 'password'
app.config['MY_PFP'] = os.environ.get('MY_PFP') or 'default.png'
app.config['MY_ROLE'] = os.environ.get('MY_ROLE') or 'User'

# Browser settings (保留原有配置，但上面已经设置了 SECRET_KEY)
SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME') or 'sess_python_flask'
JWT_TOKEN_NAME = os.environ.get('JWT_TOKEN_NAME') or 'jwt_python_flask'
app.config['SESSION_COOKIE_NAME'] = SESSION_COOKIE_NAME
app.config['JWT_TOKEN_NAME'] = JWT_TOKEN_NAME

# Database settings
IS_PRODUCTION = os.environ.get('IS_PRODUCTION') or None
dbName = 'user_management'
DB_ENDPOINT = os.environ.get('DB_ENDPOINT') or None
DB_USERNAME = os.environ.get('DB_USERNAME') or None
DB_PASSWORD = os.environ.get('DB_PASSWORD') or None
if DB_ENDPOINT and DB_USERNAME and DB_PASSWORD:
   DB_PORT = '3306'
   DB_NAME = dbName
   dbString = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}:{DB_PORT}'
   dbURI = dbString + '/' + dbName
   backupURI = None
else:
   dbString = 'sqlite:///volumes/'
   dbURI = dbString + dbName + '.db'
   backupURI = dbString + dbName + '_bak.db'

app.config['DB_ENDPOINT'] = DB_ENDPOINT
app.config['DB_USERNAME'] = DB_USERNAME
app.config['DB_PASSWORD'] = DB_PASSWORD
app.config['SQLALCHEMY_DATABASE_NAME'] = dbName
app.config['SQLALCHEMY_DATABASE_STRING'] = dbString
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SQLALCHEMY_BACKUP_URI'] = backupURI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Image upload settings
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Data folder for shared file-based storage
app.config['DATA_FOLDER'] = os.path.join(app.instance_path, 'data')
os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)

# GITHUB settings
app.config['GITHUB_API_URL'] = 'https://api.github.com'
app.config['GITHUB_TOKEN'] = os.environ.get('GITHUB_TOKEN') or None
app.config['GITHUB_TARGET_TYPE'] = os.environ.get('GITHUB_TARGET_TYPE') or 'user'
app.config['GITHUB_TARGET_NAME'] = os.environ.get('GITHUB_TARGET_NAME') or 'open-coding-society'

# Gemini API settings
app.config['GEMINI_SERVER'] = os.environ.get('GEMINI_SERVER') or 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent'
app.config['GEMINI_API_KEY'] = os.environ.get('GEMINI_API_KEY') or None

# KASM settings
app.config['KASM_SERVER'] = os.environ.get('KASM_SERVER') or 'https://kasm.opencodingsociety.com'
app.config['KASM_API_KEY'] = os.environ.get('KASM_API_KEY') or None
app.config['KASM_API_KEY_SECRET'] = os.environ.get('KASM_API_KEY_SECRET') or None

# GROQ API settings
app.config['GROQ_SERVER'] = os.environ.get('GROQ_SERVER') or 'https://api.groq.com/openai/v1/chat/completions'
app.config['GROQ_API_KEY'] = os.environ.get('GROQ_API_KEY') or None