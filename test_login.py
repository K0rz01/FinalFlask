import requests

def test_login():
    url = "http://127.0.0.1:5000/api/login"
    data = {
        "email": "admin@tecnocomputer.com",
        "password": "123456"
    }
    session = requests.Session()
    response = session.post(url, json=data)
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    test_login()
