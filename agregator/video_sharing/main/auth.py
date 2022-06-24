import requests

def login(uname, pwd):
    headers = { "accept": "*/*",
                    "Content-Type": "application/x-www-form-urlencoded"
        }
    data = { "username": uname,
            "password":  pwd
        }

    login_request = requests.post("http://authapi-service:6000/user/login", data = data, headers = headers)
    return login_request.json()


def register(uname, nMec, email, pwd, confirmpwd):
    headers = { "accept": "*/*",
                    "Content-Type": "application/x-www-form-urlencoded"
        }
    data = { "username": uname,
            "nMec": nMec,
            "email": email,
            "password": pwd,
            "confirmPassword":  confirmpwd
        }

    register_request = requests.post("http://authapi-service:6000/user", data = data, headers = headers)
    return register_request.json()

def is_logged(token):
    headers = { "accept": "*/*",
                    "Content-Type": "application/x-www-form-urlencoded"
        }
    url= "http://authapi-service:6000/user/status/"+token
    login_request = requests.post(url, headers = headers)
    return login_request.json()["is_logged"]
