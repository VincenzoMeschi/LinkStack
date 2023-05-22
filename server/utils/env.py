from dotenv import load_dotenv
import os

def load_env_variables():
  load_dotenv()

  env_varaibles = {
    "POSTGRE_PASSWORD": os.getenv("POSTGRE_PASSWORD"),
    "POSTGRE_USERNAME": os.getenv("POSTGRE_USERNAME"),
    "POSTGRE_HOST": os.getenv("POSTGRE_HOST"),
    "POSTGRE_PORT": os.getenv("POSTGRE_PORT"),
    "POSTGRE_DATABASE": os.getenv("POSTGRE_DATABASE"),
    "JWT_SECRET": os.getenv("JWT_SECRET")
  }

  return env_varaibles
