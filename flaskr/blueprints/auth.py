from flask import Blueprint, render_template, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    elif request.method == 'GET':
        return render_template('pages/login.html')
    
    # Logic for handling login
    return "Login Page"

@auth_bp.route('/logout')
def logout():
    # Logic for handling logout
    return "Logout Page"

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(request.form)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return "Signup Page"
    elif request.method == 'GET':
        return render_template('pages/signup.html')
