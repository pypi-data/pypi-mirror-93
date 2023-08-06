from datetime import datetime
from logging import Logger
from fastapi import HTTPException, Depends
from fastapi import APIRouter
from pydantic import BaseModel
from pyvise.base import AuthJWT, create_jwt_token_by_email, get_logger
from pyvise.backend.magic_backend import find_magic_user
from pyvise.backend.account_backend import create_account_profile

profile_router = APIRouter()
logger = get_logger(__name__)


class CreateProfileRequestSchema(BaseModel):
    email_address: str
    did_token: str = None

    def generate_response(self, email_address, did_token, magic_user, jwt_token):
        logger.info(f'Creating profile for {email_address}')
        return {
            'data': {
                'email_address': email_address,
                'jwt_token': jwt_token,
                'did_token': did_token,
                'user': magic_user,
            },
            'errors': ""
        }


@profile_router.post('/create',  tags=["account_profile", "public"])
def create_url(req_schema: CreateProfileRequestSchema, Authorize: AuthJWT = Depends()):
    """
    Validates user against magic (using didToken), creates backend record
    and returns a JWT token
    
    [Reference Design](https://docs.magic.link/admin-sdk/python/examples/user-signup)
    - Step 1 of signup, called after onRedirectLogin
    # 
    """
    try:
        valid_user = find_magic_user(
            req_schema.email_address, req_schema.did_token)

        if(valid_user is not None):
            jwt_token_dict = create_jwt_token_by_email(
                Authorize,
                req_schema.email_address, 365)

            create_account_profile(
                valid_user.key, req_schema.email_address,
                jwt_token_dict['access_token'],
                jwt_token_dict['expiration'])

            return req_schema.generate_response(
                req_schema.email_address,
                req_schema.did_token,
                valid_user,
                jwt_token_dict['access_token']
            )
        else:
            return {'errors': 'Could not validate user or create profile'}
    except Exception as magicDIDTokenError:
        # raise BadRequest('DID Token is invalid: {}'.format(magicDIDTokenError))
        raise HTTPException(
            status_code=401, detail=f"Invalid DID Token likely. Error: {magicDIDTokenError}")
