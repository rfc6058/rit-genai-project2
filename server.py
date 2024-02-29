from flask import Flask, request, render_template, redirect, url_for, jsonify
import pyotp
from datetime import datetime, timedelta
import uuid
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# In-memory storage for demo purposes
user_secrets = {}
user_last_timestamps = {}  # Track the last successful timestamp for each user

@app.route('/')
def index():
    return redirect(url_for('generate_secret_page'))

@app.route('/generate_secret', methods=['GET', 'POST'])
def generate_secret_page():
    if request.method == 'POST':
        username = request.form['username']
        secret = pyotp.random_base32()
        user_secrets[username] = secret
        # Ensure there's no last timestamp for a new secret
        user_last_timestamps[username] = 0
        return redirect(url_for('show_code', username=username))
    return render_template('generate_secret.html')

@app.route('/show_code')
def show_code():
    username = request.args.get('username')
    secret = user_secrets.get(username)
    if not secret:
        return "User not found", 404
    totp = pyotp.TOTP(secret)
    code = totp.now()
    return render_template('show_code.html', code=code, username=username)

@app.route('/verify_form')
def verify_form():
    return render_template('verify_result.html')

tokens = {}  # Store tokens with expiration
@app.route('/verify', methods=['POST'])
def verify_code():
    username = request.form['username']
    code = request.form['code']
    secret = user_secrets.get(username)
    
    if not secret:
        return redirect(url_for('invalid_code'))
    
    totp = pyotp.TOTP(secret)
    current_time = datetime.now()
    current_time_step = totp.timecode(current_time)
    
    # Check if the code is being reused
    if is_code_reused(username, current_time_step):
        return redirect(url_for('invalid_code'))
    
    if totp.verify(code):
        # Update the last valid time step for the user
        user_last_timestamps[username] = current_time_step
        
        # Token generation and storage upon successful verification
        token = str(uuid.uuid4())
        tokens[token] = datetime.now() + timedelta(minutes=5)  # Token expires in 5 minutes
        return redirect(url_for('valid_code', token=token))
    else:
        return redirect(url_for('invalid_code'))


@app.route('/validate_token', methods=['GET'])
def validate_token():
    token = request.args.get('token')
    if token in tokens and tokens[token] > datetime.now():
        # Token is valid
        return jsonify({"valid": True})
    else:
        # Token is invalid or expired
        return jsonify({"valid": False})
    
# Cleanup expired tokens periodically
@app.before_request
def before_request():
    current_time = datetime.now()
    expired_tokens = [token for token, expiry in tokens.items() if expiry < current_time]
    for token in expired_tokens:
        tokens.pop(token, None)

@app.route('/valid_code')
def valid_code():
    token = request.args.get('token')
    # Server B's URL with the token parameter
    server_b_url = f"http://localhost:5001/success?token={token}"
    return render_template('valid_code.html', server_b_url=server_b_url)


@app.route('/invalid_code')
def invalid_code():
    return render_template('invalid_code.html')


def is_code_reused(username, current_time_step):
    last_used_time_step = user_last_timestamps.get(username, 0)
    return current_time_step <= last_used_time_step


if __name__ == '__main__':
    app.run(debug=True)
