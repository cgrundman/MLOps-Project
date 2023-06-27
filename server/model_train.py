import random
import pickle 

class Model():
    def __init__(self):
        pass

    def predict(self, features:list):
        # make random predictions
        predictions = [random.uniform(0, 1) for feature in features]
        return predictions

def createModel():
    model = Model()
    model_path = "model/naive_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    return model_path

if __name__=='__main__':
    createModel()