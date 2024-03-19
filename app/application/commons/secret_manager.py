import base64
import json
import boto3
from botocore.exceptions import ClientError


def aws_connection():
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name="us-east-1",
    )
    return client


def return_variables(client):
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId="foodieFlow_secrets"
        )
    except ClientError as e:
        raise Exception(
            "Não foi possível recuperar o secret: {}".format(
                e.response["Error"]["Message"]
            )
        )
    else:
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = base64.b64decode(get_secret_value_response["SecretBinary"])

    secret_dict = json.loads(secret)
    return secret_dict
