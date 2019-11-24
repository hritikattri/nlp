from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle

app = Flask(__name__)
api = Api(app)

with open('vectorizer.pkl', 'rb') as f:
	vectorizer = pickle.load(f)

with open('sentiment_classifier.pkl', 'rb') as f:
	sentiment_classifier = pickle.load(f)

parser = reqparse.RequestParser()
parser.add_argument('query')

class PredictSentiment(Resource):
	def get(self):
		args = parser.parse_args()
		user_query = args['query']

		user_input = vectorizer.transform([str(user_query)])
		prediction = sentiment_classifier.predict(user_input)

		result = 'Negative' if prediction == 0 else 'Positive'
		output = {'Prediction': result}

		return output

api.add_resource(PredictSentiment, '/')

if __name__ == '__main__':
	app.run(debug = True)

