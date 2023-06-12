import requests
import json

# Set the URL of the server
# If running on raspberry pi replace <RASPBERRY_PI_IP_ADDRESS> with the actual IP address
server_url = 'http://raspberrypi:5000/predict'
#server_url = 'http://localhost:5000/predict'


# Example input data: Modify this according to the input format expected by your model
query = input("Query: ")
query = query

# Advanced Search Filters
since = "2023-06-06"
until = "2023-06-08"

data = {'query': query, 'until' : until, 'since' : since}

# Send the request to the server
response = requests.post(server_url, json=data)

# Check if the request was successful
if response.status_code == 200:
    response = response.json()

    for tweet in response:
        print(f"User: {tweet['username']}\tDate: {tweet['date']}")
        print(tweet['content'])
        print(f"\nSentiment Score: {tweet['prediction']}")
        print("\n- - - - - - - - - - - - -\n")
else:
    print('Error:', response.status_code)

