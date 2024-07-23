from flask import Flask, request, render_template
import re
import os

app = Flask(__name__)

COMMON_PASSWORDS_PATH = os.path.join('common-passwords', '10-million-password-list-top-1000.txt')
with open(COMMON_PASSWORDS_PATH, 'r') as file:
    common_passwords = set(file.read().splitlines())

def is_password_strong(password):
    if len(password) < 10:
        return False
    if password in common_passwords:
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        password = request.form['password']
        if is_password_strong(password):
            return render_template('welcome.html', password=password)
        else:
            return render_template('home.html', error='Password not valid')
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
