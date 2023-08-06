from dataclasses import dataclass
from typing import ClassVar
from pyvise.graphy import HasuraBase


@dataclass
class User:
    """
    A domain user object.  This models individual users in the system.
    This is currently not stored in a database, but can be linked
    in the account_profile via email address today
    """
    key: str = None
    email_address: str = None
    friendly_name: str = None
    did_token: str = ""
    authenticated: bool = False
    expired: bool = False


@dataclass
class AccountProfile(HasuraBase):
    """
    GraphQL domain representation of profile Object
    """
    __tablename__: ClassVar[str] = 'account_profiles'
    __schema__: ClassVar[dict] = {
        'email_address': {'required': 'true'}
    }
    __operations__: ClassVar[dict] = {
        'create': 'insert_account_profiles_one'
    }

    key: str = None
    friendly_name: str = None
    email_address: str = None
    created_at: str = None
    current_role: str = None

    @classmethod
    def generate_upsert_mutation(cls):
        return """mutation CreateAccountProfile(
        $key: String, 
        $email_address: String, 
        $access_token: String,
        $expiration: timestamptz) {
            insert_account_profiles_one(
            object: {
                email_address: $email_address, 
                key: $key
                account_access_tokens:{
                data: {
                    access_token: $access_token
                    expiration: $expiration
                }
                }
            },
            on_conflict: {
                constraint: person_profile_pkey,
                update_columns: [email_address]
    }
            ) 
        {
            email_address
            key    
        }
        }
      """

    @classmethod
    def generate_find_by_query(cls, **kwargs):
        """
        TODO: parse kwargs to create the input parameter and equal value
        """
        return """
      query FindAccountProfileByEmailAddress($email_address: String) {
  account_profiles(where: {email_address: {_eq: $email_address}}, limit: 1) {
    email_address
    friendly_name
    key
    current_role
    updated_at
    created_at
  }
}
      """
