"""
Application configuration file. Do not hardcode passwords or secret strings here
"""
import os
import secrets

from dotenv import load_dotenv


# Loading environmental variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = secrets.token_urlsafe(32)
    CSRF_TOKEN = secrets.token_urlsafe(32)
    LOGIN_EXPIRE_MINUTES: int = 60 * 24 * 30
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')

    PAY_STACK_KEY: str = os.getenv('PAY_STACK_KEY')

    @staticmethod
    def init_app():
        pass

config = Config()
