import requests
import json

def query_and_date(query, start_date, end_date):
    # Set the URL of the server
    # If running on raspberry pi replace <RASPBERRY_PI_IP_ADDRESS> with the actual IP address
    #server_url = 'http://raspberrypi:5000/predict'
    server_url = 'http://0.0.0.1:5000/predict'

    data = {'query': query, 'since': start_date, 'until': end_date}

    # Send the request to the server
    response = requests.post(server_url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        response = response.json()

        # Sort and rank tweets
        sorted_tweets = sorted(response, key=lambda x: x['prediction'])
        ranked_tweets = [{'rank': rank+1, **tweet} for rank, tweet in enumerate(sorted_tweets)]

        top = ranked_tweets[-5:]
        low = ranked_tweets[:5]

        # Their accordingly contents
        top_contents = [tweet['content'] for tweet in top]
        low_contents = [tweet['content'] for tweet in low]

        # Average Sentiment Score
        score = [float(tweet['prediction']) for tweet in response]
        avg_score = sum(score)/len(score)

        for tweet in response:
            print(f"User: {tweet['username']}\tDate: {tweet['date']}")
            print(tweet['content'])
            print(f"\nSentiment Score: {tweet['prediction']}")
            print("\n- - - - - - - - - - - - -\n")


        print(f"\nAverage Score: {avg_score}")

        return top, low, top_contents, low_contents, avg_score
    
    else:
        print('Error:', response.status_code)
        return None, None, None, None, None
    
