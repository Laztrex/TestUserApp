from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import json
import random
app = Flask(__name__)
api = Api(app)


class Quote(Resource):
    def get(self, id=0):
        with open('users.json', "r", encoding='utf-8') as read_file:
            loaded_json_file = json.load(read_file)
            a = list(filter(lambda x: x["id"] == id, loaded_json_file))
            if a:
                return a[0]['name'], 200
            return "Quote not found", 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int)
        parser.add_argument("name")
        params = parser.parse_args()
        # TODO: проверять на кол-во двух полей id и name
        results = self._read_json_with_condition()
        for user_id in results:
            if params['id'] == user_id['id']:
                return f"Quote with id {params['id']} already exists", 400
        results.append(params)

        self._write_json_with_condition(data=results)

        return params, 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        params = parser.parse_args()

        result = self._read_json_with_condition()
        for user_id in result:
            if int(id) == user_id['id']:
                user_id['name'] = params['name']
                break
        else:
            return f"Quote with id {params['id']} already exists", 400

        self._write_json_with_condition(data=result)

        return params, 201

    def delete(self, id):
        self._write_json_with_condition(data=self._read_json_with_condition(condition=id))
        return f"Quote with id {id} is deleted.", 200

    def _read_json_with_condition(self, condition=None):
        with open('users.json', "r", encoding='utf-8') as read_file:
            loaded_json_file = json.load(read_file)
            if condition:
                loaded_json_file = [user for user in loaded_json_file if user['id'] != condition]
        return loaded_json_file

    def _write_json_with_condition(self, data):
        with open('users.json', "w", encoding='utf-8') as write_file:
            json.dump(data, write_file, indent=2, ensure_ascii=False)


api.add_resource(Quote, "/ai-quotes", "/ai-quotes/<int:id>")
if __name__ == '__main__':
    app.run(debug=True)
