from pyvise.base import get_magic_instance, get_logger
from pyvise.models import User

logger = get_logger(__name__)


def find_magic_user(email_address: str, did_token: str) -> User:
    try:
        magic = get_magic_instance()

        magic.Token.validate(did_token)
        issuer = magic.Token.get_issuer(did_token)
        magic_user_meta = magic.User.get_metadata_by_issuer(issuer)

        if(magic_user_meta.data.get('email') == email_address):
            # magic.User.get_metadata_by_public_address
            # magic.User.get_metadata_by_token
            return User(key=issuer,email_address=email_address)        
        else:
            return None
    except Exception as exc:
        print(f"Exception thrown, suppressing and returning False {exc}")
        # logger.exception("Could not validate did token", exc)
    return None