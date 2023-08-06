# External Interface to code
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from .base import create_jwt_token_by_email
from .configuration import configure, get_setting, get_AuthJWT_instance
from .backend import account_backend
from .backend import magic_backend
from .models import User, AccountProfile
from .routers.profile_router import profile_router
