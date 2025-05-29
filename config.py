import os

# Get absolute path to current directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SQLite DB path (safe across OS)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'crm.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # App secret key (for Flask sessions and CSRF protection)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # in seconds (1 hour)


# User roles constant
VALID_ROLES = {'admin', 'agent', 'analyst'}