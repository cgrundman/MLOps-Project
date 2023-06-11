from flask import Flask, request, jsonify
import os
from model_train import Model, createModel # import the model class
import pickle # import here the library to load your trained model
from TwitterScraper import getTweets

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
    # Modify the code below according to the requirements of your model
    # Example: Assuming the input data is a list of features
    tweets = getTweets(data["query"], max = 10)
    tweetContent = [tweet[2] for tweet in tweets]
    predictions = model.predict(tweetContent)

    # Return the predictions as a JSON response
    response = {'predictions': predictions, 'tweet_Content' : tweetContent}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the server on all available network interfaces