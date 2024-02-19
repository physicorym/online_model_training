
from envparse import Env

env = Env()

DATABAE_URL = env.str(
    "DATABAE_URL",
    default="postgresql + asyncpg://postgres:postgres@0.0.0.0:5432/postgress"
)