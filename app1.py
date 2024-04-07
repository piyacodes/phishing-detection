from flask import Flask, request, jsonify, redirect, url_for, session, render_template
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.secret_key = "SERver@123"

# MongoDB connection
app.config["MONGO_URI"] = "mongodb+srv://aratrika03:mumu2003@cluster0.9g8jonr.mongodb.net/phising_database?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db  # This is your database object

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Your registration code
        return redirect(url_for('login'))

    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Your login code
        return jsonify({'message': 'Logged in successfully!'})

    return render_template('login.html')

# User logout route
@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully!'})

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Report route (handling report submission)
@app.route('/report', methods=['POST'])
def report_website():
    data = request.get_json()
    if not data or 'website_url' not in data:
        return jsonify({'error': 'Invalid data or missing website URL'}), 400

    # Extract features from the request data
    website_url = data['website_url']
    domain = data.get('Domain')
    have_ip = data.get('Have_IP')
    have_at = data.get('Have_At')
    url_length = data.get('URL_Length')
    url_depth = data.get('URL_Depth')
    redirection = data.get('Redirection')
    https_domain = data.get('https_Domain')
    tiny_url = data.get('TinyURL')
    prefix_suffix = data.get('Prefix/Suffix')
    dns_record = data.get('DNS_Record')
    web_traffic = data.get('Web_Traffic')
    domain_age = data.get('Domain_Age')
    domain_end = data.get('Domain_End')
    iframe = data.get('iFrame')
    mouse_over = data.get('Mouse_Over')
    right_click = data.get('Right_Click')
    web_forwards = data.get('Web_Forwards')
    label = data.get('Label')
    
    # Check if the website is already reported
    collection = db.report
    existing_report = collection.find_one({'website_url': website_url})
    if existing_report:
        return jsonify({'message': 'Website already reported'}), 200

    # Store the report in the database
    report_data = {
        'website_url': website_url,
        'Domain': domain,
        'Have_IP': have_ip,
        'Have_At': have_at,
        'URL_Length': url_length,
        'URL_Depth': url_depth,
        'Redirection': redirection,
        'https_Domain': https_domain,
        'TinyURL': tiny_url,
        'Prefix/Suffix': prefix_suffix,
        'DNS_Record': dns_record,
        'Web_Traffic': web_traffic,
        'Domain_Age': domain_age,
        'Domain_End': domain_end,
        'iFrame': iframe,
        'Mouse_Over': mouse_over,
        'Right_Click': right_click,
        'Web_Forwards': web_forwards,
        'Label': label
    }
    
    # Store the report in the database
    collection.insert_one(report_data)
    return jsonify({'message': 'Report submitted successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
