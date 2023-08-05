import datetime
import logging
import sys
from fastapi_jwt_auth import AuthJWT
from .configuration import get_setting, get_AuthJWT_instance

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
def get_logger(name):
    return logging.getLogger(name)


def create_jwt_token(Authorize: AuthJWT, did_token):
    access_token = Authorize.create_access_token(subject=did_token)
    return access_token


def create_jwt_token_by_email(Authorize: AuthJWT, email_address, valid_for=365):
    in_1_year = datetime.timedelta(days=valid_for)
    access_token = Authorize.create_access_token(subject=email_address, expires_time=in_1_year)
    return {
        'access_token': access_token,
        'expiration': in_1_year
    }

def decode_jwt(token: str) -> dict:
    instance = get_AuthJWT_instance()

    result = instance.get_raw_jwt(encoded_token=token)
    """
    {'sub': 'dennis@payonk.com', 
    'iat': 1611082366, 
    'nbf': 1611082366, 
    'jti': 'd602bcf3-a367-42be-8d3f-b2ac6601343a', 
    'exp': 1611083266, 
    'type': 'access', 
    'fresh': False}
    """
    print("TODO: check expiration")
    return result['sub']