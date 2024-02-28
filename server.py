from flask import Flask, request, render_template, redirect, url_for
import pyotp

app = Flask(__name__)

# In-memory storage for demo purposes
user_secrets = {}

@app.route('/')
def index():
    return redirect(url_for('generate_secret_page'))

@app.route('/generate_secret', methods=['GET', 'POST'])
def generate_secret_page():
    if request.method == 'POST':
        username = request.form['username']
        secret = pyotp.random_base32()
        user_secrets[username] = secret
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

@app.route('/verify', methods=['POST'])
def verify_code():
    username = request.form['username']
    code = request.form['code']
    secret = user_secrets.get(username)
    if not secret:
        return redirect(url_for('invalid_code'))
    else:
        totp = pyotp.TOTP(secret)
        if totp.verify(code):
            return redirect(url_for('valid_code'))
        else:
            return redirect(url_for('invalid_code'))

@app.route('/valid_code')
def valid_code():
    return "<h1>Valid code entered!</h1>"

@app.route('/invalid_code')
def invalid_code():
    return "<h1>Invalid code.</h1>"

if __name__ == '__main__':
    app.run(debug=True)
