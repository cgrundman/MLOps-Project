import requests
import json

# Set the URL of the server
# If running on raspberry pi replace <RASPBERRY_PI_IP_ADDRESS> with the actual IP address
server_url = 'http://raspberrypi:5000/predict'
#server_url = 'http://localhost:5000/predict'


# Example input data: Modify this according to the input format expected by your model
data = {'sentences': ["sentence 1", "sentence 2", "sentence 3"]}

# Send the request to the server
response = requests.post(server_url, json=data)

# Check if the request was successful
if response.status_code == 200:
    predictions = response.json()['predictions']
    print('Predictions:', predictions)
else:
    print('Error:', response.status_code)

