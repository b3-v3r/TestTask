import hashlib

from .config import SECRET_KEY


def sign_params( **kwargs ) -> str:
    '''
    Parameter hashing with sha256 algorithm
    '''
    sorted_list = (str(value) for _,value in sorted(kwargs.items()))

    sign_str = ':'.join(sorted_list) + SECRET_KEY

    return hashlib.sha256( sign_str.encode("utf-8") ).hexdigest()