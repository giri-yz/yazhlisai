# server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database for user accounts and files
users = {'user1': {'password': 'pass1', 'files': ['file1.txt', 'file2.txt']},
         'user2': {'password': 'pass2', 'files': ['file3.txt']}}

@app.route('/login', methods=['POST'])
def login():
    # User authentication logic
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username]['password'] == password:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failure', 'message': 'Invalid credentials'})

@app.route('/list_files', methods=['GET'])
def list_files():
    # Provide a list of available files
    return jsonify({'files': [file for user in users.values() for file in user['files']]})

@app.route('/download', methods=['POST'])
def download():
    # Handle file download logic
    data = request.get_json()
    username = data.get('username')
    file_to_download = data.get('file')

    if username in users and file_to_download in users[username]['files']:
        return jsonify({'status': 'success', 'message': 'File download logic here'})
    else:
        return jsonify({'status': 'failure', 'message': 'Invalid request'})

if __name__ == '__main__':
    app.run(debug=True)
