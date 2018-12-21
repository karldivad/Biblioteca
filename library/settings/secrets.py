import os

SOCIAL_AUTH_TRAILING_SLASH = False              # Remove end slash from routes
SOCIAL_AUTH_AUTH0_DOMAIN = 'libraryinkalabs.auth0.com'
SOCIAL_AUTH_AUTH0_KEY = os.environ.get('AUTH0_CLIENT_ID')
SOCIAL_AUTH_AUTH0_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')


SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile'
]