from logging import Logger
from magic_admin import Magic
from pyvise.base import get_logger, get_setting
from pyvise.models import User

logger = get_logger(__name__)


def get_magic_instance():
    magic = Magic(api_secret_key=get_setting('MAGIC_SECRET_KEY'),
                  retries=5, timeout=5, backoff_factor=0.01,
                  )
    return magic


def find_magic_user(email_address: str, did_token: str) -> User:
    try:
        magic = get_magic_instance()

        magic.Token.validate(did_token)
        issuer = magic.Token.get_issuer(did_token)
        magic_user_meta = magic.User.get_metadata_by_issuer(issuer)

        if(magic_user_meta.data.get('email') == email_address):
            # magic.User.get_metadata_by_public_address
            # magic.User.get_metadata_by_token
            return User(key=issuer, email_address=email_address)
        else:
            return None
    except Exception as exc:
        message = f"backend.magic_backend: Magic API threw an exception.  It's likely an invalid user"
        Logger.exception(message, exc)
        # logger.exception("Could not validate did token", exc)
    return None
