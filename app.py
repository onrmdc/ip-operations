from flask import Flask, request, render_template, jsonify, flash
from find_port_with_ip import *
from form import UserForm
import os


app = Flask(__name__)
app.secret_key = os.environ["FLASKSECRETKEY"]


@app.route("/", methods=['POST', 'GET'])
def index():
    result = None
    form = UserForm(request.form)
    if request.method == 'POST':

        if form.validate_on_submit():
            input_ip_address = request.form['input_ip_address']
            result = main_func(input_ip_address)

    return render_template('find-interface.html', form=form, result=result)


@app.route("/switch_ports.json", methods=['GET', 'POST'])
def switch_ports():
    if request.method == 'POST':
        ip_address = request.get_json()
        print(ip_address)
        result_dict = main_func(ip_address)
        return jsonify(result_dict)
    else:
        return "Not Found", 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
