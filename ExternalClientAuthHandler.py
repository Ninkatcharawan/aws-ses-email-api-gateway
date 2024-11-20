import os
import boto3
import json

def lambda_handler(event, context):
    ssm = boto3.client('ssm')

    parameter_name = os.environ.get('TOKEN_PARAM_NAME', '/default/path/to-token')
    try:
        parameter = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        custom_token = parameter['Parameter']['Value']
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to retrieve token", "message": str(e)})
        }

    if 'authorizationToken' not in event:
        return {
            "principalId": "user",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {"Action": "execute-api:Invoke", "Effect": "Deny", "Resource": event['methodArn']}
                ]
            }
        }

    token_from_request = event['authorizationToken']

    if token_from_request == custom_token:
        return {
            "principalId": "user",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {"Action": "execute-api:Invoke", "Effect": "Allow", "Resource": event['methodArn']}
                ]
            }
        }
    else:
        return {
            "principalId": "user",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {"Action": "execute-api:Invoke", "Effect": "Deny", "Resource": event['methodArn']}
                ]
            }
        }
