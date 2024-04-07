from flask import Flask, request, jsonify, redirect, url_for, session
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
        users = db.users  # Assuming you have a 'users' collection
        existing_user = users.find_one({'$or': [{'username': request.form['username']}, {'email': request.form['email']}]})

        if existing_user:
            return jsonify({'error': 'Username or email already exists!'})

        hash_pass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        user_id = users.insert_one({'username': request.form['username'], 'email': request.form['email'], 'password': hash_pass})
        session['username'] = request.form['username']
        session['user_id'] = str(user_id.inserted_id)  # Use 'inserted_id' to get the inserted document's ID
        return redirect(url_for('login'))

    return '''
        <form method="post">
            <p>Email: <input type="text" name="email"></p>
            <p>Username: <input type="text" name="username"></p>
            <p>Password: <input type="password" name="password"></p>
            <p><input type="submit" value="Register"></p>
        </form>
    '''

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = db.users
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['username'] = request.form['username']
                session['user_id'] = str(login_user['_id'])
                return jsonify({'message': 'Logged in successfully!'})
            else:
                return jsonify({'error': 'Invalid password!'})
        else:
            return jsonify({'error': 'User not found!'})

    return '''
        <form method="post">
            <p>Username: <input type="text" name="username"></p>
            <p>Password: <input type="password" name="password"></p>
            <p><input type="submit" value="Login"></p>
        </form>
    '''

# User logout route
@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully!'})

# Report route
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
