from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient('mongodb://localhost:27017/')
db = client['survey_system']
users = db['users']

for user in users.find():
    if 'password' in user and not user['password'].startswith('pbkdf2:sha256:'):
        hashed_password = generate_password_hash(user['password'])
        users.update_one({'_id': user['_id']}, {'$set': {'password': hashed_password}})
        print(f"Updated password for user: {user['email']}")

print("Password update complete.")