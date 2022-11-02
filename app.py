from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def hello_world():  # put application's code here
    data = request.json
    print(data['username'])
    print(data.get('username'))
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
