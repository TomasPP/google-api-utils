import os.path
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
# noinspection PyPackageRequirements
from googleapiclient.discovery import build
# noinspection PyPackageRequirements
from google.auth.transport.requests import Request


def get_authenticated_service(secrets_file, service_name, service_version, scopes):
    service, credentials = get_authenticated(secrets_file, service_name, service_version, scopes)
    return service


def get_authenticated(secrets_file, service_name, service_version, scopes):
    credentials = None

    # The pickle file stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    secrets_file_name = os.path.splitext(secrets_file)[0]
    token_pickle_file = secrets_file_name + '.pickle'
    if os.path.exists(token_pickle_file):
        with open(token_pickle_file, 'rb') as token:
            credentials = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                secrets_file, scopes)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_pickle_file, 'wb') as token:
            pickle.dump(credentials, token)
    service = build(service_name, service_version, credentials=credentials)
    return service, credentials
