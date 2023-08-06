import os
import logging
import sys
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

logger = logging.getLogger(__name__)
if (os.environ.get('ENV') == 'development'):
    # Using stdout logging in development mode
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)


APP_CONFIGS = {}  # SINGLETON Variable to hold configurations
DEFAULTS__MAGIC_SECRET_KEY = os.environ.get('MAGIC_SECRET_KEY') # from magic
DEFAULTS__JWT_SECRET = os.environ.get('JWT_SECRET') # token to authorize calls

# Used by GraphQL backend to persist data
DEFAULTS__HASURA_ENDPOINT = os.environ.get('HASURA_ENDPOINT')
DEFAULTS__HASURA_SECRET = os.environ.get('HASURA_SECRET')


def get_setting(key):
    if APP_CONFIGS.get(key) is not None:
        return APP_CONFIGS.get(key)
    # This should throw an exception
    if key == 'HASURA_ENDPOINT':        
        return DEFAULTS__HASURA_ENDPOINT
    elif key == 'HASURA_SECRET':
        return DEFAULTS__HASURA_SECRET
    elif key == 'MAGIC_SECRET_KEY':
        return DEFAULTS__MAGIC_SECRET_KEY
    elif key == 'JWT_SECRET':
        return DEFAULTS__JWT_SECRET

    return None


JWT_SINGLETON = None

def configure(**kwargs):
    """
    Iterate over configurations to override APP_CONFIGS and return an AuthJWT object
    Should set MAGIC_SECRET_KEY, JWT_SECRET, HASURA_SECRET, HASURA_ENDPOINT
    By default, it will try and pull environment variables
    """
    global JWT_SINGLETON
    global APP_CONFIGS

    for k, v in kwargs.items():
        APP_CONFIGS[k] = v

    if(len(APP_CONFIGS.items()) < 4):
        logger.warning('All configurations have not been set')

    logger.info("Configuring AuthJWT")
    @AuthJWT.load_config
    class Config(BaseModel):
        authjwt_secret_key: str = get_setting('JWT_SECRET')

    JWT_SINGLETON = AuthJWT()
    return JWT_SINGLETON


def get_AuthJWT_instance():
    global JWT_SINGLETON
    if JWT_SINGLETON is None:
        logger.warning('AuthJWT has not been initialied, using default')
        JWT_SINGLETON = configure()

    return JWT_SINGLETON
