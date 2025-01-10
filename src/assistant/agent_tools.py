from src.db.meili_client import Mclient
mclient = Mclient()

def get_unique_categories(payloads):
    return set(payload['category_name'] for payload in payloads)


def write_query():
    pass


def search(query:str):
    return mclient.search(query)