from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('hello_form.html')
    return template.render()

@app.route("/hello", methods=['POST'])
def hello():
    first_name = request.form['first_name']
    template = jinja_env.get_template('hello_greeting.html')
    return template.render(name=first_name)

def is_valid(data):
    #valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    valid_data = str(data)
    if valid_data.isalnum():
        return True
    else:
        return False


  
def valid_email(email):
    ats = -1
    dots = -1
    at_email = request.form['email']
    dot_email = request.form['email']
    substring1= "@"
    substring2= "."
    ats= ats + at_email.count(substring1)
    dots= dots + dot_email.count(substring2)

    if ats is 0 and dots is 0:
        return True
    else: 
        return False


def is_valid_email(data):
    valid_characters = "@.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    space_list = []
    valid_data = str(data)
    for letter in data:
        if letter not in valid_characters:
            return False
        elif letter in valid_characters:
            space_list.append(letter)
    else:
        return True
   



@app.route('/', methods=['POST'])
def validate_data():

    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']


    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

#Username Errors
    if len(username) <= -1:
        username_error= "Must type a username."
        username= ''
        password= ''
        verify= ''
        email= email

    if len(username) <= 2:
        username_error = 'Length of username must be between 3 and 20 characters.'
        username= ''
        password= ''
        verify= ''
        email= email

    if len(username) > 19:
        username_error = 'Length of username must be between 3 and 20 characters.'
        username= ''
        password= ''
        verify= ''
        email= email

    if not is_valid(username):
        username_error = 'Not a valid username.'
        username= ''
        password= ''
        verify= ''
        email= email



#Password Errors
    if len(username) <= -1:
        password_error= "Must type a password."
        username= username
        password= ''
        verify= ''
        email= email    

    if len(password) <= 2:
        password_error = 'Length of password must be between 3 and 20 characters.'
        username= username
        password= ''
        verify= ''
        email= email   

    if len(password) > 19 :
        password_error = 'Length of password must be between 3 and 20 characters.'
        username= username
        password= ''
        verify= ''
        email= email   

    if not is_valid(password):
        password_error = 'Not a valid password.'
        username= username
        password= ''
        verify= ''
        email= email



#Verify Password Errors
    if len(verify) <= -1:
        verify_error= "Must verify password."
        username= username
        password= ''
        verify= ''
        email= email

    if not verify == password:
        verify_error = 'Passwords do not match.'
        username= username
        password= ''
        verify= ''
        email= email


#Email Errors
    #if len(email) == -1:
    if email == '':
        username= username
        password= password
        verify= verify
        email= ''

    else:

        if not valid_email(email):
            email_error= "Not a valid email address."
            username= username
            password= ''
            verify= ''
            email= email

        elif not is_valid_email(email):
            email_error= "Not a valid email addressmmmm."
            username= username
            password= ''
            verify= ''
            email= email
    
        else:
            username= username
            password= password
            verify= verify
            email= email 
    

#General Errors
    if not password_error and not username_error and not verify_error and not email_error:
        user = str(username)
        return redirect('/hellouser?user={0}'.format(user))
    else:
        template = jinja_env.get_template('hello_form.html')
        return template.render(username_error=username_error,
            password_error=password_error, verify_error= verify_error,
            email_error=email_error,
            username=username,
            password=password,
            verify=verify,
            email=email)


@app.route('/hellouser')
def valid_user():
    user = request.args.get('user')
    return '<h1>Hello, {0}.</h1>'.format(user)




app.run()