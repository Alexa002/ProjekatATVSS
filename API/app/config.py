import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dating_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600 
    
    cloudinary.config(
    cloud_name='dnwievzrk', 
    api_key='163271492299255',        
    api_secret='-EeypUWVCXno8vE_Sh7zG9NjbbM'   
    )