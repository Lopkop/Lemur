from dotenv import dotenv_values

config = dotenv_values(".env")

DATABASE_URL = config.get("DATABASE_URL")
SECRET_KEY = config.get('SECRET_KEY')
