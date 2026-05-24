from flask import Flask, render_template, request, jsonify # type: ignore
import database

app = Flask(__name__)
database.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(database.get_all_todos())

@app.route('/todos', methods=['POST'])
def add_todo():
    task = request.json.get('task')
    todo_id = database.create_todo(task)
    return jsonify({'id': todo_id, 'task': task, 'completed': False})

@app.route('/todos/<int:id>', methods=['PUT'])
def toggle_todo(id):
    new_status = database.toggle_todo_status(id)
    return jsonify({'success': True, 'completed': new_status})

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    database.delete_todo_by_id(id)
    return jsonify({'success': True})

if __name__ == '__main__':
    # host='0.0.0.0' is required for Docker to expose the port correctly
    app.run(host='0.0.0.0', port=5009)