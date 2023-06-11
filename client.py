import requests
import json

# Set the URL of the server
# If running on raspberry pi replace <RASPBERRY_PI_IP_ADDRESS> with the actual IP address
server_url = 'http://raspberrypi:5000/predict'
#server_url = 'http://localhost:5000/predict'


# Example input data: Modify this according to the input format expected by your model
query = "#Deutschlandticket"
data = {'query': query}

# Send the request to the server
response = requests.post(server_url, json=data)

# Check if the request was successful
if response.status_code == 200:
    predictions = response.json()['predictions']
    tweetContents = response.json()['tweet_Content']
    #print('Predictions:', predictions)
    for prediction, tweetContent in zip(predictions, tweetContents):
        print(tweetContent)
        print(f"\nSentiment Score: {prediction}")
        print("\n- - - - - - - - - - - - -\n")
else:
    print('Error:', response.status_code)

