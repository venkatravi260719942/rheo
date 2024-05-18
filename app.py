#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import requests  # Import the requests library

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Be Glad. Be good, Be brave',
        'description': u'If i were a neurosurgon and i announce that i had to leave my guests to go in',
        'done': False
    },
    {
        'id': 2,
        'title': u'Remarkable Essay',
        'description': u'While shailesh was eriting this book, He published a short, Remarkable essay',
        'done': False
    }
]

@app.route('/')
def index():
    return "Welcome to the Flask App"

@app.route('/external-api', methods=['GET'])
def external_api():
    response = requests.get('https://api.example.com/data')  # Example of making a request to an external API
    return jsonify(response.json())

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid Request made Not found'}), 404)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    print(request.json)
    if not request.json or not 'title' in request.json:
        abort(404)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
