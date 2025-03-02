# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'insecure_secret_key'  # VULNERABLE
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add CSRF Protection, Set session cookie to be https only and set samesite attribute to strict to prevent CSRF attacks
    SESSION_COOKIE_HTTPONLY = True  # Vulnerable without this set to true.
    SESSION_COOKIE_SAMESITE = 'Lax'  # 'Lax' or 'Strict' - Vulnerable in some scenarios.
    SESSION_COOKIE_SECURE = False  # Only works when your site serves through https