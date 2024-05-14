from flask import Flask, request, jsonify, send_from_directory
from numbers_parser import Document
import os

app = Flask(__name__, static_folder=".")

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(file.filename)
    doc = Document(file.filename)
    tables = []
    for table in doc.sheets[0].tables:
        t = {
            'name': table.name,
            'rows': [[row[0].value, row[1].value, row[2].value, row[3].value] for row in table.rows()]
        }
        t['rows'].pop(0)
        tables.append(t)
    
    os.remove(file.filename)
    return jsonify(tables=tables)

if __name__ == '__main__':
    app.run(debug=True)
