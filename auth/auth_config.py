from functools import wraps
import os
from authlib.integrations.flask_client import OAuth
from flask import session, redirect, url_for

auth0 = OAuth()
auth0.register(
    'auth0',
    client_id='1I1UFlfiBrhZgJa7xnnrev3XDRiaqpUN',
    client_secret='bVXUMGgtb009nDCzqzvJAKbom6-Ahj3q8X6B92FIFLZvuDTqJF',
    api_base_url='https://dev-hksxwmy56tydw4gu.jp.auth0.com',
    access_token_url='https://dev-hksxwmy56tydw4gu.jp.auth0.com/oauth/token',
    authorize_url='https://dev-hksxwmy56tydw4gu.jp.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def mock_requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If no user in session, return to the login page (or skip entirely for testing)
        if 'user' not in session:
            return redirect(url_for('login'))  # Or skip authentication check entirely
        return f(*args, **kwargs)
    return decorated_function
