from pyvise import graphy  # considering moving to own module
from pyvise.models import AccountProfile


def find_account_profile_by_email(email_address: str) -> AccountProfile:
    query_variables = {
        'email_address': email_address
    }
    graph_query = graphy.GraphQLQuery(
        query=AccountProfile.generate_find_by_query(email=email_address))
    client = graphy.GraphQLAPIClient()
    data = client.execute_single_query(graph_query, query_variables)
    account = data.get('account_profiles')
    if(len(account) > 0):
        account = AccountProfile.from_dict(account[0])
        return account
    else:
        return None


def create_account_profile(key: str, email_address: str, access_token: str, expiration: str):
    query = AccountProfile.generate_upsert_mutation()
    expiration_string = '2022-01-22'  # expiration
    query_variables = {
        'key': key,
        'email_address': email_address,
        'access_token': access_token,
        'expiration': expiration_string
    }
    graph_query = graphy.GraphQLQuery(query=query)
    client = graphy.GraphQLAPIClient()
    data = client.execute_single_query(graph_query, query_variables)
    # TODO: figure out return types in graphql
    account = data.get('insert_account_profiles_one')
    return account
