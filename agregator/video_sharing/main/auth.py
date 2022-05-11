import requests

def login(uname, pwd):
    headers = { "accept": "*/*",
                    "Content-Type": "application/x-www-form-urlencoded"
        }
    data = { "username": uname,
            "password":  pwd
        }

    login_request = requests.post("http://127.0.0.1:7001/user/login", data = data, headers = headers)
    return login_request.json()