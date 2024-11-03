from flask import Flask, request
from todo_list_backend.resources import EntryManager, Entry

app = Flask(__name__)
FOLDER = 'D:\\back-end-developer\python_project\\todoBackend\pythonProject'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/entries/")
def get_entries():
    entryManager = EntryManager(FOLDER)
    entryManager.load()
    entryList = []
    for entry in entryManager.entries:
        entryList.append(entry.json())
    return entryList


@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    response = request.get_json()
    for entry in response:
        entry_manager.entries.append(Entry.from_json(entry))
    entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)