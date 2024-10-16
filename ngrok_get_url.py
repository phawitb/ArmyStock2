# https://dashboard.ngrok.com/get-started/setup/linux
# ngrok config add-authtoken 2nLJwN5SqkrtH9bxLeirZByTgWR_6G3wNZZbWEepxGxtiUZZY
# ngrok http http://localhost:8509

import requests

# Replace with your local URL
url = 'http://localhost:4040/api/tunnels'

try:
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for HTTP errors

    data = response.text
    print(data)


except requests.exceptions.RequestException as e:
    print(f'Error fetching data: {e}')
