from flask import Flask, request, jsonify
import os
from model_train import Model, createModel # import the model class
import pickle # import here the library to load your trained model
from TwitterScraper import getTweets, build_query

app = Flask(__name__)

# check if model exists, otherwise create it (only for testing!!!)
model_path = "model/naive_model.pkl"
if not os.path.exists(model_path):
    model_path = createModel()

# Load your trained model
with open(model_path, 'rb') as f: # Update with the actual path to your model file
    model = pickle.load(f)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get the data from the request

    # Process the input data and make predictions using your model
    query = build_query(**data)
    tweets = getTweets(query, max = 10)

    usernames = [tweet['username'] for tweet in tweets]
    dates = [tweet['date'] for tweet in tweets]
    contents = [tweet['content'] for tweet in tweets]

    predictions = model.predict(contents)

    # Prepare Response data
    response = [{'username': usernames[i],
                'date': dates[i],
                'content' : contents[i],
                'prediction': predictions[i]}
                for i in range(len(predictions))]
    
    # Return the predictions as a JSON response
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the server on all available network interfaces