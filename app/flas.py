from flask import Flask, request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_name():
    if request.data:
       return request.data


@app.route('/<name>/<password>')
def read_data(name, password):
    if name == 'admin' and password == 'admin':
        return redirect(url_for('admin'))


@app.route('/admin')
def admin():
    return "this is public variable"


if __name__ =='__main__':

    app.run(debug=True,port=3000)