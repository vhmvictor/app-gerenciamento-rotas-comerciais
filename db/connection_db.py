import os
import psycopg2
import dotenv

dotenv.load_dotenv()

try: 
    conn = psycopg2.connect(database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"), host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"))
    print("Database Connected")

    cur = conn.cursor()

except:
    print("Database not connected")