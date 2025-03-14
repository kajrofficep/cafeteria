import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://admin:123@192.168.3.86/farjad'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'jljokdldsADfsdf4646fsad@!@'
