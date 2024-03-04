import time
import hashlib
import base64
import os
from flask import Flask, request, jsonify
from binascii import hexlify


app = Flask(__name__)

# Dictionary to store the seed for each user
seeds = {}

# Function to generate TOTP

def generate_totp(seed, interval=30):
    # Calculate the number of intervals that have passed since the Unix epoch
    intervals = int(time.time()) // interval
    # Convert the intervals to bytes
    intervals_bytes = intervals.to_bytes(8, 'big')
    # Calculate the HMAC-SHA1 of the intervals using the seed as the key
    hmac = hashlib.sha1(seed)
    hmac.update(intervals_bytes)
    hmac_digest = hmac.digest()
    # Truncate the HMAC to obtain the TOTP
    offset = hmac_digest[-1] & 0x0f
    binary = int.from_bytes(hmac_digest[offset:offset+4], 'big') & 0x7fffffff
    totp = binary % (10 ** 6)
    return totp





# Endpoint to enroll a new user
@app.route('/enroll', methods=['POST'])
def enroll():
    # Get the username and password from the request
    username = request.form['username']
    password = request.form['password']
    # Generate a random seed
    seed = os.urandom(20)
    # Store the seed for the user
    seeds[username] = seed
    # Return the seed to the client
    return base64.b64encode(seed).decode('utf-8')

# Endpoint to verify a TOTP for a user
@app.route('/verify/<username>', methods=['POST'])
def verify(username):
    # Get the TOTP from the request
    totp = request.form['totp']
    # Calculate the expected TOTP using the stored seed for the user
    expected_totp = generate_totp(seeds[username])
    # Check if the TOTP is correct
    if totp == expected_totp:
        return 'OK'
    else:
        print(totp)
        print(expected_totp)
        return 'error'

if __name__ == '__main__':
    app.run()