from dotenv import dotenv_values

config = dotenv_values(".env")

DATABASE_URL = config.get("DATABASE_URL", "postgresql://lopkop@localhost:5454/example")
