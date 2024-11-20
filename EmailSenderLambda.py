import os
import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    required_fields = ['from_name', 'from_address', 'to_address', 'email_subject', 'body_text', 'body_html']
    for field in required_fields:
        if field not in event:
            return {
                'statusCode': 400,
                'body': json.dumps(f'Missing required field: {field}')
            }

    SENDER_NAME = os.environ.get('SENDER_NAME', 'Default Sender')
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'default@example.com')
    SENDER = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    
    RECIPIENT = event['to_address']
    SUBJECT = event['email_subject']
    BODY_TEXT = event['body_text']
    BODY_HTML = event['body_html']
    CHARSET = "UTF-8"

    ses = boto3.client('ses')

    try:
        response = ses.send_email(
            Destination={
                'ToAddresses': [RECIPIENT],
            },
            Message={
                'Body': {
                    'Html': {'Charset': CHARSET, 'Data': BODY_HTML},
                    'Text': {'Charset': CHARSET, 'Data': BODY_TEXT},
                },
                'Subject': {'Charset': CHARSET, 'Data': SUBJECT},
            },
            Source=SENDER
        )
    except ClientError as e:
        print(f"Error sending email: {e.response['Error']['Message']}")
        return {'statusCode': 500, 'body': json.dumps('Error sending email')}
    else:
        print(f"Email sent! Message ID: {response['MessageId']}")
        return {'statusCode': 200, 'body': json.dumps(f"Email sent! Message ID: {response['MessageId']}")}
