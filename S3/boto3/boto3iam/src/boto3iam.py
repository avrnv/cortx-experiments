#!/usr/bin/python3

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests

IS_SECURE = False
PROTO = 'https' if IS_SECURE else 'http'
HOST = 'localhost'
PORT = 9443 if IS_SECURE else 9080
URL = f"{PROTO}://{HOST}:{PORT}/"
LOGIN = "sgiamadmin"
PASSWORD = "7fXINmqEVQYX"

TEST_ACCOUNT_NAME='testacc'
TEST_ACCOUNT_EMAIL='testacc@test.com'

SERVICE_NAME='iam'
REGION='us-west2'


def main():
    session = boto3.Session(aws_access_key_id=LOGIN, aws_secret_access_key=PASSWORD)
    credentials = session.get_credentials()
    creds = credentials.get_frozen_credentials()

    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain',
        'host': f'{HOST}:{PORT}'
    }
    data = {
        'Action': 'CreateAccount',
        'AccountName': TEST_ACCOUNT_NAME,
        'Email': TEST_ACCOUNT_EMAIL
    }

    request = AWSRequest(method='POST', url='/', data=data, headers=headers)
    SigV4Auth(creds, SERVICE_NAME, REGION).add_auth(request)
    response = requests.request(method='POST', url=URL, headers=dict(request.headers), data=data)
    print(f'{response.status_code} - {response.text}')


if __name__ == "__main__":
    main()
