# app.py
from flask import Flask, render_template, request, session, redirect, flash
import joblib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'  # Update with your database URI
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

app.app_context()
app.secret_key = 'DeeSupportClinic2233'


with app.app_context():
    # Create the database tables
    db.create_all()



@app.route('/')
def index():
    if session.get('user_id'):
        return render_template('index.html')
    else:
        flash('You must log in first.')
        return redirect('/login')


@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user input from the form
    age = float(request.form['Age'])
    gender = int(request.form['Gender'])
    bmi = float(request.form['BMI'])
    fasting_blood_sugar = float(request.form['Fasting_Blood_Sugar'])
    family_history = int(request.form['Family_History_of_Diabetes'])
    smoking_status = int(request.form['Smoking_Status'])
    activity_level = int(request.form['Physical_Activity_Level'])
    numbness = int(request.form['Numbness_in_Extremities'])
    blurred_vision = int(request.form['Blurred_Vision'])
    systolic_bp = float(request.form['Systolic_BP'])
    diastolic_bp = float(request.form['Diastolic_BP'])

    # Prepare user input for prediction
    user_input = [[age, gender, bmi, fasting_blood_sugar, family_history,
                   smoking_status, activity_level, numbness, blurred_vision,
                   systolic_bp, diastolic_bp]]

    # Load the saved model and make a prediction
    loaded_model = joblib.load('naive_bayes_model.joblib')
    prediction = loaded_model.predict(user_input)
    confidence_scores = loaded_model.predict_proba(user_input)
    
    # Convert the confidence scores to Python list and then process each element
    confidence_scores_percent = [round(float(score) * 100, 5) for score in confidence_scores.tolist()[0]]


    # Convert the prediction to a readable label
    prediction_label = 'Positive' if prediction[0] == 1 else 'Negative'

    return render_template('result.html', prediction=prediction_label, confidence=confidence_scores_percent, user_input=user_input[0])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect('/login')

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful.')
            return redirect('/')
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return redirect('/')

        return render_template('profile.html', user=user)

    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User.query.get(user_id)

        if username != "":
            user.username = username
        else:
            flash('Usernane is required')
            return redirect('/profile/'+user_id)

        if email != '':
            user.email = email
        else:
            flash('Email is required')
            return redirect('/profile/'+user_id)

        if password != '':
            user.password = password

        db.session.commit()
        flash('Profile update successful.')
        return redirect('/profile/'+str(user_id))



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear the session and log the user out.
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
