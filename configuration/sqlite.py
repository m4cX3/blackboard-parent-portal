from configuration.api_response import get_response, post_response
from configuration.appconfig import get_access_token
from configuration.error_checking import user_exists
import sqlite3, json

access_token = get_access_token()

def fetch_users_to_database(users):
    
    print("Fetching users to database...")
    
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Create the table if it doesn't already exist
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            FormID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentID INTEGER,
            userName TEXT,
            password TEXT,
            gender TEXT,
            institutionRoleIds TEXT,
            systemRoleIds TEXT,
            availability TEXT,
            name TEXT,
            contact TEXT
        )
    ''')

    # Insert JSON strings for the relevant fields if they're not already strings
    for user in users:
        # Convert lists or dicts to JSON strings
        if isinstance(institutionRoleIds, (list, dict)):
            institutionRoleIds = json.dumps(institutionRoleIds)
        if isinstance(systemRoleIds, (list, dict)):
            systemRoleIds = json.dumps(systemRoleIds)
        if isinstance(availability, (dict, list)):
            availability = json.dumps(availability)
        if isinstance(name, dict):
            name = json.dumps(name)
        if isinstance(contact, dict):
            contact = json.dumps(contact)

        # Insert into the table with the converted JSON values
        cursor.execute(''' 
            INSERT OR REPLACE INTO users (userName, institutionRoleIds, systemRoleIds, availability, name, contact)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user.get('userName'),
            institutionRoleIds,  # Use the JSON string
            systemRoleIds,       # Use the JSON string
            availability,        # Use the JSON string
            name,                # Use the JSON string
            contact              # Use the JSON string
        ))

    conn.commit()  # Commit the changes to the database
    cursor.close()
    conn.close()


def send_to_database(sample_data):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Create the table if it doesn't already exist
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS parents (
            FormID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentID INTEGER,
            userName TEXT,
            password TEXT,
            gender TEXT,
            institutionRoleIds TEXT,
            systemRoleIds TEXT,
            availability TEXT,
            name TEXT,
            contact TEXT
        )
    ''')
    conn.commit()

    # Fields that may need JSON conversion
    json_fields = ["institutionRoleIds", "systemRoleIds", "availability", "name", "contact"]

    # Convert lists/dicts to JSON strings for specified fields
    for field in json_fields:
        if isinstance(sample_data.get(field), (list, dict)):
            sample_data[field] = json.dumps(sample_data[field])

    # Insert the data into the database
    cursor.execute('''INSERT INTO parents 
                      (userName, password, gender, institutionRoleIds, systemRoleIds, 
                      availability, name, contact) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (sample_data["userName"], sample_data["password"], sample_data["gender"],
                    sample_data["institutionRoleIds"], sample_data["systemRoleIds"],
                    sample_data["availability"], sample_data["name"], sample_data["contact"]))

    conn.commit()
    print("Data inserted successfully.")
    
    cursor.close()
    conn.close()

    return sample_data


def fetch_from_database_to_api(users):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT userName, password, gender, institutionRoleIds, systemRoleIds, 
                      availability, name, contact FROM parents WHERE userName = ?''', 
                   (users["userName"],))
    row = cursor.fetchone()

    if not row:
        fetched_data = {}
    else:
        check_get_response = get_response()

        if check_get_response.status_code == 200:
            fetched_data = {
                "userName": row[0],
                "password": row[1],
                "gender": row[2],
                "institutionRoleIds": json.loads(row[3]) if row[3] else None,
                "systemRoleIds": json.loads(row[4]) if row[4] else None,
                "availability": json.loads(row[5]) if row[5] else None,
                "name": json.loads(row[6]) if row[6] else None,
                "contact": json.loads(row[7]) if row[7] else None
            }
            
            
            if user_exists(fetched_data['userName']):
                print("User already exists in the API. No insertion done.")
            
            else:
                post_response(fetched_data)
                print("Data imported successfully.")
        
            cursor.close()
            conn.close()

            print("Data inserted and fetched successfully.")
            return fetched_data