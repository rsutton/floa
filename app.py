import json

from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/<id>")
def find_by_id(id):
    for i in library:
        if i['id'] == int(id):
            break
    return i

@app.route("/have/<id>")
def have(id):
    item = find_by_id(id)
    item['have'] = 1
    item['want'] = 0
    return item

@app.route("/want/<id>")
def want(id):
    item = find_by_id(id)
    item['have'] = 0
    item['want'] = 1
    return item

@app.route("/title/<query>")
def search(query):
    results = []
    q = query.lower()
    for i in library:
        if q in i['title'].lower():
            results.append(i)
    return jsonify(results)

def add(id, title):
    library.append({'id': id, 'title': title, 'have': 0, 'want': 0})

def save():
    json.dump(library, open('library.json', 'w'))

@app.route("/list")
def list():
    return jsonify(library)

# library.json is the annotated version of loa.json
# containing 'have' and 'want' fields
library = json.load(open('library.json', 'r'))

if __name__ == "__main__":
    app.run(debug=True)