from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/')
def main():
    return redirect(url_for('hello', username='Peter'))
        # Also pass an optional URL variable

@app.route('/hello/<username>')
def hello(username):
    return 'Hello, {}'.format(username)

if __name__ == '__main__':
    app.run(debug=True, port= 5200)