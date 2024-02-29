from flask import Flask, request, abort
import requests

app = Flask(__name__)

@app.route('/success')
def success():
    token = request.args.get('token')
    if token and verify_token_with_server_a(token):
        return "<h1>Access Granted</h1><p>Welcome to Server B!</p>"
    else:
        abort(403)

def verify_token_with_server_a(token):
    response = requests.get(f"http://localhost:5000/validate_token?token={token}")
    if response.status_code == 200:
        result = response.json()
        return result.get("valid", False)
    return False

if __name__ == '__main__':
    app.run(port=5001, debug=True)
