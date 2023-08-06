import os
# Decoupled config service

APP_CONFIGS = {}  # overridden


# Used to talk to the Magic Backend
MAGIC_SECRET_KEY = os.environ.get('MAGIC_SECRET_KEY')

# Used to authorize calls
JWT_SECRET = os.environ.get('JWT_SECRET')

# Used by AccountBackend
HASURA_ENDPOINT = os.environ.get('HASURA_ENDPOINT')
HASURA_SECRET = os.environ.get('HASURA_SECRET')

def get(key):
    if key == 'HASURA_ENDPOINT':
        if APP_CONFIGS.get(key) is not None:
            return APP_CONFIGS.get(key)
        else:
            return HASURA_ENDPOINT
    
    return None


def configure(**kwargs):
    """
    Iterate over configurations to override
    """
    if kwargs.get('HASURA_ENDPOINT'):
        APP_CONFIGS['HASURA_ENDPOINT'] = kwargs.get('HASURA_ENDPOINT')
    