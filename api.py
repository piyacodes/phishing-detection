import requests
import json

# Login with the provided username and password
def login_user():
    url = 'http://localhost:5000/login'
    data = {'username': 'ahana', 'password': 'ahana123'}
    response = requests.post(url, data=data)
    print(response.json())

# Logout
def logout_user():
    url = 'http://localhost:5000/logout'
    response = requests.get(url)
    print(response.json())

# Submit a report
def submit_report(website_url, report_data):
    url = 'http://localhost:5000/report'
    data = {'website_url': website_url, **report_data}
    response = requests.post(url, json=data)
    print(response.json())

if __name__ == '__main__':
    # Login with the provided username and password
    login_user()

    # Submit a report (assuming the user is logged in)
    report_data = {
        'Domain': 'example.com',
        'Have_IP': True,
        'Have_At': False,
        'URL_Length': 10,
        'URL_Depth': 2,
        'Redirection': False,
        'https_Domain': True,
        'TinyURL': False,
        'Prefix/Suffix': True,
        'DNS_Record': True,
        'Web_Traffic': 'Medium',
        'Domain_Age': 365,
        'Domain_End': False,
        'iFrame': False,
        'Mouse_Over': True,
        'Right_Click': False,
        'Web_Forwards': False,
        'Label': 'Phishing'
    }
    submit_report('http://example.com', report_data)

    # Logout the user
    logout_user()
