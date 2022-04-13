import connexion
import six

from swagger_server.models.confirm import Confirm  # noqa: E501
from swagger_server.models.information import Information  # noqa: E501
from swagger_server.models.method import Method  # noqa: E501
from swagger_server.models.state import State  # noqa: E501
from swagger_server.models.transaction import Transaction  # noqa: E501
from swagger_server import util


def confirm_payment(order_id, method_id, token, body=None, nif=None):  # noqa: E501
    """confirm payment

    verify client&#x27;s authentication and proceed to payment # noqa: E501

    :param order_id: 
    :type order_id: int
    :param method_id: 
    :type method_id: int
    :param token: 
    :type token: 
    :param body: 
    :type body: dict | bytes
    :param nif: pass NIF for bill
    :type nif: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = Confirm.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_information(order_id, token):  # noqa: E501
    """get payment information

    get information # noqa: E501

    :param order_id: 
    :type order_id: int
    :param token: 
    :type token: 

    :rtype: Information
    """
    return 'do some magic!'


def payment_method(order_id):  # noqa: E501
    """selects payment method

    selecting the order, client is redirect to this endpoint to select the payment method # noqa: E501

    :param order_id: 
    :type order_id: int

    :rtype: List[Method]
    """
    return 'do some magic!'


def proceed_payment(token, body=None):  # noqa: E501
    """transaction

    make transaction # noqa: E501

    :param token: 
    :type token: 
    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Transaction.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def set_state(order_id, token, body=None):  # noqa: E501
    """payment state

    set state # noqa: E501

    :param order_id: 
    :type order_id: int
    :param token: 
    :type token: 
    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = State.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
