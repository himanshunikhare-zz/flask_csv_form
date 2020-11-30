from flask import Flask, render_template, request, redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from _datetime import datetime
import pandas as pd
import numpy as np
from wtforms import Form, TextField, TextAreaField, DateField, DateTimeField, DecimalField, IntegerField, BooleanField, RadioField, SelectField, validators
from wtforms.fields.html5 import DecimalRangeField
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db =SQLAlchemy(app)
data=pd.read_csv("./temp.csv")
data=data.set_index('Form_Label').T
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
app.config.from_object(__name__)

class UserForm(Form):

    for i in data:
        print(i)
        print(data[i]['Type'])

        if data[i]['Type'] == 'Text':
            formElement='TextField("%s",validators=[validators.required()])' %(i)
            pass

        elif data[i]['Type'] == 'Radio':
            choice = list(data[i][2:].dropna().unique().tolist())
            choiceStr=''
            for k in choice:
                ch = k.split('/')
                if len(ch)>1:
                    choiceStr +="('"+ch[1]+"','"+ch[0]+"')," 
                else:
                    choiceStr +="('"+k+"','"+k+"'),"
            formElement = 'RadioField("%s",validators=[validators.required()],choices=[%s], default="%s")' %(i,choiceStr, choice[0])
            pass

        elif data[i]['Type'] == 'DropDown':
            choice = list(data[i][2:].dropna().unique().tolist())
            choiceStr=''
            for k in choice:
                    choiceStr +="('"+k+"','"+k+"')," 
            formElement = 'SelectField("%s",validators=[validators.required()],choices=[%s])' %(i,choiceStr)
            pass

        elif data[i]['Type'] == 'TextArea':

            choice = list(data[i][2:].dropna().unique().tolist())
            formElement = 'TextAreaField("%s")' %(i)
            pass

        elif data[i]['Type'] == 'Boolean':
            formElement = 'BooleanField("%s")' %(i)
            pass

        elif data[i]['Type'] == 'Date':
            formElement = 'DateField("%s")' %(i)
            pass

        elif data[i]['Type'] == 'DateTime':
            formElement = 'DateTimeField("%s")' %(i)
            pass

        elif data[i]['Type'] == 'Decimal':
            formElement = 'DecimalField("%s", places=2)' %(i)
            pass

        elif data[i]['Type'] == 'File':
            formElement = 'FileField("%s")' %i
            pass

        elif data[i]['Type'] == 'Recaptcha':
            formElement = 'RecaptchaField()'
            pass
        
        elif data[i]['Type'] == 'Password':
            formElement = 'PasswordField("%s")' %i
            pass

        elif data[i]['Type'] == 'Integer':
            formElement = 'IntegerField("%s")' %i
            pass

        else:
            print('Unable to create form for :',i)

        exec("%s=%s" % (data[i]['Form_Value'],formElement))

        def validate_image(form, field):
            if field.data:
                field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

def upload(request):
    form = UploadForm(request.POST)
    if form.image.data:
        image_data = request.FILES[form.image.name].read()
        open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        formData = {}
        for i in request.form:
            formData[i] = request.form[i]
        print(formData)
        pass

    if form.validate():
        flash('Succesfully submitted')
    else:
        flash('All the form fields are required. ')
    return render_template('index.html',values=data,form=form)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
