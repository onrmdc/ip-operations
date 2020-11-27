from flask import Flask,request,render_template
from find_port_with_ip import *
from form import UserForm


app = Flask(__name__)
app.secret_key = 'fa43422c30f0153f9ad461572fd32e1955db2865289c8198'


@app.route("/", methods=['POST', 'GET'])
def index():
    result = None
    form = UserForm(request.form)
    if request.method == 'POST':

        if form.validate_on_submit():
            input_ip_address = request.form['input_ip_address']
            result = main_func(input_ip_address)

    return render_template('find-interface.html', form=form, result=result)


if __name__ == '__main__':
    app.run(debug=True)
