from flask import Blueprint, jsonify,render_template,request,flash,redirect,url_for,current_app  
from .models import User
from . import db
from flask_login import login_user, login_required,logout_user,current_user

from werkzeug.security import generate_password_hash,check_password_hash

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('logged in successfully',category='success')
                login_user(user,remember=True)
                return jsonify({'message':"login successfully","success":True})
            else:
                return jsonify({'message':"email or password error"})
        else:
            return jsonify({'message':"user does not exists"})


 
    return render_template("login.html",user=current_user)
    
@auth.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    try:
        if current_user.is_authenticated:
            # Log the user's logout attempt
            current_app.logger.info(f"User {current_user.username} is logging out.")
        
        # Call logout_user() to log the user out
        logout_user()
        
        # Return a success message
        return jsonify({"success": True}), 200

    except Exception as e:
        # Log the error for debugging
        current_app.logger.error(f"Error during logout: {str(e)}")
        
        # Return a failure message with error details
        return jsonify({"success": False, "error": str(e)}), 500

@auth.route('/signup',methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
           return jsonify({'message':"email already exists"})
        if len(email) <4:
            return jsonify({'message':"email should greater than 4 char",})
        elif len(username) <2:
            return jsonify({'message':"username should greater than 2 char",})
        elif password1 != password2:
            return jsonify({'message':"password mismatch",})
        elif len(password1) <7:
            return jsonify({'message':"password must greater than 7 char",})
        else:
            new_user = User(email=email,username=username,password=generate_password_hash(password1,method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)


           
            return jsonify({'message':"user created successfully","success":True})

    return render_template("signup.html",user=current_user )