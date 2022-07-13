import os

from flask import Flask, jsonify

from flask_cognito import cognito_auth_required, current_user, current_cognito_jwt
from flask_cognito import CognitoAuth

from dotenv import load_dotenv

from object_ai.app.models import User
from object_ai.paths import ENV_FILE_PATH

load_dotenv(ENV_FILE_PATH)

application = Flask(__name__)


# configuration
application.config.update({
    'COGNITO_REGION': os.environ.get('COGNITO_REGION'),
    'COGNITO_USERPOOL_ID': os.environ.get('COGNITO_USERPOOL_ID'),

    # optional
    'COGNITO_APP_CLIENT_ID': os.environ.get('COGNITO_APP_CLIENT_ID'),  # client ID you wish to verify user is authenticated against
    'COGNITO_CHECK_TOKEN_EXPIRATION': False,  # disable token expiration checking for testing purposes
    'COGNITO_JWT_HEADER_NAME': 'X-MyApp-Authorization',
    'COGNITO_JWT_HEADER_PREFIX': 'Bearer',
})


# initialize extension
cogauth = CognitoAuth(application)

@application.route("/")
def home():
    return "hello world"


@cogauth.identity_handler
def lookup_cognito_user(payload):
    """Look up user in our database from Cognito JWT payload."""
    return User.query.filter(User.cognito_username == payload['username']).one_or_none()


@application.route('/api/private')
@cognito_auth_required
def api_private():
    # user must have valid cognito access or ID token in header
    # (accessToken is recommended - not as much personal information contained inside as with idToken)
    return jsonify({
        'cognito_username': current_cognito_jwt['username'],   # from cognito pool
        'user_id': current_user.id,   # from your database
    })

if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True)
