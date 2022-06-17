import requests

def payment_transaction(order_id,method_id,price,uname):
    headers = { "accept": "*/*",
                    "Content-Type": "application/x-www-form-urlencoded"
        }
    data = { "price": price,
            "username":  uname
        }

    pay_request = requests.post("http://127.0.0.1:7002/payment/"+order_id+'/'+method_id, data = data, headers = headers)
    return pay_request.json()


def payment_confirmation(token,orderid,uname):
    headers = { "accept": "*/*",
                    "Content-Type": "application/x-www-form-urlencoded"
        }
    data = { "order_id": orderid,
            "username": uname
        }

    confirm_request = requests.post("http://127.0.0.1:7002/payment/"+token, data = data, headers = headers)
    return confirm_request.json()

def method(order_id):
    headers = { "accept": "*/*",
                    "Content-Type": "application/x-www-form-urlencoded"
        }
    url= "http://127.0.0.1:7002/payment/"+order_id
    method_request = requests.post(url, headers = headers)
    return method_request.json()
