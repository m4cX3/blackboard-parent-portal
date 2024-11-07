import requests
from configuration.appconfig import get_access_token

access_token = get_access_token

def user_exists(user_name):
    response = requests.get(
        'https://malayanmindanao-test.blackboard.com/learn/api/public/v1/users',  # Replace with actual user API endpoint
        timeout=5,
        headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
        },
        params={
        'userName': user_name
        })
    
    if response.status_code == 200:
        users = response.json()
        for user in users['results']:
            if user['userName'] == user_name:
                return True
    
    return False