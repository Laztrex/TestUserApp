import re
from string import punctuation
import os
from flask import Flask, request, jsonify, Response
from flask_restful import Api, Resource, reqparse
import json

app = Flask(__name__)
api = Api(app)


def theme_validate(data):
    errors = []

    if data['id'] is None:
        errors.append(
            "No <id> JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return None, errors

    if not data['name']:
        errors.append(
            "No <name> JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return None, errors

    if len(re.sub(f'[{punctuation}]', '', data['name'].strip())) < 2:
        errors.append(
            f"Field '{data}' is very strange")

    return data, errors


def resp(code, data):
    return Response(
        status=code,
        mimetype="application/json",
        response=json.dumps(data)
    )


class User(Resource):
    def get(self, _id=None):
        results = self._read_json_with_condition()
        if _id is not None:
            filtered_users = list(filter(lambda x: x["id"] == _id, results))
            return f"Hello, my name is {filtered_users[0]['name']}. Im here", 200
        return jsonify([name['name'] for name in results], )

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int)
        parser.add_argument("name")
        params, errors = theme_validate(parser.parse_args())

        # TODO: проверять на кол-во двух полей id и name
        if errors:
            return resp(400, {"errors": errors})

        results = self._read_json_with_condition()
        for user_id in results:
            if params['id'] == user_id['id']:
                return f"User with id {params['id']} already exists", 400
        results.append(params)

        self._write_json_with_condition(data=results)

        return f"Add user {params['name']}", 201

    def put(self, _id):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        params = parser.parse_args()

        result = self._read_json_with_condition()
        for user_id in result:
            if int(_id) == user_id['id']:
                user_id['name'] = params['name']
                break
        else:
            return f"User with id {params['id']} already exists", 400

        self._write_json_with_condition(data=result)

        return f"Fix user {_id}", 201

    def delete(self, _id):
        self._write_json_with_condition(data=self._read_json_with_condition(condition=_id))
        return f"User with id {_id} is deleted.", 200

    def _read_json_with_condition(self, condition=None):
        with open(os.path.dirname(__file__) + '/files/users.json', "r", encoding='utf-8') as read_file:
            loaded_json_file = json.load(read_file)
            if condition:
                loaded_json_file = [user for user in loaded_json_file if user['id'] != condition]
        return loaded_json_file

    def _write_json_with_condition(self, data):
        with open(os.path.dirname(__file__) + '/files/users.json', "w", encoding='utf-8') as write_file:
            json.dump(data, write_file, indent=2, ensure_ascii=False)


api.add_resource(User, "/users", "/users/<int:_id>")
if __name__ == '__main__':
    app.run(debug=True)
