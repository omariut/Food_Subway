from typing import Dict
import logging

from django.conf import settings

import requests
from django.contrib.auth import get_user_model
User= get_user_model()

logger = logging.getLogger('django')


def sslcommerz_payment_create(data: Dict, customer: User) -> Dict:
    """
    :param data:
    :param customer:
    :return:
    """
    customer_name = 'Evaly Customer'
    if customer.first_name and customer.last_name:
        customer_name = f'{customer.first_name} {customer.last_name}'
    try:
        body = {
            'store_id': settings.SSL_STORE_ID,
            'store_passwd': settings.SSL_STORE_PASSWORD,
            'currency': 'BDT',
            'cus_name': customer_name,
            'cus_add1': 'Dhaka',#customer.address if customer.address else 'Dhaka',
            'cus_city': 'Dhaka',
            'cus_country': 'Bangladesh',
            'cus_phone': customer.username,
            'cus_email': customer.email if customer.email else 'no-email@evaly.com.bd',
            'shipping_method': 'YES',
            'ship_name': 'Dhaka',#customer.address if customer.address else 'Dhaka',
            'ship_city': 'Dhaka',
            'ship_country': 'Bangladesh',
            'ship_postcode': 1000,
            'ship_add1': 'Dhaka'#customer.address if customer.address else 'Dhaka',
        }
        body.update(data)
        response = requests.post(
            url=f'https://sandbox.sslcommerz.com/gwprocess/v4/api.php',
            data=body,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=5,
        )
        resp: Dict = response.json()
        status=resp.get('status')
        
        if  status == 'SUCCESS':
            return resp
        logger.error('SSL_COMMERZ_PAYMENT_ERROR_RESPONSE: ', str(data['failedreason']))
        return {}
    except requests.exceptions.Timeout as e:
        logger.error('SSL_COMMERZ_PAYMENT_TIMEOUT_ERROR: ', str(e))
    except requests.exceptions.HTTPError as e:
        logger.error('SSL_COMMERZ_PAYMENT_HTTP_ERROR: ', str(e))
    except requests.exceptions.ConnectionError as e:
        logger.error('SSL_COMMERZ_PAYMENT_CONNECTION_ERROR: ', str(e))
    return {}


def sslcommerz_payment_validation(query_params: Dict) -> Dict:
    """
    :param query_params:
    :return:
    """
    try:
        params = {
            'store_id': settings.SSL_STORE_ID,
            'store_passwd': settings.SSL_STORE_PASSWORD,
            'format': 'json',
        }
        params.update(query_params)
        response = requests.get(
            url=f'https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php?store_id={settings.SSL_STORE_ID}&store_passwd={settings.SSL_STORE_PASSWORD}&format=json&val_id={params["val_id"]}',
        )
        resp: Dict = response.json()
        if resp.get('status') and resp['status'] == 'VALID':
            return resp
        logger.error('SSL_COMMERZ_PAYMENT_ERROR_RESPONSE: ', str(resp))
        return {}
    except requests.exceptions.Timeout as e:
        logger.error('SSL_COMMERZ_PAYMENT_QUERY_TIMEOUT_ERROR: ', str(e))
    except requests.exceptions.HTTPError as e:
        logger.error('SSL_COMMERZ_PAYMENT_QUERY_HTTP_ERROR: ', str(e))
    except requests.exceptions.ConnectionError as e:
        logger.error('SSL_COMMERZ_PAYMENT_QUERY_CONNECTION_ERROR: ', str(e))
    return {}