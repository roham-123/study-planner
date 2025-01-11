from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://roham:Roham137789@study-planner-db.c3k2akqmsl3v.us-east-1.rds.amazonaws.com:5432/study-planner-db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-very-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Token valid for 1 hour