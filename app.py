from flask import Flask, request
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api(app)

api_key_to_stored_integer = {}

class PostEndpoint(Resource):
    def post(self):
        api_key = request.headers.get('API-KEY')
        integer_json = request.data.decode('utf-8')
        integer_data = json.loads(integer_json)

        stored_integer = int(integer_data['integer'])

        if api_key is None:
            return {"error": "Missing API key"}

        api_key_to_stored_integer[api_key] = stored_integer

        return {"message": "Integer updated successfully"}


class GetEndpoint(Resource):
    def get(self):
        api_key = request.headers.get('API-KEY')
        multiplier = int(request.args.get('multiplier', 1))

        if api_key not in api_key_to_stored_integer:
            return {"error": "Invalid API key"}

        stored_integer = api_key_to_stored_integer[api_key]
        result = stored_integer * multiplier

        return f"<h1>{result}</h1>"

api.add_resource(PostEndpoint, '/post')
api.add_resource(GetEndpoint, '/get')

if __name__ == '__main__':
    app.run(debug=True)

#curl -X POST -H "API-KEY: your_api_key" -H "Content-Type: application/json" -d '{"integer": 7}' http://localhost:5000/post

#curl -X GET -H "API-KEY: your_api_key" http://localhost:5000/get?multiplier=3
