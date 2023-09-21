from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed
from pymongo import MongoClient
from models import User, Professional, db
from bson import ObjectId, os
import uuid
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Configure the upload set for images
images = UploadSet('images', IMAGES)
app.config['UPLOADED_IMAGES_DEST'] = 'uploads'
configure_uploads(app, images)

# Custom Jinja2 filter function to generate image URLs
@app.template_filter('image_src')
def image_src(filename):
    return images.url(filename)

# Configure Flask-Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Secret Key Configuration
app.secret_key = 'your_secret_key_here'

# MongoDB Configuration (replace with your settings)
client = MongoClient('mongodb://localhost:27017/')
db = client['pau_para_toda_obra']

# Home Page
@app.route('/')
def index():
    # Implement logic to list registered professionals
    return render_template('index.html')

# Serve Uploaded Files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_IMAGES_DEST'], filename)

# User and Professional Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash the password before saving it to the database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if user_type == 'user':
            user = User(name, email, hashed_password)  # Save the hashed password
            # Save the user to the MongoDB database
            db.users.insert_one(user.__dict__)
        elif user_type == 'professional':
            company_name = request.form.get('company_name')
            services = request.form.get('services').split(',')
            raw_whatsapp = request.form.get('whatsapp')

            # Format the WhatsApp number to ensure it starts with '+'
            whatsapp = raw_whatsapp if raw_whatsapp.startswith('+') else f'+{raw_whatsapp}'

            price_range = request.form.get('price_range')

            # Check if a profile image is uploaded
            if 'profile_image' in request.files:
                profile_image = request.files['profile_image']
                if profile_image.filename != '':
                    try:
                        # Generate a unique filename for the uploaded image
                        image_filename = str(uuid.uuid4()) + os.path.splitext(profile_image.filename)[-1]

                        # Save the image to the 'uploads' folder using the configured upload set
                        images.save(profile_image, name=image_filename)

                        # Set the image URL to the path where the image is stored
                        image_url = os.path.join(app.config['UPLOADED_IMAGES_DEST'], image_filename)
                    except UploadNotAllowed:
                        flash('Invalid file format for profile image. Allowed formats are: JPG, PNG, GIF.', 'danger')
                        return redirect(url_for('register'))
                else:
                    image_url = None
            else:
                image_url = None

            professional = Professional(name, email, hashed_password, company_name, services, whatsapp, price_range, image_url)

            # Save the professional to the MongoDB database (with the updated image_url)
            db.professionals.insert_one(professional.__dict__)

        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# User and Professional Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Authentication logic here
        # Check if the email and password match a user/professional in the database

        user = db.users.find_one({'email': email, 'password': password})
        professional = db.professionals.find_one({'email': email, 'password': password})

        if user:
            # Authenticated user, set a session to keep them logged in
            session['user_id'] = str(user['_id'])
            session['user_type'] = 'user'  # Set user_type to 'user'
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard page

        elif professional:
            # Authenticated professional, set a session to keep them logged in
            session['professional_id'] = str(professional['_id'])
            session['user_type'] = 'professional'  # Set user_type to 'professional'
            flash('Login successful!', 'success')
            return redirect(url_for('professional_dashboard'))  # Redirect to the professional dashboard page

        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

# User Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # If the user is logged in
        user_id = session['user_id']

        # Retrieve professionals from the database (a simplified example)
        professionals = db.professionals.find()

        return render_template('dashboard.html', professionals=professionals)
    else:
        flash('You need to be logged in to access the dashboard.', 'danger')
        return redirect(url_for('login'))

# Professional Dashboard
@app.route('/professional_dashboard')
def professional_dashboard():
    if 'professional_id' in session:
        # Retrieve the professional's data from the database (you need to implement this part)
        professional_id = session['professional_id']
        professional_data = db.professionals.find_one({'_id': ObjectId(professional_id)})

        if professional_data:
            # Render the template and pass the professional's data to it
            return render_template('professional_dashboard.html',
                                   professional_name=professional_data['name'],
                                   company_name=professional_data['company_name'],
                                   whatsapp=professional_data['whatsapp'],
                                   price_range=professional_data['price_range'],
                                   services=professional_data['services'])
        else:
            flash('Error retrieving professional information.', 'danger')
            return redirect(url_for('login'))
    else:
        flash('You need to be logged in as a professional to access the dashboard.', 'danger')
        return redirect(url_for('login'))

# WhatsApp Redirect
@app.route('/whatsapp/<phone>')
def whatsapp_redirect(phone):
    # Ensure 'phone' is in the international format (e.g., '+1234567890')
    # You may need to format it correctly based on your database structure

    # Generate the WhatsApp link with the pre-typed message
    pre_typed_message = "Olá, vi seu contato no Pau Para Toda Obra. Gostaria de fazer um orçamento ou contratar seus serviços."
    whatsapp_link = f"https://wa.me/{phone}?text={pre_typed_message}"

    # Redirect to the WhatsApp link
    return redirect(whatsapp_link)

# Logout
@app.route('/logout')
def logout():
    # Logout logic here
    # Clear the user's session
    session.clear()
    flash('Logout successful!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
