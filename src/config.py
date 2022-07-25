from dotenv import dotenv_values

config = dotenv_values(".env")

DATABASE_URL = config.get(
    "DATABASE_URL", "postgresql://postgres:example@localhost:5454"
)
