from mongoengine import connect
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

user = os.getenv('USER_NAME')
password = os.getenv('PASS')
cluster = os.getenv('CLUSTER')
domain = os.getenv('DOMAIN')
db_name = os.getenv('DB_NAME')

connect(
    db=db_name,
    host=f'mongodb+srv://{user}:{password}@{cluster}.{domain}',
    tlsCAFile=certifi.where()
)
